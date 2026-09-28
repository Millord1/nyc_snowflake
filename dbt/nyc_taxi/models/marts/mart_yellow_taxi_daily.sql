{{ config(
    tags=["marts"]
) }}

SELECT
    DATE(pickup_datetime) AS trip_date,
    COUNT(*) AS trip_count,
    SUM(total_amount) AS total_revenue,
    AVG(fare_amount) AS avg_fare_amount,
    AVG(trip_distance) AS avg_trip_distance,
    AVG(trip_duration_minutes) AS avg_trip_duration_minutes,
    SUM(tip_amount) AS total_tip_amount,
    SUM(tolls_amount) AS total_tolls_amount
FROM {{ ref('stg_yellow_taxi') }}
GROUP BY 1