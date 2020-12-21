import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from vk_api import VkUpload 

from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build

from urllib.request import urlretrieve

import os
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import requests
import threading
import io
import logging
from pprint import pprint

import setings

logging.basicConfig(
    filename='logCristmas.log' ,
    level=logging.INFO,
    format='%(asctime)s - %(message)s', datefmt='%H:%M:%S'
    )

vk_session = vk_api.VkApi(token = setings.vkDdkgtaApi)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()


CRISTMAS_FOLDER_IN_DRIVE = '1G6l7gZLeXUhD-GJE-9jdo68hElS6pHw6'
print('sea')

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = '/Users/igorgerasimov/Desktop/Мусор/KGTAprojects-3bfc7b7d22f4.json'
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
service = build('drive', 'v3', credentials=credentials)

def getMessege (stringOtvet, user_id): # Получаем сообщение от конкретного пользователя
    for event in longpoll.listen(): # цикл для каждго ивента сервера
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.user_id == user_id: # ждать ответа от данного юзера 
            vk.messages.getConversations(offset = 0, count = 1)  
    
            if event.text == stringOtvet: # если событие текст и он равен сообщению которое отправил пользователь
                return True

            return False

start = False

def newUser(userId):
    global columCell

    print("Проверка пользователя")

    try:

        usersId.index(userId)
        print("Cтарый пользователь")
        numberOfQuestion = usersId.index(userId) * 2
        print(f'Находиться в {numberOfQuestion} строке')
        return False

    except ValueError:

        print("Новый пользователь")
        return True

    userInfo = vk.users.get(user_ids = event.user_id) 
    print(userInfo)# Получили ответ в виде массива из одного списка

def get_type_attachment(conversations):
    typeAttachment = conversations['items'][0]['last_message']['attachments'][0]['type']
    return typeAttachment

def upload_file(trackFile: str, nameFile: str):
    #upload
    folder_id = '1G6l7gZLeXUhD-GJE-9jdo68hElS6pHw6'
    name = nameFile
    file_path = trackFile
    file_metadata = {
                    'name': name,
                    'parents': [folder_id]
                }
    media = MediaFileUpload(file_path, resumable=True)
    r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

def start_get():

    a = vk.messages.getConversations(offset = 0, count = 1)
    startMessage = event.text 
    infoUser = vk.users.get(user_ids=a['items'][0]['conversation']['peer']['id'], fields=['screen_name'], name_case='nom')
        # pprint(a)
    print(startMessage)

    try:
        typeAttachment = get_type_attachment(a)
        nameFile = f"""({ infoUser[0]['screen_name'] })_{ infoUser[0]['first_name'] }_{ infoUser[0]['last_name'] }"""
            
        if typeAttachment == 'photo':
            trackFile = a['items'][0]['last_message']['attachments'][0]['photo']['sizes'][-1]['url']
            formatFile = '.png'
            formatFile = formatFile.split('.')

        elif typeAttachment == 'doc':
            trackFile = a['items'][0]['last_message']['attachments'][0]['doc']['url']
            formatFile = a['items'][0]['last_message']['attachments'][0]['doc']['title']
            formatFile = formatFile.split('.')
                
    except IndexError:
        logging.error('Не фото и не файл\n ')
        print('это текст ')
    
          
    t = urlretrieve(trackFile, nameFile+"."+formatFile[1])
    p = os.path.abspath(nameFile+"."+formatFile[1])
        
    upload_file(p, nameFile+"."+formatFile[1])
    print('загружено')
    os.remove(p)

    return threading.Thread._stop
        # pprint(a)    


for event in longpoll.listen():
    print(event.type)
    if event.type == VkEventType.MESSAGE_NEW: #and event.to_me and event.text:
        
        threading.Thread(target=start_get).start()
        
        