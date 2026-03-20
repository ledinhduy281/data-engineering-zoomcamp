import pandas as pd

df = pd.read_csv('green_tripdata_2019-10.csv.gz', usecols=['lpep_pickup_datetime', 'PULocationID', 'DOLocationID', 'tip_amount'])
df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
df.dropna(inplace=True)

# Question 4: Tumbling window - pickup location
df_q4 = df.copy()
df_q4.set_index('lpep_pickup_datetime', inplace=True)
q4_counts = df_q4.groupby('PULocationID').resample('5min').size().reset_index(name='num_trips')
print("Q4 answers:")
print(q4_counts.sort_values('num_trips', ascending=False).head(5))

# Question 5: Session window - longest streak
df_q5 = df.copy()
df_q5.sort_values(by=['PULocationID', 'lpep_pickup_datetime'], inplace=True)
df_q5['time_diff'] = df_q5.groupby('PULocationID')['lpep_pickup_datetime'].diff()
df_q5['new_session'] = (df_q5['time_diff'] > pd.Timedelta(minutes=5)).astype(int)
df_q5['session_id'] = df_q5.groupby('PULocationID')['new_session'].cumsum()

streak_df = df_q5.groupby(['PULocationID', 'session_id']).size().reset_index(name='streak_count')
print("\nQ5 answers:")
print(streak_df.sort_values('streak_count', ascending=False).head(5))

# Question 6. Tumbling window - largest tip
df_q6 = df.copy()
df_q6.set_index('lpep_pickup_datetime', inplace=True)
q6_tips = df_q6.resample('1h')['tip_amount'].sum().reset_index()
print("\nQ6 answers:")
print(q6_tips.sort_values('tip_amount', ascending=False).head(5))
