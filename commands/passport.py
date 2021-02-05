import command_system
from models import Person as Passport
from config import db, session
from keyboards import keyboardChangeAccess as keyboard

command_cat = command_system.CommandCat()
command_cat.title = 'Паспротные'
command_cat.description = 'Команды связанные напрямую с паспортом'

command_name = command_system.Command()
command_surname = command_system.Command()
command_middlename = command_system.Command()
command_dob = command_system.Command()
command_pob = command_system.Command()
command_por = command_system.Command()
command_nation = command_system.Command()
command_sexual_orientation = command_system.Command()
command_gender = command_system.Command()
command_photo = command_system.Command()
command_show = command_system.Command()

command_cat.commands = [
    command_name,
    command_surname,
    command_middlename,
    command_dob,
    command_pob,
    command_por,
    command_nation,
    command_sexual_orientation,
    command_gender,
    command_photo,
    command_show
]
def name(nsv):
    print(nsv)
    attachment = ''
    from_id = command_system.arg['system_vars']['from_id']
    User = Passport.query.filter_by(vk_id=from_id).first()
    new_name = ''
    namevar = ''
    if len(nsv['words']) >= 1:
        for n in nsv['words']:
            new_name += n + ' '
        namevar = new_name[:-1]
    else:
        keyboard = {}
        message = 'Имя не найдено а переменных сообщения, пожайлуста напишите имя в сообщении\np.s. Убедитесь в том что у вас нет лишних пробелов!'
        return message, attachment, keyboard
    User.Name = namevar
    db.session.commit()
    message = 'Имя [id' + str(from_id) + '|пользователя] установленно как ' + namevar + '!'
    return message, attachment, keyboard

command_name.keysm = ['name', 'имя']
command_name.keysp = ['set_name']
command_name.desciption = 'Устанавивает ваше имя в паспорте'
command_name.process = name

def surname(nsv):
    print(nsv)
    attachment = ''
    from_id = command_system.arg['system_vars']['from_id']
    User = Passport.query.filter_by(vk_id=from_id).first()
    new_name = ''
    namevar = ''
    if len(nsv['words']) >= 1:
        for n in nsv['words']:
            new_name += n + ' '
        namevar = new_name[:-1]
    else:
        keyboard = {}
        message = 'Фамилия не найдено а переменных сообщения, пожайлуста напишите фамилия в сообщении\np.s. Убедитесь в том что у вас нет лишних пробелов!'
        return message, attachment, keyboard
    User.Surname = namevar
    db.session.commit()
    message = 'Фамилия [id' + str(from_id) + '|пользователя] установленна как ' + namevar + '!'
    return message, attachment, keyboard

command_surname.keysm = ['surname', 'фамилия']
command_surname.keysp = ['set_surname']
command_surname.desciption = 'Устанавивает вашу фамилию в паспорте'
command_surname.process = surname

def middlename(nsv):
    print(nsv)
    attachment = ''
    from_id = command_system.arg['system_vars']['from_id']
    User = Passport.query.filter_by(vk_id=from_id).first()
    new_name = ''
    namevar = ''
    if len(nsv['words']) >= 1:
        for n in nsv['words']:
            new_name += n + ' '
        namevar = new_name[:-1]
    else:
        keyboard = {}
        message = 'Отчество не найдено а переменных сообщения, пожайлуста напишите отчество в сообщении\np.s. Убедитесь в том что у вас нет лишних пробелов!'
        return message, attachment, keyboard
    User.Middlename = namevar
    db.session.commit()
    message = 'Отчество [id' + str(from_id) + '|пользователя] установленно как ' + namevar + '!'
    return message, attachment, keyboard

command_middlename.keysm = ['middlename', 'отчество']
command_middlename.keysp = ['set_middlename']
command_middlename.desciption = 'Устанавивает ваше отчество в паспорте'
command_middlename.process = middlename
def dob(nsv):
    print(nsv)
    attachment = ''
    from_id = command_system.arg['system_vars']['from_id']
    User = Passport.query.filter_by(vk_id=from_id).first()
    new_name = ''
    namevar = ''
    if len(nsv['words']) >= 1:
        for n in nsv['words']:
            new_name += n + ' '
        namevar = new_name[:-1]
    else:
        keyboard = {}
        message = 'Дата рождения не найдено а переменных сообщения, пожайлуста напишите дата рождения в сообщении\np.s. Убедитесь в том что у вас нет лишних пробелов!'
        return message, attachment, keyboard
    User.Data_of_Birth = namevar
    db.session.commit()
    message = 'Дата рождения [id' + str(from_id) + '|пользователя] установленна как ' + namevar + '!'
    return message, attachment, keyboard

command_dob.keysm = ['дата рождения', 'date of birth', 'dob', 'др', 'дата']
command_dob.keysp = ['set_dob']
command_dob.desciption = 'Устанавивает вашу дату рождения в паспорте'
command_dob.process = dob
def Place_of_Birth(nsv):
    print(nsv)
    attachment = ''
    from_id = command_system.arg['system_vars']['from_id']
    User = Passport.query.filter_by(vk_id=from_id).first()
    new_name = ''
    namevar = ''
    if len(nsv['words']) >= 1:
        for n in nsv['words']:
            new_name += n + ' '
        namevar = new_name[:-1]
    else:
        message = 'Место рождения не найдено а переменных сообщения, пожайлуста напишите место рождения в сообщении\np.s. Убедитесь в том что у вас нет лишних пробелов!'
        return message, attachment, keyboard
    User.Place_of_Birth = namevar
    db.session.commit()
    message = 'Место рождения [id' + str(from_id) + '|пользователя] установленно как ' + namevar + '!'
    return message, attachment, keyboard

command_pob.keysm = ['place of birth', 'место рождения', 'pob']
command_pob.keysp = ['set_pob']
command_pob.desciption = 'Устанавивает вашу фамилию в паспорте'
command_pob.process = Place_of_Birth
def Place_of_residence(nsv):
    print(nsv)
    attachment = ''
    from_id = command_system.arg['system_vars']['from_id']
    User = Passport.query.filter_by(vk_id=from_id).first()
    new_name = ''
    namevar = ''
    if len(nsv['words']) >= 1:
        for n in nsv['words']:
            new_name += n + ' '
        namevar = new_name[:-1]
    else:
        keyboard = {}
        message = 'Место проживания не найдено а переменных сообщения, пожайлуста напишите место проживания в сообщении\np.s. Убедитесь в том что у вас нет лишних пробелов!'
        return message, attachment, keyboard
    User.Place_of_residence = namevar
    db.session.commit()
    message = 'Место проживания [id' + str(from_id) + '|пользователя] установленно как ' + namevar + '!'
    return message, attachment, keyboard

command_por.keysm = ['place of residence', 'место проживания', 'место жительства', 'por']
command_por.keysp = ['set_por']
command_por.desciption = 'Устанавивает ваше место проживание в паспорте'
command_por.process = Place_of_residence
def Gender(nsv):
    print(nsv)
    attachment = ''
    from_id = command_system.arg['system_vars']['from_id']
    User = Passport.query.filter_by(vk_id=from_id).first()
    new_name = ''
    namevar = ''
    if len(nsv['words']) >= 1:
        for n in nsv['words']:
            new_name += n + ' '
        namevar = new_name[:-1]
    else:
        keyboard = {}
        message = 'Пол не найдено а переменных сообщения, пожайлуста напишите пол в сообщении\np.s. Убедитесь в том что у вас нет лишних пробелов!'
        return message, attachment, keyboard
    User.Gender = namevar
    db.session.commit()
    message = 'Пол [id' + str(from_id) + '|пользователя] установлен как ' + namevar + '!'
    return message, attachment, keyboard

command_gender.keysm = ['gender', 'пол']
command_gender.keysp = ['set_gender']
command_gender.desciption = 'Устанавивает ваш пол в паспорте'
command_gender.process = Gender
def nation(nsv):
    print(nsv)
    attachment = ''
    from_id = command_system.arg['system_vars']['from_id']
    User = Passport.query.filter_by(vk_id=from_id).first()
    new_name = ''
    namevar = ''
    if len(nsv['words']) >= 1:
        for n in nsv['words']:
            new_name += n + ' '
        namevar = new_name[:-1]
    else:
        keyboard = {}
        message = 'Национальность не найдено а переменных сообщения, пожайлуста напишите национальность в сообщении\np.s. Убедитесь в том что у вас нет лишних пробелов!'
        return message, attachment, keyboard
    User.Nation = namevar
    db.session.commit()
    message = 'Национальность [id' + str(from_id) + '|пользователя] установленна как ' + namevar + '!'
    return message, attachment, keyboard

command_nation.keysm = ['nation', 'нация', 'национальность']
command_nation.keysp = ['set_nation']
command_nation.desciption = 'Устанавивает вашу национальность в паспорте'
command_nation.process = nation
def sex_orien(nsv):
    print(nsv)
    attachment = ''
    from_id = command_system.arg['system_vars']['from_id']
    User = Passport.query.filter_by(vk_id=from_id).first()
    new_name = ''
    namevar = ''
    if len(nsv['words']) >= 1:
        for n in nsv['words']:
            new_name += n + ' '
        namevar = new_name[:-1]
    else:
        keyboard = {}
        message = 'Секс. Оринтация не найдено а переменных сообщения, пожайлуста напишите секс. ориентацию в сообщении\np.s. Убедитесь в том что у вас нет лишних пробелов!'
        return message, attachment, keyboard
    User.Sexual_Orientation = namevar
    db.session.commit()
    message = 'Секс. Ориентация [id' + str(from_id) + '|пользователя] установленна как ' + namevar + '!'
    return message, attachment, keyboard

command_sexual_orientation.keysm = ['sexual orientation', 'сексуальная ориентация']
command_sexual_orientation.keysp = ['set_sex_orien']
command_sexual_orientation.desciption = 'Устанавивает вашу сексуальяную ориентацию в паспорте'
command_sexual_orientation.process = sex_orien
def photo(nsv):
    print(nsv)
    attachment = ''
    if not nsv['attachment']:
        keyboard = {}
        message = "Нет вложений"
        return message, attachment, keyboard
    else:
        photo = {}
        for attachment in nsv['attachment']:
            if attachment['type'] == "photo":
                photo = attachment['photo']
                break;
        else:
            keyboard = {}
            message = "Фото не было прикреплено"
            return message, attachment, keyboard
    max_height = 0
    photo_url = ''
    for size in photo['sizes']:
        if size['height'] > max_height:
            max_height = size['height']
            photo_url = size['url']
    User.Img = photo_url
    db.session.commit()
    message = 'Принято! Ссылка на фото:\n\n' + photo_url
    attachment = 'photo' + str(photo['owner_id']) + '_' + str(photo['id'])
    return message, attachment, keyboard
command_photo.keysm = ['photo', 'фото', 'изображение', 'img']
command_photo.keysp = ['set_photo']
command_photo.desciption = 'Устанавивает ваше фото в паспорте'
command_photo.process = photo
def show(nsv):
    print(nsv)
    keyboard = {}
    from_id = command_system.arg['system_vars']['from_id']
    session.send_message(from_id, 'Пожайлуста подождите⌛.\nПаспорту нужно время на обработку.')
    print(nsv)
    if nsv['isPayload']:
        try:
            id = nsv['payload']['id']
        except:
            id = Passport.query.filter_by(vk_id=from_id).first().id
    else:
        try:
            id = nsv['words'][0]
        except:
            id = Passport.query.filter_by(vk_id=from_id).first().id
    from passport import createPassport
    User = Passport.query.filter_by(id=id).first()
    if not User:
        keyboard = {}
        message = 'Пользователь с таким индефикатором не найден'
        return message, attachment, keyboard
    img = createPassport(User.Name, User.Surname, User.Middlename, User.Gender, User.Data_of_Birth, User.Place_of_Birth, User.Place_of_residence, User.Nation, User.Sexual_Orientation, Photo=str(User.Img))
    attachment = session.inputIMGMSG(img, peer_id)
    if User.vk_id == from_id:
        from keyboards import keyboardPassport as keyboard
        message = 'Вот ваш паспорт!\nСчёт - ' + str(User.Count) + 'Ŀ !\nVk_ID - ' + str(User.vk_id) + '\nUserID - ' + str(User.id)
    else:
        message = 'Вот паспорт пользователя [id' + str(User.vk_id) + '|' + User.Name + ' ' + User.Surname + '] !\nСчёт - ' + str(User.Count) + 'Ŀ !\nVk_ID - ' + str(User.vk_id) + '\nUserID - ' + str(User.id)
    return message, attachment, keyboard
command_show.keysm = ['passport', 'паспорт', 'показать паспорт', 'паспорт показать', 'passport show']
command_show.keysp = ['show_passport']
command_show.desciption = 'Покажет паспорт'
command_show.process = show
