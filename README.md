# Duplicate Data Finder (PS No. 27)

A complete, beginner-friendly Python 3 application that reads text entries (one entry per line), identifies duplicates, calculates repetition counts, displays summary metrics, and exports clean unique entries to `unique.txt`.

**Key Concepts Used:**
- **Lists:** Storing raw and cleaned lines of entries in original sequence
- **Sets:** Fast $O(1)$ uniqueness tracking while preserving item order
- **Loops & Conditions:** Counting duplicate occurrences and filtering options
- **File Handling & Try-Except:** Safe file reading, encoding support, and saving output

---

## 🚀 3 Ways to Run (Accessible for Everyone)

### 1. 🖥️ Desktop GUI App (Double-Click Ready)
*No terminal needed, zero external packages required.*

- **On Windows:** Simply double-click **`run_desktop_app.bat`** or **`duplicate_finder_gui.pyw`**.
- **Or via Command Prompt:**
  ```bash
  python duplicate_finder_gui.py
  ```
- **Features:**
  - 📄 **Browse file dialog** to easily select any `.txt` file
  - ✏️ **Direct text paste tab** (paste lists directly without saving to a file first)
  - 🔘 Toggle between **Exact match** vs **Ignore case & extra spaces**
  - 📊 Visual **KPI Cards** for Total Items, Unique Items, and Duplicates
  - ⚠️ Sortable **Duplicates table** with repetition counts
  - 💾 **Save to unique.txt**, **Save As...**, and **Copy to Clipboard**

---

### 2. 🌐 Interactive Web Browser App
*Runs locally and automatically opens in your default web browser.*

- **On Windows:** Double-click **`run_web_app.bat`**.
- **Or via Command Prompt:**
  ```bash
  python web_app.py
  ```
- Opens automatically at `http://127.0.0.1:5000/`.
- **Features:**
  - 📂 **Drag & Drop** text files directly into the browser
  - ⚡ Instant live reporting and visual metrics
  - 📱 Works seamlessly across modern desktop & laptop browsers
  - 💾 One-click **"Save unique.txt"** and **"Copy"** buttons
  - 100% built using Python standard library (no `pip install` required!)

---

### 3. ⌨️ Classic Console / Terminal CLI
*The original academic script.*

- **Run:**
  ```bash
  python duplicate_finder.py
  ```
  *(Or double-click `run_cli.bat`)*

---

## 📁 Project Structure

```
PROJECT/
├── duplicate_finder.py        # Core algorithm & Console CLI (PS No. 27)
├── duplicate_finder_gui.py    # Modern Tkinter Desktop GUI
├── duplicate_finder_gui.pyw   # Windowless executable launcher for Windows
├── web_app.py                 # Pure-Python browser-based web application
├── run_desktop_app.bat        # 1-Click launcher for Desktop GUI
├── run_web_app.bat            # 1-Click launcher for Web App
├── run_cli.bat                # 1-Click launcher for Console CLI
├── build_exe.bat              # Script to build standalone Windows .EXE
├── data.txt                   # Sample input dataset (Test Case 1)
├── tc2_single.txt             # Test Case 2 (Single item)
├── tc3_empty.txt              # Test Case 3 (Empty file)
├── tc4_case.txt               # Test Case 4 (Case insensitivity test)
└── README.md                  # Complete documentation
```

---

## 🧪 Test Cases & Results

| # | Test Scenario | Input Data | Matching Mode | Expected Output | Status |
|---|---|---|---|---|---|
| **TC 1** | Standard Duplicates | `apple, banana, apple, orange, banana, apple` | Exact Match | Total: 6 \| Unique: 3 \| Duplicates: apple (3), banana (2) | ✅ Pass |
| **TC 2** | Single Item | `apple` | Exact Match | Total: 1 \| Unique: 1 \| No duplicates | ✅ Pass |
| **TC 3a**| Missing File | `missing_file.txt` | Any | Error message prompted; reprompts cleanly | ✅ Pass |
| **TC 3b**| Empty File | `tc3_empty.txt` (0 bytes) | Any | "File is empty. Nothing to check." | ✅ Pass |
| **TC 4** | Mixed Casing & Spaces | `Apple, apple, banana, APPLE` | Ignore Case & Spaces | Total: 4 \| Unique: 2 \| Duplicates: apple (3) | ✅ Pass |

---

## 📦 How to Create a Standalone Windows .EXE (Optional)
If you want to share this app with someone who does **not** have Python installed:
1. Double-click **`build_exe.bat`**.
2. PyInstaller will package `duplicate_finder_gui.py` into a standalone Windows `.exe` application located in `dist/DuplicateDataFinder/`.
