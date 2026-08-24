import pandas as pd
import random
from datetime import datetime, timedelta
import json


rows = []
base_time = datetime(2026, 8, 20, 9, 0, 0)

event_id = 1

products = [
    ("P100", "Laptop"),
    ("P200", "Phone"),
    ("P300", "Monitor"),
    ("P400", "Keyboard")
]

pages = [
    "home",
    "pricing",
    "products",
    "checkout",
    "about"
]

devices = [
    "mobile",
    "desktop",
    "tablet"
]


while len(rows) < 1200:

    user_num = random.randint(1, 250)

    anon_id = f"anon_{user_num:03d}"
    user_id = f"user_{user_num:03d}"

    current_time = base_time + timedelta(
        days=random.randint(0, 20),
        hours=random.randint(0, 12),
        minutes=random.randint(0, 59)
    )

    # Anonymous activity
    anonymous_events = random.randint(1, 5)

    for _ in range(anonymous_events):

        event_type = random.choice([
            "page_view",
            "product_viewed"
        ])

        if event_type == "page_view":

            properties = {
                "page": random.choice(pages),
                "device": random.choice(devices)
            }

        else:

            product_id, product_name = random.choice(products)

            properties = {
                "product_id": product_id,
                "product_name": product_name
            }

        rows.append([
            f"evt_{event_id:06d}",
            event_type,
            None,
            anon_id,
            current_time,
            current_time + timedelta(seconds=random.randint(1, 5)),
            json.dumps(properties)
        ])

        event_id += 1

        current_time += timedelta(
            minutes=random.randint(1, 60)
        )

    # Some users get identified, some don't
    if random.random() < 0.80:

        rows.append([
            f"evt_{event_id:06d}",
            "identify",
            user_id,
            anon_id,
            current_time,
            current_time + timedelta(seconds=random.randint(1, 5)),
            json.dumps({
                "email": f"user{user_num}@example.com",
                "name": f"User {user_num}"
            })
        ])

        event_id += 1

        current_time += timedelta(
            minutes=random.randint(1, 30)
        )

        # Post-identification activity
        identified_events = random.randint(1, 8)

        for _ in range(identified_events):

            event_type = random.choice([
                "page_view",
                "product_viewed",
                "add_to_cart",
                "purchase"
            ])

            if event_type == "page_view":

                properties = {
                    "page": random.choice(pages),
                    "device": random.choice(devices)
                }

            elif event_type == "product_viewed":

                product_id, product_name = random.choice(products)

                properties = {
                    "product_id": product_id,
                    "product_name": product_name
                }

            elif event_type == "add_to_cart":

                product_id, product_name = random.choice(products)

                properties = {
                    "product_id": product_id,
                    "quantity": random.randint(1, 4)
                }

            else:

                properties = {
                    "order_id": f"ORD{random.randint(10000, 99999)}",
                    "amount": round(random.uniform(50, 1500), 2)
                }

            rows.append([
                f"evt_{event_id:06d}",
                event_type,
                user_id,
                anon_id,
                current_time,
                current_time + timedelta(seconds=random.randint(1, 5)),
                json.dumps(properties)
            ])

            event_id += 1

            current_time += timedelta(
                minutes=random.randint(1, 180)
            )


# Keep exactly 1,000 rows
df = pd.DataFrame(
    rows[:1000],
    columns=[
        "event_id",
        "event_name",
        "user_id",
        "anonymous_id",
        "sent_at",
        "received_at",
        "properties"
    ]
)

df.to_csv(
    "segment_events_1000.csv",
    index=False
)

print(df.shape)

print("\nEvent distribution:")
print(df["event_name"].value_counts())

print("\nIdentified vs anonymous:")
print(df["user_id"].notna().value_counts())