from app.config import db, app


class Quest(db.Model):

    __tablename__ = 'quest'

    id = db.Column(db.Integer, primary_key=True)
    quiz = db.Column(db.Integer, default = 1)
    text = db.Column(db.String, default = 'N/A')
    answer_count = db.Column(db.Integer, default = 1)
    correct_answer = db.Column(db.Integer)
    answers = db.Column(db.PickleType, nullable=True)
    tip = db.Column(db.String, nullable=True)

    def __repr__(self):
        return '<Quest %r>' % self.text

    def __init__(self, quiz, text, answer_count, correct_answer, answers, tip):
        with app.app_context():
            # if Quest.query.filter_by(text = text).first():
            #     print("false")
            # else:
             self.quiz = quiz
             self.text = text
             self.answer_count = answer_count
             self.correct_answer = correct_answer
             self.answers = answers
             self.tip = tip
             db.session.add(self)
             db.session.commit()

def getQuestList(quizId):
    with app.app_context():
        questList = list(map(lambda x: x, Quest.query.filter_by(quiz=str(quizId)).all()))
        return questList



# with app.app_context():
#     quest = Quest(
#         quiz = 1,
#         text="0+0=?",
#         answer_count=2,
#         answers=['1','0'],
#         correct_answer=1
#     )
#     quest = Quest(
#         quiz=1,
#         text="1+1=?",
#         answer_count=2,
#         answers=['2', '10'],
#         correct_answer=0
#     )
#     db.session.commit()
#     quest = Quest.query.filter_by(id=6).first()
#     quest.quiz=6
#     db.session.commit()

# with app.app_context():
#     quiz = 1
#     quest = Quest.query.filter(Quest.quiz==quiz).all()
#     for i in range(len(quest)):
#         Quest.query.filter_by(quiz=quiz).delete()
#     db.session.commit()


# print(getQuestList(1))