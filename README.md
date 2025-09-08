# paper_notes_organizer
A lightweight, keyword-searchable system for maintaining structured notes on academic papers, with PDF export support via LaTeX.

---

## 🧩 Structure

```bash
paper-reading-log/
├── notes/                  # ← Your paper notes (.txt)
├── templates/              # LaTeX templates for PDF rendering
│   ├── full_template.tex
│   └── simple_template.tex
├── exporter.py             # Main script to search and export notes
├── config.yaml             # Config: keywords + export mode
├── .gitignore
└── README.md
```
---

## ✍️ How to Write Notes (very important)

Each paper should have its own `.txt` file inside the `notes/` directory.

### 🔹 Required formatting rules:

- **Each field ends with a `.`** (even multiline fields).
- Field names and values are separated by a colon `:`.
- All lines must follow the pattern:  
  `Field_Name: value.`  
- Multi-line values are supported as long as they end with a single `.` on the last line.
- Field names are case-sensitive (e.g., `First_Author`, not `First Author`).

### ✅ Example note file: `Me2025.txt`

Year: 2025.
First_Author: Me.
PI: My PI.
University: My school.
Title: My title.
Conclusion: My conclusion. 
Experiment_Methods: method1, method2.
Analysis_Methods: model1, model2.
Notes: None.
Keywords: keyword1, keyword2, keyword3.

---

## ⚙️ Configuration: `config.yaml`

Use this file to control what gets exported.

```yaml
keywords:
  - SST
  - PV

export_mode: full  # or "simple"
```
---

## 🚀 Export Notes to PDF

- Ensure LaTeX is installed (`pdflatex` in your PATH)
- From the root of the repo, run:
```
python exporter.py
```
- This will:
  - Read all notes from `notes/`
  - Filter them based on keywords in `config.yaml`
  - Sort them by Year
  - Render them using the specified LaTeX template (`full_template.tex` or `simple_template.tex`)
  - Compile a clean PDF file: `filtered_notes_full.pdf` or `filtered_notes_simple.pdf`