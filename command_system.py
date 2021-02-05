command_list = []
command_cat_list = []

arg = {'system_vars': {}, 'notsystem_vars': {'words': [], 'attachments': [], 'comments': [], 'payload': {}, 'isPayload': False}}

class Command:
   def __init__(self):
       self.__keys = {'message': [], 'payload': []}
       self.description = ''
       self.show = True
       self.isAdmin = False
       command_list.append(self)

   @property
   def keys(self):
       return self.__keys

   @keys.setter
   def keysm(self, mas):
       for k in mas:
           self.__keys['message'].append(k.lower())

   @keys.setter
   def keysp(self, mas):
       for k in mas:
           self.__keys['payload'].append(k)

   def process(self):
       pass

class CommandCat:
    def __init__(self):
        self.title = ''
        self.description = ''
        self.show = True
        self.commands = []
        command_cat_list.append(self)
