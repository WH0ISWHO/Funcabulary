from app import create_app, db
# from app.days import days
from app.models import Day
from app.utils import insert_data, delete_data_by_day

app = create_app()

# with app.app_context():
#     print("Creating tables...")
#     db.create_all()  # create a table of db
#     print("Tables created successfully!")

#     new_data = len(days)
#     existing_data = Day.query.count()

#     if existing_data != new_data:  # execute only if Day's table is empty
#         print("Inserting data...")
#         insert_data(days)
#         print("Setup complete!")
#     else:
#         print("Data already exists. Skipping insertion.")


import os
db_path = os.path.join("instance", "vocabulary.db")

if not os.path.exists(db_path):
    with open(db_path, "w") as f:
        pass

    # DB
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=3333)