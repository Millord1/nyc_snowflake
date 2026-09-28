{{ config(
    tags=["marts"]
) }}

SELECT *
FROM {{ ref('mart_yellow_taxi_daily') }}
WHERE trip_count <= 0