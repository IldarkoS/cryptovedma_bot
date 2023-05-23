from app.config import db, app

import app.models.NewQuizModel as NewQuizModel
import app.models.NewQuestModel as NewQuestModel
import app.models.QuestModel as QuestModel

class Quiz(db.Model):
    __tablename__ = 'quiz'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    quest_count = db.Column(db.Integer, default = 0)
    reward = db.Column(db.Boolean, default = False)
    reward_type = db.Column(db.String, default = 'identical')
    rewards = db.Column(db.PickleType, nullable=True)
    rewards_remain = db.Column(db.Integer, default=0)
    rewards_initial = db.Column(db.PickleType, nullable=True)

    def __repr__(self):
        return '<Quiz %r>' % self.name

    def __init__(self, name, quest_count, reward, reward_type, rewards, rewards_remain):
        with app.app_context():
            if Quiz.query.filter_by(name = name).first():
                print("false")
            else:
                 self.name = name
                 self.quest_count = quest_count
                 self.reward = reward
                 self.reward_type = reward_type
                 self.rewards = rewards
                 self.rewards_remain = rewards_remain
                 self.rewards_initial = rewards
                 db.session.add(self)
                 db.session.commit()


def getQuizList():
    with app.app_context():
        quizList = list(map(lambda x: x, Quiz.query.filter(Quiz.id is not None).all()))
        return quizList

def getLastId():
    with app.app_context():
        c = Quiz.query.filter(Quiz.id is not None).all()
        return c[-1].id

def getQuiz(id):
    with app.app_context():
        quiz = Quiz.query.filter_by(id=id).first()
        return quiz

def createQuiz(quiz: NewQuizModel.NewQuiz):
    with app.app_context():
        Quiz(name=quiz.name,
             quest_count=quiz.quest_count,
             reward=quiz.reward,
             reward_type=quiz.reward_type,
             rewards = quiz.rewards,
             rewards_remain = quiz.rewards_remain
             )
        quizId = getLastId()
        NewQuizModel.NewQuiz.query.filter_by(id=quiz.id).delete()
        quests = NewQuestModel.NewQuest.query.filter_by(quiz=quiz.id).all()

        for quest in quests:
            QuestModel.Quest(quiz=quizId,
                             text=quest.text,
                             answer_count=quest.answer_count,
                             correct_answer=0,
                             answers=quest.answers,
                             tip=quest.tip)
            NewQuestModel.NewQuest.query.filter_by(id=quest.id).delete()
        db.session.commit()

def deleteQuiz(quizId: int):
    with app.app_context():
        Quiz.query.filter_by(id=quizId).delete()
        quests = QuestModel.Quest.query.filter_by(quiz=quizId).all()
        for quest in quests:
            QuestModel.Quest.query.filter_by(id=quest.id).delete()
        db.session.commit()


def check_rewards(quiz_id):
    with app.app_context():
        quiz = Quiz.query.filter_by(id=quiz_id).first()
        return quiz.reward

def check_remainder(quiz_id):
    with app.app_context():
        quiz = Quiz.query.filter_by(id=quiz_id).first()
        if quiz.rewards_remain != 0:
            return True
        return False

def reward_take(quiz_id):
    with app.app_context():
        quiz = Quiz.query.filter_by(id=quiz_id).first()
        if quiz.rewards_remain != 0:
            if quiz.reward_type == "unique":
                return quiz.rewards[0]
            else:
                return quiz.rewards
        else:
            return "Error"
def reward_reduce(quiz_id):
    with app.app_context():
        quiz = Quiz.query.filter_by(id=quiz_id).first()
        if quiz.rewards_remain != 0:
            quiz.rewards_remain -= 1
            if quiz.reward_type == "unique":
                quiz.rewards = quiz.rewards[1:]
            db.session.commit()


# with app.app_context():
#     quiz = Quiz.query.filter_by(id=1).first()
#     quiz.quest_count = 3
#     db.session.commit()

# with app.app_context():
#     quiz = Quiz.query.filter_by(id=14).delete()
#     db.session.commit()

# with app.app_context():
#     quiz = Quiz(
#         name='Первая викторина',
#         quest_count = 2
#     )
#     quiz = Quiz(
#         name='Вторая викторина',
#         quest_count=2
#     )
#     quiz = Quiz(
#         name='Третья викторина',
#         quest_count=3
#     )
#     db.session.commit()

# print(getQuizList())
#

with app.app_context():
    quiz = Quiz.query.filter_by(id=14).first()
    print(quiz.rewards_initial)
