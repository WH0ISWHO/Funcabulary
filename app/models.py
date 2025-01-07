from . import db

# Days
class Day(db.Model):
    __tablename__ = 'days'
    id = db.Column(db.Integer, primary_key=True)
    # 관계 설정: 하나의 Day에는 여러 Word가 있을 수 있음
    words = db.relationship('Word', backref='day', lazy=True)

# words
class Word(db.Model):
    __tablename__ = 'words'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    day_id = db.Column(db.Integer, db.ForeignKey('days.id'), nullable=False)  # connect to Day
    word = db.Column(db.String(100), nullable=False)
    example = db.Column(db.Text, nullable=True)
    note = db.Column(db.Text, nullable=True)

    details = db.relationship('Detail', backref='word', lazy=True)
    derivatives = db.relationship('Derivative', backref='parent_word', lazy=True)

# part of speech
class POS(db.Model):
    __tablename__ = 'pos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pos = db.Column(db.String(10), unique=True, nullable=False)
    # 관계 설정: 하나의 POS는 여러 Detail과 Derivative에 사용될 수 있음
    details = db.relationship('Detail', backref='pos', lazy=True)
    derivatives = db.relationship('Derivative', backref='pos', lazy=True)

# details
class Detail(db.Model):
    __tablename__ = 'details'
    word_id = db.Column(db.Integer, db.ForeignKey('words.id'), primary_key=True)  # foreign key that connected with the word
    pos_id = db.Column(db.Integer, db.ForeignKey('pos.id'), nullable=False)
    synonyms = db.Column(db.String(100), primary_key=True, nullable=True)
    meaning = db.Column(db.String(100), nullable=False)
    # 복합 기본키 설정
    __table_args__ = (
        db.PrimaryKeyConstraint('word_id', 'synonyms'),
    )


# derivative
class Derivative(db.Model):
    __tablename__ = 'derivatives'
    word_id = db.Column(db.Integer, db.ForeignKey('words.id'), primary_key=True)  # foreign key that connected with the word
    pos_id = db.Column(db.Integer, db.ForeignKey('pos.id'), nullable=True)
    word = db.Column(db.String(50), primary_key=True, nullable=True)
    # 복합 기본키 설정
    __table_args__ = (
        db.PrimaryKeyConstraint('word_id', 'word'),
    )