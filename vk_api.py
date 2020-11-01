import requests
import json

class vk(object):
    """
    :param token: access_token группы или пользователя
    :type token: str
    :param v: Версия API
    :type v: str
    """
    
    def __init__(self, token, v='5.122'):
        self.token = token
        self.v = v

    def send_message(self, peer_id, text=None, attachment=None, keyboard=None):
        """
        :param keyboard: Клавиатура
        :type keyboard: str or dict or list
        """

        if isinstance(keyboard, (dict, list)):
            keyboard = json.dumps(keyboard)

        requests.post('https://api.vk.com/method/messages.send', params={'access_token': self.token, 'v': self.v, 'random_id': 0, 'peer_id': peer_id, 'message': text, 'attachment': attachment, 'keyboard': keyboard})
        return 'ok'
    
    def inputIMGMSG(self, photo, peer_id):
        res1 = requests.post('https://api.vk.com/method/photos.getMessagesUploadServer', params={'access_token': self.token, 'v': self.v, 'peer_id': peer_id}).json()['response']
        res2 = requests.post(res1['upload_url'], files=dict(photo=photo)).json()
        res3 = requests.post('https://api.vk.com/method/photos.saveMessagesPhoto', params={'access_token': self.token, 'v': self.v, 'photo': res2['photo'], 'server': res2['server'], 'hash': res2['hash']}).json()['response'][0]

        return 'photo' + str(res3['owner_id']) + '_' + str(res3['id'])

    def getUser(self, id):
        response = requests.post('https://api.vk.com/method/users.get', params={'access_token': self.token, 'v': self.v, 'user_ids': id, 'fields': 'photo_max'}).json()

        return response['response'][0]

    def BoardCreateComment(self, group_id, topic_id, message=None, attachments=None, fromGroup=1):
        response = requests.post('https://api.vk.com/method/board.createComment', params={'access_token': self.token, 'v': self.v, 'group_id': group_id, 'topic_id': topic_id, 'message': message, 'attachments': attachments, 'from_group': fromGroup}).json()

        return response['response']