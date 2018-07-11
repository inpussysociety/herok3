import telebot

import json

import functions as functions
#main variables
#TOKEN = "530182728:AAERfi7Kw6id4EmxDhR5bt9_RXKAlXra-Hw"
TOKEN = "465626881:AAERi-riKUStf-1so8lwyt9NQz0336J6pFo"
BOT = telebot.TeleBot(TOKEN)

# TASK

class Task:
    # take "i" from loops
    book_code = 0
    subject_code = 0
    # fill during chatting
    subject = 'name'
    author = ''
    task = 0
    # advanced params
    depth = 1
    unit = 0
    lesson = 0
    isLong = True
    # create a list
    output = []
    def buildTask(self):
        self.output = []
        self.output.append(self.subject)
        self.output.append(self.author)
        self.output.append(self.unit)
        self.output.append(self.lesson)
        self.output.append(self.task)
        self.output.append(self.depth)
        self.output.append(self.isLong)
        return self.output
#subject, author, unit, lesson, task, depth, isLong
TASK = Task()
# TASK
# ---------------------------------------------------------------
#ELECTION


#ELECTION


@BOT.message_handler(commands=['start'])
def start_handler(message):
    chat_id = message.chat.id
    text = message.text
    msg = BOT.send_message(chat_id, 'Предмет?')
    BOT.register_next_step_handler(msg, askSubject)

def askSubject(message):
    chat_id = message.chat.id
    subject = message.text
    subject_data = functions.check_subject(subject)
    if not subject_data[0]:
        msg = BOT.send_message(chat_id, 'Такого предмета нету, введи корректно.')
        BOT.register_next_step_handler(msg, askSubject)
        return

    TASK.subject_code = subject_data[2]
    TASK.subject = subject_data[1]
    TASK.author = subject_data[3]
    TASK.isLong = subject_data[4]
    depth = functions.analyze_book(TASK.subject_code)
    TASK.depth = depth
    if depth == 3:
        msg = BOT.send_message(chat_id, 'Раздел/Глава/Unit?')
        BOT.register_next_step_handler(msg, askUnit)
        return
    elif depth == 2:
        welcome_message_d2 = 'Глава/Упражнение?'
        msg = BOT.send_message(chat_id, welcome_message_d2)
        BOT.register_next_step_handler(msg, askLesson)
        return
    elif depth == 1:
        msg = BOT.send_message(chat_id, 'Номер/Задание?')
        BOT.register_next_step_handler(msg, askTask)
        return
    else:
        msg = BOT.send_message(chat_id, 'ERROR: depth is out of range')
        BOT.register_next_step_handler(msg, go)
        return

#def askUnit(message):

def askLesson(message):
	chat_id = message.chat.id
	lesson = message.text
	leson_data = functions.check_lesson(TASK.subject_code, TASK.unit, lesson)
	if not leson_data[0]:
		msg = BOT.send_message(chat_id, 'Такого Урока/Главы не существует. Введите корректно.')
		BOT.register_next_step_handler(msg, askLesson)
		return
	TASK.lesson = int(lesson) - 1
	msg = BOT.send_message(chat_id, 'Номер/Задание?')
	BOT.register_next_step_handler(msg, askTask)

def askTask(message):
    chat_id = message.chat.id
    task = message.text
    task_data = functions.check_task(TASK.subject_code, TASK.unit, TASK.lesson,
                                                                          task)
    #STUB, NEED TASKS AMOUNT OF EVERY BOOK
    if not task_data[0]:
        msg = BOT.send_message(chat_id, 'Такого задания нет. Введите задание корректно.')
        BOT.register_next_step_handler(msg, askTask)
        return
    TASK.task = int(task) #TASK
    msg = BOT.send_message(chat_id, 'Сейчас найду!')
    output = TASK.buildTask()
    print(output)
    imgLinksList = functions.getImgLinks(output[0], output[1], output[2],
                              output[3], output[4], output[5], output[6])
    for i in range(len(imgLinksList)):
        BOT.send_message(chat_id, imgLinksList[i])

@BOT.message_handler(content_types=['text'])
def text_hanlde(message):
    askSubject(message)


BOT.polling()
