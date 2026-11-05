"""
============================================================
Duplicate Data Finder - Modern Web Application (PS No. 27)
Language : Python 3 (Pure Standard Library - Zero dependencies!)
============================================================
Features:
- Runs locally and opens directly in your default web browser
- Drag & drop .txt files OR paste entries directly
- Instant statistics (Total items, Unique items, Duplicate count)
- Duplicates breakdown table with frequency badges
- One-click 'Download unique.txt' and 'Copy to Clipboard'
- Fast, clean, accessible on any device
============================================================
"""

import sys
import os
import json
import webbrowser
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

# ------------------------------------------------------------
# Core Logic (from PS No. 27)
# ------------------------------------------------------------

def clean_entry(text):
    """Ignore-case mode: make lowercase and remove extra spaces."""
    words = text.lower().split()
    return " ".join(words)


def get_unique(entries):
    """Return unique entries as a list (keeps the original order)."""
    seen = set()
    unique_list = []
    for item in entries:
        if item not in seen:
            seen.add(item)
            unique_list.append(item)
    return unique_list


def find_duplicates(entries, unique_list):
    """Use a loop to count each unique entry.
    Return a list of (entry, count) for entries repeated more than once."""
    duplicates = []
    for item in unique_list:
        count = 0
        for entry in entries:
            if entry == item:
                count += 1
        if count > 1:
            duplicates.append({"item": item, "count": count})
    return duplicates


def process_entries(entries, ignore_case=False):
    """Clean (if required), calculate unique entries and duplicates."""
    if ignore_case:
        processed = [clean_entry(e) for e in entries]
    else:
        processed = entries

    unique_list = get_unique(processed)
    duplicates = find_duplicates(processed, unique_list)
    return processed, unique_list, duplicates


HTML_PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Duplicate Data Finder (PS No. 27)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --primary: #2563eb;
      --primary-hover: #1d4ed8;
      --success: #16a34a;
      --warning: #d97706;
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --text-main: #0f172a;
      --text-muted: #64748b;
      --border: #e2e8f0;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: var(--bg);
      color: var(--text-main);
      padding: 30px 16px;
      line-height: 1.5;
    }
    .container {
      max-width: 920px;
      margin: 0 auto;
    }
    header {
      background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
      color: white;
      padding: 24px 28px;
      border-radius: 14px;
      box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.1);
      margin-bottom: 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }
    .header-text h1 {
      font-size: 1.6rem;
      font-weight: 700;
      letter-spacing: -0.02em;
    }
    .header-text p {
      font-size: 0.9rem;
      color: #94a3b8;
      margin-top: 4px;
    }
    .badge-ps {
      background: rgba(37, 99, 235, 0.25);
      border: 1px solid rgba(147, 197, 253, 0.4);
      color: #bfdbfe;
      padding: 4px 12px;
      border-radius: 9999px;
      font-size: 0.8rem;
      font-weight: 600;
    }
    .card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 20px;
      box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
    }
    .section-title {
      font-size: 1rem;
      font-weight: 600;
      margin-bottom: 14px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    /* Tabs & Drop Zone */
    .drop-zone {
      border: 2px dashed #cbd5e1;
      border-radius: 10px;
      padding: 24px 16px;
      text-align: center;
      cursor: pointer;
      background: #f8fafc;
      transition: all 0.2s ease;
      margin-bottom: 14px;
    }
    .drop-zone:hover, .drop-zone.dragover {
      border-color: var(--primary);
      background: #eff6ff;
    }
    .drop-zone p {
      color: var(--text-muted);
      font-size: 0.95rem;
    }
    .drop-zone strong {
      color: var(--primary);
    }
    textarea {
      width: 100%;
      height: 110px;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 10px 12px;
      font-family: 'Fira Code', monospace;
      font-size: 0.9rem;
      resize: vertical;
      outline: none;
      transition: border-color 0.2s;
    }
    textarea:focus {
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
    }
    /* Options & Controls */
    .controls-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 14px;
      margin-top: 14px;
      padding-top: 14px;
      border-top: 1px solid var(--border);
    }
    .radio-group {
      display: flex;
      gap: 16px;
      flex-wrap: wrap;
      font-size: 0.9rem;
    }
    .radio-label {
      display: flex;
      align-items: center;
      gap: 6px;
      cursor: pointer;
    }
    .btn-group {
      display: flex;
      gap: 8px;
    }
    button {
      cursor: pointer;
      font-family: inherit;
      border: none;
      padding: 9px 18px;
      border-radius: 7px;
      font-size: 0.9rem;
      font-weight: 600;
      transition: all 0.15s ease;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .btn-primary {
      background: var(--primary);
      color: white;
    }
    .btn-primary:hover {
      background: var(--primary-hover);
    }
    .btn-secondary {
      background: #e2e8f0;
      color: #334155;
    }
    .btn-secondary:hover {
      background: #cbd5e1;
    }
    .btn-success {
      background: var(--success);
      color: white;
    }
    .btn-success:hover {
      background: #15803d;
    }
    /* Stats Cards */
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 14px;
      margin-bottom: 20px;
    }
    .stat-card {
      background: white;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 16px;
      box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.04);
    }
    .stat-label {
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      color: var(--text-muted);
      letter-spacing: 0.05em;
    }
    .stat-number {
      font-size: 1.8rem;
      font-weight: 700;
      margin-top: 4px;
    }
    .stat-total { color: var(--primary); }
    .stat-unique { color: var(--success); }
    .stat-dup { color: var(--warning); }

    /* Results Split */
    .results-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 18px;
    }
    @media (max-width: 768px) {
      .results-grid { grid-template-columns: 1fr; }
    }
    .table-container {
      max-height: 280px;
      overflow-y: auto;
      border: 1px solid var(--border);
      border-radius: 8px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.88rem;
    }
    th, td {
      padding: 10px 14px;
      text-align: left;
      border-bottom: 1px solid var(--border);
    }
    th {
      background: #f1f5f9;
      font-weight: 600;
      color: #475569;
      position: sticky;
      top: 0;
    }
    tr:last-child td { border-bottom: none; }
    .badge-count {
      background: #fef3c7;
      color: #92400e;
      padding: 2px 8px;
      border-radius: 9999px;
      font-size: 0.78rem;
      font-weight: 600;
    }
    .code-box {
      font-family: 'Fira Code', monospace;
      font-size: 0.88rem;
      background: #f8fafc;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 12px;
      height: 280px;
      overflow-y: auto;
      white-space: pre;
    }
    .quick-samples {
      display: flex;
      gap: 8px;
      align-items: center;
      margin-bottom: 12px;
      font-size: 0.85rem;
      color: var(--text-muted);
    }
    .sample-pill {
      background: #e2e8f0;
      color: #1e293b;
      padding: 2px 8px;
      border-radius: 4px;
      cursor: pointer;
      font-size: 0.8rem;
    }
    .sample-pill:hover {
      background: #cbd5e1;
    }
    .toast {
      position: fixed;
      bottom: 20px;
      right: 20px;
      background: #0f172a;
      color: white;
      padding: 10px 18px;
      border-radius: 8px;
      font-size: 0.85rem;
      opacity: 0;
      transition: opacity 0.3s ease;
      pointer-events: none;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .toast.show { opacity: 1; }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="header-text">
        <h1>🔍 Duplicate Data Finder</h1>
        <p>Interactive Data Cleaning & Repetition Analysis</p>
      </div>
      <span class="badge-ps">PS No. 27</span>
    </header>

    <!-- Input Card -->
    <div class="card">
      <div class="section-title">
        <span>1. Provide Your Data</span>
      </div>

      <div class="quick-samples">
        <span>Quick Test Data:</span>
        <span class="sample-pill" onclick="loadSample(1)">Sample 1 (Fruits)</span>
        <span class="sample-pill" onclick="loadSample(4)">Sample 4 (Mixed Cases)</span>
        <span class="sample-pill" onclick="loadSample(2)">Sample 2 (Single item)</span>
      </div>

      <div class="drop-zone" id="dropZone" onclick="document.getElementById('fileInput').click()">
        <p>📁 Drag and drop your <strong>.txt</strong> file here, or <strong>click to browse</strong></p>
        <p style="font-size: 0.8rem; margin-top: 4px;" id="fileLabel">No file chosen yet</p>
        <input type="file" id="fileInput" accept=".txt,text/plain" style="display: none" onchange="handleFileSelect(event)">
      </div>

      <textarea id="rawText" placeholder="...or directly paste / type items here (one entry per line)">apple
banana
apple
orange
banana
apple</textarea>

      <div class="controls-row">
        <div class="radio-group">
          <label class="radio-label">
            <input type="radio" name="matchMode" value="1" checked> Exact match
          </label>
          <label class="radio-label">
            <input type="radio" name="matchMode" value="2"> Ignore case & extra spaces
          </label>
        </div>

        <div class="btn-group">
          <button class="btn-primary" onclick="analyzeData()">🔍 Analyze Data</button>
          <button class="btn-secondary" onclick="clearData()">🔄 Clear</button>
        </div>
      </div>
    </div>

    <!-- Stats Grid -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-label">Total Entries</div>
        <div class="stat-number stat-total" id="statTotal">0</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Unique Entries</div>
        <div class="stat-number stat-unique" id="statUnique">0</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Duplicates Groups</div>
        <div class="stat-number stat-dup" id="statDup">0</div>
      </div>
    </div>

    <!-- Results Card -->
    <div class="card">
      <div class="results-grid">
        <!-- Left: Duplicates List -->
        <div>
          <div class="section-title">
            <span>⚠️ Duplicates Found</span>
          </div>
          <div class="table-container">
            <table>
              <thead>
                <tr>
                  <th>Entry Item</th>
                  <th style="width: 120px; text-align: center;">Frequency</th>
                </tr>
              </thead>
              <tbody id="dupTableBody">
                <tr><td colspan="2" style="text-align: center; color: var(--text-muted);">No analysis performed yet.</td></tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Right: Unique Entries -->
        <div>
          <div class="section-title" style="justify-content: space-between;">
            <span>✅ Unique Items (<span id="uniqueCountBadge">0</span>)</span>
            <div class="btn-group">
              <button class="btn-secondary" style="padding: 4px 10px; font-size: 0.8rem;" onclick="copyUnique()">📋 Copy</button>
              <button class="btn-success" style="padding: 4px 10px; font-size: 0.8rem;" onclick="downloadUnique()">💾 Save unique.txt</button>
            </div>
          </div>
          <div class="code-box" id="uniqueBox"></div>
        </div>
      </div>
    </div>
  </div>

  <div class="toast" id="toastMsg">Notification</div>

  <script>
    let currentUniqueList = [];

    const SAMPLES = {
      1: "apple\nbanana\napple\norange\nbanana\napple",
      4: "Apple\napple\nbanana\nAPPLE",
      2: "apple"
    };

    function loadSample(id) {
      document.getElementById('rawText').value = SAMPLES[id];
      if (id === 4) {
        document.querySelector('input[name="matchMode"][value="2"]').checked = true;
      } else {
        document.querySelector('input[name="matchMode"][value="1"]').checked = true;
      }
      document.getElementById('fileLabel').textContent = "Sample " + id + " loaded";
      analyzeData();
    }

    // Drag and Drop
    const dropZone = document.getElementById('dropZone');
    ['dragenter', 'dragover'].forEach(name => {
      dropZone.addEventListener(name, (e) => { e.preventDefault(); dropZone.classList.add('dragover'); }, false);
    });
    ['dragleave', 'drop'].forEach(name => {
      dropZone.addEventListener(name, (e) => { e.preventDefault(); dropZone.classList.remove('dragover'); }, false);
    });
    dropZone.addEventListener('drop', (e) => {
      const files = e.dataTransfer.files;
      if (files.length > 0) {
        loadFile(files[0]);
      }
    });

    function handleFileSelect(e) {
      if (e.target.files.length > 0) {
        loadFile(e.target.files[0]);
      }
    }

    function loadFile(file) {
      document.getElementById('fileLabel').textContent = "Selected: " + file.name + " (" + file.size + " bytes)";
      const reader = new FileReader();
      reader.onload = function(evt) {
        document.getElementById('rawText').value = evt.target.result;
        showToast("Loaded file: " + file.name);
        analyzeData();
      };
      reader.readAsText(file);
    }

    function clearData() {
      document.getElementById('rawText').value = "";
      document.getElementById('fileLabel').textContent = "No file chosen yet";
      document.getElementById('fileInput').value = "";
      document.getElementById('statTotal').textContent = "0";
      document.getElementById('statUnique').textContent = "0";
      document.getElementById('statDup').textContent = "0";
      document.getElementById('dupTableBody').innerHTML = '<tr><td colspan="2" style="text-align: center; color: var(--text-muted);">No analysis performed yet.</td></tr>';
      document.getElementById('uniqueBox').textContent = "";
      document.getElementById('uniqueCountBadge').textContent = "0";
      currentUniqueList = [];
    }

    async function analyzeData() {
      const text = document.getElementById('rawText').value;
      const ignoreCase = document.querySelector('input[name="matchMode"]:checked').value === "2";

      try {
        const response = await fetch('/api/analyze', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: text, ignoreCase: ignoreCase })
        });
        const data = await response.json();

        // Update statistics
        document.getElementById('statTotal').textContent = data.total;
        document.getElementById('statUnique').textContent = data.unique_count;
        document.getElementById('statDup').textContent = data.duplicate_count;
        document.getElementById('uniqueCountBadge').textContent = data.unique_count;

        // Update duplicates table
        const tbody = document.getElementById('dupTableBody');
        tbody.innerHTML = "";
        if (data.duplicates.length === 0) {
          tbody.innerHTML = '<tr><td colspan="2" style="text-align: center; color: #16a34a; font-weight: 500;">✅ No duplicates found! All items are unique.</td></tr>';
        } else {
          data.duplicates.forEach(d => {
            const tr = document.createElement('tr');
            tr.innerHTML = `<td><strong>${escapeHtml(d.item)}</strong></td><td style="text-align: center;"><span class="badge-count">${d.count} times</span></td>`;
            tbody.appendChild(tr);
          });
        }

        // Update unique entries box
        currentUniqueList = data.unique_list;
        document.getElementById('uniqueBox').textContent = data.unique_list.join('\n');
        showToast("Analysis complete!");
      } catch (err) {
        showToast("Error processing data: " + err.message);
      }
    }

    function escapeHtml(str) {
      return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }

    function copyUnique() {
      if (!currentUniqueList || currentUniqueList.length === 0) {
        showToast("No unique entries to copy!");
        return;
      }
      navigator.clipboard.writeText(currentUniqueList.join('\n')).then(() => {
        showToast("Copied " + currentUniqueList.length + " unique items to clipboard!");
      });
    }

    function downloadUnique() {
      if (!currentUniqueList || currentUniqueList.length === 0) {
        showToast("No unique entries to download!");
        return;
      }
      const blob = new Blob([currentUniqueList.join('\n') + '\n'], { type: 'text/plain;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'unique.txt';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      showToast("Downloaded unique.txt successfully!");
    }

    function showToast(msg) {
      const toast = document.getElementById('toastMsg');
      toast.textContent = msg;
      toast.classList.add('show');
      setTimeout(() => toast.classList.remove('show'), 2500);
    }

    // Auto-run on load
    window.addEventListener('DOMContentLoaded', () => {
      analyzeData();
    });
  </script>
</body>
</html>
"""


class DuplicateFinderRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Quieter server logging
        sys.stderr.write(f"[{self.log_date_time_string()}] {format % args}\n")

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/" or parsed.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/analyze":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8")
            data = json.loads(body) if body else {}

            raw_text = data.get("text", "")
            ignore_case = bool(data.get("ignoreCase", False))

            # Split lines, strip, ignore blanks
            lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
            entries, unique_list, duplicates = process_entries(lines, ignore_case=ignore_case)

            response_data = {
                "total": len(entries),
                "unique_count": len(unique_list),
                "duplicate_count": len(duplicates),
                "unique_list": unique_list,
                "duplicates": duplicates
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()


def start_server(port=5000):
    server_address = ("127.0.0.1", port)
    try:
        httpd = HTTPServer(server_address, DuplicateFinderRequestHandler)
    except OSError:
        # Port might be in use, fallback to dynamic port
        server_address = ("127.0.0.1", 0)
        httpd = HTTPServer(server_address, DuplicateFinderRequestHandler)
        port = httpd.server_port

    url = f"http://127.0.0.1:{port}/"
    print("=" * 60)
    print("      DUPLICATE DATA FINDER - WEB APP")
    print("=" * 60)
    print(f"App running at: {url}")
    print("Opening in your web browser automatically...")
    print("Press Ctrl+C in this console to stop the server.")
    print("=" * 60)

    # Open browser in separate thread
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping web server. Goodbye!")
        httpd.server_close()


if __name__ == "__main__":
    start_server(5000)
