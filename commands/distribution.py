import command_system
from models import Person as Passport
from config import db

def distribution():
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
    keuboard = {}
    return message, attachment, keyboard

command_distribution = command_system.Command()
command_distribution.keysm = ['рассылка', 'distribution']
command_distribution.keysp = ['distribution']
command_distribution.desciption = 'Отключает/включает рассылку'
command_distribution.process = distribution
