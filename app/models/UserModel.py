import json

from app.config import db, app


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    chatId = db.Column(db.BigInteger, nullable=False)
    sub_status = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(64), default="N/A")
    quiz_current = db.Column(db.Integer, default=0)
    gpt_context = db.Column(db.JSON)

    def __repr__(self):
        return '<Account %r>' % self.chatId

    def __init__(self, chatId: int, username: str):
        with app.app_context():
            if User.query.filter_by(chatId = chatId).first():
                print("false")
            else:
                 self.chatId = chatId
                 self.username = username
                 db.session.add(self)
                 db.session.commit()

def theEconomistSub(chatId: int, key:int):
    with app.app_context():
        user = User.query.filter_by(chatId=chatId).first()
        if key == 1:
            user.sub_status = True
            db.session.commit()
        else:
            user.sub_status = False
            db.session.commit()


def quizCompleteCounter(chatId):
    with app.app_context():
        user = User.query.filter_by(chatId=chatId).first()
        user.quiz_current+=1
        db.session.commit()

def createUser(chatId, username):
    with app.app_context():
        if User.query.filter_by(chatId=chatId).first():
            pass
        else:
            User(chatId=chatId, username=username)

def getUsername(chatId: int):
    with app.app_context():
        user = User.query.filter_by(chatId=chatId).first()
    return user.username

def getUser(chatId: int):
    with app.app_context():
        user = User.query.filter_by(chatId=chatId).first()
    return user

def getSubStatus(chatId):
    with app.app_context():
        user = User.query.filter_by(chatId=chatId).first()
    return user.sub_status

def zeroingQuiz(chatId):
    with app.app_context():
        user = User.query.filter_by(chatId=chatId).first()
        user.quiz_current = 0
        db.session.commit()

def addContext(chatId, data):
    with app.app_context():
        user = User.query.filter_by(chatId=chatId).first()
        data = json.dumps(data)
        user.gpt_context = data
        db.session.commit()

def clearContext(chatId):
    with app.app_context():
        user = User.query.filter_by(chatId=chatId).first()
        user.gpt_context = None
        db.session.commit()

def getContext(chatId):
    with app.app_context():
        user = User.query.filter_by(chatId=chatId).first()
        if user.gpt_context != None:
            text = json.loads(user.gpt_context)
        else:
            text = []
        return text

# data = []
# data.append({"role": "user", "content": "{}".format("test")})
# data.append({"role": "assistant", "content": "{}".format("test")})
#
# # addContext(479516545, data)
#
# print(getContext(479516545))
# clearContext(479516545)
# with app.app_context():
#     user = User.query.filter_by(chatId=479516545).first()
#     user.economist_issue = '2023#12'
#     db.session.commit()

# def fetchAllUsers():
#     with app.app_context():
#         return User.query.filter(User.test == "asd").filter(User.chatId == 12).all()

#updateUser(chatId=10, test="asd")
# c = User(chatId=3, test="asd")
# with app.app_context():
#     db.session.commit()

# with app.app_context():
#     User.query.filter(User.chatId ==3).delete()
#     db.session.commit()

# with app.app_context():
# #     b = User.query.filter_by(chatId=13).first()
# #     b.updateUser(test="sad")
# #     db.session.commit()
#
# print(fetchAllUsers())