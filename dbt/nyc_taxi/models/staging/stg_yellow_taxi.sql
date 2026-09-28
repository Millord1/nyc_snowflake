{{ config(
    tags=["staging"]
) }}

WITH source AS (

    SELECT *
    FROM NYC_TAXI.RAW.YELLOW_TAXI

),

typed AS (

    SELECT
        "VendorID" AS vendor_id,

        TO_TIMESTAMP_NTZ(
            "tpep_pickup_datetime" / 1000000
        ) AS pickup_datetime,

        TO_TIMESTAMP_NTZ(
            "tpep_dropoff_datetime" / 1000000
        ) AS dropoff_datetime,

        "passenger_count" AS passenger_count,

        CASE
            WHEN "trip_distance" > 1000 THEN NULL
            ELSE "trip_distance"
        END AS trip_distance,

        "RatecodeID" AS rate_code_id,
        "store_and_fwd_flag" AS store_and_fwd_flag,
        "PULocationID" AS pickup_location_id,
        "DOLocationID" AS dropoff_location_id,
        "payment_type" AS payment_type,
        "fare_amount" AS fare_amount,
        "extra" AS extra,
        "mta_tax" AS mta_tax,
        "tip_amount" AS tip_amount,
        "tolls_amount" AS tolls_amount,
        "improvement_surcharge" AS improvement_surcharge,
        "total_amount" AS total_amount,
        "congestion_surcharge" AS congestion_surcharge,
        "Airport_fee" AS airport_fee,
        "cbd_congestion_fee" AS cbd_congestion_fee

    FROM source

)

SELECT
    *,

    CASE
        WHEN pickup_datetime > dropoff_datetime THEN NULL

        WHEN DATEDIFF(
            'minute',
            pickup_datetime,
            dropoff_datetime
        ) > 180 THEN NULL

        ELSE DATEDIFF(
            'minute',
            pickup_datetime,
            dropoff_datetime
        )
    END AS trip_duration_minutes

FROM typed