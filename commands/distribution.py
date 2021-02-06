import command_system
from models import Person as Passport
from config import db, group_config

command_cat = command_system.CommandCat()
command_cat.title = 'Уведомления'
command_cat.description = 'Команды связанные с уведомлениями'

command_distribution = command_system.Command()
command_admin = command_system.Command()

command_cat.commands = [
    command_distribution,
    command_admin
]

def distribution(nsv):
    from_id = command_system.arg['system_vars']['from_id']
    User = Passport.query.filter_by(vk_id=from_id).first()
    if User.distribution:
        User.distribution = False
        db.session.commit()
        message =  ' ❌📢 | Уведомления были отключены'
    else:
        User.distribution = True
        db.session.commit()
        message =  ' ✅📢 | Уведомления были включены'
    attachment = ''
    keyboard = {}
    return message, attachment, keyboard

command_distribution.keysm = ['рассылка', 'distribution', 'sending']
command_distribution.keysp = ['distribution']
command_distribution.desciption = 'Отключает/включает рассылку'
command_distribution.process = distribution

def admin(nsv):
    if len(nsv['comments']) <= 0:
        comment = '✉ | Вопроса заранее нет.'
    else:
        for c in nsv['comments']:
            com = c + '\n'
        com = com[:-1]
        comment = '✉ | Вопрос заранее:\n' + com
    for a in group_config['admin_ids']:
        session.send_message(a, text = 'Здравия, вас зовут!\nhttps://vk.com/gim193840305?sel=' + str(from_id) + '\n' + comment)
    message = "Уведомления разосланы админам"
    attachment = ''
    keyboard = {}
    return message, attachment, keyboard
command_admin.keysm = ['admin', 'админ', 'позовите админа']
command_admin.keysp = ['admin']
command_admin.desciption = 'Позвать админа'
command_admin.process = admin
