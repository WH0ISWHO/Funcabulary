from app import create_app, db
# from app.days import days
from app.models import Day
from app.utils import insert_data, delete_data_by_day
from flask_migrate import upgrade

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

if __name__ == '__main__':
    # with app.app_context():

    #     print("Running migrations...")
    #     upgrade()
    #     print("Migrations complete!")

    #     new_data = len(days)
    #     existing_data = Day.query.count()

    #     # execute only if Day's table is empty
    #     if existing_data != new_data:
    #         print("Inserting data...")
    #         insert_data(days)
    #         print("Setup complete!")
    #     else:
    #         print("Data already exists. Skipping insertion.")

    app.run(debug=True, port=3333)