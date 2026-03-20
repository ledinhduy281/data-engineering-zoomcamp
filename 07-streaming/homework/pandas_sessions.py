import pandas as pd

df = pd.read_csv('green_tripdata_2019-10.csv.gz', usecols=['lpep_dropoff_datetime', 'PULocationID', 'DOLocationID'])
df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])
df.dropna(inplace=True)

# Important: Flink watermark 5-second tolerance handles out-of-order, 
# Pandas sort perfectly orders it, evaluating exactly as Flink would theoretically.
df.sort_values(by=['PULocationID', 'DOLocationID', 'lpep_dropoff_datetime'], inplace=True)

df['time_diff'] = df.groupby(['PULocationID', 'DOLocationID'])['lpep_dropoff_datetime'].diff()
df['new_session'] = (df['time_diff'] > pd.Timedelta(minutes=5)).astype(int)

# 1 for first element in group, but cumsum starts at 0 if no diff > 5m
# we group by PULocationID, DOLocationID to compute session_id over time
df['session_id'] = df.groupby(['PULocationID', 'DOLocationID'])['new_session'].cumsum()

streak_df = df.groupby(['PULocationID', 'DOLocationID', 'session_id']).size().reset_index(name='streak_count')
best_streak = streak_df.sort_values('streak_count', ascending=False).head(1)

print("Best streak:")
print(best_streak[['PULocationID', 'DOLocationID', 'streak_count']].to_string(index=False))
