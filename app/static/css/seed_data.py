from app import create_app, db
from app.models import TrashBin
from random import randint, uniform
from datetime import datetime, timedelta

app = create_app()

def seed_trash_bins():
    with app.app_context():
        # Clear existing data
        TrashBin.query.delete()

        # Add sample trash bins
        locations = [
            "Main St & 1st Ave", "Oak Rd & Elm St", "Park Ave & 5th St",
            "River Rd & Bridge Ln", "Market Square", "Central Park",
            "School Zone", "Industrial Park", "Shopping Center", "Residential Area"
        ]

        for i, location in enumerate(locations, 1):
            bin = TrashBin(
                location=location,
                fill_level=randint(1, 5),
                last_pickup=datetime.utcnow() - timedelta(days=randint(0, 7)),
                latitude=uniform(40.7, 40.8),
                longitude=uniform(-74.0, -73.9)
            )
            db.session.add(bin)

        db.session.commit()
        print("Sample trash bins added to the database.")

if __name__ == "__main__":
    seed_trash_bins()