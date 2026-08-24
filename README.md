# Segment CDP Warehouse Validation

## Overview

This project demonstrates a lightweight v0 warehouse implementation for validating Segment CDP event data.

The objective is to show that raw Segment-style events are:

* Arriving in the Snowflake warehouse
* Correctly associated between `anonymous_id` and `user_id`
* Consistent in event and property structure
* Usable for downstream analytics and dashboarding

The implementation uses:

**Python → CSV → Snowflake → dbt → Tableau**

---

## Technology Stack

* **Snowflake** — data warehouse
* **Python / Pandas** — mock Segment event generation
* **dbt** — data transformation and modeling
* **Tableau** — lightweight analytics dashboard

---

## Snowflake Environment

The assessment uses the provided Snowflake environment:

* Database: `SNOWFLAKE_LEARNING_DB`
* Schema: `AAKASH_DATA_ENGG`
* Warehouse: `SNOWFLAKE_LEARNING_WH`
* Role: `SNOWFLAKE_LEARNING_ROLE`

---

## Dataset

A synthetic Segment-style event dataset is generated using Python.

The dataset contains:

* `event_id`
* `event_name`
* `user_id`
* `anonymous_id`
* `sent_at`
* `received_at`
* `properties`

The `properties` column contains JSON-formatted event properties.

The dataset intentionally represents realistic variation in user behavior rather than forcing every user through an identical event sequence.

Examples of supported event types:

* `page_view`
* `product_viewed`
* `identify`
* `add_to_cart`
* `purchase`

---

## Warehouse Validation

The raw events are validated in Snowflake for three key requirements.

### 1. Event arrival

Event volumes are checked by event type:

```sql
SELECT
    event_name,
    COUNT(*) AS event_count
FROM segment_events_raw
GROUP BY 1
ORDER BY 1 DESC;
```

### 2. Identity stitching

Anonymous and identified activity is compared using:

```sql
SELECT
    anonymous_id,
    user_id,
    COUNT(*) AS event_count
FROM segment_events_raw
GROUP BY 1, 2
ORDER BY 1, 2;
```

This demonstrates the transition from anonymous activity to identified user activity.

### 3. Property consistency

Event property names are inspected by event type to identify inconsistent schemas or property naming.

```sql
SELECT
    event_name,
    ARRAY_AGG(
        DISTINCT property_name
    ) AS property_names
FROM segment_events_raw,
     LATERAL FLATTEN(INPUT => OBJECT_KEYS(PARSE_JSON(properties))) f,
     LATERAL (
         SELECT f.VALUE::VARCHAR AS property_name
     )
GROUP BY 1
ORDER BY 1 asc;
```

## dbt Models

### `events_src`

Standardizes the raw event data.

Key fields:

* `event_id`
* `event_type`
* `event_timestamp`
* `user_id`
* `anonymous_id`
* `properties`

Duplicate event IDs are deduplicated using `ROW_NUMBER()`.

### `users_dims`

Creates a unified user-level view containing:

* `user_id`
* `email`
* `name`
* `first_seen`
* `last_seen`

### `active_users_7d`

Provides a derived metric showing the number of identified users active during the previous seven days.

---

## dbt Project Structure

```text
data_pulse/
│
├── models/
│   ├── src_staging/
│   │   └── events_src.sql
│   │
│   ├── dims/
│   │   └── users_dims.sql
│   │
│   └── facts/
│       └── active_users_7d.sql
│
├── seeds/
│   └── segment_events_raw.csv
│
├── dbt_project.yml
├── README.md
└── requirements.txt
```

## Running the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Validate the dbt configuration:

```bash
dbt debug
```

Load the seed data:

```bash
dbt seed --select segment_events_raw --target sand
```

Build the models:

```bash
dbt run --target sand
```

Run a specific model:

```bash
dbt run --select events_src --target sand
```

---

## Tableau Dashboard

The final dashboard is designed as an MVP with two primary analytical views:

1. **Event volume over time**
2. **Purchase activity / purchase volume**

The dashboard demonstrates that the warehouse data is available, structured, and usable for business-facing analytics.

---

## Outcome

This implementation provides a demo-grade v0 data foundation that validates the Segment implementation from raw event ingestion through warehouse modeling and BI consumption.

The architecture is intentionally lightweight and focuses on proving:

**Data arrives → identities can be associated → events are modeled → business metrics can be visualized.**

## Warehouse Runbook

### Daily
- Check event volumes by type.
- Check identity stitching (`anonymous_id` → `user_id`).
- Confirm dbt models run successfully.

### Weekly
- Review event/property consistency.
- Check for unexpected schema or event changes.
- Review key metrics such as purchases and active users.
