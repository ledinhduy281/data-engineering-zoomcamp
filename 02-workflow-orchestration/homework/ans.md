# Module 2 Homework: Workflow Orchestration

This document contains solutions for the Module 2 Homework of the Data Engineering Zoomcamp.

---

## Question 1. Uncompressed file size

**Question:**
Within the execution for `Yellow` Taxi data for the year `2020` and month `12`: what is the uncompressed file size (i.e. the output file `yellow_tripdata_2020-12.csv` of the `extract` task)?

**Options:**
- [x] **128.3 MiB**
- [ ] 134.5 MiB
- [ ] 364.7 MiB
- [ ] 692.6 MiB

### Explanation

**Method:**
Calculated by streaming the file `https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2020-12.csv.gz` and measuring the decompressed size.
- Exact size: 134,481,400 bytes
- Converted: 128.3 MiB

---

## Question 2. Variable rendering

**Question:**
What is the rendered value of the variable `file` when the inputs `taxi` is set to `green`, `year` is set to `2020`, and `month` is set to `04` during execution?

**Options:**
- [ ] `{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv`
- [x] **`green_tripdata_2020-04.csv`**
- [ ] `green_tripdata_04_2020.csv`
- [ ] `green_tripdata_2020.csv`

### Explanation

**Method:**
Variable inputs substitution into `{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv`:
- `taxi`: green
- `year`: 2020
- `month`: 04
- Result: `green_tripdata_2020-04.csv`

---

## Question 3. Yellow Taxi 2020 Rows

**Question:**
How many rows are there for the `Yellow` Taxi data for all CSV files in the year 2020?

**Options:**
- [ ] 13,537.299
- [x] **24,648,499**
- [ ] 18,324,219
- [ ] 29,430,127

### Explanation

**Method:**
Sum of rows for all yellow taxi CSV files from 2020-01 to 2020-12.
- Total Rows: 24,648,499

---

## Question 4. Green Taxi 2020 Rows

**Question:**
How many rows are there for the `Green` Taxi data for all CSV files in the year 2020?

**Options:**
- [ ] 5,327,301
- [ ] 936,199
- [x] **1,734,051**
- [ ] 1,342,034

### Explanation

**Method:**
Sum of rows for all green taxi CSV files from 2020-01 to 2020-12.
- Total Rows: 1,734,051

---

## Question 5. Yellow Taxi Marsh 2021 Rows

**Question:**
How many rows are there for the `Yellow` Taxi data for the March 2021 CSV file?

**Options:**
- [ ] 1,428,092
- [ ] 706,911
- [x] **1,925,152**
- [ ] 2,561,031

### Explanation

**Method:**
Count of rows in `yellow_tripdata_2021-03.csv`.
- Rows: 1,925,152

---

## Question 6. Schedule Trigger Timezone

**Question:**
How would you configure the timezone to New York in a Schedule trigger?

**Options:**
- [ ] Add a `timezone` property set to `EST` in the `Schedule` trigger configuration
- [x] **Add a `timezone` property set to `America/New_York` in the `Schedule` trigger configuration**
- [ ] Add a `timezone` property set to `UTC-5` in the `Schedule` trigger configuration
- [ ] Add a `location` property set to `New_York` in the `Schedule` trigger configuration

### Explanation

**Method:**
Kestra `Schedule` trigger supports a `timezone` property which expects a Zone ID (e.g., `America/New_York`).
