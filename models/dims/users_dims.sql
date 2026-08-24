{{
    config(
        materialized = 'view'
    )
}}

SELECT
    user_id,
    MAX(PARSE_JSON(properties):email::VARCHAR) AS email,
    MAX(PARSE_JSON(properties):name::VARCHAR) AS name,
    MIN(event_timestamp) AS first_seen,
    MAX(event_timestamp) AS last_seen

FROM {{ ref('events_src') }}

WHERE user_id IS NOT NULL

GROUP BY user_id