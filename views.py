from config import app, db, group_config, session, session_papochka
from models import Person as Passport
from flask import request
import json
from vk_api import vk
import random
from messages_handler import create_answer

def exceptionHelp (e, peer_id):
    from keyboards import BugReport1 as keyboard
    print(e)
    session.send_message(peer_id, 'Жесть, ошибка!', keyboard=json.dumps(keyboard))

@app.route('/bot', methods=['POST'])
async def bot():
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
                command_text1 = text.lower().split('\n')[0].split(' ')[0]
                try:
                    command_text2 = text.lower().split('\n')[0].split(' ')[1]
                except:
                    command_text2 = ''

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

                # Только в личных сообщениях
                if peer_id == from_id:
                    if text.lower() == 'start' or text.lower() == 'начать' or payload['command'] == 'start':
                        from keyboards import keyboardStart
                        session.send_message(peer_id, 'Здравия, товарищ для начала, вам нужен паспорт, в сообщении появится кнопка', keyboard=json.dumps(keyboardStart))
                    if text.lower() == 'passport create' or text.lower() == 'паспорт создать' or payload['command'] == 'create_passport' or text.lower() == 'паспорт изменить' or text.lower() == 'изменить паспорт' or text.lower() == 'создать паспорт':
                        session.send_message(peer_id, 'Что бы редактировать данные в паспорте, есть данные команды:\n"Фамилия (Фамилия)"\n"Имя (Имя)"\n"Отчество (Отчество)"\n"Пол (Пол)"\n"Дата рождения (Дата рождения)"\n"Место рождения (Место рождения)"\n"Место проживания (Место жительства)"\n"Национальность (Национальность)"\n"Сексуальная ориентация (Сексуальная ориентация)"\n"Фото" и отправить своё фото\nНадеемся, что понятно объяснили!')
                    if command_text1 == 'фамилия':
                        if text.split(' ')[1]:
                            try:
                                User = Passport.query.filter_by(vk_id=from_id).first()
                                User.Surname = ' '.join(text.split(' ')[1:])
                                db.session.commit()
                                from keyboards import keyboardChangeAccess
                                session.send_message(peer_id, 'Фамилия установленна! Ваша фамилия - ' + ' '.join(text.split(' ')[1:]), keyboard=json.dumps(keyboardChangeAccess))
                            except Exception as e:
                                exceptionHelp(e, peer_id)
                        else:
                            session.send_message(peer_id, 'Введите фамилию пыжы')
                    if command_text1 == 'отчество':
                        if text.split(' ')[1]:
                            try:
                                User = Passport.query.filter_by(vk_id=from_id).first()
                                User.Middlename = ' '.join(text.split(' ')[1:])
                                db.session.commit()
                                from keyboards import keyboardChangeAccess
                                session.send_message(peer_id, 'Отчество установленно! Ваше отчество - ' + ' '.join(text.split(' ')[1:]), keyboard=json.dumps(keyboardChangeAccess))
                            except Exception as e:
                                exceptionHelp(e, peer_id)
                        else:
                            session.send_message(peer_id, 'Введите отчество пыжы')
                    if command_text1 == 'дата':
                        if text.lower().split(' ')[1] == 'рождения':
                            if text.split(' ')[2]:
                                try:
                                    User = Passport.query.filter_by(vk_id=from_id).first()
                                    User.Data_of_Birth = ' '.join(text.split(' ')[2:])
                                    db.session.commit()
                                    from keyboards import keyboardChangeAccess
                                    session.send_message(peer_id, 'Дата рождения установленна! Ваша дата рождения - ' + ' '.join(text.split(' ')[2:]), keyboard=json.dumps(keyboardChangeAccess))
                                except Exception as e:
                                    exceptionHelp(e, peer_id)
                            else:
                                session.send_message(peer_id, 'Введите дату рождения пыжы')
                        else:
                            session.send_message(peer_id, 'Дата чего? Рождения? Ну так и напишите: "Дата рождения (Дата рождения)"')
                    if command_text1 == 'место':
                        if text.lower().split(' ')[1] == 'рождения':
                            if text.split(' ')[2]:
                                try:
                                    User = Passport.query.filter_by(vk_id=from_id).first()
                                    User.Place_of_Birth = ' '.join(text.split(' ')[2:])
                                    db.session.commit()
                                    from keyboards import keyboardChangeAccess
                                    session.send_message(peer_id, 'Место рождения установленно! Ваше место рождения - ' + ' '.join(text.split(' ')[2:]), keyboard=json.dumps(keyboardChangeAccess))
                                except Exception as e:
                                    exceptionHelp(e, peer_id)
                            else:
                                session.send_message(peer_id, 'Введите место рождения пыжы')
                        elif text.lower().split(' ')[1] == 'проживания':
                            if text.split(' ')[2]:
                                try:
                                    User = Passport.query.filter_by(vk_id=from_id).first()
                                    User.Place_of_residence = ' '.join(text.split(' ')[2:])
                                    db.session.commit()
                                    from keyboards import keyboardChangeAccess
                                    session.send_message(peer_id, 'Место проживания установленно! Ваше место проживания - ' + ' '.join(text.split(' ')[2:]), keyboard=json.dumps(keyboardChangeAccess))
                                except Exception as e:
                                    exceptionHelp(e, peer_id)
                            else:
                                session.send_message(peer_id, 'Введите место проживания пыжы')
                        else:
                            session.send_message(peer_id, 'Место чего? Рождения? Или проживания? Ну так и напишите: "Место рождения (Место рождения)" или "Место проживания (Место проживания)"')
                    if command_text1 == 'национальность' or command_text1 == 'нация' or command_text1 == 'раса':
                        if text.split(' ')[1]:
                            try:
                                User = Passport.query.filter_by(vk_id=from_id).first()
                                User.Nation = ' '.join(text.split(' ')[1:])
                                db.session.commit()
                                from keyboards import keyboardChangeAccess
                                session.send_message(peer_id, 'Национальность установленна! Ваша национальность - ' + ' '.join(text.split(' ')[1:]), keyboard=json.dumps(keyboardChangeAccess))
                            except Exception as e:
                                exceptionHelp(e, peer_id)
                        else:
                            session.send_message(peer_id, text='Введите национальность пыжы')
                    if command_text1 == 'сексуальная':
                        if text.lower().split(' ')[1] == 'ориентация':
                            if text.split(' ')[2]:
                                try:
                                    User = Passport.query.filter_by(vk_id=from_id).first()
                                    User.Sexual_Orientation = ' '.join(text.split(' ')[2:])
                                    db.session.commit()
                                    from keyboards import keyboardChangeAccess
                                    session.send_message(peer_id, 'Сексуальная ориентация установленна! Ваша сексуальная ориентация - ' + ' '.join(text.split(' ')[2:]), keyboard=json.dumps(keyboardChangeAccess))
                                except Exception as e:
                                    exceptionHelp(e, peer_id)
                            else:
                                session.send_message(peer_id, 'Введите дату рождения пыжы')
                        else:
                            session.send_message(peer_id, 'Да, вы очень сексуальный(ая), но той же вы ориентации? "Сексуальная ориентация (Сексуальная ориентация)"')
                    if command_text1 == 'пол':
                        if text.split(' ')[1]:
                            try:
                                User = Passport.query.filter_by(vk_id=from_id).first()
                                User.Gender = ' '.join(text.split(' ')[1:])
                                db.session.commit()
                                from keyboards import keyboardChangeAccess
                                session.send_message(peer_id, 'Пол установленн! Ваш пол - ' + ' '.join(text.split(' ')[1:]), keyboard=json.dumps(keyboardChangeAccess))
                            except Exception as e:
                                exceptionHelp(e, peer_id)
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
                        except Exception as e:
                            exceptionHelp(e, peer_id)
                    if command_text1 + ' ' + command_text2 == 'паспорт показать' or command_text1 + ' ' + command_text2 == 'показать паспорт' or payload['command'] == 'show_passport':
                        session.send_message(peer_id, 'Пожайлуста подождите⌛.\nПаспорту нужно время на обработку.')
                        if payload['command'] != 'show_passport':
                            try:
                                id = int(text.lower().split(' ')[2])
                            except:
                                id = Passport.query.filter_by(vk_id=from_id).first().id
                        elif payload['command'] == 'show_passport':
                            try:
                                id = payload['id']
                            except:
                                id = Passport.query.filter_by(vk_id=from_id).first().id
                        try:
                            from passport import createPassport
                            from keyboards import keyboardPassport
                            User = Passport.query.filter_by(id=id).first()
                            if User == None:
                                session.send_message(peer_id, text='Пользователь с таким ID не найден!')
                            else:
                                img = createPassport(User.Name, User.Surname, User.Middlename, User.Gender, User.Data_of_Birth, User.Place_of_Birth, User.Place_of_residence, User.Nation, User.Sexual_Orientation, Photo=str(User.Img))
                                img_id = session.inputIMGMSG(img, peer_id)
                                if User.vk_id == from_id:
                                    session.send_message(peer_id, text='Вот ваш паспорт!\nСчёт - ' + str(
                                        User.Count) + 'Ŀ !\nVk_ID - ' + str(User.vk_id) + '\nUserID - ' + str(User.id),
                                                         attachment=img_id, keyboard=json.dumps(keyboardPassport))
                                else:
                                    session.send_message(peer_id, text='Вот паспорт пользователя [id' + str(
                                        User.vk_id) + '|' + User.Name + ' ' + User.Surname + '] !\nСчёт - ' + str(
                                        User.Count) + 'Ŀ !\nVk_ID - ' + str(User.vk_id) + '\nUserID - ' + str(User.id),
                                                         attachment=img_id)
                        except Exception as e:
                            exceptionHelp(e, peer_id)
                    if command_text1 == 'перевести':
                        try:
                            FirstUser = Passport.query.filter_by(vk_id=from_id).first()
                            SecondUser = Passport.query.filter_by(id=int(text.split('\n')[0].split(' ')[1])).first()
                            if SecondUser == None:
                                session.send_message(peer_id, text='Пользователь с таким ID не найден!')
                            else:
                                if peer_id != SecondUser.vk_id:
                                    summ = int(text.split('\n')[0].split(' ')[2])
                                    if FirstUser.Count >= summ:
                                        FirstUser.Count = FirstUser.Count - summ
                                        SecondUser.Count = SecondUser.Count + summ
                                        db.session.commit()
                                        try:
                                            if len(text.split('\n')[1]) > 0:
                                                comment = '✉ | Комментарий к переводу: ' + text.split('\n')[1]
                                            else:
                                                comment = '✉ | Комментария к переводу нет.'
                                        except IndexError as e:
                                            comment = '✉ | Комментария к переводу нет.'
                                        from keyboards import keyboardTransfer1 as keyboard1
                                        from keyboards import keyboardTransfer2 as keyboard2
                                        session.send_message(peer_id, '💳✔ | Перевод в сумму ' + str(
                                            summ) + 'Ŀ - успешно совершен!\n[id' + str(
                                            SecondUser.vk_id) + '|' + SecondUser.Name + ' ' + SecondUser.Surname + '] - Тот, кому вы перевели Ŀ\n💳 | Ваш баланс - ' + str(
                                            FirstUser.Count) + '\n💳 | Баланс получившего - ' + str(
                                            SecondUser.Count) + '\n' + comment,
                                                             keyboard=json.dumps(keyboard1(SecondUser.id)))
                                        session.send_message(
                                            SecondUser.vk_id, '💳 | [id' + str(
                                                SecondUser.vk_id) + '|' + SecondUser.Name + ' ' + SecondUser.Surname + '], к вам пришел перевод в размере ' + str(
                                            summ) + 'Ŀ!\nОт [id' + str(
                                                from_id) + '|' + FirstUser.Name + ' ' + FirstUser.Surname + ']\n💳 | Ваш баланс - ' + str(
                                            SecondUser.Count) + '\n💳 | Баланс переводившего - ' + str(
                                            FirstUser.Count) + '\n' + comment,
                                            keyboard=json.dumps(keyboard2(FirstUser.id)))
                                    else:
                                        session.send_message(peer_id,
                                                             text='💳❌ | У вас сумма перевода больше, чем у вас имеется на счету денег.')
                                else:
                                    session.send_message(peer_id, text='💳❌ | Вы не можите перевести самому себе')
                        except Exception as e:
                            exceptionHelp(e, peer_id)
                    if text.lower().split('\n')[0] == 'позовите админа':
                        session.send_message(peer_id, 'Зовём-зовём. Ждите админа.')
                        try:
                            if len(text.split('\n')[1]) > 0:
                                comment = '✉ | Вопрос заранее: ' + text.split('\n')[1]
                            else:
                                comment = '✉ | Вопроса заранее нет.'
                        except IndexError as e:
                            comment = '✉ | Вопроса заранее нет.'
                        for a in group_config['admin_ids']:
                            session.send_message(a,
                                                 text = 'Здравия, вас зовут!\nhttps://vk.com/gim193840305?sel=' + str(from_id) + '\n' + comment)
                    if payload['command'] == 'bug_report':
                        from keyboards import BugReport2 as keyboard
                        id = Passport.query.filter_by(vk_id=from_id).first().id
                        session.send_message(578425189,
                                             text='Здравия, была обнаружена ошибка! Обнаржил её [id'+ str(from_id
                                             ) +'|данный пользователь]\nhttps://vk.com/gim193840305?sel=' + str(
                                                 from_id) + '\nНаградить ли его?', keyboard=json.dumps(keyboard(id)))
                        session.send_message(peer_id, 'Сообщение администратору бота отправлено, он попытается решить проблемму')
                    if payload['command'] == 'bug_report_money':
                        try:
                            id = payload['id']
                            summ = 150
                            User = Passport.query.filter_by(id=id).first()
                            User.Count = User.Count + summ
                            db.session.commit()
                            from keyboards import keyboardChangeAccess as keyboard
                            session.send_message(User.vk_id,
                                                 'Здравия, так как вы нашли ошибку, вы были вознаграждены 150Ŀ!',
                                                 keyboard=json.dumps(keyboard))
                            session.send_message(peer_id, 'Вознаграждение отправлено!')
                        except Exception as e:
                            exceptionHelp(e, peer_id)
                    if text.lower() == 'ладно ок ладно':
                        from keyboards import BugReport1 as keyboard
                        session.send_message(peer_id, 'Жесть, ошибка!', keyboard=json.dumps(keyboard))
                    if command_text1 == 'штраф':
                        if from_id in group_config['admin_ids']:
                            User = Passport.query.filter_by(id=int(text.split('\n')[0].split(' ')[1])).first()
                            summ = int(text.split('\n')[0].split(' ')[2])
                            if User == None:
                                session.send_message(peer_id, 'Пользователя с таким id нет!')
                            else:
                                try:
                                    comment = '✉ | Комментарий к штрафу: ' + text.split('\n')[1]
                                except IndexError as e:
                                    comment = '✉ | Комментария к штрафу нет.'
                                try:
                                    User.Count = User.Count - summ
                                    db.session.commit()
                                    from keyboards import fineKeyboard as keyboard1
                                    from keyboards import keyboardChangeAccess as keyboard2
                                    session.send_message(peer_id, '💸 | Штраф в размере ' + str(
                                        summ) + ' оформлен!\nПоучивший штраф - [id' + str(
                                        User.vk_id) + '|' + User.Name + ' ' + User.Surname + ']\n💳 | Баланс оштрафованного - ' + str(
                                        User.Count) + 'Ŀ\n' + comment,
                                        keyboard=json.dumps(keyboard1(User.id)))
                                    session.send_message(User.vk_id, '💸 | Вам штраф в размере ' + str(
                                        summ) + 'Ŀ!\n💳 | Ваш баланс - ' + str(User.Count) + 'Ŀ\n' + comment,
                                        keyboard=json.dumps(keyboard2))
                                except Exception as e:
                                    exceptionHelp(e, peer_id)
                    if command_text1 == 'приз':
                        if from_id in group_config['admin_ids']:
                            User = Passport.query.filter_by(id=int(text.split('\n')[0].split(' ')[1])).first()
                            summ = int(text.split('\n')[0].split(' ')[2])
                            if User == None:
                                session.send_message(peer_id, 'Пользователя с таким id нет!')
                            else:
                                try:
                                    comment = '✉ | Комментарий к призу: ' + text.split('\n')[1]
                                except IndexError as e:
                                    comment = '✉ | Комментария к призу нет.'
                                try:
                                    User.Count = User.Count + summ
                                    db.session.commit()
                                    from keyboards import fineKeyboard as keyboard1
                                    from keyboards import keyboardChangeAccess as keyboard2
                                    session.send_message(peer_id, '🎁💷 | Приз в размере ' + str(
                                        summ) + ' оформлен!\nПоучивший приз - [id' + str(
                                        User.vk_id) + '|' + User.Name + ' ' + User.Surname + ']\n💳 | Баланс получившего - ' + str(
                                        User.Count) + 'Ŀ\n' + comment,
                                                         keyboard=json.dumps(keyboard1(User.id)))
                                    session.send_message(User.vk_id, '🎁💷 | Вам приз в размере ' + str(
                                        summ) + 'Ŀ!\n💳 | Ваш баланс - ' + str(User.Count) + 'Ŀ\n' + comment,
                                                         keyboard=json.dumps(keyboard2))
                                except Exception as e:
                                    exceptionHelp(e, peer_id)
                        else:
                            session.send_message(peer_id, '🙍‍♂️❌ | У вас недостаточнго прав!')
                    await create_answer(message, session)

                elif peer_id != from_id:
                    pass
            if data['type'] == 'group_leave':
                pidaras_id = data['object']['user_id']
                pidaras_info = session.getUser(pidaras_id)
                Name = pidaras_info['first_name']
                Surname = pidaras_info['last_name']
                fragment_message = random.choice(['чекай свою мамку.', 'слит.', 'вернись, либо пидорас.', 'ты окаался, как и твой батя, лохом, геем, пидором.', 'вернись.'])
                message = '[id' + str(pidaras_id) + '|' + Name + ' ' + Surname + '], ' + fragment_message
                session_papochka.BoardCreateComment(group_id=group_config['id'], topic_id=46593350, message=message)
            if data['type'] == 'wall_post_new':
                if str(data['object']['from_id'])[0] == '-':
                    distribution_users = Passport.query.filter_by(distribution=True).all()
                    for user in distribution_users:
                        session.send_message(user.vk_id, '📢 | Новый пост в нашей группе!', attachment='wall' + str(data['object']['owner_id']) + '_' + str(data['object']['id']))
            return 'ok', 200
