import telebot
from telebot import types
from datetime import datetime

hideMenu = types.ReplyKeyboardRemove()

def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k

months = {
    "JAN": 1,
    "FEB": 2,
    "MAR": 3,
    "APR": 4,
    "MAY": 5,
    "JUN": 6,
    "JUL": 7,
    "AUG": 8,
    "SEP": 9,
    "OCT": 10,
    "NOV": 11,
    "DEC": 12
}

years = [i for i in range(1997, datetime.now().year + 1)]


def startMenu():
    startMenu = types.InlineKeyboardMarkup(row_width=1)
    startMenuBtn1 = types.InlineKeyboardButton(text="Перейти в канал",url="https://t.me/testcryptovedmabot")
    startMenuBtn2 = types.InlineKeyboardButton(text="Подтвердить", callback_data="chatMemberConfirm")
    startMenu.add(startMenuBtn1, startMenuBtn2)
    return startMenu


def firstMenu():
    firstMenu = types.InlineKeyboardMarkup(row_width=1)
    firstMenuBtn1 = types.InlineKeyboardButton(text="Викторины", callback_data="toQuizzes")
    firstMenuBtn2 = types.InlineKeyboardButton(text="The Economist", callback_data="toTheEconomist")
    firstMenuBtn3 = types.InlineKeyboardButton(text="Для связи со мной", callback_data="forCommunication")
    firstMenuBtn4 = types.InlineKeyboardButton(text="ChatGPT", callback_data="toChatGPT")
    firstMenu.add(firstMenuBtn1,firstMenuBtn2,firstMenuBtn3, firstMenuBtn4)
    return firstMenu


def theEconomistFirstMenu():
    theEconomistFirstMenu = types.InlineKeyboardMarkup(row_width=1)
    theEconomistFirstMenuBtn1 = types.InlineKeyboardButton(text="Выбрать выпуск", callback_data="theEconomistСhoiceIssue")
    theEconomistFirstMenuBtn2 = types.InlineKeyboardButton(text="Подписка", callback_data="theEconomistSub")
    theEconomistFirstMenuBtn3 = types.InlineKeyboardButton(text="Вернуться в главное меню", callback_data="toMainMenu")
    theEconomistFirstMenu.add(theEconomistFirstMenuBtn1,theEconomistFirstMenuBtn2,theEconomistFirstMenuBtn3)
    return theEconomistFirstMenu


def theEconomistSubMenu():
    theEconomistSubMenu = types.InlineKeyboardMarkup(row_width=1)
    theEconomistSubMenuBtn1 = types.InlineKeyboardButton(text="Подписаться", callback_data="theEconomistSubscribe")
    theEconomistSubMenuBtn2 = types.InlineKeyboardButton(text="Отписаться", callback_data="theEconomistUnsub")
    theEconomistSubMenuBtn3 = types.InlineKeyboardButton(text="Назад", callback_data="toTheEconomist")
    theEconomistSubMenu.add(theEconomistSubMenuBtn1,theEconomistSubMenuBtn2, theEconomistSubMenuBtn3)
    return theEconomistSubMenu


def fromSubToMainMenu():
    fromSubToMainMenu = types.InlineKeyboardMarkup(row_width=1)
    fromSubToMainMenuBtn1 = types.InlineKeyboardButton(text="Назад", callback_data="theEconomistSub")
    fromSubToMainMenu.add(fromSubToMainMenuBtn1)
    return fromSubToMainMenu

def menuQuiz(quizList):
    menu = types.InlineKeyboardMarkup(row_width=1)
    if len(quizList) != 0:
        for quiz in quizList:
            menu.add(
                types.InlineKeyboardButton(f'{quiz.name}',
                                           callback_data=f'toOpenQuiz#{quiz.id}')
            )
    menu.add(types.InlineKeyboardButton(text="Назад", callback_data="toMainMenu"))
    return menu


def adminMenu():
    menu = types.InlineKeyboardMarkup(row_width=1)
    menu.add(types.InlineKeyboardButton(text="Создать викторину", callback_data="createQuiz"))
    menu.add(types.InlineKeyboardButton(text="Просмотреть мои викторины", callback_data="viewQuizess"))
    menu.add(types.InlineKeyboardButton(text="Удалить себя из админов", callback_data="deleteAdmin"))
    return menu

def adminAfterCreateQuiz():
    menu = types.InlineKeyboardMarkup(row_width=1)
    menu.add(types.InlineKeyboardButton(text="В главное меню", callback_data="toAdminMenu"))
    return menu


def adminQuizDelete(quizList):
    menu = types.InlineKeyboardMarkup(row_width=1)
    if len(quizList) != 0:
        for quiz in quizList:
            menu.add(
                types.InlineKeyboardButton(f'{quiz.name}',
                                           callback_data=f'toDeleteQuiz#{quiz.id}')
            )
    menu.add(types.InlineKeyboardButton(text="В главное меню", callback_data="toAdminMenu"))
    return menu


def adminQuizView(quizList):
    menu = types.InlineKeyboardMarkup(row_width=1)
    if len(quizList) != 0:
        for quiz in quizList:
            menu.add(
                types.InlineKeyboardButton(f'{quiz.name}',
                                           callback_data=f'toOpenAdminQuiz#{quiz.id}')
            )
    menu.add(types.InlineKeyboardButton(text="Удалить викторину", callback_data="deleteQuiz"))
    menu.add(types.InlineKeyboardButton(text="Назад", callback_data="toAdminMenu"))
    return menu

def create_quiz_tips():
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(types.InlineKeyboardButton(text="Да", callback_data="withTip"),
             types.InlineKeyboardButton(text="Нет", callback_data="withoutTip"))
    menu.add(types.InlineKeyboardButton(text="Сбросить викторину и в главное меню", callback_data="resetQuiz"))
    return menu

def resetQuiz():
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(types.InlineKeyboardButton(text="Сбросить викторину и в главное меню", callback_data="resetQuiz"))
    return menu

def create_quiz_back():
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(types.InlineKeyboardButton(text="Сбросить викторину и в главное меню", callback_data="resetQuiz"))
    return menu

def create_quiz_step0_back():
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(types.InlineKeyboardButton(text="Назад", callback_data="createQuiz"))
    menu.add(types.InlineKeyboardButton(text="Сбросить викторину и в главное меню", callback_data="resetQuiz"))
    return menu

def quizReward():
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(types.InlineKeyboardButton(text="Да", callback_data="withReward"),
             types.InlineKeyboardButton(text="Нет", callback_data="withoutReward"))
    menu.add(types.InlineKeyboardButton(text="Сбросить викторину и в главное меню", callback_data="resetQuiz"))
    return menu

def quizRewardChoose():
    menu = types.InlineKeyboardMarkup(row_width=2)
    menu.add(types.InlineKeyboardButton(text="Для всех", callback_data="rewardForAll"),
             types.InlineKeyboardButton(text="Уникальная", callback_data="uniqueReward"))
    menu.add(types.InlineKeyboardButton(text="Сбросить викторину и в главное меню", callback_data="resetQuiz"))
    return menu

def reset_polls(tip):
    menu = types.InlineKeyboardMarkup(row_width=1)
    if tip != 'no':
        menu.add(types.InlineKeyboardButton(text="Подсказка", url=tip))
    menu.add(types.InlineKeyboardButton(text="Вернуться в главное меню", callback_data="toMainMenu"))
    return menu

def adminQuizViewText(quiz, quests):
    text = f"Информация о викторине: {quiz.name}\n\n"
    text += "Вопросы:\n\n"
    i = 1
    for quest in quests:
        text += f"{i} вопрос:  "
        text += quest.text + "\n"
        if quest.tip != 'no':
            text += f"Подсказка: {quest.tip}\n"
        text += "Правильный ответ: " + quest.answers[0] + "\n\n"
        i += 1
    if quiz.reward:
        reward = "С наградой: "
        text += reward
        if quiz.reward_type == "unique":
            reward_type = "уникальные"
            text += reward_type + "\n\n"

            for i in quiz.rewards_initial:
                text += str(i) + "\n"
            text += "\n" + "Осталось призов: " + str(quiz.rewards_remain)
        else:
            reward_type = "одинаковые"
            text += reward_type + "\n\n"
            text += quiz.rewards + "\n\n"
            text += "Осталось призов: " + str(quiz.rewards_remain)
    else:
        reward = "Без награды"
        text += reward
    return text

def adminQuizViewButton():
    menu = types.InlineKeyboardMarkup(row_width=1)
    menu.add(types.InlineKeyboardButton(text="Удалить викторину", callback_data="deleteQuiz"))
    menu.add(types.InlineKeyboardButton(text="Назад", callback_data="viewQuizess"))
    return menu

def resetEconomist():
    menu = types.InlineKeyboardMarkup(row_width=1)
    menu.add(types.InlineKeyboardButton(text="Вернуться в главное меню", callback_data="toMainMenu"))
    return menu

def backToQuiz():
    menu = types.InlineKeyboardMarkup(row_width=1)
    menu.add(types.InlineKeyboardButton(text="Вернуться к викторинам", callback_data="toQuizzes"))
    return menu

def backToMonth(month):
    menu = types.InlineKeyboardMarkup(row_width=1)
    menu.add(types.InlineKeyboardButton(text="Назад", callback_data=f"toEconomistMonth#{get_key(months, month)}"))
    menu.add(types.InlineKeyboardButton(text="Вернуться в главное меню", callback_data="toMainMenu"))
    return menu

def economistMonth():
    menu = types.InlineKeyboardMarkup(row_width=3)
    row = []
    if len(months) != 0:
        for month in months:
            row.append(
                types.InlineKeyboardButton(f'{month}',
                                           callback_data=f'toEconomistMonth#{month}')
            )
            if len(row) == 3:
                menu.add(*row)
                row = []
    menu.add(types.InlineKeyboardButton(text="Назад", callback_data="theEconomistСhoiceIssue"))
    return menu

def economistYear():
    row = []
    menu = types.InlineKeyboardMarkup(row_width=3)
    if len(years) != 0:
        for year in years:
            row.append(
                types.InlineKeyboardButton(f'{year}',
                                           callback_data=f'toEconomistYear#{year}')
            )
            if len(row) == 3:
                menu.add(*row)
                row = []
    menu.add(types.InlineKeyboardButton(text="Назад", callback_data="toTheEconomist"))
    return menu

def economistEditions(editionsList, year):
    menu = types.InlineKeyboardMarkup(row_width=1)
    if len(editionsList) != 0:
        for edition in editionsList:
            menu.add(
                types.InlineKeyboardButton(f'{edition.name}',
                                           callback_data=f'toOpenEconomistEdition#{edition.id}')
            )
    menu.add(types.InlineKeyboardButton(text="Назад", callback_data=f"toEconomistYear#{year}"))
    return menu

def economistEditionText(name, month, year,  url):
    text = f"Выпуск: \n'{name}' от {month}.{year}" + "\n\n"
    text += url
    return text

def adminCreateQuizText(current, all):
    text = f"Введите {current} ответ из {all}:"
    return text

def reward_take(code):
    text = f"Ты одним из первых ответил на все вопросы правильно! Вот твой код:\n{code}"
    return text

def collected_code_text(code):
    text = f"Поздравляю! Ты снова ответил правильно на все вопросы, но ты уже получил код!\n{code}",
    return text

def already_collected_code_text(correct, all, code):
    text = f"Вы правильно ответили на {correct} из {all}" + "\n"
    text += f"Полученный ранее код: {code}"
    return text

def chatGPT():
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    menu.add(types.KeyboardButton("🧹Очистить контекст"))
    menu.add(types.KeyboardButton("◀️Вернуться в главное меню"))
    # menu.add(types.InlineKeyboardButton(text="🧹Очистить контекст", callback_data="clearContext"))
    # menu.add(types.InlineKeyboardButton(text="Вернуться в главное меню", callback_data="toMainMenu"))
    return menu