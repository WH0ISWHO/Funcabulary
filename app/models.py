# from . import db




# class Day(db.Model):
#     __tablename__ = 'days'
#     id = db.Column(db.Integer, primary_key=True)

#     words = db.relationship('Word', backref='day_record', lazy=True)



# class Word(db.Model):
#     __tablename__ = 'words'
#     id = db.Column(db.Integer, primary_key=True)
#     day = db.Column(db.Integer, db.ForeignKey('days.id'), nullable=False)
#     word = db.Column(db.String(100), nullable=False)
#     meaning = db.Column(db.String(255), nullable=False)
#     derivatives = db.Column(db.JSON, nullable=True)
#     synonyms = db.Column(db.JSON, nullable=True)
#     example = db.Column(db.Text, nullable=True)

#     def __repr__(self):
#         return f"<Day {self.day}: {self.word}>"
