import command_system
from models import Person as Passport
from config import db, session

command_category = command_system.CommandCat()
command_category.title = 'Баланс'
command_category.desciption = 'Команды связанные с балансом'

command_bug_report = command_system.Command()
command_bug_report_money = command_system.Command()
command_transition = command_system.Command()
command_gift = command_system.Command()
command_penalty = command_system.Command()

command_category.commands = [command_bug_report, command_bug_report_money,
 command_transition, command_gift, command_penalty, command_transition]

command_bug_report_money.keysp = ['bug_report_money']
command_bug_report_money.show = False
command_bug_report_money.isAdmin = True
command_bug_report_money.desciption = 'Отправляет вознаграждение за баг'

command_bug_report.keysp = ['bug_report']
command_bug_report.show = False
command_bug_report.desciption = 'Отправляет сообщение об баге админу'

command_penalty.keysp = ['penalty']
command_penalty.desciption = 'Оштрафует пользователя'
command_penalty.keysm = ['штраф', 'penalty']
command_penalty.isAdmin = True

command_gift.keysm = ['приз', 'подарок', 'чеканить']
command_gift.keysp = ['gift']
command_gift.desciption = 'Чеканит волюту пользователю'
command_gift.isAdmin = True

command_transition.keysm = ['перевод', 'перевести', 'transition']
command_transition.keysp = ['transition']
command_gift.desciption = 'Перевод пользователю'

def command_bug_report_money(nsv):
    from keyboards import keyboardChangeAccess as keyboard1
    id = nsv['payload']['id']
    attachment = ''
    keyboard = {}
    User = Passport.query.filter_by(id=id).first()
    User.Count += 150
    db.session.commit()
    session.send_message(User.vk_id,
                         'Здравия, так как вы нашли ошибку, вы были вознаграждены 150Ŀ!',
                         keyboard=json.dumps(keyboard1))
    message = 'Вознаграждение отправлено!'
    return message, attachment, keyboard
def command_bug_report(nsv):
    from keyboards import BugReport2 as keyboard1
    attachment = ''
    keyboard = {}
    from_id = command_system.arg['system_vars']['from_id']
    id = Passport.query.filter_by(vk_id=from_id).first().id
    session.send_message(578425189,
                         text='Здравия, была обнаружена ошибка! Обнаржил её [id'+ str(from_id
                         ) +'|данный пользователь]\nhttps://vk.com/gim193840305?sel=' + str(
                             from_id) + '\nНаградить ли его?', keyboard=keyboard1(id))
    message = 'Сообщение администратору бота отправлено, он попытается решить проблему'
    return message, attachment, keyboard
def command_penalty(nsv):
    attachment = ''
    try:
        secondId = int(nsv['words'][0])
    except:
        message = 'Переменная "id" должна быть числом'
        keyboard = {}
        return message, attachment, keyboard
    User = Passport.query.filter_by(id=secondId).first()
    from_id = command_system.arg['system_vars']['from_id']
    if not SecondUser:
        message = 'Пользователь с таким индефикатором не найден'
        keyboard = {}
        return message, attachment, keyboard
    try:
        summ = int(nsv['words'][1])
    except:
        message = 'Переменная "сумма" должна быть числом'
        keyboard = {}
        return message, attachment, keyboard
    from keyboards import fineKeyboard as keyboard1, keyboardChangeAccess as keyboard2
    keyboard = fineKeyboard(User.id)
    User.Count -= summ
    db.session.commit()
    if len(nsv['comments']) <= 0:
        comment = '✉ | Комментария к штрафу нет.'
    else:
        for c in nsv['comments']:
            com = c + '\n'
        com = com[:-1]
        comment = '✉ | Комментарий к штрафу:\n' + com
    session.send_message(User.vk_id, '💸 | Вам штраф в размере ' + str(
        summ) + 'Ŀ!\n💳 | Ваш баланс - ' + str(User.Count) + 'Ŀ\n' + comment, 'keyboard'=keyboard2)
    message = '💸 | Штраф в размере ' + str(summ) + ' оформлен!\nПолучивший штраф - [id' + str(User.vk_id) + '|' + User.Name + ' ' + User.Surname + ']\n💳 | Баланс оштрафованного - ' + str(User.Count) + 'Ŀ\n' + comment
    return message, attachment, keyboard

def command_gift(nsv):
    attachment = ''
    try:
        secondId = int(nsv['words'][0])
    except:
        message = 'Переменная "id" должна быть числом'
        keyboard = {}
        return message, attachment, keyboard
    User = Passport.query.filter_by(id=secondId).first()
    from_id = command_system.arg['system_vars']['from_id']
    if not SecondUser:
        message = 'Пользователь с таким индефикатором не найден'
        keyboard = {}
        return message, attachment, keyboard
    try:
        summ = int(nsv['words'][1])
    except:
        message = 'Переменная "сумма" должна быть числом'
        keyboard = {}
        return message, attachment, keyboard
    from keyboards import fineKeyboard as keyboard1, keyboardChangeAccess as keyboard2
    keyboard = giftKeyboard(User.id)
    User.Count += summ
    db.session.commit()
    if len(nsv['comments']) <= 0:
        comment = '✉ | Комментария к призу нет.'
    else:
        for c in nsv['comments']:
            com = c + '\n'
        com = com[:-1]
        comment = '✉ | Комментарий к призу:\n' + com
    session.send_message('🎁💷 | Вам приз в размере ' + str(
        summ) + 'Ŀ!\n💳 | Ваш баланс - ' + str(User.Count) + 'Ŀ\n' + comment, 'keyboard'=keyboard2)
    message = '🎁💷 | Приз в размере ' + str(summ) + ' оформлен!\nПолучивший приз - [id' + str(User.vk_id) + '|' + User.Name + ' ' + User.Surname + ']\n💳 | Баланс получившего - ' + str(User.Count) + 'Ŀ\n' + comment
    return message, attachment, keyboard
def command_transition(nsv):
    attachment = ''
    FirstUser = Passport.query.filter_by(vk_id=from_id).first()
    try:
        secondId = int(nsv['words'][0])
    except:
        message = 'Переменная "id" должна быть числом'
        keyboard = {}
        return message, attachment, keyboard
    SecondUser = Passport.query.filter_by(id=secondId).first()
    from_id = command_system.arg['system_vars']['from_id']
    if not SecondUser:
        message = 'Пользователь с таким индефикатором не найден'
        keyboard = {}
        return message, attachment, keyboard
    if peer_id == SecondUser.vk_id:
        message = 'Самому себе нельзя переводить'
        keyboard = {}
        return message, attachment, keyboard
    try:
        summ = int(nsv['words'][1])
    except:
        message = 'Переменная "сумма" должна быть числом'
        keyboard = {}
        return message, attachment, keyboard
    if int(nsv['words'][1]) < FirstUser.Count:
        message = 'Сумма слишком большая для вашего баланса'
        keyboard = {}
        return message, attachment, keyboard
    from keyboards import keyboardTransfer1, keyboardTransfer2
    keyboard = keyboardTransfer1(SecondUser.id)
    keyboard2 = keyboardTransfer2(FirstUser.id)
    FirstUser.Count -= summ
    SecondUser.Count += summ
    db.session.commit()
    if len(nsv['comments']) <= 0:
        comment = '✉ | Комментария к переводу нет.'
    else:
        for c in nsv['comments']:
            com = c + '\n'
        com = com[:-1]
        comment = '✉ | Комментарий к переводу:\n' + com
    session.send_message(SecondUser.vk_id, '💳 | [id' + str(SecondUser.vk_id) + '|' + SecondUser.Name + ' ' + SecondUser.Surname + '], к вам пришел перевод в размере ' + str(summ) + 'Ŀ!\nОт [id' + str(from_id) + '|' + FirstUser.Name + ' ' + FirstUser.Surname + ']\n💳 | Ваш баланс - ' + str(SecondUser.Count) + '\n💳 | Баланс переводившего - ' + str(FirstUser.Count) + '\n' + comment, 'keyboard'=keyboard2)
    message = '💳✔ | Перевод в сумму ' + str(summ) + 'Ŀ - успешно совершен!\n[id' + str(SecondUser.vk_id) + '|' + SecondUser.Name + ' ' + SecondUser.Surname + '] - Тот, кому вы перевели Ŀ\n💳 | Ваш баланс - ' + str(FirstUser.Count) + '\n💳 | Баланс получившего - ' + str(SecondUser.Count) + '\n' + comment
    return message, attachment, keyboard

command_bug_report_money.process = command_bug_report_money
command_bug_report.process = command_bug_report
command_penalty.process = command_penalty
command_gift.process = command_gift
command_transition.process = command_transition
