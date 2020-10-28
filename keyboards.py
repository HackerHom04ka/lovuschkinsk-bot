import json

keyboardStart = {
    'inline': True,
    'buttons': [
            [
                {
                    'action': {
                        'type': 'text',
                        'label': '📖 | Инструкция по созданию паспорта',
                        'payload': json.dumps({'command': 'create_passport'})
                    },
                    'color': 'positive'
                }
            ]
        ]
}
keyboardChangeAccess = {
    'inline': True,
    'buttons': [
            [
                {
                    'action': {
                        'type': 'text',
                        'label': '📖 | Показать паспорт',
                        'payload': json.dumps({'command': 'show_passport'})
                    },
                    'color': 'positive'
                }
            ]
        ]
}
keyboardPassport = {
    'inline': True,
    'buttons': [
            [
                {
                    'action': {
                        'type': 'text',
                        'label': '🖊 | Поменять данные',
                        'payload': json.dumps({'command': 'create_passport'})
                    },
                    'color': 'positive'
                }
            ]
        ]
}
def keyboardTransfer1 (id):
    keyboard = {
        'inline': True,
        'buttons': [
            [
                {
                    'action': {
                        'type': 'text',
                        'label': '📖 | Показать паспорт получившего',
                        'payload': json.dumps({'command': 'show_passport', 'id': id})
                    },
                    'color': 'positive'
                },
                {
                    'action': {
                        'type': 'text',
                        'label': '📖 | Показать свой паспорт',
                        'payload': json.dumps({'command': 'show_passport'})
                    },
                    'color': 'positive'
                }
            ]
        ]
    }
    return keyboard

def keyboardTransfer2 (id):
    keyboard = {
        'inline': True,
        'buttons': [
            [
                {
                    'action': {
                        'type': 'text',
                        'label': '📖 | Показать паспорт переведшего',
                        'payload': json.dumps({'command': 'show_passport', 'id': id})
                    },
                    'color': 'positive'
                },
                {
                    'action': {
                        'type': 'text',
                        'label': '📖 | Показать свой паспорт',
                        'payload': json.dumps({'command': 'show_passport'})
                    },
                    'color': 'positive'
                }
            ]
        ]
    }
    return keyboard