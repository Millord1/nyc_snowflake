{{ config(
    tags=["staging", "test_staging"]
) }}


SELECT *
FROM {{ ref('stg_yellow_taxi') }}
WHERE trip_duration_minutes < 0
   OR trip_duration_minutes > 180