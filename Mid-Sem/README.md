# CRE II Mid-Sem Study Pack

## Confirmed coverage from the professor's email

The Mid-Semester Examination covers topics discussed up to the lecture on **11 September 2026**:

- **Module 1:** J. M. Smith, Chapters 7 and 8.
- **Module 2:** H. S. Fogler, Chapter 10 through **Section 10.4.4**.
- **Module 3:** O. Levenspiel, Chapter 18 through **Section 18.3**. The solution of the concentration-profile differential equation is not the focus, but the problem formulation, effectiveness factor, and Thiele modulus are included. H. S. Fogler Chapter 15 through **Section 15.3.1** is additional explanation.
- Tutorials 1, 2, and 3, and class notes through 11 September 2026.

This supersedes the earlier assumption that the examination covered only Modules 1 and 2.

## Confirmed book extracts

| File | Source coverage | Printed pages |
|---|---|---|
| `Confirmed Book Extracts/01 - JMS Chapters 7-8.pdf` | J. M. Smith, complete Chapters 7 and 8 | 273–328 |
| `Confirmed Book Extracts/02 - HSF Chapter 10 through 10.4.4.pdf` | H. S. Fogler, Chapter 10 through Section 10.4.4 (all of Example 10-2) | 399–446 |
| `Confirmed Book Extracts/03 - OL Chapter 18 through 18.3.pdf` | O. Levenspiel, Chapter 18 through Section 18.3 (including the summary, eqs 34 and 35) | 376–391 |
| `Confirmed Book Extracts/04 - HSF Chapter 15 through 15.3.1.pdf` | H. S. Fogler, Chapter 15 through Section 15.3.1 (including eqs 15-33 and 15-34) | 719–733 |

Checked on 14 September 2026 against the syllabus, the lecture plan and the email. Extracts 02, 03 and 04 originally stopped one to three pages before the end of their last section; the missing pages were added from the full textbook PDFs in the course folder. The last page of 02, 03 and 04 also shows the start of the next section (§10.5, §18.4, §15.3.2), which is outside the mid-sem syllabus.

The professor's email is included as `Topics of Mid-Semester Examination of CRE II (MO2026).eml`. Tutorials 1, 2, and 3 are also copied into this folder. The original syllabus and lecture plan are included for cross-checking. Page numbers in the extracts are the printed book pages; PDF page numbers may differ because the source files are scans.

## Study pack (HTML)

Open `Study Pack/index.html` in a browser. Pages:

| File | Contents |
|---|---|
| `index.html` | Exam scope, module map, study plan, must-know checklist |
| `m1-heterogeneous-catalysis.html` | Module 1: J. M. Smith Ch. 7–8 |
| `m2-rate-laws.html` | Module 2: Fogler Ch. 10 to §10.4.4, including the full Example 10-2 |
| `m3-pore-diffusion.html` | Module 3: Levenspiel Ch. 18 to §18.3 (with eqs 34, 35), Fogler Ch. 15 to §15.3.1 (with eqs 15-33, 15-34) |
| `tutorials.html` | Tutorials 1, 2, 3 fully solved, with the exact Fogler problem statements for P10-3, P10-5 and P10-6 |
| `formula-sheet-and-practice.html` | Formula sheet, decision charts, exam traps, 15 practice problems, mock paper, rapid-fire questions |

How the pack presents things:

- **Math:** every equation, symbol, unit and chemical formula is typeset with KaTeX, including the labels inside diagrams and the chart axis titles.
- **Diagrams and flowcharts:** drawn as SVG.
- **Charts:** interactive Plotly charts with sliders, toggles and hover values.
- **Offline use:** KaTeX, Plotly and the fonts are bundled in `Study Pack/assets/`, so the pack works without internet.

## Editing the pack

The editable sources are in `Study Pack/_build/src/`; equations are written as `\( ... \)` or `$$ ... $$`, and labels inside SVG diagrams as `<m x=".." y="..">TeX</m>`.

1. `cd "Study Pack/_build"` and run `npm install` once.
2. `node build.js ..` renders the math and writes the pages into `Study Pack/`.
3. `python lint.py ..` fails if any page still contains plain-text math (it needs `beautifulsoup4` and `lxml`).
4. Optional: `node check.js .. shots` opens every page in headless Chrome and saves a screenshot of every figure and chart.
