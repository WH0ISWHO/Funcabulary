from .models import Day, Word, POS, Detail, Derivative
from . import db

def insert_data(days):
    pos_dict = ["n.", "v.", "adj.", "adv.", "pron.", "prep.", "conj.", "int.", "phr."]

    # insert POS data
    existing_pos = {pos.pos for pos in POS.query.all()}
    new_pos = [POS(pos=pos_value) for pos_value in pos_dict if pos_value not in existing_pos]
    db.session.add_all(new_pos)
    db.session.commit()

    # insert day id
    existing_days = {day.id for day in Day.query.all()}
    new_days = [Day(id=i) for i in range(1, len(days) + 1) if i not in existing_days]
    db.session.add_all(new_days)
    db.session.commit()

    # insert word, detail, derivative
    for day_name, word_list in days.items():  # days.items() returns (key, value)
        day = Day.query.filter_by(id=int(day_name)).first()
        if not day:
            print(f"Error: Day{day_name} not found. Skipping...")
            continue

        for word_data in word_list:
            word = Word(
                day_id=day.id,
                word=word_data["word"],
                example=word_data.get("example"),
                note=word_data.get("note")
            )
            db.session.add(word)
            db.session.flush()  # flush for word id

            # detail
            for detail_data in word_data.get("details", []):
                pos = POS.query.filter_by(pos=detail_data["pos"]).first()
                if not pos:
                    print(f"Error: POS {detail_data['pos']} not found. Skipping detail...")
                    continue

                detail = Detail(
                    word_id=word.id,
                    pos_id=pos.id,
                    synonyms=detail_data.get("synonyms"),
                    meaning=detail_data["meaning"]
                )
                db.session.add(detail)

            # derivative
            for derivative_data in word_data.get("derivatives", []):
                pos = POS.query.filter_by(pos=derivative_data["pos"]).first()
                if not pos:
                    print(f"Error: POS {derivative_data['pos']} not found. Skipping derivative...")
                    continue

                derivative = Derivative(
                    word_id=word.id,
                    pos_id=pos.id,
                    word=derivative_data["word"]
                )
                db.session.add(derivative)

        db.session.commit()  # commit word, detail, derivative data to db