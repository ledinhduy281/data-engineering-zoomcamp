import dlt
import requests
import duckdb

@dlt.resource(name="rides", write_disposition="replace")
def ny_taxi():
    url = "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api"
    page = 1
    while True:
        response = requests.get(url, params={"page": page})
        response.raise_for_status()
        data = response.json()
        if not data:
            break
        yield data
        page += 1

if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="taxi_pipeline",
        destination="duckdb",
        dataset_name="taxi_data"
    )
    
    # Run the pipeline
    load_info = pipeline.run(ny_taxi())
    print("Pipeline Load Info:")
    print(load_info)
    
    # Connect to the DuckDB database
    conn = duckdb.connect(f"{pipeline.pipeline_name}.duckdb")
    
    conn.execute("SET search_path = 'taxi_data'")
    
    # Question 1: What is the start date and end date of the dataset?
    print("\n--- Question 1 ---")
    res1 = conn.execute("SELECT MIN(trip_dropoff_date_time), MAX(trip_dropoff_date_time) FROM rides").fetchall()
    print(f"Dropoff dates: {res1}")
    
    # Question 2: What proportion of trips are paid with credit card?
    print("\n--- Question 2 ---")
    res2 = conn.execute("SELECT payment_type, COUNT(*) as cnt FROM rides GROUP BY payment_type").fetchall()
    print(f"Payment types counts: {res2}")
    
    total = sum(row[1] for row in res2)
    credit_cnt = next((row[1] for row in res2 if row[0] == 'Credit'), 0)
    print(f"Credit card proportion: {credit_cnt / total * 100:.2f}%")

    # Question 3: What is the total amount of money generated in tips?
    print("\n--- Question 3 ---")
    res3 = conn.execute("SELECT SUM(tip_amt) FROM rides").fetchone()[0]
    print(f"Total tips: {res3}")
