# Week 7 Homework

## Question 1. Redpanda version

Run `rpk version` inside the Redpanda container:

```bash
docker exec -it workshop-redpanda-1 rpk version
```

What version of Redpanda are you running?

**v24.2.18 - f9a22d443087b824803638623d6b7492ec8221f9**

## Question 2. Sending data to Redpanda

Create a topic called `green-trips`. Now write a producer to send the green taxi data to this topic.
Convert each row to a dictionary and send it to the `green-trips` topic.
You'll need to handle the datetime columns - convert them to strings before serializing to JSON.
Measure the time it takes to send the entire dataset and flush.

How long did it take to send the data?

- **10 seconds**
- 60 seconds
- 120 seconds
- 300 seconds

## Question 3. Consumer - trip distance

Write a Kafka consumer that reads all messages from the `green-trips` topic (set `auto_offset_reset='earliest'`).

Count how many trips have a `trip_distance` greater than 5.0 kilometers.

How many trips have `trip_distance` > 5?

- 6506
- 7506
- **8506**
- 9506

## Question 4. Tumbling window - pickup location

Create a Flink job that reads from `green-trips` and uses a 5-minute tumbling window to count trips per `PULocationID`.

Write the results to a PostgreSQL table with columns: `window_start`, `PULocationID`, `num_trips`.

Which `PULocationID` had the most trips in a single 5-minute window?

- 42
- **74**
- 75
- 166

## Question 5. Session window - longest streak

Create another Flink job that uses a session window with a 5-minute gap on `PULocationID`, using `lpep_pickup_datetime` as the event time with a 5-second watermark tolerance.

A session window groups events that arrive within 5 minutes of each other. When there's a gap of more than 5 minutes, the window closes.

Write the results to a PostgreSQL table and find the `PULocationID` with the longest session (most trips in a single session).

How many trips were in the longest session?

- 12
- 31
- 51
- **81**

## Question 6. Tumbling window - largest tip

Create a Flink job that uses a 1-hour tumbling window to compute the total `tip_amount` per hour (across all locations).

Which hour had the highest total tip amount?

- 2025-10-01 18:00:00
- **2025-10-16 18:00:00**
- 2025-10-22 08:00:00
- 2025-10-30 16:00:00
