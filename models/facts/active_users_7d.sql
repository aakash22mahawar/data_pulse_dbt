{{
    config(
        materialized = 'view'
    )
}}

SELECT
    COUNT(DISTINCT user_id) AS active_users_last_7_days
FROM {{ ref('events_src') }}
WHERE user_id IS NOT NULL
  AND event_timestamp >= DATEADD(day, -7, CURRENT_TIMESTAMP())