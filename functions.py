# -*- coding: utf-8 -*-
import telebot # Library of API bot.
from telebot import types # Types from API bot
import time
import random
import datetime
import codecs
import sys
import json
from os.path import exists
import os
import token
import user
import feedparser
import owners
#import re
import logging
import commands
import subprocess

TOKEN = token.token_id
bot = telebot.TeleBot(TOKEN) # Creating our bot object.
bot.skip_pending=True
#######################################
#TRIGGERS SECTION
triggers = {}
tfile = "triggers.json"
ignored = []
separator = '/'
#user = [line.rstrip('\n') for line in open('user.txt','rt')]

#Check if Triggers file exists and load, if not, is created.
if exists('triggers.json'):
    with open('triggers.json') as f:
        triggers = json.load(f)
    print('Triggers file loaded.')
else:
    with open('triggers.json', 'w') as f:
        json.dump({}, f)

#Function to save Triggers - Response
def save_triggers():
    with open('triggers.json', 'w') as f:
        json.dump(triggers, f)
    print('Triggers file saved.')

#Function to get triggers list for a group.
def get_triggers(group_id):
    if(str(group_id) in triggers.keys()):
        return triggers[str(group_id)]
    else:
        return False

#Function to check if a message is too old(60 seconds) to answer.
def is_recent(m):
    return (time.time() - m.date) < 60


added_message = '''
New Trigger Created:
Trigger [{}]
Response [{}]
'''
#END TRIGGERS SECTION
#######################################

#######################################
#Triggers Management Section
#Adds another trigger-response. ex: "/add Hi / Hi!! :DD"
def format_list(list, cols=2):
    for i in range(0, len(list), cols):
        return '\n'.join(["\t".join(list[i:i+cols])])

@bot.message_handler(commands=['add'])
def add(m):
    if(m.reply_to_message):
        if(m.reply_to_message.text):
            if(len(m.reply_to_message.text.split()) < 2):
                bot.reply_to(m, 'Bad Arguments. Try with /add [trigger] / [response]')
                return
            trigger_word = m.text.split(' ', 1)[1].strip()
            trigger_response = m.reply_to_message.text.strip()
        else:
            bot.reply_to(m, 'Only text triggers are supported.')
            return
    else:
        if(len(m.text.split()) < 2):
            bot.reply_to(m, 'Bad Arguments. Try with /add [trigger] / [response]')
            return
        if(m.text.find(separator, 1) == -1):
            bot.reply_to(m, 'Separator not found. Try with /add [trigger] / [response]')
            return
        rest_text_unencoded = m.text.split(' ', 1)[1]
        rest_text = rest_text_unencoded.encode('utf-8')
        trigger_word = rest_text.split(separator)[0].strip()
        trigger_response = rest_text.split(separator, 1)[1].strip()

    if(len(trigger_word) < 4):
        bot.reply_to(m, 'Trigger too short. [chars < 4]')
        return
    if(len(trigger_response) < 1):
        bot.reply_to(m, 'Invalid Response.')
        return
    if(m.chat.type in ['group', 'supergroup']):
        if(get_triggers(m.chat.id)):
            get_triggers(m.chat.id)[trigger_word] = trigger_response
        else:
            triggers[str(m.chat.id)] = {trigger_word : trigger_response}
        msg = added_message.format(trigger_word, trigger_response)
        bot.reply_to(m, msg)
        save_triggers()
    else:
        if(m.chat.id != '-8861523'):
            return

@bot.message_handler(commands=['del'])
def delete(m):
    if(len(m.text.split()) < 2):
        bot.reply_to(m, 'Bad Arguments')
        return
    del_text = m.text.split(' ', 1)[1].strip()
    if(m.chat.type in ['group', 'supergroup']):
        trg = get_triggers(m.chat.id)
        if(trg and del_text in trg.keys()):
            trg.pop(del_text)
            bot.reply_to(m, 'Trigger [{}] deleted.'.format(del_text))
            save_triggers()
        else:
            bot.reply_to(m, 'Trigger [{}] not found.'.format(del_text))

#Answers with the size of triggers.
@bot.message_handler(commands=['size'])
def size(m):
    if(m.chat.type in ['group', 'supergroup']):
        trg = get_triggers(m.chat.id)
        if(trg):
            msg = 'Size of Triggers List = {}'.format(len(trg))
            bot.reply_to(m, msg)
        else:
            bot.reply_to(m, 'Size of Triggers List = 0')

@bot.message_handler(commands=['all'])
def all(m):
    if(m.chat.type in ['group', 'supergroup']):
        trg = get_triggers(m.chat.id)
        if(trg):
            if(len(trg.keys()) == 0):
                bot.reply_to(m, 'This group doesn\'t have triggers.')
            else:
                bot.reply_to(m, 'Triggers:\n' + str('\n'.join(trg)))
        else:
            bot.reply_to(m, 'This group doesn\'t have triggers.')

#End Triggers Management Section
#######################################

#######################################
#Function for feedparser
#CODE TAKEN FROM:
#https://gist.github.com/Jeshwanth/99cf05f4477ab0161349
def get_feed(url):
    try:
        feed = feedparser.parse(url)
    except:
        return 'Invalid url.'
    y = len(feed[ "items" ])
    y = 5 if y > 5 else y
    if(y < 1):
        return 'Nothing found'
    lines = ['*Feed:*']
    for x in range(y):
        lines.append('- [{}]({})'.format(feed['items'][x]['title'].replace(']', ':').replace('[', '').encode('utf-8'), feed['items'][x]['link']))
    return '\n'.join(lines)
#    for x in range(y):
#        lines.append(
#        u'-&gt <a href="{1}">{0}</a>.'.format(
#        u'' + feed[ "items" ][x][ "title" ],
#        u'' + feed[ "items" ][x][ "link" ]))
#    return u'' + '\n'.join(lines)

#######################################

# Search function used as easter eggs
#find_python = re.compile(r"(?i)\bPYTHON\b").search

#Functions
@bot.message_handler(content_types=['new_chat_members'])
def command_new_user(m):
    cid = m.chat.id
    grupo = m.chat.title
    usuario = bot.get_chat_member(cid, m.new_chat_member.id).user
    bots = m.new_chat_member.id
    markup = types.InlineKeyboardMarkup()
#    itembtnnormas = types.InlineKeyboardButton('<Click Aquí>', url="https://t.me/neositelinuxgrupo/4")
    markup.row(itembtnnormas)

    if (m.chat.id == -1001269808796):
       itembtnnormas = types.InlineKeyboardButton('<Click Aquí>', url="https://t.me/neositelinuxgrupo/4")
    else:
       itembtnnormas = types.InlineKeyboardButton('<Click Aquí>', url="https://github.com/neoranger/NeoBot")

    if usuario.is_bot:
       bot.kick_chat_member(cid, bots)

    if (m.new_chat_member.username != None and m.new_chat_member.first_name != None and m.new_chat_member.last_name != None):
        bot.send_message(cid, "Bienvenido {0} {1} !! A.K.A. @{2} a {3}. Te sugerimos leer las reglas en el mensaje anclado o click en el botón.".format(m.new_chat_member.first_name, m.new_chat_member.last_name, m.new_chat_member.username, grupo))
        bot.send_message(cid, "Normas", reply_markup=markup)
    elif (m.new_chat_member.username != None and m.new_chat_member.first_name == None and m.new_chat_member.last_name == None):
        bot.send_message(cid, "Bienvenido!! @{0} a {1}. No tenés nombres, podrías completar los datos. Te sugerimos leer las reglas en el mensaje anclado o click en el botón.".format(m.new_chat_member.username, grupo))
        bot.send_message(cid, "Normas", reply_markup=markup)
    elif (m.new_chat_member.username != None and m.new_chat_member.first_name != None and m.new_chat_member.last_name == None):
        bot.send_message(cid, "Bienvenido {0} A.K.A. @{1} a {2}. Te sugerimos leer las reglas en el mensaje anclado o click en el botón.".format(m.new_chat_member.first_name,m.new_chat_member.username, grupo))
        bot.send_message(cid, "Normas", reply_markup=markup)
    elif (m.new_chat_member.username != None and m.new_chat_member.first_name == None and m.new_chat_member.last_name != None):
        bot.send_message(cid, "Bienvenido {0}!! A.K.A. @{1} a {2}. Te sugerimos leer las reglas en el mensaje anclado o click en el botón.".format(m.new_chat_member.last_name,m.new_chat_member.username, grupo))
        bot.send_message(cid, "Normas", reply_markup=markup)
    elif (m.new_chat_member.username == None and m.new_chat_member.first_name != None and m.new_chat_member.last_name != None):
        bot.send_message(cid, "Bienvenido {0} {1} a {2}. No tenes alias, seria mejor que te crees uno. Te sugerimos tambien leer las reglas en el mensaje anclado o click en el botón.".format(m.new_chat_member.first_name,m.new_chat_member.last_name,grupo))
        bot.send_message(cid, "Normas", reply_markup=markup)
    elif (m.new_chat_member.username == None and m.new_chat_member.first_name == None and m.new_chat_member.last_name != None):
        bot.send_message(cid, "Bienvenido {0}!! a {1}. No tenes alias, seria mejor que te crees uno. Te sugerimos tambien leer las reglas en el mensaje anclado o click en el botón.".format(m.new_chat_member.last_name, grupo))
        bot.send_message(cid, "Normas", reply_markup=markup)
    elif (m.new_chat_member.username == None and m.new_chat_member.first_name != None and m.new_chat_member.last_name == None):
        bot.send_message(cid, "Bienvenido {0} a {1}. No tenes alias, seria mejor que te crees uno. Te sugerimos tambien leer las reglas en el mensaje anclado o click en el botón.".format(m.new_chat_member.first_name, grupo))
        bot.send_message(cid, "Normas", reply_markup=markup)

#@bot.message_handler(content_types=['left_chat_member'])
#def command_left_user(m):
#    cid = m.chat.id
#    bot.send_message(cid, "@{0} Gracias por pasar!! Bye!!".format(left_chat_member.username))

#@bot.message_handler(commands=['kick'])
#def command_kick(m):
#    cid = m.chat.id
#    bot.send_photo( cid, open( './imagenes/kick.jpg', 'rb'))

#@bot.message_handler(commands=['uppercut'])
#def command_uppercut(m):
#    cid = m.chat.id
#    bot.send_photo( cid, open( './imagenes/uppercut.jpg', 'rb'))

#@bot.message_handler(commands=['hadouken'])
#def command_hadouken(m):
#    cid = m.chat.id
#    bot.send_document( cid, open( './imagenes/hadouken.gif', 'rb'))

#@bot.message_handler(commands=['windowsero'])
#def command_windowsero(m):
#    cid = m.chat.id
#    try:
#     bot.send_photo( cid, open( './imagenes/windowsero.jpg', 'rb'))
#    except Exception as a:
#     bot.send_message(cid, "Error: {}".format(a))

@bot.message_handler(commands=['acerca'])
def command_acerca(m):
    cid = m.chat.id
    bot.send_message( cid, 'Acerca de @NeoSiteBot: Creado por NeoRanger - www.neositelinux.com')

@bot.message_handler(commands=['help'])
def command_ayuda(m):
    cid = m.chat.id
    bot.send_message( cid, "Comandos Disponibles:\n /welcome\n /hola\n /hello\n /add\n /del\n /size\n /ignore\n /kick\n /stallman\n /nsa\n /deletethat\n /spoiler\n /viernes\n /roll\n /blog\n /neofeed\n /programador\n /id\n /acerca\n /support\n /invitameuncafe\n /help\n")

@bot.message_handler(commands=['hola'])
def command_hola(m):
    cid = m.chat.id
    bot.send_message( cid, 'Hola, bienvenido!')

@bot.message_handler(commands=['hello'])
def command_hello(m):
    cid = m.chat.id
    bot.send_message( cid, 'Hello and welcome!')

#@bot.message_handler(commands=['attack'])
#def command_attack(m):
#    cid = m.chat.id
#    bot.send_photo( cid, open( './imagenes/dictionary_attack.jpg', 'rb'))

@bot.message_handler(commands=['nsa'])
def command_nsa(m):
    cid = m.chat.id
    bot.send_photo( cid, open( './imagenes/tiosam.jpg', 'rb'))

@bot.message_handler(commands=['roll'])
def command_roll(m):
    cid = m.chat.id
    bot.send_message( cid, random.randint(1,6) )

# @bot.message_handler(commands=['time'])
# def command_time(m):
#     cid = m.chat.id
#     bot.send_message( cid, str(datetime.datetime.now()))

#@bot.message_handler(commands=['gentoo'])
#def command_gentoo(m):
#    cid = m.chat.id
#    bot.send_photo( cid, open( './imagenes/gentoo.jpg', 'rb'))

 #@bot.message_handler(commands=['vicman'])
 #def command_vicman(m):
 #    cid = m.chat.id
 #    bot.send_photo( cid, open( './imagenes/vicman.jpg', 'rb'))

# @bot.message_handler(commands=['tuxamigos'])
# def command_tuxamigos(m):
#     cid = m.chat.id
#     bot.send_photo( cid, open( './imagenes/tuxamigos.jpg', 'rb'))

@bot.message_handler(commands=['deletethat'])
def command_deletethat(m):
    cid = m.chat.id
    bot.send_photo( cid, open( './imagenes/deletethat.jpg', 'rb'))

@bot.message_handler(commands=['flame'])
def command_flame(m):
    cid = m.chat.id
    bot.send_photo( cid, open( './imagenes/popcorn.jpg', 'rb'))

@bot.message_handler(commands=['stallman'])
def command_stallman(m):
    cid = m.chat.id
    bot.send_photo( cid, open( './imagenes/dancingstallman.jpg', 'rb'))

#@bot.message_handler(commands=['ok'])
#def command_ok(m):
#    cid = m.chat.id
#    bot.send_photo( cid, open( './imagenes/ok.jpg', 'rb'))

#@bot.message_handler(commands=['coding'])
#def command_coding(m):
#    cid = m.chat.id
#    bot.send_photo( cid, open( './imagenes/coding.jpg', 'rb'))

#@bot.message_handler(commands=['nelson'])
#def command_nelson(m):
#    cid = m.chat.id
#    bot.send_photo( cid, open( './imagenes/nelson.jpg', 'rb'))

#@bot.message_handler(commands=['yes'])
#def command_fuckyeah(m):
#    cid = m.chat.id
#    bot.send_photo( cid, open( './imagenes/fuckyeah.jpg', 'rb'))

@bot.message_handler(commands=['spoiler'])
def command_spoiler(m):
    cid = m.chat.id
    bot.send_photo( cid, open( './imagenes/spoileralert.jpg', 'rb'))

@bot.message_handler(commands=['viernes'])
def command_viernes(m):
    cid = m.chat.id
    bot.send_photo( cid, open( './imagenes/viernes.jpg', 'rb'))

#@bot.message_handler(commands=['kde'])
#def command_kde(m):
#    cid = m.chat.id
#    bot.send_photo( cid, open( './imagenes/kderock.jpg', 'rb'))

#@bot.message_handler(commands=['what'])
#def command_what(m):
#    cid = m.chat.id
#    bot.send_photo( cid, open( './imagenes/what.jpg', 'rb'))

#@bot.message_handler(commands=['vegetta'])
#def command_vegetta(m):
#    cid = m.chat.id
#    bot.send_photo( cid, open( './imagenes/vegetta.jpg', 'rb'))

@bot.message_handler(commands=['welcome'])
def command_welcome(m):
    if (m.chat.id == -1001042117783):  #ID del grupo No Solo Linux
        cid = m.chat.id
        bot.send_photo(cid, open('./imagenes/welcome.jpg', 'rb'))
    elif (m.chat.id == -1001269808796): #ID del grupo NeoSiteLinux
        cid = m.chat.id
        bot.send_photo(cid, open('./imagenes/welcome2.jpg', 'rb'))
    else:
        bot.reply_to(m, 'Este comando es exclusivo de otro grupo')
        return

#@bot.message_handler(commands=['tabla'])
#def command_tabla(m):
#    cid = m.chat.id
#    bot.send_photo( cid, open( './imagenes/tabla.jpg', 'rb'))

#@bot.message_handler(commands=['solus'])
#def command_solus(m):
#    cid = m.chat.id
#    bot.send_photo( cid, open( './imagenes/bleh.jpg', 'rb'))

#@bot.message_handler(commands=['takataka'])
#def command_taka(m):
#    cid = m.chat.id
#    bot.send_photo( cid, open( './imagenes/takataka.jpg', 'rb'))

#@bot.message_handler(commands=['kill'])
#def command_kill(m):
#    cid = m.chat.id
#    list = str(m.text).split(None,1)
#    killed = str(list[1])
#    bot.send_message( cid, "Muere {0}!!!".format(killed))
#    bot.send_photo( cid, open( './imagenes/rambo.jpg', 'rb'))

#@bot.message_handler(commands=['format'])
#def command_format(m):
#    cid = m.chat.id
#    try:
#        bot.send_message( cid, m.text.split(None,1)[1],parse_mode='markdown')
#    except IndexError:
#        bot.send_message( cid, "Argument missing" )
#    except Exception:
#        bot.send_message( cid, "Invalid Argument")

#@bot.message_handler(commands=['maestruli'])
#def command_maestruli(m):
#    cid = m.chat.id
#    bot.send_document( cid, open( './imagenes/maestruli.mp4', 'rb'))

#@bot.message_handler(commands=['fuckyou'])
#def command_fuckyou(m):
#    cid = m.chat.id
#    bot.send_document( cid, open( './imagenes/fuckyou.mp4', 'rb'))

#@bot.message_handler(commands=['arch'])
#def command_arch(m):
#    cid = m.chat.id
#    bot.send_photo( cid, open( './imagenes/arch.jpg', 'rb'))

#@bot.message_handler(commands=['love'])
#def command_love(m):
#    cid = m.chat.id
#    bot.send_photo( cid, open( './imagenes/love.jpg', 'rb'))

@bot.message_handler(commands=['feed'])
def command_feed(m):
    cid = m.chat.id
    url = str(m.text).split(None,1)
    try:
        print (url)
        bot.send_message(cid, get_feed(url[1]),disable_web_page_preview=True,parse_mode="markdown")
    except IndexError:
        bot.send_message( cid, "Missing Argument - Example: /feed http://www.example.com" )

@bot.message_handler(commands=['id'])
def command_id(m):
    cid = m.chat.id
    username = m.from_user.username
    uid = m.from_user.id
    bot.send_message(cid, "You are: @" + str(username)+ " " + "And your Telegram ID is: " + str(uid))

@bot.message_handler(commands=['support'])
def command_help(message):
    markup = types.InlineKeyboardMarkup()
    itembtnneo = types.InlineKeyboardButton('NeoRanger', url="telegram.me/NeoRanger")
    itembtngroup = types.InlineKeyboardButton('NeoSiteLinux Grupo', url="telegram.me/neositelinuxgrupo")
    itembtnblog = types.InlineKeyboardButton('URL Blog', url="https://www.neositelinux.com")
    itembtnrepo = types.InlineKeyboardButton('Repo Github', url="http://github.com/neoranger/NeoBot")
    markup.row(itembtnneo)
    markup.row(itembtngroup)
    markup.row(itembtnblog)
    markup.row(itembtnrepo)
    bot.send_message(message.chat.id, "Choose an option:", reply_markup=markup)

#@bot.message_handler(commands=['deal'])
#def command_deal(m):
#    cid = m.chat.id
#    bot.send_document( cid, open( './imagenes/deal.mp4', 'rb'))
    
# @bot.message_handler(commands=['blog'])
# def command_blog(m):
#     cid = m.chat.id
#     if (cid == -1001030218798):
#         busqueda = 'http://kernelpanicblog.wordpress.com/search/%s/feed/rss'
#     else:
#         busqueda = 'http://www.neositelinux.com/search/%s/feed/rss'
#     url = (busqueda % m.text.split()[1])
#     try:
#         bot.send_message(cid, get_feed(url),disable_web_page_preview=True,parse_mode="HTML")
#     except IndexError:
#         bot.send_message( cid, "Missing Argument" )

#@bot.message_handler(commands=['blog'])
#def command_blog(m):
#    cid = m.chat.id
#    busqueda = 'https://www.neositelinux.com/search/index.html?query='
#    print busqueda
#    if len(m.text.split()) >= 2:
#        palabras = m.text.split()
#        palabras.pop(0)
#        a_buscar = '+'.join(palabras)
#        print a_buscar
#        url = (busqueda + a_buscar)
#        print url
#        bot.send_message(cid, get_feed(url),disable_web_page_preview=True,parse_mode="markdown")
#    else:
#        bot.send_message( cid, "Missing Argument" )
        
@bot.message_handler(commands=['programador'])
def command_dev(m):
    cid = m.chat.id
    bot.send_document( cid, open( './imagenes/soyprogramador.mp4', 'rb'))
    
#@bot.message_handler(commands=['windowseros'])
#def command_windowseros(m):
#    cid = m.chat.id
#    bot.send_photo( cid, open( './imagenes/nohaywindowseros.jpg', 'rb'))

#@bot.message_handler(commands=['friends'])
#def command_friends(m):
#    cid = m.chat.id
#    bot.send_photo( cid, open( './imagenes/friends.jpg', 'rb'))

#@bot.message_handler(commands=['apache'])
#def command_apache(m):
#    cid = m.chat.id
#    bot.send_document( cid, open( '/home/neoranger/scripts_vps/apache2.conf', 'rb'))
    
@bot.message_handler(commands=['neofeed'])
def neo_feed(m):
    cid = m.chat.id
    url = str("https://neositelinux.com/feed.xml")
    print (url)
    bot.send_message(cid, get_feed(url),disable_web_page_preview=True,parse_mode="markdown")

@bot.message_handler(commands=['kick'])
def command_kick_user(m):
        cid = m.chat.id
        uid = m.from_user.id
        if bot.get_chat_member(cid, uid).status in ["administrator", "creator"] and bot.get_chat_member(cid, m.reply_to_message.from_user.id).status not in ["administrator", "creator"]:
           bot.send_message(cid, 'Hasta la vista, Baby')
           bot.kick_chat_member(cid, m.reply_to_message.from_user.id)

@bot.message_handler(commands=['invitameuncafe'])
def command_cafe(m):
    cid = m.chat.id
    markup = types.InlineKeyboardMarkup()
    itembtncafe = types.InlineKeyboardButton('Te invito!', url="https://www.paypal.me/neoranger")
    markup.row(itembtncafe)
    bot.send_message(cid, '¿Te parece que el proyecto merece crecer? Invítame un café!.',reply_markup=markup)

###############################################################################
#Specials functions
def send_message_checking_permission(m, response):
    cid = m.chat.id
    uid = m.from_user.id
    if uid != user.user_id:
        bot.send_message(cid, "You can't use the bot")
        return
    bot.send_message(cid, response)

@bot.message_handler(func=lambda m: True)
def response(m):
    if(m.chat.type in ['group', 'supergroup']):
        trg = get_triggers(m.chat.id)
        if(trg):
            for t in trg.keys():
                if t.lower() in m.text.lower():
                    bot.reply_to(m, trg[t])
###############################################################################
print('Functions loaded')
