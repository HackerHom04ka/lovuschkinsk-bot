from vk_api import vk
from messages_handler import create_answer as messages
import random
from config import group_config
import asyncio

async def events(data, session: vk, session_papochka: vk):
    if data['type'] == 'message_new':
        messages(data['object']['message'], session)
    if data['type'] == 'group_leave':
        pidaras_id = data['object']['user_id']
        pidaras_info = session.getUser(pidaras_id)
        Name = pidaras_info['first_name']
        Surname = pidaras_info['last_name']
        fragment_message = random.choice(['чекай свою мамку.', 'слит.', 'вернись, либо пидорас.', 'ты окаался, как и твой батя, лохом, геем, пидорасом.', 'вернись.'])
        message = '[id' + str(pidaras_id) + '|' + Name + ' ' + Surname + '], ' + fragment_message
        session_papochka.BoardCreateComment(group_id=group_config['id'], topic_id=46593350, message=message)
        session.send_message(peer_id=578425189, text='[id' + str(pidaras_id) + '|' + Name + ' ' + Surname + '], вышел из группы, какое наказание? анальное?')
    # if data['type'] == 'wall_post_new':
    #     if str(data['object']['from_id'])[0] == '-':
    #         from keyboards import sendingKeyboard
    #         distribution_users = Passport.query.filter_by(distribution=True).all()
    #         distribution_users1 = []
    #         for user in distribution_users:
    #             print(user.vk_id)
    #             if user.id not in distribution_users1:
    #                 session.send_message(user.vk_id, '📢 | Новый пост в нашей группе!', attachment='wall' + str(data['object']['owner_id']) + '_' + str(data['object']['id']), keyboard=sendingKeyboard)
    #                 distribution_users1.append(user.id)

eventLoop = asyncio.get_event_loop()