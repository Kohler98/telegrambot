import os
import sys
import telebot

from modulos.config import *

from modulos.colores import *

from modulos.chat_gpt import ChatGpt

bot =  telebot.TeleBot(TELEGRAM_TOKEN)
# procesa todos los mensajes de texto

@bot.message_handler(content_types=["text"])
def mensajes_recibidos(m):


    #enviamos el prompt
    respuesta = chatgpt.chatear(m.text,formato="html")
  

    # #enviamos la respuesta
    bot.send_message(m.chat.id,respuesta, parse_mode="html", disable_web_page_preview=True)






















#########################################
if __name__ == "__main__":
    
    chatgpt = ChatGpt(correo,clave)
    print(f'{verde}BOT INICIADO {gris_claro}')
    # bucle principal
    bot.infinity_polling()