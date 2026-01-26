# Module 1 Homework: Docker & SQL

This document contains solutions for the Module 1 Homework of the Data Engineering Zoomcamp.

---

## Question 1. Understanding Docker images

**Question:**
Run docker with the `python:3.13` image. Use an entrypoint `bash` to interact with the container.
What's the version of pip in the image?

**Options:**
- [ ] 24.3.1
- [ ] 24.2.1
- [ ] 23.3.1
- [x] **25.3**

### Explanation

**Step 1:** Run the container interactively.
```bash
docker run -it --rm --entrypoint=bash python:3.13
```

**Step 2:** Check the pip version inside the container.
```bash
root@dfc2fcc502e8:/# pip --version
```

**Output:**
```
pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)
```

---

## Question 2. Understanding Docker networking and docker-compose

**Question:**
Given the provided `docker-compose.yaml`, what is the hostname and port that `pgadmin` should use to connect to the postgres database?

**Options:**
- [ ] postgres:5433
- [ ] localhost:5432
- [ ] db:5433
- [ ] postgres:5432
- [x] **db:5432**

### Explanation

Containers within the same Docker Compose network communicate using the **service name** and the **internal port**.

Analyzing `docker-compose.yaml`:
1.  **Service Name:** The Postgres service is named `db`.
2.  **Internal Port:** Inside the container, Postgres listens on port `5432`.
3.  **Host Port:** The mapping `5433:5432` exposes it to the host machine on port 5433, but this does not affect internal container-to-container communication.

Therefore, `pgadmin` must connect to details strictly internal to the docker network: **Host: `db`**, **Port: `5432`**.

---

## Prepare the Data (For Questions 3–6)

The following steps set up the environment to answer the SQL questions.

**1. Start Infrastructure**
```bash
docker compose up -d
```

**2. Download Datasets**
```bash
mkdir -p data
wget https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet -O data/green_tripdata_2025-11.parquet
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv -O data/taxi_zone_lookup.csv
```

**3. Ingest Data**
Using the provided `ingest_data.py` script:
```bash
uv run python homework/ingest_data.py
```

**4. Verify Data in pgAdmin**
- **URL:** `http://localhost:8080`
- **Login:** `pgadmin@pgadmin.com` / `pgadmin`
- **Connect to Server:** Host `db`, Port `5432`, User `postgres`, Password `postgres`, DB `ny_taxi`.

---

## Question 3. Counting short trips

**Question:**
For the trips in **November 2025** (`2025-11-01` to `2025-12-01`), how many trips had a `trip_distance` of less than or equal to 1 mile?

**Options:**
- [ ] 7,853
- [ ] 8,254
- [ ] 8,421
- [x] **8,007**

### Explanation

```sql
SELECT COUNT(*)
FROM green_trips
WHERE lpep_pickup_datetime >= '2025-11-01'
  AND lpep_pickup_datetime < '2025-12-01'
  AND trip_distance <= 1;
```
**Result:** `8007`

---

## Question 4. Longest trip for each day

**Question:**
Which was the pick-up day with the longest trip distance? Only consider trips with `trip_distance` less than 100 miles.

**Options:**
- [ ] 2025-11-20
- [ ] 2025-11-23
- [ ] 2025-11-25
- [x] **2025-11-14**

### Explanation

```sql
SELECT
  DATE(lpep_pickup_datetime) AS pickup_day,
  MAX(trip_distance) AS max_trip_distance
FROM green_trips
WHERE lpep_pickup_datetime >= '2025-11-01'
  AND lpep_pickup_datetime < '2025-12-01'
  AND trip_distance < 100
GROUP BY DATE(lpep_pickup_datetime)
ORDER BY max_trip_distance DESC
LIMIT 1;
```
**Result:** `2025-11-14` (Distance: 88.03)

---

## Question 5. Biggest pickup zone

**Question:**
Which was the pickup zone with the largest `total_amount` (sum of all trips) on **November 18th, 2025**?

**Options:**
- [ ] East Harlem South
- [ ] Morningside Heights
- [ ] Forest Hills
- [x] **East Harlem North**

### Explanation

```sql
SELECT
  z."Zone" AS pickup_zone,
  SUM(t.total_amount) AS total_amount_sum
FROM green_trips t
JOIN zones z
  ON t."PULocationID" = z."LocationID"
WHERE t.lpep_pickup_datetime >= '2025-11-18'
  AND t.lpep_pickup_datetime <  '2025-11-19'
GROUP BY z."Zone"
ORDER BY total_amount_sum DESC
LIMIT 1;
```
**Result:** `East Harlem North` (Sum: ~9281.92)

---

## Question 6. Largest tip

**Question:**
For the passengers picked up in **"East Harlem North"** in November 2025, which drop-off zone had the largest tip?

**Options:**
- [ ] JFK Airport
- [ ] East Harlem North
- [ ] LaGuardia Airport
- [x] **Yorkville West**

### Explanation

```sql
SELECT
  z_drop."Zone" AS dropoff_zone,
  t.tip_amount
FROM green_trips t
JOIN zones z_pick
  ON t."PULocationID" = z_pick."LocationID"
JOIN zones z_drop
  ON t."DOLocationID" = z_drop."LocationID"
WHERE z_pick."Zone" = 'East Harlem North'
  AND t.lpep_pickup_datetime >= '2025-11-01'
  AND t.lpep_pickup_datetime <  '2025-12-01'
ORDER BY t.tip_amount DESC
LIMIT 1;
```
**Result:** `Yorkville West` (Tip: 81.89)

---

## Question 7. Terraform Workflow

**Question:**
Which of the following sequences describes the workflow for:
1.  Downloading provider plugins and setting up backend.
2.  Generating proposed changes and auto-executing the plan.
3.  Removing all resources managed by Terraform.

**Options:**
- [ ] terraform import, terraform apply -y, terraform destroy
- [ ] teraform init, terraform plan -auto-apply, terraform rm
- [ ] terraform init, terraform run -auto-approve, terraform destroy
- [x] **terraform init, terraform apply -auto-approve, terraform destroy**
- [ ] terraform import, terraform apply -y, terraform rm

### Explanation

*   **`terraform init`**: Initializes the working directory, downloads plugins, sets up backend.
*   **`terraform apply -auto-approve`**: Creates/updates resources based on the plan without asking for confirmation (`-auto-approve`).
*   **`terraform destroy`**: Destroys all resources managed by the state.