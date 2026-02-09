# Module 3 Homework: Data Warehouse

This document contains solutions for the Module 3 Homework of the Data Engineering Zoomcamp.

---

## Question 1. Count of records for the 2024 Yellow Taxi Data

**Question:**
What is count of records for the 2024 Yellow Taxi Data?

**Options:**
- [ ] 65,623
- [ ] 840,402
- [x] **20,332,093**
- [ ] 85,431,289

### Explanation

**Method:**
Counted rows in Parquet files for Jan-Jun 2024.
- Total Rows: 20,332,093

---

## Question 2. Estimated amount of data (Distinct PULocationID)

**Question:**
Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.
What is the **estimated amount** of data that will be read when this query is executed on the External Table and the Table?

**Options:**
- [ ] 18.82 MB for the External Table and 47.60 MB for the Materialized Table
- [x] **0 MB for the External Table and 155.12 MB for the Materialized Table**
- [ ] 2.14 GB for the External Table and 0MB for the Materialized Table
- [ ] 0 MB for the External Table and 0MB for the Materialized Table

### Explanation

**Reasoning:**
- **External Table**: BigQuery often reports 0 MB (or simply cannot estimate accurately without reading files) for external tables before execution because metadata is not managed by BQ.
- **Materialized Table**: Scanning `PULocationID` (Int64, 8 bytes) for ~20.3M rows: 20,332,093 * 8 bytes ≈ 162 MB. 155.12 MB is the closest value (likely compressed or slight variance in row count/data types).

---

## Question 3. Columnar Scan (PULocationID vs PULocationID + DOLocationID)

**Question:**
Why are the estimated number of Bytes different?

**Options:**
- [x] **BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.**
- [ ] BigQuery duplicates data across multiple storage partitions...
- [ ] BigQuery automatically caches the first queried column...
- [ ] When selecting multiple columns, BigQuery performs an implicit join...

### Explanation

BigQuery stores data in columns. Selecting more columns means reading more data blocks.

---

## Question 4. Count of records with fare_amount = 0

**Question:**
How many records have a fare_amount of 0?

**Options:**
- [ ] 128,210
- [ ] 546,578
- [ ] 20,188,016
- [x] **8,333**

### Explanation

**Method:**
Filtered rows where `fare_amount == 0` in the Jan-Jun 2024 dataset.
- Count: 8,333

---

## Question 5. Best Strategy for Optimized Table

**Question:**
What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID?

**Options:**
- [x] **Partition by tpep_dropoff_datetime and Cluster on VendorID**
- [ ] Cluster on by tpep_dropoff_datetime and Cluster on VendorID
- [ ] Cluster on tpep_dropoff_datetime Partition by VendorID
- [ ] Partition by tpep_dropoff_datetime and Partition by VendorID

### Explanation

- **Partitioning** by `tpep_dropoff_datetime` prunes partitions during filtering.
- **Clustering** by `VendorID` co-locates data for faster sorting/aggregation.

---

## Question 6. Estimated Bytes for Distinct VendorIDs (Partitioned vs Non-Partitioned)

**Question:**
Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive).
What are the estimated bytes processed for non-partitioned vs partitioned tables?

**Options:**
- [ ] 12.47 MB for non-partitioned table and 326.42 MB for the partitioned table
- [x] **310.24 MB for non-partitioned table and 26.84 MB for the partitioned table**
- [ ] 5.87 MB for non-partitioned table and 0 MB for the partitioned table
- [ ] 310.31 MB for non-partitioned table and 285.64 MB for the partitioned table

### Explanation

- **Non-partitioned**: Scans `tpep_dropoff_datetime` and `VendorID` for the entire dataset (~20.3M rows). Eqiv to ~310 MB.
- **Partitioned**: Scans only the partitions for March 1-15 (approx 15 days out of 180 days). 310 MB * (15/180) ≈ 26 MB.

---

## Question 7. External Table Storage

**Question:**
Where is the data stored in the External Table you created?

**Options:**
- [ ] Big Query
- [ ] Container Registry
- [x] **GCP Bucket**
- [ ] Big Table

### Explanation

External tables in BigQuery point to data stored in external storage systems, in this case, Google Cloud Storage (GCP Bucket).

---

## Question 8. Clustering Best Practice

**Question:**
It is best practice in Big Query to always cluster your data:

**Options:**
- [ ] True
- [x] **False**

### Explanation

For small tables (typically < 1 GB), clustering and partitioning might not provide significant performance benefits and can add metadata overhead.

---

## (Bonus) Question 9. Count(*) on Materialized Table

**Question:**
Write a `SELECT count(*)` query FROM the materialized table you created. How many bytes does it estimate will be read? Why?

**Answer**: 0 bytes. BigQuery stores table metadata, including row counts, so it doesn't need to scan any data for a simple `COUNT(*)`.
