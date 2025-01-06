# import sqlite3
# import os

# db_path = "/Volumes/Jayden's Hard/MacBook/Work/Coding/Visual Studio/HTML/05.Vocabulary/db/vocabulary.db"

# # 디렉토리가 존재하지 않으면 생성
# os.makedirs(os.path.dirname(db_path), exist_ok=True)

# # DB 연결
# conn = sqlite3.connect(db_path)
# cursor = conn.cursor()

# # 테이블 확인
# # cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='words';")
# # result = cursor.fetchone()

# # if result:
# #     print("테이블이 존재합니다.")
# # else:
# #     print("테이블이 없습니다.")


# # day 테이블 생성
# def create_day_table():
#     try:
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS words (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 day_id INTEGER NOT NULL,
#                 pos_id INTEGER NOT NULL,
#                 word TEXT NOT NULL,
#                 meaning TEXT NOT NULL,
#                 example TEXT NOT NULL,
#                 note TEXT DEFAULT NULL,
#                 FOREIGN KEY (day_id) REFERENCES days(id),
#                 FOREIGN KEY (pos_id) REFERENCES pos(id)
#             )
#         """)

#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS derived(
#                 word_id INTEGER NOT NULL,
#                 pos_id INTEGER NOT NULL,
#                 derived_word TEXT NOT NULL,
#                 meaning TEXT NOT NULL,
#                 FOREIGN KEY (word_id) REFERENCES words(id) ON DELETE CASCADE,
#                 FOREIGN KEY (pos_id) REFERENCES pos(id)
#             )
#         """)

#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS synonyms(
#                 word_id INTEGER NOT NULL,
#                 synonym TEXT NOT NULL,
#                 meaning TEXT NOT NULL,
#                 FOREIGN KEY (word_id) REFERENCES words(id)
#             )
#         """)
#         '''
#             CREATE TABLE days (id INTEGER PRIMARY KEY)

#             CREATE TABLE pos (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 name TEXT NOT NULL UNIQUE
#             )

#             CREATE TABLE IF NOT EXISTS words (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 day_id INTEGER NOT NULL,
#                 pos_id INTEGER NOT NULL,
#                 word TEXT NOT NULL,
#                 meaning TEXT NOT NULL,
#                 example TEXT NOT NULL,
#                 note TEXT DEFAULT NULL,
#                 FOREIGN KEY (day_id) REFERENCES days(id),
#                 FOREIGN KEY (pos_id) REFERENCES pos(id)
#             )

#             CREATE TABLE IF NOT EXISTS derived(
#                 word_id INTEGER NOT NULL,
#                 pos_id INTEGER NOT NULL,
#                 derived_word TEXT NOT NULL,
#                 meaning TEXT NOT NULL,
#                 FOREIGN KEY (word_id) REFERENCES words(id) ON DELETE CASCADE,
#                 FOREIGN KEY (pos_id) REFERENCES pos(id)
#             )

#             CREATE TABLE IF NOT EXISTS synonyms(
#                 word_id INTEGER NOT NULL,
#                 synonym TEXT NOT NULL,
#                 meaning TEXT NOT NULL,
#                 FOREIGN KEY (word_id) REFERENCES words(id)
#             )

#         테이블 days 에는 1 ~ 30 까지 데이터가 있고, 테이블 pos에는 8품사 + phr.도 이미 들어있어. 나머지 애들도 내가 만든 테이블들에 맞춰서 데이터를 삽입하고 싶은데 예를 들어서
#         1일차 particular 라는 단어를 넣고 싶어 품사는 adj.이고 동의어는 specific; special이 있어. 뜻은 특정한; 특별한이고 example은 "Galieo tried to disprove one particular statement of Aristotle's"를 넣고 싶어. 중요한 파생어는 값이 있을수도 있고 없을 수도 있어. 그럼 코드를 어떻게 짜야될까? 그리고 이런게 여러개가 있으면 어떻게 코드를 짜야 효율적이게 할 수 있을까?
#         '''
#         conn.commit()
#         print("테이블이 성공적으로 생성되었습니다.")
#     except sqlite3.Error as e:
#         print(f"테이블 생성 중 오류 발생: {e}")

# def drop_table():
#     try:
#         # 테이블 삭제
#         cursor.execute("DROP TABLE IF EXISTS words")
#         # cursor.execute("DROP TABLE IF EXISTS derived")
#         # cursor.execute("DROP TABLE IF EXISTS synonyms")
        
#         # 변경 사항 저장
#         conn.commit()
#         print("테이블이 성공적으로 삭제되었습니다.")
#     except sqlite3.Error as e:
#         print(f"테이블 삭제 중 오류 발생: {e}")


# def insert():
#     today = 1
#     pos_dict = {
#         "n": 1,
#         "v": 2,
#         "adj": 3,
#         "adv": 4,
#         "pron": 5,
#         "prep": 6,
#         "conj": 7,
#         "int": 8,
#         "phr": 9
#     }

#     X = [
#         {
#             'day_id': today,
#             'pos_id': 'v',
#             'word': 'exploit',
#             'synonyms': ['utilize', 'use', 'make use of', 'take advantage of'],
#             'derived': ['exploitation'],
#             'derived_pos': 'n',
#             'meaning': ['(부당하게) 이용하다'],
#             'derived_meaning': ['착취', '이용', '개발'],
#             'example': 'Human rights activists have led protests against companies that exploit child labor.',
#             'note': '명사로도 많이 쓰인다. "the exploits of brave knights(용감한 기사들의 위업)에서처럼 "위업","공적"이라는 뜻으로 주로 쓰이며, 동의어로는 accomplishment, feat가 있다."',
#         },
#         {
#             'day_id': today,
#             'pos_id': 'phr',
#             'word': 'account for',
#             'synonyms': [['explain', 'justify', 'give a reason for'], ['make up', 'comprise', 'constitute'], ['cause']],
#             'meaning': [['(이유 등을)설명하다'], ['(부분, 비율) 차지하다'], ['원인이 되다']],
#             'derived': [],
#             'derived_pos': None,
#             'derived_meaning': [],
#             'example': "The suspect couldn't account for his whereabouts last night",
#             'note': None,
#         },
#         {
#             'day_id': today,
#             'pos_id': 'adj',
#             'word': 'particular',
#             'synonyms': ["specific;", "special"],
#             'meaning': ["특정한;", "특별한"],
#             'derived': [],
#             'derived_pos': None,
#             'derived_meaning': [],
#             'example': "Galileo tried to disprove one particular statement of Aristotle's.",
#             'note': None,
#         },
#     ]

#     for x in X:
#         word = x["word"]
#         pos_id = pos_dict[x["pos_id"]]
#         derived_pos = pos_dict.get(x["derived_pos"]) if x["derived_pos"] else None  # derived_pos가 None일 때 처리
#         meaning = x["meaning"]
#         derived_meaning = x["derived_meaning"]
#         example = x["example"]
#         synonyms = x["synonyms"]
#         derived_words = x["derived"]
#         note = x["note"]
#         day_id = x["day_id"]
        
#         # 1. 단어 삽입 (words 테이블)
#         if note is None:
#             cursor.execute("""
#                 INSERT INTO words (day_id, pos_id, word, meaning, example)
#                 VALUES (?, ?, ?, ?, ?)
#             """, (day_id, pos_id, word, ', '.join(meaning), example))  # 의미는 ','로 구분하여 저장
#         else:
#             cursor.execute("""
#                 INSERT INTO words (day_id, pos_id, word, meaning, example, note)
#                 VALUES (?, ?, ?, ?, ?, ?)
#             """, (day_id, pos_id, word, ', '.join(meaning), example, note))  # 의미는 ','로 구분하여 저장

#         # 방금 삽입한 word의 id 가져오기
#         cursor.execute("SELECT last_insert_rowid()")
#         word_id = cursor.fetchone()[0]

#         # 2. 동의어 삽입 (synonyms 테이블)
#         for synonym in synonyms:
#             cursor.execute("""
#                 INSERT INTO synonyms (word_id, synonym, meaning)
#                 VALUES (?, ?, ?)
#             """, (word_id, synonym, ', '.join(meaning)))  # 의미는 ','로 구분하여 저장

#         # 3. 파생어 삽입 (derived 테이블)
#         for i, derived_word in enumerate(derived_words):
#             # 파생어의 의미를 가져오고, 여러 개일 경우 첫 번째 의미를 사용
#             derived_word_meaning = derived_meaning[i] if i < len(derived_meaning) else None
#             cursor.execute("""
#                 INSERT INTO derived (word_id, pos_id, derived_word, meaning)
#                 VALUES (?, ?, ?, ?)
#             """, (word_id, derived_pos, derived_word, derived_word_meaning))

#     # 변경사항 커밋
#     conn.commit()


# # create_day_table()
# # drop_table()

# # 연결 종료
# conn.close()