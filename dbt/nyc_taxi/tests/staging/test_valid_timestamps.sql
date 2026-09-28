{{ config(
    tags=["staging", "test_staging"],
    severity="warn"
) }}

SELECT *
FROM {{ ref('stg_yellow_taxi') }}
WHERE pickup_datetime > dropoff_datetime