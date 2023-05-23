from app.config import db, app


class NewQuest(db.Model):

    __tablename__ = 'newquest'

    id = db.Column(db.Integer, primary_key=True)
    quiz = db.Column(db.Integer, default = 1)
    text = db.Column(db.String, default = 'N/A')
    answer_count = db.Column(db.Integer, default = 1)
    correct_answer = db.Column(db.Integer)
    answers = db.Column(db.PickleType, nullable=True)
    tip = db.Column(db.String, nullable=True)

    def __repr__(self):
        return '<Quest %r>' % self.text

    def __init__(self, quiz, text):
        with app.app_context():
            # if NewQuest.query.filter_by(text=text).first():
            #     pass
            # else:
             self.quiz = quiz
             self.text = text
             self.answers = []
             db.session.add(self)
             db.session.commit()

def getLastId():
    with app.app_context():
        c = NewQuest.query.filter(NewQuest.id is not None).all()
        return c[-1].id

def getQuestList(quizId):
    with app.app_context():
        questList = list(map(lambda x: x, NewQuest.query.filter_by(quiz=str(quizId)).all()))
        return questList

def set_tip(questId, tip):
    with app.app_context():
        quest = NewQuest.query.filter_by(id=questId).first()
        quest.tip = tip
        db.session.commit()

def setAnswerCount(questId, answer_count):
    with app.app_context():
        quest = NewQuest.query.filter_by(id=questId).first()
        quest.answer_count = answer_count
        db.session.commit()

def appendAnswer(questId, answer):
    with app.app_context():
        quest = NewQuest.query.filter_by(id=questId).first()
        answers_current = quest.answers[:]
        answers_current.append(answer)
        quest.answers = answers_current
        print(quest.answers)
        db.session.commit()

def filledAnswers(questId):
    with app.app_context():
        quest = NewQuest.query.filter_by(id=questId).first()
        return len(quest.answers)

def getQuest(questId):
    with app.app_context():
        return NewQuest.query.filter_by(id=questId).first()
