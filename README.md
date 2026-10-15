# South African School Capacity Explorer

A Python-powered education support-planning dashboard using public Department of Basic Education school data for South Africa. It explores reported 2025 learner and educator counts across provinces and districts, with views of school quintile and urban/rural context.

## Run locally

Requirements: Python 3.10+.

```powershell
python -m pip install -r requirements.txt
python analyze_sa.py
```

Then open `app/index.html` in a browser. Python creates province and district aggregate summaries and embeds them in the HTML, so no web server is needed. Run `analyze_sa.py` again whenever the source workbook changes.

## Data source and scope

The workbook in `data/sa-school-masterlist-q3-2025.xlsx` is the National sheet from the DBE EMIS Schools Masterlist, Quarter 3 of 2025, downloaded from the [official DBE EMIS downloads page](https://www.education.gov.za/Programmes/EMIS/EMISDownloads.aspx).

The analysis includes institutions marked `OPEN`, `PUBLIC`, and `ORDINARY SCHOOL`. Ratio summaries include only records with positive reported `Learners2025` and `Educators2025` counts. The dashboard shows coverage so excluded rows are visible in context.

## What the indicators mean

- **Weighted learner-to-educator ratio:** total reported learners divided by total reported educators across a province or district.
- **Median school ratio:** median of each included school's reported learners divided by educators.
- **Quintiles:** recorded school quintile categories Q1–Q5, shown as counts. Unknown or other categories are excluded from the quintile chart and retained in the data-coverage notes.
- **Rural share:** proportion of included schools marked Rural in the source workbook.
- **District geography:** mean school coordinates per district, used as an approximate centroid. The coordinate plot is not a boundary map.

These are system-planning context measures. A learner-to-educator ratio is not a class size, teacher workload or subject-coverage measure, school-quality score, causal explanation, or automatic funding recommendation. Use aggregate patterns to guide follow-up with local education teams; do not rank individual schools using this dashboard.

The app publishes province and district aggregates only. It does not put school names, addresses, school codes, phone numbers, or individual learner data into the web-facing data.

## Planning workflow

The overview includes a follow-up shortlist for districts with at least 30 reporting schools, ordered by learner-to-educator ratio. It compares each listed ratio with the national aggregate and suggests questions for local validation. This display floor is a usability choice, not a statistical confidence threshold or a determination of need. The filtered district aggregates can be downloaded as a CSV for further review. Always validate against current school-level information and local context before taking action.
