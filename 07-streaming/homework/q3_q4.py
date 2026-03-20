import json
import pandas as pd
from time import time
from kafka import KafkaProducer

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

server = 'localhost:9092'

# Question 3
try:
    producer = KafkaProducer(
        bootstrap_servers=[server],
        value_serializer=json_serializer
    )
    print("Q3:", producer.bootstrap_connected())
except Exception as e:
    print("Failed answering Q3:", e)

# Question 4
try:
    topic_name = 'green-trips'
    columns = [
        'lpep_pickup_datetime',
        'lpep_dropoff_datetime',
        'PULocationID',
        'DOLocationID',
        'passenger_count',
        'trip_distance',
        'tip_amount'
    ]

    print("Loading dataframe...")
    df_green = pd.read_csv('green_tripdata_2019-10.csv.gz', usecols=columns)
    
    # We should convert datetime columns to strings or similar if necessary, 
    # but kafka-python can serialize strings. Let's make sure it's serialized correctly.
    # However, read_csv keeps them as strings anyway unless parse_dates is used.
    
    t0 = time()
    for row in df_green.itertuples(index=False):
        row_dict = {col: getattr(row, col) for col in columns}
        producer.send(topic_name, value=row_dict)
        
    producer.flush()
    t1 = time()
    print(f"Q4: Took {t1 - t0} seconds")
except Exception as e:
    print("Failed answering Q4:", e)
