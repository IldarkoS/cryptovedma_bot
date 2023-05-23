from app.config import db, app
from app.bot.markups import months

class EconomistIssue(db.Model):

    __tablename__ = 'economistissue'

    id = db.Column(db.Integer, primary_key = True)
    year = db.Column(db.Integer, default = 2023)
    month = db.Column(db.Integer, default = 1)
    name = db.Column(db.String, default = 'N/A')
    url = db.Column(db.String, default = 'N/A')
    image_url = db.Column(db.String, default = 'N/A')

    def __repr__(self):
        return '<Quiz %r>' % self.name

    def __init__(self, name, year, month, url, image_url):
        with app.app_context():
            if EconomistIssue.query.filter_by(url=url).first():
                print("false")
            else:
                 self.name = name
                 self.year = year
                 self.month = month
                 self.url = url
                 self.image_url = image_url
                 db.session.add(self)
                 db.session.commit()


def getEditionList(month, year):
    with app.app_context():
        a = list(map(lambda x: x, EconomistIssue.query.filter(EconomistIssue.month==month, EconomistIssue.year==year).all()))
        return a


def getEditionInfo(id):
    with app.app_context():
        edition = EconomistIssue.query.filter_by(id=id).first()
        return edition

# getEditionList(11, 2021)
# addEconomistEdition()
