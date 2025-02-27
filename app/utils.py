from .models import Day, Word, POS, Detail, Derivative
from . import db

def insert_data(days):
    pos_dict = ["n.", "v.", "adj.", "adv.", "pron.", "prep.", "conj.", "int.", "phr."]
    added_words = []

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
    for day_num, word_list in days.items():  # days.items() returns (key, value)
        day = Day.query.filter_by(id=int(day_num)).first()
        if not day:
            print(f"Error: Day{day_num} not found. Skipping...")
            continue

        for word_data in word_list:
            existing_word = Word.query.filter_by(day_id=day.id, word=word_data["word"]).first()
            if existing_word:
                continue

            word = Word(
                day_id=day.id,
                word=word_data["word"],
                note=word_data.get("note")
            )
            db.session.add(word)
            db.session.flush()  # flush for word id
            added_words.append(word_data["word"])

            # detail
            for detail_data in word_data.get("details", []):
                pos = POS.query.filter_by(pos=detail_data["pos"]).first()
                if not pos:
                    continue

                existing_detail = Detail.query.filter_by(
                    word_id=word.id, pos_id=pos.id, meaning=detail_data["meaning"]).first()
                if existing_detail:
                    continue

                detail = Detail(
                    word_id=word.id,
                    pos_id=pos.id,
                    synonyms=detail_data["synonyms"],
                    meaning=detail_data["meaning"],
                    example=detail_data.get("example")
                )
                db.session.add(detail)

            # derivative
            for derivative_data in word_data.get("derivatives", []):
                pos = POS.query.filter_by(pos=derivative_data["pos"]).first()
                if not pos:
                    continue

                existing_derivative = Derivative.query.filter_by(
                    word_id=word.id, pos_id=pos.id, word=derivative_data["word"]).first()
                if existing_derivative:
                    continue

                derivative = Derivative(
                    word_id=word.id,
                    pos_id=pos.id,
                    word=derivative_data["word"]
                )
                db.session.add(derivative)

        db.session.commit()  # ensure all data is committed at once

    print(f"\nData insertion complete!\nNewly added words ({len(added_words)}):")
    print(", ".join(added_words))



def delete_data_by_day(x):
    day = Day.query.filter_by(id=int(x)).first()
    if day:
        db.session.delete(day)
        db.session.commit()
        print("Deleted!")
    else:
        print("Data does not exist. Skipping deletion.")


from google import genai
from google.genai import types
import os
def ask(txt):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    prompt = f"{txt}\n\n(최대한 짧고 간결하게 한국어로 대답해 주세요.)"

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"{prompt}",
        config=types.GenerateContentConfig(
            max_output_tokens=100,
            temperature=0.1
        )

    )
    return response.text