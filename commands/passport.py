import command_system
from models import Person as Passport
from config import db

command_distribution = command_system.Command()

def name(nsv):
    attachment = ''
    keyboard = {}
    from_id = command_system.arg['system_vars']['from_id']
    User = Passport.query.filter_by(vk_id=from_id).first()
    new_name = ''
    try:
        if nsv:
            for n in nsv[1:]:
                new_name += n + ' '
            name = new_name[:-1]
    except:
        message = 'Имя не найдено а переменных сообщения, пожайлуста напишите имя в сообщении\np.s. Убедитесь в том что у вас нет лишних пробелов!'
        return message, attachment, keyboard
    User.Name = name
    db.session.commit()
    message = 'Имя [id' + str(from_id) + '|пользователя] установленно как ' + name + '!'
    return message, attachment, keyboard

command_distribution.keysm = ['name', 'имя']
command_distribution.keysp = ['set_name']
command_distribution.desciption = 'Устанавивает ваше имя в паспорте'
command_distribution.process = name
