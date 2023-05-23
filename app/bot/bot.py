import markups as mk
from app.models.UserModel import User
from app.models.QuizModel import Quiz
from app.models.QuestModel import Quest
from app.models.AdminModel import Admin
from app.models.EconomistIssueModel import EconomistIssue
from app.models.NewQuizModel import NewQuiz
from app.models.NewQuestModel import NewQuest
from app.models.PrizeModel import Prize

from datetime import datetime
from random import shuffle

import app.models.AdminModel as AdminModel
import app.models.NewQuestModel as NewQuestModel
import app.models.NewQuizModel as NewQuizModel
import app.models.UserModel as UserModel
import app.models.QuizModel as QuizModel
import app.models.QuestModel as QuestModel
import app.models.EconomistIssueModel as EconomistIssueModel
import app.models.PrizeModel as PrizeModel

from dotenv import load_dotenv
import openai
import json
import telebot
from telebot import types
# from telebot.types import
from app.config import db, app

bot = telebot.TeleBot("TG_BOT_KEY")
openai.api_key = "OPEN_AI_KEY"

# variables

quest_creating = dict()
quiz = dict()
quiz_tr = dict()
economist_edition = dict()
msg_to_delete = dict()
quiz_creating = dict()

@bot.message_handler(commands=["start"])
def start(message):

    quiz.pop(message.chat.id, None)
    quiz_creating.pop(message.chat.id, None)
    quest_creating.pop(message.chat.id, None)
    economist_edition.pop(message.chat.id, None)
    quiz_tr.pop(message.chat.id, None)
    if AdminModel.checkAdmin(message.chat.id):
        bot.send_message(chat_id=message.chat.id, text="Админ панель", reply_markup=mk.adminMenu())
    else:
        username = message.from_user.username
        UserModel.createUser(message.chat.id, username)
        bot.send_message(
            chat_id=message.chat.id,
            parse_mode="MARKDOWN",
            text=
            '''Привет, это CryptoVedmaBot\nДля работы бота необходимо подписаться на @namechannel
            ''',
            reply_markup=mk.startMenu()
            # reply_markup=mk.hideMenu
        )
    UserModel.clearContext(message.chat.id)


@bot.message_handler(content_types=["text"])
def adminStart(message):
    print(f"Это message - {message.text}")
    if message.text == "Админ":
        bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id
        )
        bot.send_message(
            chat_id=message.chat.id,
            text="Введите пароль:"
        )
        bot.register_next_step_handler(message, adminLogin)
    if message.text == "◀️Вернуться в главное меню":
        bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id
        )
        msg = bot.send_message(message.chat.id, "⚙️", reply_markup=mk.hideMenu)
        bot.delete_message(
            chat_id=message.chat.id,
            message_id=msg.message_id
        )
        bot.send_message(
            chat_id=message.chat.id,
            text=f'''{UserModel.getUsername(chatId=message.chat.id)}! Добро пожаловать в @CryptoVedmaBot!''',
            reply_markup=mk.firstMenu()
        )


def adminLogin(message):
    if message.text == '123':
        AdminModel.addAdmin(message.chat.id)
        bot.send_message(
            chat_id=message.chat.id,
            text="admin панель",
            reply_markup=mk.adminMenu()
        )


def checkChatMember(chatId):
    if bot.get_chat_member(chat_id="@testcryptovedmabot", user_id=chatId).status != "left":
        return True
    else:
        bot.send_message(
            chat_id=chatId,
            text="Вы не подписались!",
            reply_markup=mk.startMenu()
        )
        return False

@bot.callback_query_handler(func=lambda call: True)
def chatMemberConfirm(call):
    print(f"Это callback {call.data}")
    if call.data == "chatMemberConfirm":
        if checkChatMember(call.message.chat.id):
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id
            )
            bot.send_message(
                chat_id=call.message.chat.id,
                text=f'''Привет, {UserModel.getUsername(call.message.chat.id)}! Добро пожаловать в @CryptoVedmaBot!''',
                reply_markup=mk.firstMenu()
            )
        else:
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id
            )
            bot.send_message(
                chat_id=call.message.chat.id,
                text="Вы не подписались!",
                reply_markup=mk.startMenu()
            )
    if call.data == "toQuizzes":
        if checkChatMember(call.message.chat.id):
            quiz.pop(call.message.chat.id, None)
            quiz_tr.pop(call.message.chat.id, None)
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id
            )
            bot.send_message(
                chat_id=call.message.chat.id,
                text="Выберите викторину",
                reply_markup=mk.menuQuiz(QuizModel.getQuizList())
            )
    if call.data == "toTheEconomist":
        if checkChatMember(call.message.chat.id):
            economist_edition.pop(call.message.chat.id, None)
            quiz.pop(call.message.chat.id, None)
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id
            )
            bot.send_message(
                chat_id=call.message.chat.id,
                text='Оформи подписку на оповещения о новых выпусках журнала-оракула "The economist" прямо в @CryptoVedmaBot! Давай предсказывать будущее вместе! www.economist.com/',
                reply_markup=mk.theEconomistFirstMenu()
            )
    if call.data == "forCommunication":
        if checkChatMember(call.message.chat.id):
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id
            )
            bot.send_message(
                chat_id=call.message.chat.id,
                text="Для связи, вопросов, сотрудничества и предложений @CryptoRichWitch",
                reply_markup=mk.firstMenu()
            )
    if call.data == "toMainMenu":
        if checkChatMember(call.message.chat.id):
            economist_edition.pop(call.message.chat.id, None)
            quiz.pop(call.message.chat.id, None)
            quiz_tr.pop(call.message.chat.id, None)
            bot.clear_step_handler_by_chat_id(call.message.chat.id)
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id
            )
            bot.send_message(
                chat_id=call.message.chat.id,
                text=f'''{UserModel.getUsername(chatId=call.message.chat.id)}! Добро пожаловать в @CryptoVedmaBot!''',
                reply_markup=mk.firstMenu()
            )
    if call.data == "theEconomistSub":
        if checkChatMember(call.message.chat.id):
            if UserModel.getSubStatus(chatId=call.message.chat.id):
                sub_status = "Активна"
            else:
                sub_status = "Неактивна"
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id
            )
            bot.send_message(
                chat_id=call.message.chat.id,
                text=f"Получайте новые выпуски The Economist самыми первыми!\n\n Статус подписки - {sub_status}",
                reply_markup=mk.theEconomistSubMenu()
            )
    if call.data == "theEconomistSubscribe":
        if checkChatMember(call.message.chat.id):
            if UserModel.getSubStatus(chatId=call.message.chat.id):
                bot.delete_message(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id
                )
                bot.send_message(
                    chat_id=call.message.chat.id,
                    text="Вы уже подписаны на рассылку!",
                    reply_markup=mk.fromSubToMainMenu()
                )
            else:
                UserModel.theEconomistSub(call.message.chat.id, 1)
                bot.delete_message(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id
                )
                bot.send_message(
                    chat_id=call.message.chat.id,
                    text="Теперь вы подписаны на рассылку о новых выпусках The Economist",
                    reply_markup=mk.fromSubToMainMenu()
                )
    if call.data == "theEconomistUnsub":
        if checkChatMember(call.message.chat.id):
            if UserModel.getSubStatus(chatId=call.message.chat.id):
                UserModel.theEconomistSub(call.message.chat.id, 0)
                bot.delete_message(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id
                )
                bot.send_message(
                    chat_id=call.message.chat.id,
                    text="Вы отписались от рассылки!",
                    reply_markup=mk.fromSubToMainMenu()
                )
            else:
                bot.delete_message(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id
                )
                bot.send_message(
                    chat_id=call.message.chat.id,
                    text="Вы не подписаны на рассылку!",
                    reply_markup=mk.theEconomistSubMenu()
                )
    if call.data == "theEconomistСhoiceIssue":
        if checkChatMember(call.message.chat.id):
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id
            )
            bot.send_message(
                chat_id=call.message.chat.id,
                text="Выберите год:",
                reply_markup=mk.economistYear()
            )

    if call.data.split("#")[0] == 'toOpenQuiz':
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        if checkChatMember(call.message.chat.id):
            idQuiz = call.data.split('#')[1]
            quizFromDB = QuizModel.getQuiz(idQuiz)
            UserModel.zeroingQuiz(call.message.chat.id)
            # bot.send_message(call.message.chat.id, quizFromDB.name)
            quests = QuestModel.getQuestList(quizFromDB.id)
            quiz_tr[call.message.chat.id] = idQuiz
            quiz[call.message.chat.id] = currentQuiz(quests)
            # quiz_id[call.message.chat.id] = idQuiz
            send_polls(call.message.chat.id, quiz[call.message.chat.id])

    if call.data == "createQuiz":
        quest_creating.pop(call.message.chat.id, None)
        quiz_creating.pop(call.message.chat.id, None)
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        NewQuizModel.resetQuiz()
        msg = bot.send_message(
            chat_id=call.message.chat.id,
            text="Введите название викторины (название должно быть уникальным!)",
            reply_markup=mk.create_quiz_back()
        )
        bot.register_next_step_handler(msg, createQuizStep0)

    if call.data == "viewQuizess":
        quest_creating.pop(call.message.chat.id, None)
        quiz_creating.pop(call.message.chat.id, None)
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        bot.send_message(
            chat_id=call.message.chat.id,
            text="Выберите викторину, чтобы увидеть подробную информацию",
            reply_markup=mk.adminQuizView(QuizModel.getQuizList())
        )

    if call.data.split("#")[0] == 'toOpenAdminQuiz':
        quest_creating.pop(call.message.chat.id, None)
        quiz_creating.pop(call.message.chat.id, None)
        quizId = call.data.split('#')[1]
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        bot.send_message(
            chat_id=call.message.chat.id,
            text=mk.adminQuizViewText(QuizModel.getQuiz(quizId), QuestModel.getQuestList(quizId)),
            reply_markup=mk.adminQuizViewButton()
        )

    if call.data == "deleteQuiz":
        quest_creating.pop(call.message.chat.id, None)
        quiz_creating.pop(call.message.chat.id, None)
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        bot.send_message(
            chat_id=call.message.chat.id,
            text="Какую викторину удалить?",
            reply_markup=mk.adminQuizDelete(QuizModel.getQuizList())
        )
    if call.data.split("#")[0] == 'toDeleteQuiz':
        quest_creating.pop(call.message.chat.id, None)
        quiz_creating.pop(call.message.chat.id, None)
        QuizModel.deleteQuiz(call.data.split('#')[1])
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        bot.send_message(
            chat_id=call.message.chat.id,
            text="Викторина удалена!",
            reply_markup=mk.adminMenu()
        )

    if call.data == "toAdminMenu":
        quest_creating.pop(call.message.chat.id, None)
        quiz_creating.pop(call.message.chat.id, None)
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        bot.send_message(
            chat_id=call.message.chat.id,
            text="Админ-панель",
            reply_markup=mk.adminMenu()
        )

    if call.data == "logger":
        pass

    if call.data == "deleteAdmin":
        AdminModel.deleteAdmin(call.message.chat.id)
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        bot.send_message(
            chat_id=call.message.chat.id,
            text="Вы удалены из списка админов!"
        )
        bot.send_message(
            chat_id=call.message.chat.id,
            text=f'''Привет, {UserModel.getUsername(call.message.chat.id)}! Добро пожаловать в @CryptoVedmaBot!''',
            reply_markup=mk.firstMenu()
        )
    if call.data == "resetQuiz":
        NewQuizModel.resetQuiz()
        bot.clear_step_handler_by_chat_id(call.message.chat.id)
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        bot.send_message(
            chat_id=call.message.chat.id,
            text="Админ-панель",
            reply_markup=mk.adminMenu()
        )
    if call.data.split("#")[0] == 'toEconomistYear':
        if checkChatMember(call.message.chat.id):
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id
            )
            year = call.data.split("#")[1]
            economist_edition[call.message.chat.id] = [year]
            bot.send_message(
                chat_id=call.message.chat.id,
                text="Выберите месяц:",
                reply_markup=mk.economistMonth()
            )
    if call.data.split('#')[0] == 'toEconomistMonth':
        if checkChatMember(call.message.chat.id):
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id
            )
            month = call.data.split('#')[1]
            bot.send_message(
                chat_id=call.message.chat.id,
                text="Доступные выпуски:",
                reply_markup=mk.economistEditions(
                    EconomistIssueModel.getEditionList(
                        int(mk.months[month]),
                        int(economist_edition[call.message.chat.id][0]),
                    ),
                    int(economist_edition[call.message.chat.id][0])
                )
            )

    if call.data.split("#")[0] == 'toOpenEconomistEdition':
        if checkChatMember(call.message.chat.id):
            idEdition = call.data.split('#')[1]
            edition = EconomistIssueModel.getEditionInfo(idEdition)
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id
            )
            bot.send_photo(
                chat_id=call.message.chat.id,
                caption=mk.economistEditionText(edition.name, edition.month, edition.year, edition.url),
                photo=edition.image_url,
                reply_markup=mk.backToMonth(
                    edition.month
                )
            )

    if call.data == "toChatGPT":
        if checkChatMember(call.message.chat.id):
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id
            )
            msg = bot.send_message(
                chat_id=call.message.chat.id,
                text="Ты в чате с ChatGPT🤖. Напиши ему сообщение ✍️",
                reply_markup=mk.chatGPT()
            )
            bot.register_next_step_handler(msg, chatStep1)

    if call.data == "clearContext":
        UserModel.clearContext(call.message.chat.id)
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        msg = bot.send_message(
            chat_id=call.message.chat.id,
            text="🧹 Контекст очищен",
            reply_markup=mk.chatGPT()
        )
        bot.register_next_step_handler(msg, chatStep1)

    if call.data == "withReward":
        quiz_id = quiz_creating[call.message.chat.id]
        NewQuizModel.setReward(quiz_id, key=True)
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        bot.send_message(
            chat_id=call.message.chat.id,
            text="Выберите тип награды:",
            reply_markup=mk.quizRewardChoose()
        )
    if call.data == "withoutReward":
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        quiz_id = quiz_creating[call.message.chat.id]
        NewQuizModel.setReward(quiz_id, key=False)
        QuizModel.createQuiz(NewQuizModel.getNewQuiz(quiz_id))
        bot.send_message(
            chat_id=call.message.chat.id,
            text="Викторина заполнена!",
            reply_markup=mk.adminAfterCreateQuiz()
        )
    if call.data == "rewardForAll":
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        msg = bot.send_message(
            chat_id=call.message.chat.id,
            text="Введите кол-во призовых мест:",
            reply_markup=mk.resetQuiz()
        )
        bot.register_next_step_handler(msg, createQuizStep7, reward_type="identical")
    if call.data == "uniqueReward":
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        msg = bot.send_message(
            chat_id=call.message.chat.id,
            text="Введите кол-во призовых мест:",
            reply_markup=mk.resetQuiz()
        )
        bot.register_next_step_handler(msg, createQuizStep7, reward_type="unique")

    if call.data == "withTip":
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        msg = bot.send_message(
            chat_id=call.message.chat.id,
            text="Отправьте ссылку на подсказку:",
            reply_markup=mk.resetQuiz()
        )
        bot.register_next_step_handler(msg, createQuizStep6, True)
    if call.data == "withoutTip":
        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        msg = bot.send_message(
            chat_id=call.message.chat.id,
            text="Викторина будет без подсказки"
        )
        createQuizStep6(msg, False)

@bot.message_handler(commands=['image'])
def image(message) -> None:
    if checkChatMember(message.chat.id):
        try:
            msg = bot.send_message(message.chat.id, "👨‍🎨 Напишите описание для картинки", reply_markup=mk.chatGPT(),
                                   parse_mode='MARKDOWN')
            bot.register_next_step_handler(msg, generate_image)
        except Exception as e:
            print(e)
            bot.reply_to(message, 'Error')


def generate_image(message):
    resp = openai.Image.create(
        prompt=message.text,
        n=1,
        size="1024x1024"
    )
    print(resp['data'][0]['url'])

    bot.send_message(message.chat.id, resp['data'][0]['url'], reply_markup=mk.chatGPT(),
                     parse_mode='MARKDOWN')


def chatStep1(message):
    if message.text == "🧹Очистить контекст":
        UserModel.clearContext(message.chat.id)
        bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id
        )
        msg = bot.send_message(
            chat_id=message.chat.id,
            text="🧹 Контекст очищен",
            reply_markup=mk.chatGPT()
        )
        bot.register_next_step_handler(msg, chatStep1)
    elif message.text == "◀️Вернуться в главное меню":
        bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id
        )
        msg = bot.send_message(message.chat.id, "⚙️",reply_markup=mk.hideMenu)
        bot.delete_message(
            chat_id=message.chat.id,
            message_id=msg.message_id
        )
        bot.send_message(
            chat_id=message.chat.id,
            text=f'''{UserModel.getUsername(chatId=message.chat.id)}! Добро пожаловать в @CryptoVedmaBot!''',
            reply_markup=mk.firstMenu()
        )
    else:
        try:
            msg_to_del = bot.send_message(message.chat.id, "Ждем ответ ⏳", parse_mode='MARKDOWN')
            try:
                data = UserModel.getContext(message.chat.id)
            except json.decoder.JSONDecodeError as e:
                data = []
            context_len = 0
            if len(data) != 0:
                for i in data:
                    context_len += len(i['content'])
            if context_len >= 16000:
                UserModel.clearContext(message.chat.id)
            data.append({"role": "user", "content": "{}".format(message.text)})
            try:
                completion = openai.ChatCompletion.create(
                    model='gpt-3.5-turbo',
                    messages=data,
                    temperature=0
                )
                resp_ai = completion["choices"][0]["message"]["content"]
                data.append({"role": "assistant", "content": "{}".format(resp_ai)})
                msg = bot.send_message(message.chat.id, resp_ai, reply_markup=mk.chatGPT())

                UserModel.addContext(message.chat.id, data)

            except Exception as e:
                print(e)
                UserModel.clearContext(message.chat.id)
                msg = bot.send_message(message.chat.id, "Переполнение контекста. Контекст очищен")

            bot.delete_message(chat_id=message.chat.id, message_id=msg_to_del.id)
            bot.register_next_step_handler(msg, chatStep1)
        except Exception as e:
            print(e)
            bot.reply_to(message, f'Error(')


def createQuizStep0(message):
    name = message.text
    if NewQuizModel.checkDublicate(name):
        NewQuiz(name)
        quizId = NewQuizModel.getLastId()
        quiz_creating[message.chat.id] = quizId
        msg = bot.send_message(
            chat_id=message.chat.id,
            text="Сколько будет вопросов?",
            reply_markup=mk.create_quiz_step0_back()
        )
        bot.register_next_step_handler(msg, createQuizStep1, quizId)

    else:
        bot.clear_step_handler_by_chat_id(message.chat.id)
        msg = bot.send_message(chat_id=message.chat.id, text="Викторина с таким названием уже существует! Введите другое:")
        bot.register_next_step_handler(msg, createQuizStep0)


def createQuizStep1(message, quizId):
    try:
        quest_count = int(message.text)
        NewQuizModel.setQuestCount(quizId, quest_count)
        msg = bot.send_message(chat_id=message.chat.id,
                               text=f"Введите 1 вопрос из {quest_count}",
                               reply_markup=mk.resetQuiz())
        bot.register_next_step_handler(msg, createQuizStep2, quizId)
    except:
        msg = bot.send_message(chat_id=message.chat.id, text="Некорректный ввод! Попробуйте еще раз!")
        bot.register_next_step_handler(msg, createQuizStep1, quizId)


def createQuizStep2(message, quizId):
    textOfQuest = message.text
    NewQuest(quizId, textOfQuest)
    questId = NewQuestModel.getLastId()

    msg = bot.send_message(chat_id=message.chat.id,
                           text="Сколько будет ответов?(min 2)",
                           reply_markup=mk.resetQuiz())
    bot.register_next_step_handler(msg, createQuizStep3, questId)


def createQuizStep3(message, questId):
    try:
        answer_count = int(message.text)
        NewQuestModel.setAnswerCount(questId, answer_count)
        msg = bot.send_message(chat_id=message.chat.id,
                               text=f"Введите правильный ответ:",
                               reply_markup=mk.resetQuiz())
        bot.register_next_step_handler(msg, createQuizStep4, questId)
    except:
        msg = bot.send_message(chat_id=message.chat.id, text="Некорректный ввод! Попробуйте еще раз!")
        bot.register_next_step_handler(msg, createQuizStep3, questId)


def createQuizStep4(message, questId):
    answer = message.text
    NewQuestModel.appendAnswer(questId, answer)
    current = NewQuestModel.filledAnswers(questId)+1
    msg = bot.send_message(
        chat_id=message.chat.id,
        text=mk.adminCreateQuizText(current, NewQuestModel.getQuest(questId).answer_count),
        reply_markup=mk.resetQuiz())
    bot.register_next_step_handler(msg, createQuizStep5, questId)



def createQuizStep5(message, questId):
    answer = message.text
    NewQuestModel.appendAnswer(questId, answer)
    if NewQuestModel.filledAnswers(questId) < NewQuestModel.getQuest(questId).answer_count:
        current = NewQuestModel.filledAnswers(questId)+1
        msg = bot.send_message(
            chat_id=message.chat.id,
            text=mk.adminCreateQuizText(current, NewQuestModel.getQuest(questId).answer_count),
            reply_markup=mk.resetQuiz())
        bot.register_next_step_handler(msg, createQuizStep5, questId)
    else:
        quest_creating[message.chat.id] = questId
        msg = bot.send_message(
            chat_id=message.chat.id,
            text="Будет подсказка?",
            reply_markup=mk.create_quiz_tips()
        )


def createQuizStep6(message, tip):
    quest_id = quest_creating[message.chat.id]
    if tip:
        NewQuestModel.set_tip(quest_id, message.text)
    else:
        NewQuestModel.set_tip(quest_id, "no")
    quizId = quiz_creating[message.chat.id]
    NewQuizModel.incrementFilledQuest(quizId)
    filled_quest = NewQuizModel.getNewQuiz(quizId).filled_quest
    quest_count = NewQuizModel.getNewQuiz(quizId).quest_count
    if filled_quest < quest_count:
        msg = bot.send_message(chat_id=message.chat.id,
                               text=f"Введите {filled_quest + 1} вопрос из {quest_count}",
                               reply_markup=mk.resetQuiz())
        bot.register_next_step_handler(msg, createQuizStep2, quizId)
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text="Будет награда?",
            reply_markup=mk.quizReward()
        )

def createQuizStep7(message, reward_type):
    try:
        rewards_count = int(message.text)
        NewQuizModel.setRewardsCount(quiz_creating[message.chat.id], rewards_count)
        if reward_type == "identical":
            NewQuizModel.setRewardType(quiz_creating[message.chat.id], "identical")
            msg = bot.send_message(
                chat_id=message.chat.id,
                text="Введите код:",
                reply_markup=mk.resetQuiz()
            )
            bot.register_next_step_handler(msg, createQuizStep8)
        if reward_type == "unique":
            NewQuizModel.setRewardType(quiz_creating[message.chat.id], "unique")
            current = []
            msg = bot.send_message(
                chat_id=message.chat.id,
                text="Введите коды(отдельным сообщением!)",
                reply_markup=mk.resetQuiz()
            )
            bot.register_next_step_handler(msg, createQuizStep9, rewards_count, current)
    except:
        msg = bot.send_message(chat_id=message.chat.id, text="Некорректный ввод! Попробуйте еще раз!")
        bot.register_next_step_handler(msg, createQuizStep7, reward_type)


def createQuizStep8(message):
    code = message.text
    NewQuizModel.setRewards(quiz_creating[message.chat.id], code)
    quiz_id = quiz_creating[message.chat.id]
    QuizModel.createQuiz(NewQuizModel.getNewQuiz(quiz_id))
    bot.send_message(
        chat_id=message.chat.id,
        text="Викторина заполнена!",
        reply_markup=mk.adminAfterCreateQuiz()
    )


def createQuizStep9(message, rewards_count, current):
    code = message.text
    if not code in current:
        current.append(code)
        print(current)
        if len(current) < rewards_count:
            msg = bot.send_message(
                chat_id=message.chat.id,
                text="Введите следующий код!",
                reply_markup=mk.resetQuiz()
            )
            bot.register_next_step_handler(msg, createQuizStep9, rewards_count, current)
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text="Викторина заполнена!",
                reply_markup=mk.adminAfterCreateQuiz()
            )
            NewQuizModel.setRewards(quiz_creating[message.chat.id], current)
            quiz_id = quiz_creating[message.chat.id]
            QuizModel.createQuiz(NewQuizModel.getNewQuiz(quiz_id))
            quiz_creating.pop(message.chat.id, None)
            quest_creating.pop(message.chat.id, None)
    else:
        msg = bot.send_message(
            chat_id=message.chat.id,
            text="Данный код уже введен! Повторите ввод!",
            reply_markup=mk.resetQuiz()
        )
        bot.register_next_step_handler(msg, createQuizStep9, rewards_count, current)

class currentQuiz:
    def __init__(self, qst):
        self.qst = qst
        self.length = len(qst)
        self.current = 0

    def __iter__(self):
        return self.qst[self.current]

    def __next__(self):
        self.current += 1
        if self.current >= self.length:
            raise StopIteration
        return self.qst[self.current]
    def print(self):
        return self.qst


def send_polls(chatId, quiz):
    answers = quiz.qst[quiz.current].answers
    correct_answer = answers[0]
    shuffle(answers)
    correct_answer = answers.index(correct_answer)
    quiz.qst[quiz.current].correct_answer = correct_answer
    msg = bot.send_message(chatId,
                           f"Вопрос {quiz.current + 1} из {quiz.length}:",
                           reply_markup=mk.reset_polls(quiz.qst[quiz.current].tip)
                           )
    bot.send_poll(
        chat_id=chatId,
        type="quiz",
        question=quiz.qst[quiz.current].text,
        is_anonymous=False,
        options=answers,
        correct_option_id=correct_answer,
        allows_multiple_answers=False
    )


@bot.poll_answer_handler()
def handle_poll_answer(pollAnswer):
    chatId = pollAnswer.user.id
    # quiz[chatId]
    # print(quiz[chatId].qst[quiz[chatId].current].correct_answer)
    # print(pollAnswer)
    # print(pollAnswer.option_ids)
    # print(quiz[chatId].qst[quiz[chatId].current].correct_answer)
    if quiz[chatId].qst[quiz[chatId].current].correct_answer == pollAnswer.option_ids[0]:
        UserModel.quizCompleteCounter(chatId)
    try:
        next(quiz[chatId])
        send_polls(chatId, quiz[chatId])
    except:
        print("ЗАШЕЛ")
        user = UserModel.getUser(chatId)
        correct = user.quiz_current
        quiz_id = quiz_tr[chatId]
        rewards = QuizModel.check_rewards(quiz_id)
        check_remainder = QuizModel.check_remainder(quiz_id)
        if correct == quiz[chatId].length:
            if rewards:
                if check_remainder:
                    if not PrizeModel.checkReward(quiz_id, chatId):
                        code = QuizModel.reward_take(quiz_id)
                        bot.send_message(
                            chat_id=chatId,
                            text=mk.reward_take(code),
                            reply_markup=mk.backToQuiz()
                        )
                        QuizModel.reward_reduce(quiz_id)
                        Prize(quiz_id, chatId, True, code)
                        del quiz[chatId]
                        del quiz_tr[chatId]
                    elif not PrizeModel.get_can_collect(quiz_id, chatId):
                        bot.send_message(
                            chat_id=chatId,
                            text="Поздравляю! Ты правильно ответил на все вопросы, но не с первого раза",
                            reply_markup=mk.backToQuiz()
                        )
                        del quiz[chatId]
                        del quiz_tr[chatId]
                    else:
                        bot.send_message(
                            chat_id=chatId,
                            text=mk.collected_code_text(PrizeModel.get_collected_code(quiz_id, chatId)),
                            reply_markup=mk.backToQuiz()
                        )
                        del quiz[chatId]
                        del quiz_tr[chatId]
                else:
                    bot.send_message(
                        chat_id=chatId,
                        text="Ты ответил на все вопросы правильно, но, к сожалению, коды закончились:(",
                        reply_markup=mk.backToQuiz()
                    )
                    del quiz[chatId]
                    del quiz_tr[chatId]
            else:
                bot.send_message(
                    chat_id=chatId,
                    text="Ты ответил на все вопросы правильно!",
                    reply_markup=mk.backToQuiz()
                )
                del quiz[chatId]
                del quiz_tr[chatId]
        elif PrizeModel.checkReward(quiz_id, chatId):
            code = PrizeModel.get_collected_code(quiz_id, chatId)
            bot.send_message(
                chat_id=chatId,
                text=mk.already_collected_code_text(correct, quiz[chatId].length, code),
                reply_markup=mk.backToQuiz()
            )
        else:
            bot.send_message(
                chat_id=chatId,
                text=f"Вы правильно ответили на {correct} из {quiz[chatId].length}",
                reply_markup=mk.backToQuiz()
            )
            Prize(quiz_id, chatId, False, 0)
            del quiz[chatId]
            del quiz_tr[chatId]

bot.polling(non_stop=True)