{{ config(
    tags=["staging", "test_staging"]
) }}

SELECT *
FROM {{ ref('stg_yellow_taxi') }}
WHERE trip_distance < 0
   OR trip_distance > 1000