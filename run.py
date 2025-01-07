from app import create_app, db
from app.days import days
from app.models import Day
from app.utils import insert_data

app = create_app()

with app.app_context():
    print("Creating tables...")
    db.create_all()  # create a table of db
    print("Tables created successfully!")

    if not Day.query.first():  # execute only if Day's table is empty
        print("Inserting data...")
        insert_data(days)
        print("Setup complete!")
    else:
        print("Data already exists. Skipping insertion.")

if __name__ == '__main__':
    app.run(debug=True, port=3333)