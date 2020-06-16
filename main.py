import telebot
import time
from telebot import types#, apihelper
import xlsxwriter
from os import mkdir

from tinydb import TinyDB, Query
db = TinyDB('db.json')
dbID = TinyDB('dbID.json')
allUser = TinyDB('allUser.json')
articles = TinyDB('articles.json')


token = '1247109025:AAGF25oULgH_C3pANAjlwmx8PokmSRuEsbc' #подключение к боту

#apihelper.proxy = {'https': 'socks5://localhost:9050'}

bot = telebot.TeleBot(token)

admin =[514316978, 251272982]


#Обработка команд
@bot.message_handler(commands=['mes'])
def perform_rs(message):
	for i in admin:
		if message.chat.id == i:
			try:
				msaa = allUser.search(Query().mes != None)
				print(msaa)
				msaa = msaa[0]['mes']
				if msaa != "":
					allUser2=allUser.search(Query().chatId > 1)
					for i in allUser2:
						bot.send_message(i['chatId'], msaa)
					allUser.update({'mes': ""}, Query().mes == msaa)
				else:
					bot.send_message(message.chat.id, 'Не введено сообщение для рассылки')
			except IndexError:
				bot.send_message(message.chat.id, 'Произошла ошибка во время получения доступа к сообщению.')

@bot.message_handler(commands=['rs'])
def update_rs_command(message):
	for i in admin:
		if message.chat.id == i:
			allUser.update({'stAdmin': True}, Query().stAdmin == False)
			bot.send_message(message.chat.id, 'Введите сообщение')

@bot.message_handler(commands=['insert_article'])
def insert_article(message):
	text = message.text.split(';;')
	try:
		last_id = int(articles.all()[-1]['id'])
	except:
		last_id = 0

	articles.insert({'id':last_id + 1,
					'glava':text[1],
					'topic':text[2],
					'url':text[3],
					'text':text[4]})
	bot.send_message(message.chat.id, text[1] + text[2] + text[3])

@bot.message_handler(commands=['list'])
def send_table(message):
	for i in admin:
		if message.chat.id == i:
			workbook = xlsxwriter.Workbook('calc.xlsx')
			worksheet = workbook.add_worksheet()
			worksheet.write(0, 0, 'Ник в Телеграмм')
			worksheet.write(0, 1, 'Тип помещения')
			worksheet.write(0, 2, 'Площадь')

			worksheet.write(0, 3, 'Количество помещений')
			worksheet.write(0, 4, '3D-визуализация')

			worksheet.write(0, 5, 'Стиль')
			worksheet.write(0, 6, 'Телефон')
			list_user = db.search(Query().chatId > 1)
			for us in range(len(list_user)):

				worksheet.write(us+1, 0, list_user[us]['username'])
				worksheet.write(us+1, 1, list_user[us]['tipPomechenya'])
				worksheet.write(us+1, 2, list_user[us]['plochad'])
				worksheet.write(us+1, 3, list_user[us]['kolPomecheniy'])
				worksheet.write(us+1, 4, list_user[us]['viz'])
				worksheet.write(us+1, 5, list_user[us]['stil'])
				worksheet.write(us+1, 6, list_user[us]['conPhone'])

			workbook.close()

			workbook = xlsxwriter.Workbook('consult.xlsx')
			worksheet = workbook.add_worksheet()
			worksheet.write(0, 0, 'Ник в Телеграмм')
			worksheet.write(0, 1, 'Тип помещения')
			worksheet.write(0, 2, 'Площадь')
			worksheet.write(0, 3, 'Стиль')
			worksheet.write(0, 4, 'Доп. Информация')
			worksheet.write(0, 5, 'План')
			worksheet.write(0, 6, 'Фото')
			worksheet.write(0, 7, 'Телефон')

			list_user = db.search(Query().chatId > 1)
			for us in range(len(list_user)):

				worksheet.write(us+1, 0, list_user[us]['username'])
				worksheet.write(us+1, 1, list_user[us]['conType'])
				worksheet.write(us+1, 2, list_user[us]['conPloch'])
				worksheet.write(us+1, 3, list_user[us]['conStyle'])
				worksheet.write(us+1, 4, list_user[us]['conExtra'])
				worksheet.insert_image(us+1, 5, list_user[us]['conPlan'], {'x_scale': 0.2, 'y_scale': 0.2})
				worksheet.insert_image(us+1, 6, list_user[us]['conPhoto'], {'x_scale': 0.2, 'y_scale': 0.2})
				worksheet.write(us+1, 7, list_user[us]['conPhone'])
				
			workbook.close()

			doc = open('calc.xlsx', 'rb')
			bot.send_document(message.chat.id, doc)

			doc = open('consult.xlsx', 'rb')
			bot.send_document(message.chat.id, doc)



#Обработка команд
@bot.message_handler(commands=['start'])
def start(message):
	dbs=db.search(Query().chatId == message.chat.id)
	if dbs==[]:
		allUser.insert({'chatId': message.chat.id})
		idUse = dbID.search(Query().idUser > 1)
		idUse = idUse[0]['idUser']
		db.insert({
		'username': message.chat.username,
		'chatId': message.chat.id,
		'prev_click': 'menu',
		'idUser': idUse,
		'status_testa': '0',
		'tipPomechenya': '0',
		'plochad': '0',
		'kolPomecheniy': '0',
		'viz': '0',
		'stil': '0',
		'conType': '0',
		'conPloch': '0',
		'conStyle': '0',
		'conExtra': '0',
		'conPlan': '0',
		'conPhoto': '0',
		'conPhone': '0',
		'conStage': '0'
		})

		dbID.update({'idUser': idUse+1}, Query().idUser == idUse)
	else:
		db.update({'status_testa': 0}, Query().chatId == message.chat.id)

	markup = types.InlineKeyboardMarkup()
	kb1 = types.InlineKeyboardButton(text="Начать", callback_data="menu")
	markup.add(kb1)
	bot.send_message(message.chat.id, '''Вітаю! Я чат-бот DV-design.
Я розповім Вам багато цікавого, якщо Ви почнете діалог''', reply_markup=markup)



#обработка сообще
@bot.callback_query_handler(func=lambda c:True)
def ans(c):

	cid = c.message.chat.id
	dbs=db.search(Query().chatId == c.message.chat.id)
	space_type = dbs[0]['tipPomechenya']
	prev_click = dbs[0]['prev_click']
	dbs = dbs[0]['status_testa']
	bot.send_chat_action(c.message.chat.id, action = "typing")
	print(prev_click)
	#time.sleep(1)


	if c.data == 'menu':
		db.update({'status_testa': 0}, Query().chatId == c.message.chat.id)
		
		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="Про компанію", callback_data="about")
		kb2 = types.InlineKeyboardButton(text="Онлайн розрахунок вартості ремонту", callback_data="calculator")
		kb3 = types.InlineKeyboardButton(text="Первинна консультация керівника студії ", callback_data="consult")
		markup.add(kb1, kb2)
		markup.add(kb3)
		try:
			bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Що вас цікавить?")
			bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)
		except telebot.apihelper.ApiException:
			bot.send_message(chat_id=c.message.chat.id, text="Що вас цікавить?", reply_markup = markup)
		db.update({'prev_click': c.data}, Query().chatId == c.message.chat.id)

	if c.data == 'about':
		db.update({'status_testa': 0}, Query().chatId == c.message.chat.id)
		
		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="Про студію", callback_data="about_studio")
		kb2 = types.InlineKeyboardButton(text="Послуги", callback_data="services")
		kb3 = types.InlineKeyboardButton(text="Портфоліо", callback_data="portfolio")
		kb4 = types.InlineKeyboardButton(text="Блог", callback_data="blog")
		kb5 = types.InlineKeyboardButton(text="Контакти", callback_data="contact")
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		back = types.InlineKeyboardButton(text="Назад", callback_data=str(prev_click))
		markup.add(kb1, kb2)
		markup.add(kb3, kb4)
		markup.add(kb5)
		markup.add(back, menu)
		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Познакомьтесь ближе с нашей компанией!")
		bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)
		db.update({'prev_click': c.data}, Query().chatId == c.message.chat.id)

	if c.data == 'about_studio': #О студии
		
		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="Сайт", url='dvdesign.com.ua')
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		back = types.InlineKeyboardButton(text="Назад", callback_data='about')
		markup.add(kb1)
		markup.add(back, menu)
		bot.send_photo(c.message.chat.id, open('img/logo.jpg', 'rb'), 
			caption = '''Студія дизайну та проектування    DV design.
		Власник студії: Дєдов  Володимир Іванович''')
		bot.send_message(c.message.chat.id, reply_markup=markup, text = '''Народився  15 травня 1986 року в місті Чернівці.  З дитинства  цікавився образотворчим  мистецтвом, закінчив художню школу з відзнакою. В 2005 році закінчив Чернівецький політехнічний технікум за  фахом « Архітектура  будівель і споруд». В наступному в 2009 році отримав ступінь магістра архітектури у Львівському Національному аграрному університеті. З  2009 року заснував свою приватну практику архітектора та дизайнера інтер’єрів.    У 2015 році прийняв участь у конкурсі на посаду головного архітектора міста Чернівці.
		За 14 років своєї діяльності було розроблено:
		дизайн-проекти квартир, заміських приватних будинків, проектування малоповерхового індивідуального житла, громадських, учбових і спортивних будівель  та споруд, дизайн-оформлення торговельних  павільйонів  у  великих торговельних центрах.
		Приймав участь у розробці таких великих проектів  як:  житловий мікрорайон, бази відпочинку, санаторії-профілакторії, церква. Також займався проектуванням багатоповерхових та малоповерхових  житлових будинків, котеджів, таунхаусів, розробкою проектів ресторанного бізнесу. Створював малі архітектурні форми, благоустрій  паркового мистецтва, ландшафтний дизайн, функціональне обладнання та меблі для авторських об’єктів .''')
		db.update({'prev_click': c.data}, Query().chatId == c.message.chat.id)

	if c.data == 'services':
		
		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="Дизайн фасаду", callback_data="service1")
		kb2 = types.InlineKeyboardButton(text="Дизайн інтерєру", callback_data="service2")
		kb3 = types.InlineKeyboardButton(text="Ландшафтний дизайн та благоустрій", callback_data="service3")
		kb4 = types.InlineKeyboardButton(text="Архітектурне проектування", callback_data="service4")
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		back = types.InlineKeyboardButton(text="Назад", callback_data='about')
		#db.update({'status_testa': 'usligi'}, Query().chatId == c.message.chat.id)
		markup.add(kb1, kb2)
		markup.add(kb3, kb4)
		markup.add(back, menu)
		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Які послуги вас цікавлять?")
		bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)
		db.update({'prev_click': c.data}, Query().chatId == c.message.chat.id)

	if c.data == 'portfolio':
		
		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="Дизайн інтерєру", callback_data="portfolio1")
		kb2 = types.InlineKeyboardButton(text="Дизайн фасаду", callback_data="portfolio2")
		kb3 = types.InlineKeyboardButton(text="Архітектурне проектування", callback_data="arhit")
		kb4 = types.InlineKeyboardButton(text="Ландшафтний дизайн та благоустрій", callback_data="land")
		kb5 = types.InlineKeyboardButton(text="Планувальні рішення", callback_data="plan") #translate below
		kb6 = types.InlineKeyboardButton(text="Дизайн в ресторану/кафе", callback_data="rest")
		kb7 = types.InlineKeyboardButton(text="Дизайн в Б'юті-індустрії", callback_data="beauty")
		kb8 = types.InlineKeyboardButton(text="Дизайн лiкувальнiх установ", callback_data="med")
		back = types.InlineKeyboardButton(text="Назад", callback_data='about')
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		
		markup.add(kb1,kb2)
		markup.add(kb3,kb4)
		markup.add(kb5,kb6)
		markup.add(kb7,kb8)
		markup.add(back,menu)
		try:
			bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Що вас цікавить?")
			bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)
		except telebot.apihelper.ApiException:
			bot.send_message(chat_id=c.message.chat.id, text="Що вас цікавить?", reply_markup = markup)
		db.update({'prev_click': c.data}, Query().chatId == c.message.chat.id)

	if c.data == 'blog':
		
		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="Поради по плануванню", callback_data="blogGlava1")
		kb2 = types.InlineKeyboardButton(text="Поради по ремонту", callback_data="blogGlava2")
		kb3 = types.InlineKeyboardButton(text="Правильне використання кольорів", callback_data="blogGlava3")
		kb4 = types.InlineKeyboardButton(text="Матеріали у дизайні", callback_data="blogGlava4")
		back = types.InlineKeyboardButton(text="Назад", callback_data='about')
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		#db.update({'status_testa': 'usligi'}, Query().chatId == c.message.chat.id)
		markup.add(kb1, kb2)
		markup.add(kb3, kb4)
		markup.add(back, menu)
		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Які послуги вас цікавлять?")
		bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)
		db.update({'prev_click': c.data}, Query().chatId == c.message.chat.id)

	if c.data == 'contact':
		db.update({'status_testa': 'conPhone'}, Query().chatId == c.message.chat.id)
		
		markup = types.InlineKeyboardMarkup()
		#kb1 = types.InlineKeyboardButton(text="Контакты", url='fb.com')
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		back = types.InlineKeyboardButton(text="Назад", callback_data=prev_click)
		markup.add(back, menu)
		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, 
			text='''Вкажіть свій номер телефону ми з Вами зв’яжемся  або зателефонуйте нам: 
		+380986655501  
		+380506680371   
		d-vdesign@ukr.net''')
		bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)
		db.update({'prev_click': c.data}, Query().chatId == c.message.chat.id)

#______________________________________________________________________________________________________________
#blog zone

	if 'blogGlava' in c.data:
		markup = types.InlineKeyboardMarkup()
		button_list = []
		for article in articles.search(Query().glava == c.data):
			button_list.append(types.InlineKeyboardButton(text=article['topic'], callback_data='article' + str(article['id'])))

		back = types.InlineKeyboardButton(text="Назад", callback_data='blog')
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		for i in range(0,len(button_list),2):
			markup.add(*button_list[i:i+2])
		markup.add(back, menu)
		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text='''Виберете цікаву для вас статтю''')
		bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)

	if 'article' in c.data:
		markup = types.InlineKeyboardMarkup()
		l_article = articles.search(Query().id == int(c.data[-1]))[0]
		back = types.InlineKeyboardButton(text="Назад", callback_data=l_article['glava'])
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		markup.add(back, menu)
		text = l_article['text'] + '\n\n*Читати далі:* '+ l_article['url']
		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text=text, parse_mode='markdown')
		bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)


#______________________________________________________________________________________________________________
#portfolio zone

	if c.data == 'portfolio1': #interior
		
		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="Класика", callback_data="interior/classic")
		kb2 = types.InlineKeyboardButton(text="Мінімалізм", callback_data="interior/min")
		kb3 = types.InlineKeyboardButton(text="Лофт", callback_data="interior/loft")
		kb4 = types.InlineKeyboardButton(text="Інший", callback_data="interior/other")
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		back = types.InlineKeyboardButton(text="Назад", callback_data='portfolio')
		markup.add(kb1, kb2)
		markup.add(kb3, kb4)
		markup.add(back, menu)

		try:
			bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Що вас цікавить?")
			bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)
		except telebot.apihelper.ApiException:
			bot.send_message(chat_id=c.message.chat.id, text="Що вас цікавить?", reply_markup = markup)
		db.update({'prev_click': c.data}, Query().chatId == c.message.chat.id)


	if c.data == 'portfolio2': #fasad
		
		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="Мінімалізм", callback_data="fasad/min")
		kb2 = types.InlineKeyboardButton(text="Неокласика", callback_data="fasad/neo")
		kb3 = types.InlineKeyboardButton(text="Барнхаус", callback_data="fasad/barn")
		kb4 = types.InlineKeyboardButton(text="Сицесія", callback_data="fasad/sic")
		kb5 = types.InlineKeyboardButton(text="Інший", callback_data="fasad/other")
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		back = types.InlineKeyboardButton(text="Назад", callback_data='portfolio')
		markup.add(kb1, kb2)
		markup.add(kb3, kb4)
		markup.add(kb5)
		markup.add(back, menu)

		try:
			bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Що вас цікавить?")
			bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)
		except telebot.apihelper.ApiException:
			bot.send_message(chat_id=c.message.chat.id, text="Що вас цікавить?", reply_markup = markup)
		db.update({'prev_click': c.data}, Query().chatId == c.message.chat.id)

	list_of_portfolio = ["arhit", "land", "plan", "rest", "beauty", "med"]

	if 'interior' in c.data or 'fasad' in c.data or c.data in list_of_portfolio:
		
		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="Більше робіт на сайті", url='dvdesign.com.ua')
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		back = types.InlineKeyboardButton(text="Назад", callback_data=prev_click)
		markup.add(kb1)
		markup.add(back, menu)

		for i in range(0,4):
			address = 'img/portfolio/' + c.data + '/' + str(i) + '.jpg'
			try:
				if i < 3:
					with open(address, 'rb') as photo:
						bot.send_photo(chat_id=c.message.chat.id, photo = photo)
				if i == 3:
					with open(address, 'rb') as photo:
						bot.send_photo(chat_id=c.message.chat.id, photo = photo, caption = "Приклади наших робіт", reply_markup = markup)
			except FileNotFoundError:
				print('photo not found')
				#bot.send_message(chat_id=c.message.chat.id, text="Photo " + address + " not found")

		#db.update({'prev_click': c.data}, Query().chatId == c.message.chat.id)

		

#______________________________________________________________________________________________________________
#services zone

	if c.data == 'service1':
		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="Портфоліо", callback_data="portfolio1")
		kb2 = types.InlineKeyboardButton(text="Отримати первинну консультацію", callback_data="consult")
		kb3 = types.InlineKeyboardButton(text="Розрахувати орiєнтовну вартість дизайн проекту", callback_data="calculator")
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		back = types.InlineKeyboardButton(text="Назад", callback_data=prev_click)
		markup.add(kb1, kb2)
		markup.add(kb3)
		markup.add(back, menu)

		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Дизайн фасаду. Ось що ми можемо Вам запропонувати:")
		bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)
		db.update({'prev_click': c.data}, Query().chatId == c.message.chat.id)

	if c.data == 'service2':
		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="Портфоліо", callback_data="portfolio2")
		kb2 = types.InlineKeyboardButton(text="Отримати первинну консультацію", callback_data="consult")
		kb3 = types.InlineKeyboardButton(text="Розрахувати орiєнтовну вартість дизайн проекту", callback_data="calculator")
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		back = types.InlineKeyboardButton(text="Назад", callback_data=prev_click)
		markup.add(kb1, kb2)
		markup.add(kb3)
		markup.add(back, menu)

		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Дизайн інтер'єру. Ось що ми можемо Вам запропонувати:")
		bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)
		db.update({'prev_click': c.data}, Query().chatId == c.message.chat.id)

	if c.data == 'service3':
		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="Портфоліо", callback_data="portfolio2")
		kb2 = types.InlineKeyboardButton(text="Отримати первинну консультацію", callback_data="consult")
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		back = types.InlineKeyboardButton(text="Назад", callback_data=prev_click)
		markup.add(kb1, kb2)
		markup.add(back, menu)
		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Ландшафтний дизайн та благоустрій. Ось що ми можемо Вам запропонувати:")
		bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)
		db.update({'prev_click': c.data}, Query().chatId == c.message.chat.id)

	if c.data == 'service4':
		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="Портфоліо", callback_data="portfolio2")
		kb2 = types.InlineKeyboardButton(text="Отримати первинну консультацію", callback_data="consult")
		kb3 = types.InlineKeyboardButton(text="Розрахувати орiєнтовну вартість дизайн проекту", callback_data="calculator")
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		back = types.InlineKeyboardButton(text="Назад", callback_data=prev_click)
		markup.add(kb1, kb2)
		markup.add(kb3)
		markup.add(back, menu)

		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Архітектурне проектування. Ось що ми можемо Вам запропонувати:")
		bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)
		db.update({'prev_click': c.data}, Query().chatId == c.message.chat.id)

#______________________________________________________________________________________________________________
#calculator

	if c.data == 'calculator':
		db.update({'status_testa': 1}, Query().chatId == c.message.chat.id)

		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="Житлове приміщення", callback_data="calc1")
		kb2 = types.InlineKeyboardButton(text="Громадське приміщення", callback_data="calc2")
		kb3 = types.InlineKeyboardButton(text="Дизайн фасаду", callback_data="contact")
		kb4 = types.InlineKeyboardButton(text="Ландшафтний дизайн та благоустрій", callback_data="contact")
		kb5 = types.InlineKeyboardButton(text="Планувальне рішення", callback_data="calc3")
		kb6 = types.InlineKeyboardButton(text="інше", callback_data="contact")
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		markup.add(kb1, kb2)
		markup.add(kb3, kb4)
		markup.add(kb5, kb6)
		markup.add(menu)
		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Виберіть тип приміщення")
		bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)


	if dbs == 1:
		if c.data == 'calc1' or c.data == 'calc2' or c.data == 'calc3':
			db.update({'status_testa': 2}, Query().chatId == c.message.chat.id)
			tipPomechenya = ''
			if c.data == 'calc1':
				tipPomechenya = 'Житлове приміщення'
			elif c.data == 'calc2':
				tipPomechenya = 'Громадське приміщення'
			elif c.data == 'calc3':
				tipPomechenya = 'Лише планувальне рішення'
			db.update({'tipPomechenya': tipPomechenya}, Query().chatId == c.message.chat.id)

			#markup = types.InlineKeyboardMarkup()
			bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Вкажіть площу приміщення:")
			#bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)


	if dbs == 3:

		db.update({'kolPomecheniy': c.data}, Query().chatId == c.message.chat.id)
		db.update({'status_testa': 'vizualiz'}, Query().chatId == c.message.chat.id)

		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="Так", callback_data="viz_yes")
		kb2 = types.InlineKeyboardButton(text="Нi", callback_data="viz_no")
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		markup.add(kb1, kb2)
		markup.add(menu)

		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Необхідна 3Д-візуалізація?")
		bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)

	if dbs == 'vizualiz':
		if c.data == 'viz_yes':
			markup = types.InlineKeyboardMarkup()
			kb1 = types.InlineKeyboardButton(text="Всіх приміщень", callback_data="viz_all")
			kb2 = types.InlineKeyboardButton(text="Вибірково", callback_data="viz_some")
			menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
			markup.add(kb1, kb2)
			markup.add(menu)
			bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Необхідна 3D-візуалізація всіх приміщень або вибірково?")
			bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)

		if c.data == 'viz_all':
			db.update({'status_testa': 4}, Query().chatId == c.message.chat.id)
			db.update({'viz': c.message.text}, Query().chatId == c.message.chat.id)

			markup = types.InlineKeyboardMarkup()
			kb1 = types.InlineKeyboardButton(text="Класика", callback_data="Класика")
			kb2 = types.InlineKeyboardButton(text="Мінімалізм", callback_data="Мінімалізм")
			kb3 = types.InlineKeyboardButton(text="Лофт", callback_data="Лофт")
			kb4 = types.InlineKeyboardButton(text="Iнший", callback_data="Iнший")
			menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
			markup.add(kb1, kb2)
			markup.add(kb3, kb4)
			markup.add(menu)
			bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Оберіть стиль, який бажаєте бачити")
			bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)

		if c.data == 'viz_some':
			db.update({'status_testa': 'conPhone'}, Query().chatId == c.message.chat.id)

			markup = types.InlineKeyboardMarkup()
			menu = types.InlineKeyboardButton(text="Контакти", callback_data="contact")
			markup.add(menu)
			bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, 
				text='''Необхідний індивідуальний розрахунок
				Вкажіть свій номер телефону ми з Вами зв’яжемся  або зателефонуйте нам
					Первинна консультація – наше з Вами перше знайомство та основа майбутньої співпраці. 
					Для Вас це можливість зрозуміти – чим я можу Вам допомогти. 
					Первинна консультація включає в себе :
					-	Повний аудит з питань планування чи перепланування 
					-	Функції та ергономіки приміщень 
					-	Визначення об’ємного просторового рішення 
					-	Оптимізація бюджету замовника для вирішення його побажань 
					-	Консультація суміжних питань будівництва та декорування 
				''')
			bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)


		if c.data == 'viz_no':
			metr=db.search(Query().chatId == c.message.chat.id)

			metr=metr[0]['plochad']

			if int(metr) < 50:
				db.update({'status_testa': 'conPhone'}, Query().chatId == c.message.chat.id)

				markup = types.InlineKeyboardMarkup()
				kb1 = types.InlineKeyboardButton(text="Отримати розрахунок!", callback_data="contact")
				kb2 = types.InlineKeyboardButton(text="Ні дякую!", callback_data="menu")
				menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
				markup.add(kb1, kb2)
				markup.add(menu)
				bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, 
					text="Приблизна вартість Вашого проекту може становити 100 $." + '''
				Вкажіть свій номер телефону ми з Вами зв’яжемся  або зателефонуйте нам 
					В цю вартість буде входити :
					-Планування приміщень
					-Перепланування перепланування приміщень
					-План- схема розміщення обладнання і меблів (проектований)
					-План демонтажу перегородок (при необхідності)
					''')
				bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)

			if int(metr) >= 50:
				db.update({'status_testa': 'conPhone'}, Query().chatId == c.message.chat.id)

				markup = types.InlineKeyboardMarkup()
				kb1 = types.InlineKeyboardButton(text="Отримати розрахунок!", callback_data="contact")
				kb2 = types.InlineKeyboardButton(text="Ні дякую!", callback_data="menu")
				menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
				markup.add(kb1, kb2)
				markup.add(menu)
				bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, 
					text='Приблизна вартість Вашого проекту може становити ' + str(int(metr)*2) + '''$. 
					В цю вартість буде входити :
					-Планування приміщень
					-Перепланування перепланування приміщень
					-План- схема розміщення обладнання і меблів (проектований)
					-План демонтажу перегородок (при необхідності)
				Вкажіть свій номер телефону ми з Вами зв’яжемся  або зателефонуйте нам
					''')
				bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)

	if dbs == 4:
		db.update({'status_testa': 'conPhone'}, Query().chatId == c.message.chat.id)
		db.update({'stil': c.message.text}, Query().chatId == c.message.chat.id)

		metr=db.search(Query().chatId == c.message.chat.id)
		metr=metr[0]['plochad']

		if int(metr) <= 40:

			markup = types.InlineKeyboardMarkup()
			kb1 = types.InlineKeyboardButton(text="Отримати розрахунок!", callback_data="contact")
			kb2 = types.InlineKeyboardButton(text="Ні дякую!", callback_data="menu")
			menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
			markup.add(kb1, kb2)
			markup.add(menu)
			bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, 
				text='Приблизна вартість Вашого проекту може становити ' + str(int(metr)*20) + '''$. 
				В цю вартість буде входити :
				-  План обмірних креслень (існуючий стан)
				-  План-схема розміщення обладнання і меблів (проектований)
				-  План перепланування
				-  План демонтажу перегородок
				-  План монтажу проектованих перегородок
				-  План – схема розміщення теплої підлоги
				-  План-схема підключення сантехнічних приладів
				-  План схема освітлення з вимикачами та прив’язками
				-  План схема розташування розеток
				-  План схема підлоги з позначенням типу покриття
				-  План схема стелі з  розрізами та січеннями
				-  Візуалізація всіх приміщень (3-4 ракурси кожного приміщення)
				Для розрахунку точноі вартості потрібна особиста первинна консультація.
			Вкажіть свій номер телефону ми з Вами зв’яжемся  або зателефонуйте нам
				''')
			bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)

		if int(metr) > 40:

			markup = types.InlineKeyboardMarkup()
			kb1 = types.InlineKeyboardButton(text="Отримати розрахунок!", callback_data="contact")
			kb2 = types.InlineKeyboardButton(text="Ні дякую!", callback_data="menu")
			menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
			markup.add(kb1, kb2)
			markup.add(menu)
			bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, 
				text='Приблизна вартість Вашого проекту може становити ' + str(int(metr)*15) + '''$. 
				В цю вартість буде входити :
				-  План обмірних креслень (існуючий стан)
				-  План-схема розміщення обладнання і меблів (проектований)
				-  План перепланування
				-  План демонтажу перегородок
				-  План монтажу проектованих перегородок
				-  План – схема розміщення теплої підлоги
				-  План-схема підключення сантехнічних приладів
				-  План схема освітлення з вимикачами та прив’язками
				-  План схема розташування розеток
				-  План схема підлоги з позначенням типу покриття
				-  План схема стелі з  розрізами та січеннями
				-  Візуалізація всіх приміщень (3-4 ракурси кожного приміщення)
				Для розрахунку точноі вартості потрібна особиста первинна консультація.
				''')
			bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)

#______________________________________________________________________________________________________________
# Consult

	if c.data == 'consult':
		
		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="Житловий об'єкт", callback_data="consult1")
		kb2 = types.InlineKeyboardButton(text="Громадський об'єкт", callback_data="consult2")
		kb3 = types.InlineKeyboardButton(text="Будівілі і споруди", callback_data="contact")
		kb4 = types.InlineKeyboardButton(text="Ландшафт і благоустрій", callback_data="contact")
		kb5 = types.InlineKeyboardButton(text="Iнше", callback_data="contact")
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		#db.update({'status_testa': 'usligi'}, Query().chatId == c.message.chat.id)
		markup.add(kb1, kb2)
		markup.add(kb3, kb4)
		markup.add(kb5)
		markup.add(menu)
		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Виберіть тип об'єкта")
		bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)
		db.update({'prev_click': c.data}, Query().chatId == c.message.chat.id)

	if c.data == 'consult1':
		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="Квартира", callback_data="flat")
		kb2 = types.InlineKeyboardButton(text="Будинок", callback_data="house")
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		back = types.InlineKeyboardButton(text="Назад", callback_data=prev_click)
		markup.add(kb1, kb2)
		markup.add(back, menu)
		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Виберіть тип об'єкта")
		bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)

#flat

	if c.data == 'flat':
		db.update({'conType': 'Квартира'}, Query().chatId == c.message.chat.id)
		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="Меньше 40м2", callback_data="flatSize1")
		kb2 = types.InlineKeyboardButton(text="40-60м2", callback_data="flatSize2")
		kb3= types.InlineKeyboardButton(text="60-100м2", callback_data="flatSize3")
		kb4 = types.InlineKeyboardButton(text="Вище 100м2", callback_data="FlatSize4")
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		markup.add(kb1, kb2)
		markup.add(kb3, kb4)
		markup.add(menu)
		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Оберіть площу квартири")
		bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)

	if 'flatSize' in c.data:
		if c.data == 'flatSize1':
			db.update({'conPloch': 'Меньше 40м2'}, Query().chatId == c.message.chat.id)
		elif c.data == 'flatSize2':
			db.update({'conPloch': '40-60м2'}, Query().chatId == c.message.chat.id)
		elif c.data == 'flatSize3':
			db.update({'conPloch': '60-100м2'}, Query().chatId == c.message.chat.id)
		elif c.data == 'flatSize4':
			db.update({'conPloch': 'Вище 100м2'}, Query().chatId == c.message.chat.id)

		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="Класика", callback_data="flatStyle1")
		kb2 = types.InlineKeyboardButton(text="Мінімалізм", callback_data="flatStyle2")
		kb3= types.InlineKeyboardButton(text="Лофт", callback_data="flatStyle3")
		kb4 = types.InlineKeyboardButton(text="Інший", callback_data="flatStyle4")
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		markup.add(kb1, kb2)
		markup.add(kb3, kb4)
		markup.add(menu)
		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Оберіть стиль:")
		bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)

	if 'flatStyle' in c.data:
		if c.data == 'flatStyle1':
			db.update({'conStyle': 'Класика'}, Query().chatId == c.message.chat.id)
		elif c.data == 'flatStyle2':
			db.update({'conStyle': 'Мінімалізм'}, Query().chatId == c.message.chat.id)
		elif c.data == 'flatStyle3':
			db.update({'conStyle': 'Лофт'}, Query().chatId == c.message.chat.id)
		elif c.data == 'flatStyle4':
			db.update({'conStyle': 'Інший'}, Query().chatId == c.message.chat.id)

		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="Потрібна", callback_data="flatViz1")
		kb2 = types.InlineKeyboardButton(text="Не потрібна", callback_data="flatViz2")
		kb3= types.InlineKeyboardButton(text="Вибірково", callback_data="flatViz3")
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		markup.add(kb1, kb2)
		markup.add(kb3)
		markup.add(menu)
		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Чи потрібна Вам візуалізація?")
		bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)

	if 'flatViz' in c.data:
		if c.data == 'flatViz':
			db.update({'conExtra': 'Потрібна візуалізація'}, Query().chatId == c.message.chat.id)
		elif c.data == 'flatViz2':
			db.update({'conExtra': 'Не потрібна візуалізація'}, Query().chatId == c.message.chat.id)
		elif c.data == 'flatViz3':
			db.update({'conExtra': 'Потрібна вибіркова візуалізація'}, Query().chatId == c.message.chat.id)

		db.update({'status_testa': 'conPlan'}, Query().chatId == c.message.chat.id)

		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="У мене немає плану", callback_data="flatNoPlan")
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		markup.add(kb1)
		markup.add(menu)
		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Для детальної консультації додайте, будьласка, план квартири (натисність на скріпку в лівому нижньому куточку щоб обрати фото)")
		bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)

	if c.data == 'flatNoPlan':
		db.update({'status_testa': 'conPhoto'}, Query().chatId == c.message.chat.id)

		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="У мене немає фото", callback_data="flatNoPhoto")
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		markup.add(kb1)
		markup.add(menu)
		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Додайте, будьласка, фото існуючого приміщення (натисність на скріпку в лівому нижньому куточку щоб обрати фото)")
		bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)

	if c.data == 'flatNoPhoto':
		db.update({'status_testa': 'conPhone'}, Query().chatId == c.message.chat.id)

		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="Контакти", callback_data="contact")
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		markup.add(kb1)
		markup.add(menu)
		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, 
			text="Зателефонуйте нам прямо зараз або напишіть свій номер телефону і ми передзвонимо найближчим часом"+'''
				Первинна консультація – наше з Вами перше знайомство та основа майбутньої співпраці. 
				Для Вас це можливість зрозуміти – чим я можу Вам допомогти. 
				Первинна консультація включає в себе :
				-	Повний аудит з питань планування чи перепланування 
				-	Функції та ергономіки приміщень 
				-	Визначення об’ємного просторового рішення 
				-	Оптимізація бюджету замовника для вирішення його побажань 
				-	Консультація суміжних питань будівництва та декорування 
			''',)
		bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)

#house

	if c.data == 'house':
		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="Таунхус", callback_data="houseType1")
		kb2 = types.InlineKeyboardButton(text="Коттедж", callback_data="houseType2")
		kb3= types.InlineKeyboardButton(text="Приватний будинок", callback_data="houseType3")
		kb4 = types.InlineKeyboardButton(text="Хочемо побудувати", callback_data="houseType4")
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		markup.add(kb1, kb2)
		markup.add(kb3, kb4)
		markup.add(menu)
		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Який у Вас тип будинку?")
		bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)

	if 'houseType' in c.data:
		if c.data == 'houseType1':
			db.update({'conType': 'Будинок: Таунхус'}, Query().chatId == c.message.chat.id)
		elif c.data == 'houseType2':
			db.update({'conType': 'Будинок: Коттедж'}, Query().chatId == c.message.chat.id)
		elif c.data == 'houseType3':
			db.update({'conType': 'Будинок: Приватний будинок'}, Query().chatId == c.message.chat.id)
		elif c.data == 'houseType4':
			db.update({'conType': 'Будинок: Хочемо побудувати'}, Query().chatId == c.message.chat.id)

		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="Iнтер’єр", callback_data="houseExtra1")
		kb2 = types.InlineKeyboardButton(text="Фасад", callback_data="houseExtra2")
		kb3= types.InlineKeyboardButton(text="Iнтер’єр фасад і благоустрій", callback_data="houseExtra3")
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		markup.add(kb1, kb2)
		markup.add(kb3)
		markup.add(menu)
		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="💚Оберіть вид проекту")
		bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)

	if 'houseExtra' in c.data:
		if c.data == 'houseExtra1':
			db.update({'conExtra': 'Вид проекту: Iнтер’єр'}, Query().chatId == c.message.chat.id)
		elif c.data == 'houseExtra2':
			db.update({'conExtra': 'Вид проекту: Фасад'}, Query().chatId == c.message.chat.id)
		elif c.data == 'houseExtra3':
			db.update({'conExtra': 'Вид проекту: Iнтер’єр фасад і благоустрій'}, Query().chatId == c.message.chat.id)

		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="Класика", callback_data="houseStyle1")
		kb2 = types.InlineKeyboardButton(text="Мінімалізм", callback_data="houseStyle2")
		kb3= types.InlineKeyboardButton(text="Лофт", callback_data="houseStyle3")
		kb4 = types.InlineKeyboardButton(text="Інший", callback_data="houseStyle4")
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		markup.add(kb1, kb2)
		markup.add(kb3)
		markup.add(menu)
		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Якому стилю віддаєте перевагу?")
		bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)

	if 'houseStyle' in c.data:
		if c.data == 'houseStyle1':
			db.update({'conStyle': 'Класика'}, Query().chatId == c.message.chat.id)
		elif c.data == 'houseStyle2':
			db.update({'conStyle': 'Мінімалізм'}, Query().chatId == c.message.chat.id)
		elif c.data == 'houseStyle3':
			db.update({'conStyle': 'Лофт'}, Query().chatId == c.message.chat.id)
		elif c.data == 'houseStyle4':
			db.update({'conStyle': 'Інший'}, Query().chatId == c.message.chat.id)

		db.update({'status_testa': 'conPlan'}, Query().chatId == c.message.chat.id)

		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="У мене немає плану", callback_data="houseNoPlan")
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		markup.add(kb1)
		markup.add(menu)
		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Додайте, будьласка, фото плану існуючого приміщення (натисність на скріпку в лівому нижньому куточку щоб обрати фото)")
		bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)

	if c.data == 'houseNoPlan':
		db.update({'status_testa': 'conPhoto'}, Query().chatId == c.message.chat.id)

		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="У мене немає фото", callback_data="houseNoPhoto")
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		markup.add(kb1)
		markup.add(menu)
		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Додайте, будьласка, фото існуючого стану будинку чи ділянки (натисність на скріпку в лівому нижньому куточку щоб обрати фото)")
		bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)

	if c.data == 'houseNoPhoto':
		db.update({'status_testa': 'conPhone'}, Query().chatId == c.message.chat.id)

		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="Контакти", callback_data="contact")
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		markup.add(kb1)
		markup.add(menu)
		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, 
			text="Зателефонуйте нам прямо зараз або напишіть свій номер телефону і ми передзвонимо найближчим часом"+'''
				Первинна консультація – наше з Вами перше знайомство та основа майбутньої співпраці. 
				Для Вас це можливість зрозуміти – чим я можу Вам допомогти. 
				Первинна консультація включає в себе :
				-	Повний аудит з питань планування чи перепланування 
				-	Функції та ергономіки приміщень 
				-	Визначення об’ємного просторового рішення 
				-	Оптимізація бюджету замовника для вирішення його побажань 
				-	Консультація суміжних питань будівництва та декорування 
			''',)
		bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)

#business
	if c.data == 'consult2':
		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="Ресторан/кафе", callback_data="bizType1")
		kb2 = types.InlineKeyboardButton(text="Офіс", callback_data="bizType2")
		kb3= types.InlineKeyboardButton(text="Бюті індустрія", callback_data="bizType3")
		kb4 = types.InlineKeyboardButton(text="Інше", callback_data="bizType4")
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		back = types.InlineKeyboardButton(text="Назад", callback_data=prev_click)
		markup.add(kb1, kb2)
		markup.add(kb3, kb4)
		markup.add(back, menu)
		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Який тип об єкту Вас цікавить?")
		bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)

	if 'bizType' in c.data:
		if c.data == 'bizType1':
			db.update({'conType': 'Громадський: Ресторан/кафе'}, Query().chatId == c.message.chat.id)
		elif c.data == 'bizType2':
			db.update({'conType': 'Громадський: Офіс'}, Query().chatId == c.message.chat.id)
		elif c.data == 'bizType3':
			db.update({'conType': 'Громадський: Бюті індустрія'}, Query().chatId == c.message.chat.id)
		elif c.data == 'bizType4':
			db.update({'conType': 'Громадський: Інше'}, Query().chatId == c.message.chat.id)

		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="Меньше 40м2", callback_data="bizSize1")
		kb2 = types.InlineKeyboardButton(text="40-60м2", callback_data="bizSize2")
		kb3= types.InlineKeyboardButton(text="60-100м2", callback_data="bizSize3")
		kb4 = types.InlineKeyboardButton(text="Вище 100м2", callback_data="bizSize4")
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		markup.add(kb1, kb2)
		markup.add(kb3, kb4)
		markup.add(menu)
		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Яка загальна площа об єкту?")
		bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)

	if 'bizSize' in c.data:
		if c.data == 'bizSize1':
			db.update({'conPloch': 'Меньше 40м2'}, Query().chatId == c.message.chat.id)
		elif c.data == 'bizSize2':
			db.update({'conPloch': '40-60м2'}, Query().chatId == c.message.chat.id)
		elif c.data == 'bizSize3':
			db.update({'conPloch': '60-100м2'}, Query().chatId == c.message.chat.id)
		elif c.data == 'bizSize4':
			db.update({'conPloch': 'Вище 100м2'}, Query().chatId == c.message.chat.id)

		db.update({'status_testa': 'conPlan'}, Query().chatId == c.message.chat.id)

		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="У мене немає плану", callback_data="bizNoPlan")
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		markup.add(kb1)
		markup.add(menu)
		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Додайте, будьласка, фото плану існуючого приміщення (натисність на скріпку в лівому нижньому куточку щоб обрати фото)")
		bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)

	if c.data == 'bizNoPlan':
		db.update({'status_testa': 'conPhoto'}, Query().chatId == c.message.chat.id)

		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="У мене немає фото", callback_data="bizNoPhoto")
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		markup.add(kb1)
		markup.add(menu)
		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Додайте, будьласка, фото існуючого стану об'єкта (натисність на скріпку в лівому нижньому куточку щоб обрати фото)")
		bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)

	if c.data == 'bizNoPhoto':
		db.update({'status_testa': 'conPhone'}, Query().chatId == c.message.chat.id)

		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="Контакти", callback_data="contact")
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		markup.add(kb1)
		markup.add(menu)
		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, 
			text="Зателефонуйте нам прямо зараз або напишіть свій номер телефону і ми передзвонимо найближчим часом"+'''
				Первинна консультація – наше з Вами перше знайомство та основа майбутньої співпраці. 
				Для Вас це можливість зрозуміти – чим я можу Вам допомогти. 
				Первинна консультація включає в себе :
				-	Повний аудит з питань планування чи перепланування 
				-	Функції та ергономіки приміщень 
				-	Визначення об’ємного просторового рішення 
				-	Оптимізація бюджету замовника для вирішення його побажань 
				-	Консультація суміжних питань будівництва та декорування 
			''')
		bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup = markup)


#______________________________________________________________________________________________________________
#______________________________________________________________________________________________________________
#______________________________________________________________________________________________________________


 
#@bot.callback_query_handler(func=lambda c:True)
#def ans(c):
#	cid = c.message.chat.id
#	keyboard = types.InlineKeyboardMarkup()
#	if c.data == "aaa":
#		keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
#		keyboard1.row('О компании', 'Онлайн расчет стоимости ремонта')
#		bot.send_message(c.message.chat.id, 'Что Вас сейчас интересует?', reply_markup=keyboard1)

@bot.message_handler(content_types=["photo"])
def photo_handler(message):
	dbs=db.search(Query().chatId == message.chat.id)
	dbs=dbs[0]['status_testa']
	bot.send_chat_action(message.chat.id, action = "typing")

	if dbs == 'conPlan':
		db.update({'status_testa': 'conPhoto'}, Query().chatId == message.chat.id)

		print(message.photo[-1].file_size)
		file_info = bot.get_file(message.photo[-1].file_id)
		downloaded_file = bot.download_file(file_info.file_path)
		src = 'img/user_uploads/' + message.photo[-1].file_id[20:-20:2] + '.jpg'
		try:
			with open(src, 'wb') as new_file:
				new_file.write(downloaded_file)
		except FileNotFoundError:
			mkdir('img/user_uploads/')
			with open(src, 'wb') as new_file:
				new_file.write(downloaded_file)

		db.update({'conPlan': src}, Query().chatId == message.chat.id)

		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="У мене немає фото", callback_data="flatNoPhoto")
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		markup.add(kb1)
		markup.add(menu)
		bot.send_message(chat_id=message.chat.id, text="Додайте, будьласка, фото існуючого приміщення (натисність на скріпку в лівому нижньому куточку щоб обрати фото)", reply_markup = markup)

	if dbs == 'conPhoto':
		db.update({'status_testa': 'conPhone'}, Query().chatId == message.chat.id)

		file_info = bot.get_file(message.photo[-1].file_id)
		downloaded_file = bot.download_file(file_info.file_path)
		src = 'img/user_uploads/' + message.photo[-1].file_id[20:-20:2] + '.jpg'
		try:
			with open(src, 'wb') as new_file:
				new_file.write(downloaded_file)
		except FileNotFoundError:
			mkdir('img/user_uploads/')
			with open(src, 'wb') as new_file:
				new_file.write(downloaded_file)
		db.update({'conPhoto': src}, Query().chatId == message.chat.id)

		markup = types.InlineKeyboardMarkup()
		kb1 = types.InlineKeyboardButton(text="Контакти", callback_data="contact")
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		markup.add(kb1)
		markup.add(menu)
		bot.send_message(chat_id=message.chat.id, 
			text="Зателефонуйте нам прямо зараз або напишіть свій номер телефону і ми передзвонимо найближчим часом"+'''
				Первинна консультація – наше з Вами перше знайомство та основа майбутньої співпраці. 
				Для Вас це можливість зрозуміти – чим я можу Вам допомогти. 
				Первинна консультація включає в себе :
				-	Повний аудит з питань планування чи перепланування 
				-	Функції та ергономіки приміщень 
				-	Визначення об’ємного просторового рішення 
				-	Оптимізація бюджету замовника для вирішення його побажань 
				-	Консультація суміжних питань будівництва та декорування 
			''', reply_markup = markup)



@bot.message_handler(content_types=["text"])
def text_handler(message):

	dbs=db.search(Query().chatId == message.chat.id)
	space_type = dbs[0]['tipPomechenya']
	dbs=dbs[0]['status_testa']
	bot.send_chat_action(message.chat.id, action = "typing")

	if dbs == 'conPhone':
		db.update({'status_testa': 0}, Query().chatId == message.chat.id)
		db.update({'conPhone': message.text}, Query().chatId == message.chat.id)

		markup = types.InlineKeyboardMarkup()
		menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
		markup.add(menu)
		bot.send_message(message.chat.id, "Дякуємо! Найближчим часом з Вами зв'яжеться менеджер", reply_markup=markup)


	if dbs == 2:

		if space_type == 'Лише планувальне рішення':
			try: 
				if int(message.text) <= 50 and int(message.text) > 5:
					db.update({'status_testa': 'conPhone'}, Query().chatId == message.chat.id)

					markup = types.InlineKeyboardMarkup()
					kb1 = types.InlineKeyboardButton(text="Контакти", callback_data="contact")
					menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
					markup.add(kb1)
					markup.add(menu)
					bot.send_message(message.chat.id, 'Загальна кінцева вартість 100 доларів'+ '''
					Вкажіть свій номер телефону ми з Вами зв’яжемся  або зателефонуйте нам''', reply_markup=markup)

				elif int(message.text) > 50 and int(message.text) <= 100:
					db.update({'status_testa': 'conPhone'}, Query().chatId == message.chat.id)

					markup = types.InlineKeyboardMarkup()
					kb1 = types.InlineKeyboardButton(text="Контакти", callback_data="contact")
					menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
					markup.add(kb1)
					markup.add(menu)
					bot.send_message(message.chat.id, 'Загальна кінцева вартість' + str(int(message.text) * 2) + ' доларів' + '''
					Вкажіть свій номер телефону ми з Вами зв’яжемся  або зателефонуйте нам''', reply_markup=markup)

				elif int(message.text) > 100:
					db.update({'status_testa': 'conPhone'}, Query().chatId == message.chat.id)

					markup = types.InlineKeyboardMarkup()
					kb1 = types.InlineKeyboardButton(text="Контакти", callback_data="contact")
					menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
					markup.add(kb1)
					markup.add(menu)
					bot.send_message(message.chat.id, '''Необхідний індивідуальний розрахунок.
					Вкажіть свій номер телефону ми з Вами зв’яжемся  або зателефонуйте нам''', reply_markup=markup)

				else:
					markup = types.InlineKeyboardMarkup()
					menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
					markup.add(menu)
					bot.send_message(message.chat.id, 'Введена занадто мала площа, спробуйте знову', reply_markup=markup)


			except ValueError:
				markup = types.InlineKeyboardMarkup()
				menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
				markup.add(menu)
				bot.send_message(message.chat.id, 'Введено невірне значення. Необхідно відправити число, спробуйте знову', reply_markup=markup)

		else:
			try:
				if int(message.text) < 50 and int(message.text) > 5:
					db.update({'status_testa': 'vizualiz'}, Query().chatId == message.chat.id)
					db.update({'plochad': message.text}, Query().chatId == message.chat.id)

					markup = types.InlineKeyboardMarkup()
					kb1 = types.InlineKeyboardButton(text="Так", callback_data="viz_yes")
					kb2 = types.InlineKeyboardButton(text="Нi", callback_data="viz_no")
					menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
					markup.add(kb1, kb2)
					markup.add(menu)
					bot.send_message(message.chat.id, 'Необхідна 3Д візуалізація? ', reply_markup=markup)

				elif int(message.text) >= 50 and int(message.text) < 100:
					db.update({'status_testa': 3}, Query().chatId == message.chat.id)
					db.update({'plochad': message.text}, Query().chatId == message.chat.id)

					markup = types.InlineKeyboardMarkup()
					kb1 = types.InlineKeyboardButton(text="До 5", callback_data="До 5")
					kb2 = types.InlineKeyboardButton(text="Більше 5", callback_data="Більше 5")
					menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
					markup.add(kb1, kb2)
					markup.add(menu)
					bot.send_message(message.chat.id, 'Виберіть кількість приміщень ', reply_markup=markup)

				elif int(message.text) >= 100:
					db.update({'status_testa': 'conPhone'}, Query().chatId == message.chat.id)
					db.update({'plochad': message.text}, Query().chatId == message.chat.id)

					markup = types.InlineKeyboardMarkup()
					kb1 = types.InlineKeyboardButton(text="Контакти", callback_data="contact")
					menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
					markup.add(kb1)
					markup.add(menu)
					bot.send_message(message.chat.id, 'Необхідний індивідуальний розрахунок'+ '''
					Вкажіть свій номер телефону ми з Вами зв’яжемся  або зателефонуйте нам''', reply_markup=markup)

				else:
					markup = types.InlineKeyboardMarkup()
					menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
					markup.add(menu)
					bot.send_message(message.chat.id, 'Введена занадто мала площа, спробуйте знову', reply_markup=markup)

			except ValueError:
				markup = types.InlineKeyboardMarkup()
				menu = types.InlineKeyboardButton(text="В головне меню", callback_data="menu")
				markup.add(menu)
				bot.send_message(message.chat.id, 'Введено невірне значення. Необхідно відправити число, спробуйте знову', reply_markup=markup)

	for i in admin:
		if message.chat.id == i:
			allUser1=allUser.search(Query().stAdmin == True)
			if allUser1 !=[]:
				allUser.update({'mes': message.text}, Query().mes == "")
				allUser.update({'stAdmin': False}, Query().stAdmin == True)

@bot.message_handler(content_types=["entities", "audio", "document", "photo", "sticker", "video", "voice", "caption", "contact", "location", "venue"])
def repeat_all_messages(message):
	bot.send_message(message.chat.id, 'Проверьте правильность вашего ответа и введите ответ снова ')


if __name__ == '__main__':
     bot.polling(none_stop=True)
