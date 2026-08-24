{{ 
  config(
    materialized = 'view'
  ) 
}}


WITH raw AS (
    SELECT 

    event_id,
    event_name AS event_type,
    sent_at AS event_timestamp,
    user_id,
    anonymous_id,
    properties

    FROM {{ source('segment', 'events_raw') }}
),



dedupe as (
    select *,
           row_number() over (
              partition by event_id
              order by event_timestamp desc
           ) as row_
    from raw QUALIFY row_ = 1
)


select * EXCLUDE(row_) from dedupe