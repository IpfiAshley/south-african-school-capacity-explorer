# South African School Capacity Explorer

A Python-powered education support-planning dashboard using public Department of Basic Education school data for South Africa. It explores reported 2025 learner and educator counts across provinces and districts, with views of school quintile and urban/rural context.

## Run locally

Requirements: Python 3.10+.

```powershell
python -m pip install -r requirements.txt
python analyze_sa.py
```

Then open `app/index.html` in a browser. Python creates province and district summaries plus a local school list with visit-planning fields and review scores. `app/schools.local.js` contains school names, locations, and school-level indicators; it is generated locally and excluded from Git. The checked-in dashboard contains only aggregate school data, so the school visit planner and school-level review screen work after running the analysis locally. Run `analyze_sa.py` again whenever the source workbook changes.

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

The checked-in dashboard data contains province and district aggregates only. It does not include school names, addresses, school codes, phone numbers, or individual learner records. Running the analysis locally creates a separate ignored file with school names, coordinates, and school-level aggregate indicators.

## Planning workflow

The overview includes a follow-up shortlist for districts with at least 30 reporting schools, ordered by learner-to-educator ratio. It compares each listed ratio with the national aggregate and suggests questions for local validation. This display floor is a usability choice, not a statistical confidence threshold or a determination of need. The filtered district aggregates can be downloaded as a CSV for further review. Always validate against current school-level information and local context before taking action.


## School visit planning

The local overview builds a school visit shortlist using user-selected district, quintile, setting, learner-to-educator threshold, and maximum visit count. It sorts the matches by the reported ratio and includes valid map links and a CSV export. `analyze_sa.py` generates `app/schools.local.js` from the official workbook. That file contains school names and locations and is intentionally excluded from Git. The public dashboard therefore provides aggregate province and district views; the school-level planner is available when you run the project locally. The planner does not estimate need or school quality. Confirm the records and local conditions before scheduling visits.


## School support risk screen

After running the analysis locally, the overview includes a school-level review screen. It can be filtered by review band and follows the selected province and district search. It lists up to 100 schools, ordered by score, and shows the indicators contributing to each score. The score is a transparent, hand-set review-priority index:

- Learner-to-educator ratio percentile within the included South African schools: up to 70 points.
- Recorded quintile context: Q1 30 points, Q2 22, Q3 14, Q4 7, Q5 0, and unknown 0.
- Review bands: high (70 or more), elevated (45–69), and routine (below 45).

This is a screening rule, not a machine-learning model, validated risk estimate, or probability of dropout, poor performance, or any other outcome. The 2025 masterlist has no longitudinal learner outcomes or school-level support-need labels, so it cannot train or validate those predictions. Quintile is broad contextual information, not an individual measure of need. Use this screen to prompt human review; do not use it by itself for funding, placement, or service decisions. School-level outputs stay in the ignored local file and are not pushed to GitHub.
