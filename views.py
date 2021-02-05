from config import app, db, group_config, session, session_papochka
from models import Person as Passport
from flask import request
import json
from vk_api import vk
import random
from events_handler import events
from after_response import AfterResponse

def exceptionHelp (e, peer_id):
    from keyboards import BugReport1 as keyboard
    print(e)
    session.send_message(peer_id, 'Жесть, ошибка!', keyboard=json.dumps(keyboard))

#@app.route('/bot', methods=['POST'])
def botFunc(data):
    # Распаковка данных
    data = json.loads(request.data)
    # Проверка группы
    if data['group_id'] == group_config['id']:
        # Проверка секретного ключа
        if data['secret'] == group_config['secret']:
            # Если пришло сообщение
            if data['type'] == 'message_new':
                from_id = message['from_id'] # Кто прислал
                if Passport.query.filter_by(vk_id=from_id).first() == None:
                    if str(from_id)[0] != '-':
                        session.send_message(peer_id, 'Был найден [id' + str(
                            from_id) + '|незарегистрированный пользователь]!')
                        try:
                            img = session.getUser(from_id)['photo_max']
                            Name = session.getUser(from_id)['first_name']
                            Surname = session.getUser(from_id)['last_name']
                            newUser = Passport(vk_id=from_id, Img=img, Name=Name, Surname=Surname, Count=200)
                            db.session.add(newUser)
                            db.session.commit()
                            session.send_message(peer_id, 'Пользователь успешно дабавлен в ДБ\nОбратитесь в ЛС к боту!')
                        except Exception as e:
                            exceptionHelp(e, peer_id)
            events(data, session, session_papochka)
@app.route('/bot', methods=['POST'])
def botResp():
    data = json.loads(request.data)
    def do_work():
        import time
        time.sleep(0.1)
        botFunc(data)
    do_work()
    # Проверка на наличие поля 'type'
    if 'type' not in data.keys():
        return 'not \'type\' in keys'
    # Проверка группы
    if data['group_id'] == group_config['id']:
        # Проверка секретного ключа
        if data['secret'] == group_config['secret']:
            # Возвращение confirmationToken на сервер
            if data['type'] == 'confirmation':
                return group_config['confirm']
            else:
                return 'ok', 200
@app.errorhandler(500)
def handler(e):
    print(e)
    return 'ok'
