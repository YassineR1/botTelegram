import json
import telebot
from telebot import types,util
from decouple import config
from googletrans import Translator

BOT_TOKEN = config("BOT_TOKEN")
bot= telebot.TeleBot(BOT_TOKEN)
bot_data={
           "name" :["admin","Admin"],
    "name1" :["أدمين","ادمين","مسوؤل"],
    "greetings":["Hello","Hi","hi","hello","welcome","Welcome","Hey"],
    "greetings1":["مرحبا","أهلا","هلا","اهلا"],
    "grt":["سلام عليكم","سلام"],
    "link":["your channel","قناتك","channel","قناة","Link","رابط","Telegram channel",
            "قناة تيليجرام","telegram channel","link","Channel","Your channel","telegram","Telegram"],
    "link1": ["group","مجموعة","مجموعة تيليغرام","Telegram group","مجموعة تيليجرام","Telegram group link",
              "رابط مجموعة تيليجرام","group link","رابط مجموعة "]
    
}
text_messages={
    "welcome": "Welcome to the Telegram group☺   مرحبًا بك في مجموعة تليجرام☺",
    "welcomeNewMember" : 
                u"اهلا بك {name} في مجموعتنا الخاصة 🙋‍♂️",
    "saying goodbye":
                u"العضو {name} غادر المجموعة 🥺",

  #  "leave":"لقد تم اضافتي الى مجموعة غير المجموعة التي صممت لها , وداعاً 🧐",
    "call" : "كيف يمكنني المساعدة ؟ 😀",
    "warn": u"❌ لقد استعمل {name} أحد الكلمات المحظورة ❌\n"
            u" 🔴 تبقى لديك {safeCounter} فرص اذا تم تجاوز العدد سيتم طردك 🔴",
    "kicked": u"👮‍♂️⚠  لقد تم طرد العضو {name} صاحب المعرف {username} بسبب مخالفته لأحد قواعد المجموعة 👮‍♂️⚠",
    
    "call1" : "كيف يمكنني المساعدة",
    "call" : " how can I help ",
    "reply" : "Hello ",
    "reply1": " مرحبا",
    "reply2": "السلام عليكم ورحمة الله وباركته",
    "reply3" : "https://t.me/AlliEXpressOffers",
    "reply4" : "https://t.me/taarofBnjOne",
    "reply5" : "https://t.me/whatssApp_com"

            

}

text_list = {
            "offensive":[ "Asshole","asshole","Bastar","bastard","Bitch","bitch","Dick",
                          "dick","Fuck","fuck","Shit",
                          "shit","Son of a bitc","son of a bitch ","Motherfucker",
                          "motherfucker","Cunt","cunt","Prick","prick","Douchebag",
                          "douchebag","Asswipe","asswipe","كلب","قحبة","غبي","تبا","سكس","قضيب",
                         "القضيب","وغد","سفيه","أحمق","تبا لك","تبا لكم","عكروت"] 
    

}

commands = {
    "translate":["translate","trans","ترجم","ترجملي"]
}
def handleNewUserData(message):
    id = str(message.new_chat_member.user.id)
    name = message.new_chat_member.user.first_name
    username =  message.new_chat_member.user.username

    with open("data.json","r") as jsonFile:
        data = json.load(jsonFile)
    jsonFile.close()
    
    users = data["users"]
    if id not in users:
        print("new user detected !")
        users[id] = {"safeCounter":5}
        users[id]["username"] = username
        users[id]["name"] = name
      

    data["users"] = users
    with open("data.json","w") as editedFile:
        json.dump(data,editedFile,indent=3)
    editedFile.close()    

def handleOffensiveMessage(message):
    id = str(message.from_user.id)
    name = message.from_user.first_name
    username =  message.from_user.username
    
    with open("data.json","r") as jsonFile:
        data = json.load(jsonFile)
    jsonFile.close()
    
    users = data["users"]
    if id not in users:
       
        users[id] = {"safeCounter":5}
        users[id]["username"] = username
        users[id]["name"] = name
      

    for index in users:
        if index == id :
           
           
            users[id]["safeCounter"] -= 1

    safeCountrerFromJson = users[id]["safeCounter"]
    if safeCountrerFromJson == 0:
        bot.kick_chat_member(message.chat.id,id)
        users.pop(id)
       
        
        bot.send_message(message.chat.id,text_messages["kicked"].format(name=name , username = username))
    else:
        bot.send_message(message.chat.id,text_messages["warn"].format(name=name , safeCounter = safeCountrerFromJson))

    data["users"] = users
    with open("data.json","w") as editedFile:
        json.dump(data,editedFile,indent=3)
    editedFile.close()

    return bot.delete_message(message.chat.id,message.message_id)

@bot.message_handler(content_types=['new_chat_members','left_chat_members','link_chat_members'])
def cmbnr (message):
    bot.delete_message(message.chat.id,message.message_id)
  
  
    

@bot.message_handler(commands=["start","help"])
def startBot(message):
    bot.send_message(message.chat.id,text_messages["welcome"])

#* saying Welcome to joined members
#* saying goodbye to left members
@bot.chat_member_handler()
def handleUserUpdates(message:types.ChatMemberUpdated):
    newResponse = message.new_chat_member
    if newResponse.status == "member":
        handleNewUserData(message=message)
        bot.send_message(message.chat.id,text_messages["welcomeNewMember"].format(name=newResponse.user.first_name))
    if newResponse.status == "left":
        bot.send_message(message.chat.id,text_messages["saying goodbye"].format(name=newResponse.user.first_name))
        



@bot.message_handler(func=lambda m:True)
def reply(message):
    words = message.text.split()
    if words [0] in bot_data["name"]:
        bot.reply_to(message,text_messages["call"])
    elif words [0] in bot_data["name1"]:
        bot.reply_to(message,text_messages["call1"])   
        
        

    elif words [0] in bot_data["greetings"]:
        bot.reply_to(message,text_messages["reply"])
    elif words [0] in bot_data["greetings1"]:
        bot.reply_to(message,text_messages["reply1"]) 
    elif words [0] in bot_data["grt"]:
        bot.reply_to(message,text_messages["reply2"])
    elif words [0] in bot_data["link"]:
        bot.reply_to(message,text_messages["reply3"])  
    elif words [0] in bot_data["link1"]:
        bot.reply_to(message,text_messages["reply4"])
 
    if words[0] in commands["translate"]:
        translator = Translator()
        translation = translator.translate(" ".join(words[1:]),dest="ar")
        bot.reply_to(message,translation.text)
    
    for word in words:
         if word in text_list["offensive"]:
            handleOffensiveMessage(message=message)
        



bot.infinity_polling(allowed_updates=util.update_types)