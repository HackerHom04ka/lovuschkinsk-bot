import os, sys, importlib
from command_system import command_list, arg
import json
from config import group_config

def damerau_levenshtein_distance(s1, s2):
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    for i in range(-1, lenstr1 + 1):
        d[(i, -1)] = i + 1
    for j in range(-1, lenstr2 + 1):
        d[(-1, j)] = j + 1
    for i in range(lenstr1):
        for j in range(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i, j)] = min(
                d[(i - 1, j)] + 1,  # deletion
                d[(i, j - 1)] + 1,  # insertion
                d[(i - 1, j - 1)] + cost,  # substitution
            )
            if i and j and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + cost)  # transposition
    return d[lenstr1 - 1, lenstr2 - 1]

def load_modules():
    # путь от рабочей директории, ее можно изменить в настройках приложения
    files = os.listdir(sys.path[1] + "/commands")
    modules = filter(lambda x: x.endswith('.py'), files)
    for m in modules:
        importlib.import_module("commands." + m[0:-3])

def get_answer(body, from_id, payload=None, attachments=None):
    message = ""
    attachment = ''
    keyboard = {}
    arg['system_vars']['from_id'] = from_id
    arg['system_vars']['peer_id'] = from_id
    arg['notsystem_vars']['attachments'] = attachments
    arg['notsystem_vars']['wordes'] = body.split('\n')[0].split()
    distance = len(body)
    command = None
    key = ''
    for c in command_list:
        if not payload or payload['command'] == '':
            for k in c.keys['message']:
                print(arg['notsystem_vars']['wordes'])
                print(len(k.split()), len(arg['notsystem_vars']['wordes']))
                if len(k.split()) > len(arg['notsystem_vars']['wordes']):
                    continue
                len_k = len(k.split())
                dist = 0
                for kw in range(len(k.split())):
                    a = arg['notsystem_vars']['wordes'][kw]
                    b = k.split()[kw]
                    dista = damerau_levenshtein_distance(a, b)
                    if dista == 0 or dista < len(a)*0.4:
                        dist += 1
                    else:
                        dist = 0
                    if dist == len_k:
                        new_body = ' '.join(str(x) for x in arg['notsystem_vars']['wordes'][0:len_k])
                        arg['notsystem_vars']['wordes'] = arg['notsystem_vars']['wordes'][len_k:]
                        break
                new_distance = len(new_body)
                d = damerau_levenshtein_distance(new_body, k)
                if d < new_distance:
                    print(arg['notsystem_vars']['wordes'])
                    distance = d
                    command = c
                    key = k
                    body = new_body
                    if command.isAdmin and peer_id not in group_config:
                        message = 'У вас нет доступа'
                        attachment = ''
                        keyboard = {}
                        return message, attachment, keyboard
                    try:
                        arg['notsystem_vars']['comments'].append(body.split('\n')[1:])
                    except:
                        pass
                    if distance == 0:
                        print(arg['notsystem_vars'])
                        message, attachment, keyboard = c.process(arg['notsystem_vars'])
                        arg['notsystem_vars'] == {'system_vars': {}, 'notsystem_vars': {'wordes': [], 'attachments': [], 'comments': [], 'payload': {}}, 'isPayload': False}
                        return message, attachment, keyboard
                    elif distance < len(body)*0.4:
                        message, attachment, keyboard = command.process(arg['notsystem_vars'])
                        message = 'По теории расстояния Дамерау-Левенштейна - Ваша комманда опознана как "%s"\n\n' % key + message
                        arg['notsystem_vars'] = {'system_vars': {}, 'notsystem_vars': {'wordes': [], 'attachments': [], 'comments': [], 'payload': {}}, 'isPayload': False}
                        return message, attachment, keyboard
        else:
            for k in c.keys['payload']:
                if payload['command'] == k:
                    new_payload = {}
                    for key, val in payload:
                        if key != 'command':
                            arg['notsystem_vars']['payload'][key] = value
                    command = c
                    key = k
                    arg['isPayload'] == True
                    message, attachment, keyboard = c.process(arg['notsystem_vars'])
                    arg['notsystem_vars'] = {'system_vars': {}, 'notsystem_vars': {'wordes': [], 'attachments': [], 'comments': [], 'payload': {}}, 'isPayload': False}
                    return message, attachment, keyboard
    return message, attachment, keyboard
def create_answer(data, session):
    load_modules()
    from_id = data['from_id']
    peer_id = data['peer_id']
    try:
        payload = json.loads(data['payload'])
    except:
        payload = {'command': ''}
    attachments = data['attachments']
    if peer_id == from_id:
        message, attachment, keyboard = get_answer(data['text'], from_id, payload, attachments)
        session.send_message(peer_id, message, attachment, keyboard)
