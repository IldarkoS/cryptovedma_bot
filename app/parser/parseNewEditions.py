from app.config import db, app
from app.parser import parser
from app.bot.markups import months
from app.models.EconomistIssueModel import EconomistIssue

def addNewEconomistEdition():
    with app.app_context():
        editions = parser.parseNewEconomist()
        for edition in editions:
            if EconomistIssue.query.filter_by(url=edition.editionsUrl).first():
                pass
            else:
                print("Добавлен", edition.editionsName)
                EconomistIssue(
                    name=edition.editionsName,
                    year=edition.editionsDate.split()[-1],
                    url=edition.editionsUrl,
                    image_url=edition.editionsImageUrl,
                    month=months[edition.editionsDate.split()[0]]
                )

addNewEconomistEdition()