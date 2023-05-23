from app.config import db, app


class Prize(db.Model):

    __tablename__ = 'prize'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, default=0)
    chat_id = db.Column(db.BigInteger, nullable=False)
    can_collect = db.Column(db.Boolean, default=True)
    code = db.Column(db.String, default = 'N/A')

    def __repr__(self):
        return '<Prize %r>' % self.name

    # def __init__(self, quiz_id, chat_id, can_collect):
    #     with app.app_context():
    #         self.quiz_id = quiz_id
    #         self.chat_id = chat_id
    #         self.can_collect = can_collect
    #         db.session.add(self)
    #         db.session.commit()
    def __init__(self, quiz_id, chat_id, can_collect, code):
        with app.app_context():
             self.chat_id=chat_id
             self.quiz_id=quiz_id
             self.can_collect=can_collect
             self.code=code
             db.session.add(self)
             db.session.commit()


def get_can_collect(quiz_id, chat_id):
    with app.app_context():
        prize = Prize.query.filter(Prize.quiz_id==quiz_id, Prize.chat_id==chat_id).first()
        if prize.can_collect:
            return True
        else:
            return False

def get_collected_code(quiz_id, chat_id):
    with app.app_context():
        prize = Prize.query.filter(Prize.quiz_id==quiz_id, Prize.chat_id==chat_id).first()
        return prize.code

def checkReward(quiz_id, chat_id):
    with app.app_context():
        if Prize.query.filter(Prize.quiz_id==quiz_id, Prize.chat_id==chat_id).first():
            return True
        return False
#
# if checkReward(63, 12):
#     print("True")
# else:
#     print("False")
