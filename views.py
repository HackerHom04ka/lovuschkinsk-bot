from config import app, db, group_config, session
from models import Person as Passport
from flask import request
import json
from vk_api import vk

@app.route('/bot', methods=['POST'])
def bot():
    # Распаковка данных
    data = json.loads(request.data)
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
            # Если пришло сообщение
            if data['type'] == 'message_new':
                message = data['object']['message'] # Объект сообщения
                text = message['text'] # Текст сообщения
                try:
                    payload = json.loads(message['payload']) # Полезная нагрузка
                except:
                    payload = {'command': ''}
                peer_id = message['peer_id'] # Откуда пришло
                from_id = message['from_id'] # Кто прислал
                command_text1 = text.lower().split(' ')[0]

                if Passport.query.filter_by(vk_id=from_id).first() == None:
                    if str(from_id)[0] != '-':
                        session.send_message(peer_id, 'Был найден [id' + str(from_id) + '|незарегистрированный пользователь]!')
                        try:
                            img = session.getUser(from_id)['photo_max']
                            Name = session.getUser(from_id)['first_name']
                            Surname = session.getUser(from_id)['last_name']
                            newUser = Passport(vk_id=from_id, Img=img, Name=Name, Surname=Surname)
                            db.session.add(newUser)
                            db.session.commit()
                            session.send_message(peer_id, 'Пользователь успешно дабавлен в ДБ\nОбратитесь в ЛС к боту!')
                        except:
                            session.send_message(peer_id, "При добавлении пользователя в ДБ, произошла ошибка:\n" + Exception)

                # Только в личных сообщениях
                if peer_id == from_id:
                    if text.lower() == 'start' or text.lower() == 'начать' or payload['command'] == 'start':
                        from keyboards import keyboardStart
                        session.send_message(peer_id, 'Здравия, товарищ для начала, вам нужен паспорт, в сообщении появится кнопка', keyboard=json.dumps(keyboardStart))
                    if text.lower() == 'passport create' or text.lower() == 'паспорт создать' or payload['command'] == 'create_passport':
                        session.send_message(peer_id, 'Что бы редактировать данные в паспорте, есть данные команды:\n"Фамилия (Фамилия)"\n"Имя (Имя)"\n"Отчество (Отчество)"\n"Пол (Пол)"\n"Дата_рождения (Дата рождения)"\n"Место рождения (Место рождения)"\n"Место проживания (Место жительства)"\n"Национальность (Национальность)"\n"Сексуальная ориентация (Сексуальная ориентация)"\n"Фото" и отправить своё фото\nНадеемся, что понятно объяснили!')
                    if command_text1 == 'имя':
                        if text.split(' ')[1]:
                            try:
                                User = Passport.query.filter_by(vk_id=from_id).first()
                                User.Name = text.split(' ')[1:-1]
                                db.session.commit()
                                from keyboards import keyboardChangeAccess
                                session.send_message(peer_id, 'Имя установленно! Ваше имя - ' + text.split(' ')[1:-1], keyboard=json.dumps(keyboardChangeAccess))
                            except:
                                session.send_message(peer_id, 'Произошла ошибка')
                        else:
                            session.send_message(peer_id, 'Введите имя пыжы')
                    if command_text1 == 'фамилия':
                        if text.split(' ')[1]:
                            try:
                                User = Passport.query.filter_by(vk_id=from_id).first()
                                User.Surname = text.split(' ')[1:-1]
                                db.session.commit()
                                from keyboards import keyboardChangeAccess
                                session.send_message(peer_id, 'Фамилия установленна! Ваша фамилия - ' + text.split(' ')[1:-1], keyboard=json.dumps(keyboardChangeAccess))
                            except:
                                session.send_message(peer_id, 'Произошла ошибка')
                        else:
                            session.send_message(peer_id, 'Введите фамилию пыжы')
                    if command_text1 == 'отчество':
                        if text.split(' ')[1]:
                            try:
                                User = Passport.query.filter_by(vk_id=from_id).first()
                                User.Middlename = text.split(' ')[1:-1]
                                db.session.commit()
                                from keyboards import keyboardChangeAccess
                                session.send_message(peer_id, 'Отчество установленно! Ваше отчество - ' + text.split(' ')[1:-1], keyboard=json.dumps(keyboardChangeAccess))
                            except:
                                session.send_message(peer_id, 'Произошла ошибка')
                        else:
                            session.send_message(peer_id, 'Введите отчество пыжы')
                    if command_text1 == 'дата':
                        if text.lower().split(' ')[1] == 'рождения':
                            if text.split(' ')[2]:
                                try:
                                    User = Passport.query.filter_by(vk_id=from_id).first()
                                    User.Data_of_Birth = text.split(' ')[2:-1]
                                    db.session.commit()
                                    from keyboards import keyboardChangeAccess
                                    session.send_message(peer_id, 'Дата рождения установленна! Ваша дата рождения - ' + text.split(' ')[2:-1], keyboard=json.dumps(keyboardChangeAccess))
                                except:
                                    session.send_message(peer_id, 'Произошла ошибка')
                            else:
                                session.send_message(peer_id, 'Введите дату рождения пыжы')
                        else:
                            session.send_message(peer_id, 'Дата чего? Рождения? Ну так и напишите: "Дата рождения (Дата рождения)"')
                    if command_text1 == 'место':
                        if text.lower().split(' ')[1] == 'рождения':
                            if text.split(' ')[2]:
                                try:
                                    User = Passport.query.filter_by(vk_id=from_id).first()
                                    User.Place_of_Birth = text.split(' ')[2:-1]
                                    db.session.commit()
                                    from keyboards import keyboardChangeAccess
                                    session.send_message(peer_id, 'Место рождения установленно! Ваше место рождения - ' + text.split(' ')[2:-1], keyboard=json.dumps(keyboardChangeAccess))
                                except:
                                    session.send_message(peer_id, 'Произошла ошибка')
                            else:
                                session.send_message(peer_id, 'Введите место рождения пыжы')
                        elif text.lower().split(' ')[1] == 'проживания':
                            if text.split(' ')[2]:
                                try:
                                    User = Passport.query.filter_by(vk_id=from_id).first()
                                    User.Place_of_residence = text.split(' ')[2:-1]
                                    db.session.commit()
                                    from keyboards import keyboardChangeAccess
                                    session.send_message(peer_id, 'Место проживания установленно! Ваше место проживания - ' + text.split(' ')[2:-1], keyboard=json.dumps(keyboardChangeAccess))
                                except:
                                    session.send_message(peer_id, 'Произошла ошибка')
                            else:
                                session.send_message(peer_id, 'Введите место проживания пыжы')
                        else:
                            session.send_message(peer_id, 'Место чего? Рождения? Или проживания? Ну так и напишите: "Место рождения (Место рождения)" или "Место проживания (Место проживания)"')
                    if command_text1 == 'национальность' or command_text1 == 'нация' or command_text1 == 'раса':
                        if text.split(' ')[1]:
                            try:
                                User = Passport.query.filter_by(vk_id=from_id).first()
                                User.Nation = text.split(' ')[1]
                                db.session.commit()
                                from keyboards import keyboardChangeAccess
                                session.send_message(peer_id, 'Национальность установленна! Ваша национальность - ' + text.split(' ')[1], keyboard=json.dumps(keyboardChangeAccess))
                            except:
                                session.send_message(peer_id, 'Произошла ошибка')
                        else:
                            session.send_message(peer_id, text='Введите национальность пыжы')
                    if command_text1 == 'сексуальная':
                        if text.lower().split(' ')[1] == 'ориентация':
                            if text.split(' ')[2]:
                                try:
                                    User = Passport.query.filter_by(vk_id=from_id).first()
                                    User.Sexual_Orientation = text.split(' ')[2]
                                    db.session.commit()
                                    from keyboards import keyboardChangeAccess
                                    session.send_message(peer_id, 'Сексуальная ориентация установленна! Ваша сексуальная ориентация - ' + text.split(' ')[2], keyboard=json.dumps(keyboardChangeAccess))
                                except:
                                    session.send_message(peer_id, 'Произошла ошибка')
                            else:
                                session.send_message(peer_id, 'Введите дату рождения пыжы')
                        else:
                            session.send_message(peer_id, 'Да, вы очень сексуальный(ая), но той же вы ориентации? "Сексуальная ориентация (Сексуальная ориентация)"')
                    if command_text1 == 'пол':
                        if text.split(' ')[1]:
                            try:
                                User = Passport.query.filter_by(vk_id=from_id).first()
                                User.Gender = text.split(' ')[1:-1]
                                db.session.commit()
                                from keyboards import keyboardChangeAccess
                                session.send_message(peer_id, 'Пол установленн! Ваш пол - ' + text.split(' ')[1:-1], keyboard=json.dumps(keyboardChangeAccess))
                            except:
                                session.send_message(peer_id, 'Произошла ошибка')
                        else:
                            session.send_message(peer_id, text='Введите пол пыжы')
                    if command_text1 == 'фото':
                        try:
                            img = data['object']['message']['attachments'][0]['photo']['sizes']
                            max_height = 0
                            for size in img:
                                if size['height'] > max_height:
                                    max_height = size['height']
                                    img_url = size['url']
                        except KeyError:
                            session.send_message(peer_id, 'Фото не было найдено.')
                        try:
                            from keyboards import keyboardChangeAccess
                            User = Passport.query.filter_by(vk_id=from_id).first()
                            User.Img = img_url
                            db.session.commit()
                            session.send_message(peer_id, 'Принято! Ссылка на фото:\n\n' + img_url, keyboard=json.dumps(keyboardChangeAccess))
                        except:
                            session.send_message(peer_id, 'Произошла ошибка!')
                    if text.lower() == 'паспорт показать' or text.lower() == 'показать паспорт' or payload['command'] == 'show_passport':
                        try:
                            from passport import createPassport
                            from keyboards import keyboardPassport
                            User = Passport.query.filter_by(vk_id=from_id).first()
                            img = createPassport(User.Name, User.Surname, User.Middlename, User.Gender, User.Data_of_Birth, User.Place_of_Birth, User.Place_of_residence, User.Nation, User.Sexual_Orientation, Photo=str(User.Img))
                            img_id = session.inputIMGMSG(img, peer_id)
                            session.send_message(peer_id, text='Вот ваш паспорт!\nСчёт - ' + str(User.Count) + 'Ŀ !\nVk_ID - ' + str(User.vk_id) + '\nUserID - ' + str(User.id), attachment=img_id, keyboard=json.dumps(keyboardPassport))
                        except Exception as e:
                            session.send_message(peer_id, 'Произошла ошибка!')
                            print(e)
                elif peer_id != from_id:
                    pass

            return 'ok'