import os
import urllib.request
import ssl
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

ssl._create_default_https_context = ssl._create_unverified_context

print("Initializing Spark...")
spark = SparkSession.builder \
    .master("local[*]") \
    .appName('hw6') \
    .getOrCreate()

print("Q1 Spark version:", spark.version)

base_dir = "/Users/dinhduy/AI/DE camp 26/data-engineering-zoomcamp/06-batch/homework"
os.makedirs(base_dir, exist_ok=True)
yellow_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-11.parquet"
yellow_file = os.path.join(base_dir, "yellow_tripdata_2025-11.parquet")

if not os.path.exists(yellow_file):
    print("Downloading yellow tripdata...")
    urllib.request.urlretrieve(yellow_url, yellow_file)
else:
    print("Yellow tripdata already exists.")

zone_url = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"
zone_file = os.path.join(base_dir, "taxi_zone_lookup.csv")

if not os.path.exists(zone_file):
    print("Downloading zone lookup data...")
    urllib.request.urlretrieve(zone_url, zone_file)
else:
    print("Zone lookup data already exists.")

print("Reading yellow tripdata...")
df = spark.read.parquet(yellow_file)

# Q2
print("Repartitioning...")
output_dir = os.path.join(base_dir, "yellow_2025_11_repartitioned")
df.repartition(4).write.mode('overwrite').parquet(output_dir)

import glob
parquet_files = glob.glob(os.path.join(output_dir, "*.parquet"))
sizes_mb = [os.path.getsize(f) / (1024 * 1024) for f in parquet_files]
avg_size = sum(sizes_mb) / len(sizes_mb) if sizes_mb else 0
print(f"Q2 Avg size of parquet files: {avg_size:.2f} MB")

# Q3
print("Q3 Counting trips on Nov 15...")
q3_count = df.filter(F.to_date(df.tpep_pickup_datetime) == '2025-11-15').count()
print("Q3 Trips on Nov 15:", q3_count)

# Q4
print("Q4 Longest trip...")
df_with_duration = df.withColumn('duration_hours', (F.unix_timestamp('tpep_dropoff_datetime') - F.unix_timestamp('tpep_pickup_datetime')) / 3600.0)
max_duration = df_with_duration.select(F.max('duration_hours')).collect()[0][0]
print("Q4 Longest trip in hours:", max_duration)

# Q6
print("Q6 Least frequent pickup zone...")
df_zones = spark.read.option("header", "true").csv(zone_file)
df_zones.createOrReplaceTempView('zones_data')
df.createOrReplaceTempView('yellow_data')

spark.sql("""
    SELECT z.Zone, COUNT(1) as trip_count
    FROM yellow_data y
    JOIN zones_data z ON y.PULocationID = z.LocationID
    GROUP BY z.Zone
    ORDER BY trip_count ASC
    LIMIT 5
""").show(truncate=False)
