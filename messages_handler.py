import os, sys, importlib
from command_system import command_list, arg
import json

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

async def get_answer(body, from_id, payload=None):
    message = ""
    attachment = ""
    keyboard = {}
    arg['system_vars']['from_id'] = from_id
    distance = len(body)
    command = None
    key = ''
    for c in command_list:
        if payload == None or payload['command'] == '':
            for k in c.keys['message']:
                new_body = ''
                new_notsystem_vars = []
                for ke in k.split():
                    for word in body.split('\n')[0].split():
                        dista = damerau_levenshtein_distance(word, ke)
                        if dista < len(word):
                            if dista == 0 or dista < len(word)*0.4:
                                for wa in arg['notsystem_vars']:
                                    if wa == word:
                                        new_notsystem_vars.append(word)
                                new_body += word + ' '
                        else:
                            arg['notsystem_vars'].append(word)
                new_body = new_body[:-1]
                new_distance = len(new_body)
                d = damerau_levenshtein_distance(new_body, k)
                if d < new_distance:
                    for i in range(len(arg['notsystem_vars'])):
                        for j in new_notsystem_vars:
                            if arg['notsystem_vars'][i] == j:
                                del arg['notsystem_vars'][i]
                    distance = d
                    command = c
                    key = k
                    body = new_body
                    try:
                        arg['notsystem_vars'].append(body.split('\n')[1])
                    except:
                        pass
                    if distance == 0:
                        print(arg['notsystem_vars'])
                        message, attachment, keyboard = await c.process()
                        arg['notsystem_vars'].clear()
                        return message, attachment, keyboard
                else:
                    arg['notsystem_vars'].clear()
        else:
            for k in c.keys['payload']:
                if payload['command'] == k:
                    new_payload = {}
                    for key, val in payload:
                        if key != payload['command']:
                            new_payload[key] = value
                    new_payload['notsystem_vars'].append(new_payload)
                    command = c
                    key = k
                    message, attachment, keyboard = await c.process()
                    arg['notsystem_vars'].clear()
                    return message, attachment, keyboard
    if distance < len(body)*0.4:
        message, attachment, keyboard = await command.process()
        message = 'По теории расстояния Дамерау-Левенштейна - Ваша комманда опознана как "%s"\n\n' % key + message
        arg['notsystem_vars'].clear()
    return message, attachment, keyboard

async def create_answer(data, session):
    load_modules()
    from_id = data['from_id']
    peer_id = data['peer_id']
    try:
        payload = json.loads(data['payload'])
    except:
        payload = {'command': ''}
    if peer_id == peer_id:
        message, attachment, keyboard = await get_answer(data['text'], from_id, payload)
        session.send_message(peer_id, message, attachment, keyboard)
