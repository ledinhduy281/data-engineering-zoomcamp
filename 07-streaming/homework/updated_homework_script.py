import pandas as pd
from time import time
import json
from kafka import KafkaProducer

file_name = 'green_tripdata_2025-10.parquet'
df = pd.read_parquet(file_name)

# Q3: trips have trip_distance > 5
q3_ans = (df['trip_distance'] > 5).sum()
print("Q3:", q3_ans)

# Q4: Tumbling window - pickup location
df_q4 = df.copy()
df_q4.set_index('lpep_pickup_datetime', inplace=True)
q4_ans = df_q4.groupby('PULocationID').resample('5min').size().reset_index(name='num_trips')
print("Q4:", q4_ans.sort_values(by='num_trips', ascending=False).head(3))

# Q5: Session window - longest streak
df_q5 = df.copy()
df_q5.sort_values(by=['PULocationID', 'lpep_pickup_datetime'], inplace=True)
df_q5['time_diff'] = df_q5.groupby('PULocationID')['lpep_pickup_datetime'].diff()
df_q5['new_session'] = (df_q5['time_diff'] > pd.Timedelta(minutes=5)).astype(int)
df_q5['session_id'] = df_q5.groupby('PULocationID')['new_session'].cumsum()

streak_df = df_q5.groupby(['PULocationID', 'session_id']).size().reset_index(name='streak_count')
print("Q5:", streak_df.sort_values(by='streak_count', ascending=False).head(3))

# Q6: Tumbling window - largest tip
df_q6 = df.copy()
df_q6.set_index('lpep_pickup_datetime', inplace=True)
q6_ans = df_q6.resample('1h')['tip_amount'].sum().reset_index()
print("Q6:", q6_ans.sort_values(by='tip_amount', ascending=False).head(3))

# Q2: Kafka send time
def json_serializer(data):
    return json.dumps(data).encode('utf-8')

try:
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=json_serializer
    )

    columns = [
        'lpep_pickup_datetime',
        'lpep_dropoff_datetime',
        'PULocationID',
        'DOLocationID',
        'passenger_count',
        'trip_distance',
        'tip_amount',
        'total_amount'
    ]

    df_send = df[columns].copy()
    # Handle datetime for json serialization
    df_send['lpep_pickup_datetime'] = df_send['lpep_pickup_datetime'].astype(str)
    df_send['lpep_dropoff_datetime'] = df_send['lpep_dropoff_datetime'].astype(str)

    t0 = time()
    for row in df_send.itertuples(index=False):
        row_dict = {col: getattr(row, col) for col in columns}
        producer.send('green-trips', value=row_dict)

    producer.flush()
    t1 = time()
    print("Q2 time taken:", t1 - t0)
except Exception as e:
    print("Kafka Error:", str(e))
