"""
============================================================
Duplicate Data Finder - Modern Desktop GUI (PS No. 27)
Language : Python 3 (Tkinter - No external packages needed!)
============================================================
Features:
- Select a .txt file OR paste text directly
- Exact match vs Ignore case and extra spaces
- Visual summary metrics (Total, Unique, Duplicates)
- Detailed duplicates table with repetition counts
- Clean unique items viewer
- Save to unique.txt or Save As...
- Single-click clipboard copy
============================================================
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


# ------------------------------------------------------------
# Core Logic Functions (from PS No. 27)
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
            duplicates.append((item, count))
    return duplicates


def parse_raw_text(raw_text):
    """Split text into lines, strip whitespace, and omit blank lines."""
    lines = raw_text.splitlines()
    entries = []
    for line in lines:
        cleaned = line.strip()
        if cleaned != "":
            entries.append(cleaned)
    return entries


def read_file_entries(file_path):
    """Read entries from a file path."""
    if not os.path.exists(file_path):
        return None
    for enc in ("utf-8", "latin-1", "cp1252"):
        try:
            with open(file_path, "r", encoding=enc) as f:
                return parse_raw_text(f.read())
        except UnicodeDecodeError:
            continue
        except Exception:
            return None
    return None


# ------------------------------------------------------------
# GUI Application
# ------------------------------------------------------------

class DuplicateFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Duplicate Data Finder - PS No. 27")
        self.root.geometry("860x700")
        self.root.minsize(760, 600)

        # State
        self.current_entries = []
        self.current_unique = []
        self.current_duplicates = []

        # Color Theme
        self.bg_color = "#f1f5f9"        # Slate light
        self.card_bg = "#ffffff"         # White
        self.header_bg = "#0f172a"       # Deep slate
        self.header_fg = "#ffffff"
        self.accent_color = "#2563eb"     # Blue accent
        self.success_color = "#16a34a"    # Green
        self.warning_color = "#d97706"    # Amber
        self.text_dark = "#1e293b"

        self.root.configure(bg=self.bg_color)
        self._setup_styles()
        self._build_ui()

    def _setup_styles(self):
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

        self.style.configure(".", background=self.bg_color, foreground=self.text_dark, font=("Segoe UI", 10))
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("Card.TFrame", background=self.card_bg, relief="flat")
        self.style.configure("TLabelframe", background=self.bg_color, font=("Segoe UI", 10, "bold"))
        self.style.configure("TLabelframe.Label", background=self.bg_color, foreground=self.text_dark)

        # Buttons
        self.style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), background=self.accent_color, foreground="#ffffff")
        self.style.map("Primary.TButton",
                       background=[("active", "#1d4ed8"), ("pressed", "#1e40af")],
                       foreground=[("active", "#ffffff"), ("pressed", "#ffffff")])

        self.style.configure("Success.TButton", font=("Segoe UI", 9, "bold"), background=self.success_color, foreground="#ffffff")
        self.style.map("Success.TButton",
                       background=[("active", "#15803d")],
                       foreground=[("active", "#ffffff")])

        self.style.configure("Secondary.TButton", font=("Segoe UI", 9))
        
        # Treeview styling
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#e2e8f0", foreground=self.text_dark)
        self.style.configure("Treeview", font=("Segoe UI", 10), rowheight=26, background="#ffffff", fieldbackground="#ffffff")
        self.style.map("Treeview", background=[("selected", "#dbeafe")], foreground=[("selected", "#1e3a8a")])

    def _build_ui(self):
        # 1. Header Banner
        header = tk.Frame(self.root, bg=self.header_bg, padx=20, pady=16)
        header.pack(fill="x", side="top")

        title_lbl = tk.Label(header, text="🔍 Duplicate Data Finder", font=("Segoe UI", 16, "bold"), fg=self.header_fg, bg=self.header_bg)
        title_lbl.pack(anchor="w")

        subtitle_lbl = tk.Label(header, text="Detect repeated items, analyze frequencies, and export clean unique lists",
                                font=("Segoe UI", 9), fg="#94a3b8", bg=self.header_bg)
        subtitle_lbl.pack(anchor="w")

        # Main Container
        main_frame = ttk.Frame(self.root, padding=16)
        main_frame.pack(fill="both", expand=True)

        # 2. Input Section (Notebook: File vs Direct Paste)
        input_group = ttk.LabelFrame(main_frame, text=" 1. Input Source ", padding=10)
        input_group.pack(fill="x", pady=(0, 10))

        self.notebook = ttk.Notebook(input_group)
        self.notebook.pack(fill="x", expand=True)

        # Tab 1: File selection
        file_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(file_tab, text=" 📄 Select File ")

        ttk.Label(file_tab, text="File Path:").pack(side="left", padx=(0, 6))
        self.file_path_var = tk.StringVar(value="data.txt" if os.path.exists("data.txt") else "")
        self.file_entry = ttk.Entry(file_tab, textvariable=self.file_path_var, font=("Segoe UI", 9))
        self.file_entry.pack(side="left", fill="x", expand=True, padx=6)

        browse_btn = ttk.Button(file_tab, text="Browse...", style="Secondary.TButton", command=self.browse_file)
        browse_btn.pack(side="left", padx=(0, 6))

        load_sample_btn = ttk.Button(file_tab, text="Load Sample", style="Secondary.TButton", command=self.load_sample)
        load_sample_btn.pack(side="left")

        # Tab 2: Direct paste
        paste_tab = ttk.Frame(self.notebook, padding=6)
        self.notebook.add(paste_tab, text=" ✏️ Paste / Type Lines ")

        self.paste_text = tk.Text(paste_tab, height=4, font=("Consolas", 10), wrap="none", relief="solid", bd=1)
        self.paste_text.pack(fill="x", expand=True)
        self.paste_text.insert("1.0", "apple\nbanana\napple\norange\nbanana\napple")

        # 3. Matching Options & Process Button
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill="x", pady=(0, 12))

        opts_group = ttk.LabelFrame(options_frame, text=" 2. Matching Mode ", padding=8)
        opts_group.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.match_mode = tk.StringVar(value="1")
        rb1 = ttk.Radiobutton(opts_group, text="Exact match (case-sensitive)", value="1", variable=self.match_mode)
        rb1.pack(side="left", padx=10)
        rb2 = ttk.Radiobutton(opts_group, text="Ignore case & extra spaces (apple == APPLE)", value="2", variable=self.match_mode)
        rb2.pack(side="left", padx=10)

        # Action Buttons Frame
        btn_frame = ttk.Frame(options_frame)
        btn_frame.pack(side="right", fill="y", padx=(0, 0))

        find_btn = ttk.Button(btn_frame, text="🔍 Analyze Data", style="Primary.TButton", command=self.run_analysis)
        find_btn.pack(side="left", padx=4, ipady=6, ipadx=10)

        clear_btn = ttk.Button(btn_frame, text="🔄 Reset", style="Secondary.TButton", command=self.reset_all)
        clear_btn.pack(side="left", padx=4, ipady=6)

        # 4. Summary Metric Cards
        self.metrics_frame = ttk.Frame(main_frame)
        self.metrics_frame.pack(fill="x", pady=(0, 12))

        self.card_total = self._create_metric_card(self.metrics_frame, "TOTAL ITEMS", "0", "#2563eb")
        self.card_unique = self._create_metric_card(self.metrics_frame, "UNIQUE ITEMS", "0", "#16a34a")
        self.card_dups = self._create_metric_card(self.metrics_frame, "DUPLICATES DETECTED", "0", "#d97706")

        self.card_total.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.card_unique.pack(side="left", fill="x", expand=True, padx=6)
        self.card_dups.pack(side="left", fill="x", expand=True, padx=(6, 0))

        # 5. Results Split View
        results_frame = ttk.Frame(main_frame)
        results_frame.pack(fill="both", expand=True, pady=(0, 10))

        # Left: Duplicates table
        dup_group = ttk.LabelFrame(results_frame, text=" ⚠️ Duplicates Found (Frequency) ", padding=8)
        dup_group.pack(side="left", fill="both", expand=True, padx=(0, 6))

        columns = ("item", "count")
        self.dup_tree = ttk.Treeview(dup_group, columns=columns, show="headings", selectmode="browse")
        self.dup_tree.heading("item", text="Entry Item")
        self.dup_tree.heading("count", text="Times Repeated")
        self.dup_tree.column("item", width=220, anchor="w")
        self.dup_tree.column("count", width=110, anchor="center")

        dup_scroll = ttk.Scrollbar(dup_group, orient="vertical", command=self.dup_tree.yview)
        self.dup_tree.configure(yscrollcommand=dup_scroll.set)
        self.dup_tree.pack(side="left", fill="both", expand=True)
        dup_scroll.pack(side="right", fill="y")

        # Right: Unique list preview
        uniq_group = ttk.LabelFrame(results_frame, text=" ✅ Unique Items List (Cleaned) ", padding=8)
        uniq_group.pack(side="right", fill="both", expand=True, padx=(6, 0))

        self.uniq_text = tk.Text(uniq_group, font=("Consolas", 10), wrap="none", relief="solid", bd=1)
        uniq_scroll = ttk.Scrollbar(uniq_group, orient="vertical", command=self.uniq_text.yview)
        self.uniq_text.configure(yscrollcommand=uniq_scroll.set)
        self.uniq_text.pack(side="left", fill="both", expand=True)
        uniq_scroll.pack(side="right", fill="y")

        # 6. Bottom Export Actions Bar
        export_frame = ttk.Frame(main_frame)
        export_frame.pack(fill="x", pady=(0, 4))

        save_default_btn = ttk.Button(export_frame, text="💾 Save to unique.txt", style="Success.TButton", command=self.save_default)
        save_default_btn.pack(side="left", padx=(0, 6), ipady=3)

        save_as_btn = ttk.Button(export_frame, text="📂 Save As...", style="Secondary.TButton", command=self.save_custom)
        save_as_btn.pack(side="left", padx=6, ipady=3)

        copy_btn = ttk.Button(export_frame, text="📋 Copy Unique to Clipboard", style="Secondary.TButton", command=self.copy_to_clipboard)
        copy_btn.pack(side="left", padx=6, ipady=3)

        # 7. Status Bar
        self.status_var = tk.StringVar(value="Ready. Select an input source and click 'Analyze Data'.")
        status_bar = tk.Label(self.root, textvariable=self.status_var, font=("Segoe UI", 9),
                              anchor="w", bg="#e2e8f0", fg="#334155", padx=12, pady=5)
        status_bar.pack(side="bottom", fill="x")

        # Auto-run if default file exists
        if os.path.exists("data.txt"):
            self.run_analysis()

    def _create_metric_card(self, parent, label_text, default_value, color):
        frame = tk.Frame(parent, bg=self.card_bg, relief="solid", bd=1, padx=12, pady=8)
        lbl_title = tk.Label(frame, text=label_text, font=("Segoe UI", 8, "bold"), fg="#64748b", bg=self.card_bg)
        lbl_title.pack(anchor="w")

        val_lbl = tk.Label(frame, text=default_value, font=("Segoe UI", 18, "bold"), fg=color, bg=self.card_bg)
        val_lbl.pack(anchor="w")

        frame.val_lbl = val_lbl
        return frame

    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Select Text File",
            filetypes=[("Text files (*.txt)", "*.txt"), ("All files (*.*)", "*.*")]
        )
        if filename:
            self.file_path_var.set(filename)
            self.notebook.select(0)
            self.run_analysis()

    def load_sample(self):
        if os.path.exists("data.txt"):
            self.file_path_var.set("data.txt")
            self.notebook.select(0)
            self.run_analysis()
        else:
            self.notebook.select(1)
            self.paste_text.delete("1.0", tk.END)
            sample = "apple\nbanana\napple\norange\nbanana\napple"
            self.paste_text.insert("1.0", sample)
            self.run_analysis()

    def reset_all(self):
        self.current_entries = []
        self.current_unique = []
        self.current_duplicates = []
        self.card_total.val_lbl.config(text="0")
        self.card_unique.val_lbl.config(text="0")
        self.card_dups.val_lbl.config(text="0")
        for row in self.dup_tree.get_children():
            self.dup_tree.delete(row)
        self.uniq_text.delete("1.0", tk.END)
        self.status_var.set("Reset complete. Ready.")

    def run_analysis(self):
        active_tab = self.notebook.index(self.notebook.select())

        if active_tab == 0:
            # File mode
            filepath = self.file_path_var.get().strip()
            if not filepath:
                messagebox.showwarning("File Missing", "Please select or type a file name.")
                return
            entries = read_file_entries(filepath)
            if entries is None:
                messagebox.showerror("File Error", f"Could not read file: '{filepath}'\nPlease verify the file exists.")
                self.status_var.set(f"Error: File '{filepath}' not found.")
                return
            source_desc = f"file '{os.path.basename(filepath)}'"
        else:
            # Direct paste mode
            raw_text = self.paste_text.get("1.0", tk.END)
            entries = parse_raw_text(raw_text)
            source_desc = "pasted text"

        if len(entries) == 0:
            messagebox.showinfo("Empty Data", "The input contains no non-empty lines.\nNothing to check.")
            self.reset_all()
            self.status_var.set("Input is empty.")
            return

        # Handle match option
        mode = self.match_mode.get()
        if mode == "2":
            processed_entries = [clean_entry(item) for item in entries]
        else:
            processed_entries = entries

        unique_list = get_unique(processed_entries)
        duplicates = find_duplicates(processed_entries, unique_list)

        # Store state
        self.current_entries = processed_entries
        self.current_unique = unique_list
        self.current_duplicates = duplicates

        # Update Metric Cards
        self.card_total.val_lbl.config(text=str(len(processed_entries)))
        self.card_unique.val_lbl.config(text=str(len(unique_list)))
        self.card_dups.val_lbl.config(text=str(len(duplicates)))

        # Update Duplicates Treeview
        for row in self.dup_tree.get_children():
            self.dup_tree.delete(row)

        if len(duplicates) == 0:
            self.dup_tree.insert("", "end", values=("(No duplicates found)", "0"))
        else:
            for item, count in duplicates:
                self.dup_tree.insert("", "end", values=(item, f"{count} times"))

        # Update Unique Textbox
        self.uniq_text.delete("1.0", tk.END)
        self.uniq_text.insert("1.0", "\n".join(unique_list))

        self.status_var.set(
            f"Analyzed {source_desc}: {len(processed_entries)} items, {len(unique_list)} unique, {len(duplicates)} duplicate group(s)."
        )

    def save_default(self):
        if not self.current_unique:
            messagebox.showwarning("Nothing to Save", "Please analyze some data before saving.")
            return
        output_file = "unique.txt"
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                for item in self.current_unique:
                    f.write(item + "\n")
            messagebox.showinfo("Saved", f"Unique entries saved successfully to:\n{os.path.abspath(output_file)}")
            self.status_var.set(f"Saved {len(self.current_unique)} unique items to {output_file}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save file: {e}")

    def save_custom(self):
        if not self.current_unique:
            messagebox.showwarning("Nothing to Save", "Please analyze some data before saving.")
            return
        output_file = filedialog.asksaveasfilename(
            title="Save Unique Entries As",
            defaultextension=".txt",
            filetypes=[("Text files (*.txt)", "*.txt"), ("All files (*.*)", "*.*")],
            initialfile="unique.txt"
        )
        if output_file:
            try:
                with open(output_file, "w", encoding="utf-8") as f:
                    for item in self.current_unique:
                        f.write(item + "\n")
                messagebox.showinfo("Saved", f"Unique entries saved to:\n{output_file}")
                self.status_var.set(f"Saved {len(self.current_unique)} items to {output_file}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save file: {e}")

    def copy_to_clipboard(self):
        if not self.current_unique:
            messagebox.showwarning("Nothing to Copy", "No unique items to copy.")
            return
        text = "\n".join(self.current_unique)
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.status_var.set(f"Copied {len(self.current_unique)} unique entries to clipboard!")


def main():
    root = tk.Tk()
    app = DuplicateFinderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
