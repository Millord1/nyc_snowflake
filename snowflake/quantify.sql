USE DATABASE NYC_TAXI;
USE SCHEMA RAW;
USE WAREHOUSE NYC_TAXI_WH;

SELECT
    COUNT(*) AS total,
    COUNT_IF("trip_distance" = 0) AS zero_distance,
    COUNT_IF("trip_distance" < 0) AS negative_distance,
    COUNT_IF("trip_distance" > 1000) AS extreme_distance,
    MIN("trip_distance") AS min_distance,
    MAX("trip_distance") AS max_distance
FROM NYC_TAXI.RAW.YELLOW_TAXI;

SELECT
    COUNT(*) AS total,
    COUNT_IF("total_amount" < 0) AS negative_amount,
    MIN("total_amount") AS min_amount,
    MAX("total_amount") AS max_amount
FROM NYC_TAXI.RAW.YELLOW_TAXI;


SELECT
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "trip_distance",
    "fare_amount",
    "total_amount",
    "PULocationID",
    "DOLocationID"
FROM NYC_TAXI.RAW.YELLOW_TAXI
WHERE "trip_distance" > 1000
ORDER BY "trip_distance" DESC
LIMIT 20;

DESC TABLE NYC_TAXI.RAW.YELLOW_TAXI;

SELECT
    "tpep_pickup_datetime",
    TO_TIMESTAMP_NTZ(
        "tpep_pickup_datetime" / 1000000
    ) AS pickup_datetime,
    TO_TIMESTAMP_NTZ(
        "tpep_dropoff_datetime" / 1000000
    ) AS dropoff_datetime
FROM NYC_TAXI.RAW.YELLOW_TAXI
LIMIT 10;


SELECT
    COUNT(*) AS total_rows,

    COUNT_IF("VendorID" IS NULL) AS vendor_id_nulls,
    COUNT_IF("tpep_pickup_datetime" IS NULL) AS pickup_datetime_nulls,
    COUNT_IF("tpep_dropoff_datetime" IS NULL) AS dropoff_datetime_nulls,
    COUNT_IF("passenger_count" IS NULL) AS passenger_count_nulls,
    COUNT_IF("trip_distance" IS NULL) AS trip_distance_nulls,
    COUNT_IF("RatecodeID" IS NULL) AS ratecode_id_nulls,
    COUNT_IF("store_and_fwd_flag" IS NULL) AS store_and_fwd_flag_nulls,
    COUNT_IF("PULocationID" IS NULL) AS pickup_location_nulls,
    COUNT_IF("DOLocationID" IS NULL) AS dropoff_location_nulls,
    COUNT_IF("payment_type" IS NULL) AS payment_type_nulls,
    COUNT_IF("fare_amount" IS NULL) AS fare_amount_nulls,
    COUNT_IF("total_amount" IS NULL) AS total_amount_nulls
FROM NYC_TAXI.RAW.YELLOW_TAXI;

SELECT
    COUNT(*) AS rows_with_both_null
FROM NYC_TAXI.RAW.YELLOW_TAXI
WHERE "passenger_count" IS NULL
  AND "RatecodeID" IS NULL;

  SELECT
    "VendorID",
    "payment_type",
    "PULocationID",
    "DOLocationID",
    "trip_distance",
    "fare_amount",
    "total_amount"
FROM NYC_TAXI.RAW.YELLOW_TAXI
WHERE "passenger_count" IS NULL
  AND "RatecodeID" IS NULL
LIMIT 20;

SELECT
    "payment_type",
    COUNT(*) AS row_count,
    COUNT_IF("passenger_count" IS NULL) AS passenger_count_nulls,
    COUNT_IF("RatecodeID" IS NULL) AS ratecode_id_nulls
FROM NYC_TAXI.RAW.YELLOW_TAXI
GROUP BY "payment_type"
ORDER BY "payment_type";

SELECT
    COUNT(*) AS total_negative,
    COUNT_IF("fare_amount" < 0) AS negative_fare,
    COUNT_IF("extra" < 0) AS negative_extra,
    COUNT_IF("mta_tax" < 0) AS negative_mta_tax,
    COUNT_IF("tip_amount" < 0) AS negative_tip,
    COUNT_IF("tolls_amount" < 0) AS negative_tolls,
    COUNT_IF("improvement_surcharge" < 0) AS negative_improvement,
    COUNT_IF("total_amount" < 0) AS negative_total
FROM NYC_TAXI.RAW.YELLOW_TAXI;

SELECT
    "payment_type",
    COUNT(*) AS row_count,
    COUNT_IF("total_amount" < 0) AS negative_total,
    MIN("total_amount") AS min_total,
    MAX("total_amount") AS max_total
FROM NYC_TAXI.RAW.YELLOW_TAXI
GROUP BY "payment_type"
ORDER BY "payment_type";

SELECT
    "payment_type",
    "fare_amount",
    "extra",
    "mta_tax",
    "tip_amount",
    "tolls_amount",
    "improvement_surcharge",
    "total_amount",
    "trip_distance"
FROM NYC_TAXI.RAW.YELLOW_TAXI
WHERE "total_amount" < 0
ORDER BY "payment_type", "total_amount"
LIMIT 50;

SELECT
    COUNT(*) AS total,
    COUNT_IF("fare_amount" < 0) AS negative_fare,
    COUNT_IF("total_amount" < 0) AS negative_total,
    COUNT_IF(
        "fare_amount" < 0
        AND "total_amount" < 0
    ) AS both_negative
FROM NYC_TAXI.RAW.YELLOW_TAXI;

SELECT
    COUNT(*) AS total_rows,
    COUNT_IF(trip_duration_minutes < 0) AS negative_duration,
    COUNT_IF(trip_duration_minutes = 0) AS zero_duration,
    MIN(trip_duration_minutes) AS min_duration,
    MAX(trip_duration_minutes) AS max_duration
FROM NYC_TAXI.STAGING.STG_YELLOW_TAXI;

SELECT
    COUNT(*) AS zero_duration_rows,
    COUNT_IF(trip_distance = 0) AS zero_duration_zero_distance,
    COUNT_IF(trip_distance > 0) AS zero_duration_with_distance,
    AVG(trip_distance) AS avg_distance,
    AVG(total_amount) AS avg_total_amount
FROM NYC_TAXI.STAGING.STG_YELLOW_TAXI
WHERE trip_duration_minutes = 0;

SELECT
    pickup_datetime,
    dropoff_datetime,
    trip_duration_minutes,
    trip_distance,
    fare_amount,
    total_amount,
    pickup_location_id,
    dropoff_location_id
FROM NYC_TAXI.STAGING.STG_YELLOW_TAXI
WHERE pickup_datetime > dropoff_datetime;

DROP SCHEMA IF EXISTS NYC_TAXI.STAGING_FINAL;