from flask_migrate import Migrate
from app.config.config import app, db

from app.models.QuizModel import Quiz
from app.models.UserModel import User
from app.models.QuestModel import Quest
from app.models.AdminModel import Admin
from app.models.EconomistIssueModel import EconomistIssue
from app.models.NewQuizModel import NewQuiz
from app.models.NewQuestModel import NewQuest
from app.models.PrizeModel import Prize

migrate = Migrate(app, db)

app.app_context().push()
