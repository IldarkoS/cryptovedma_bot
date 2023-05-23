from app.config import db, app

class Admin(db.Model):

    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    chatId = db.Column(db.BigInteger, nullable = False)

    def __repr__(self):
        return '<Quest %r>' % self.text

    def __init__(self, chatId):
        with app.app_context():
            if Admin.query.filter_by(chatId = chatId).first():
                print("false")
            else:
                 self.chatId = chatId
                 db.session.add(self)
                 db.session.commit()

def checkAdmin(chatId):
    with app.app_context():
        if Admin.query.filter_by(chatId=chatId).first():
            return True
        else:
            return False

def deleteAdmin(chatId):
    with app.app_context():
        Admin.query.filter_by(chatId=chatId).delete()
        db.session.commit()

def addAdmin(chatId):
    with app.app_context():
        if Admin.query.filter_by(chatId=chatId).first():
            pass
        else:
            Admin(chatId=chatId)