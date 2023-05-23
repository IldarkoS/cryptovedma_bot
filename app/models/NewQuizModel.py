from app.config import db, app
import app.models.QuizModel as QuizModel
import app.models.NewQuestModel as NewQuestModel

class NewQuiz(db.Model):
    __tablename__ = 'newquiz'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    quest_count = db.Column(db.Integer, default=0)
    filled_quest = db.Column(db.Integer, default=0)
    reward = db.Column(db.Boolean, default=False)
    reward_type = db.Column(db.String, default='identical')
    rewards = db.Column(db.PickleType, nullable=True)
    rewards_remain = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Quiz %r>' % self.name

    def __init__(self, name):
        with app.app_context():
            if NewQuiz.query.filter_by(name = name).first():
                print("false")
            else:
                 self.name = name
                 db.session.add(self)
                 db.session.commit()

def getNewQuiz(quizId):
    with app.app_context():
        return NewQuiz.query.filter_by(id=quizId).first()

def setQuestCount(quizId, quest_count):
    with app.app_context():
        quiz = NewQuiz.query.filter_by(id=quizId).first()
        quiz.quest_count = quest_count
        db.session.commit()

def setReward(quiz_id, key: bool):
    with app.app_context():
        quiz = NewQuiz.query.filter_by(id=quiz_id).first()
        quiz.reward = key
        db.session.commit()

def setRewardType(quiz_id, key: str):
    with app.app_context():
        quiz = NewQuiz.query.filter_by(id=quiz_id).first()
        quiz.reward_type = key
        db.session.commit()


def setRewardsCount(quiz_id, count:int):
    with app.app_context():
        quiz = NewQuiz.query.filter_by(id=quiz_id).first()
        quiz.rewards_remain = count
        db.session.commit()

def setRewards(quiz_id, rewards):
    with app.app_context():
        quiz = NewQuiz.query.filter_by(id=quiz_id).first()
        quiz.rewards = rewards
        db.session.commit()

def getLastId():
    with app.app_context():
        c = NewQuiz.query.filter(NewQuiz.id is not None).all()
        return c[-1].id

def checkDublicate(name:str):
    with app.app_context():
        if QuizModel.Quiz.query.filter_by(name=name).first():
            return False
        else:
            return True

def getQuizList():
    with app.app_context():
        quizList = list(map(lambda x: x, NewQuiz.query.filter(NewQuiz.id is not None).all()))
        return quizList

def incrementFilledQuest(quizId):
    with app.app_context():
        quiz = NewQuiz.query.filter_by(id=quizId).first()
        quiz.filled_quest += 1
        db.session.commit()

def resetQuiz():
    with app.app_context():
        quizList = list(map(lambda x: x, NewQuiz.query.filter(NewQuiz.id is not None).all()))
        for quiz in quizList:
            NewQuiz.query.filter_by(id=quiz.id).delete()
            quests = NewQuestModel.NewQuest.query.filter_by(quiz=quiz.id).all()
            for quest in quests:
                NewQuestModel.NewQuest.query.filter_by(id=quest.id).delete()
        db.session.commit()