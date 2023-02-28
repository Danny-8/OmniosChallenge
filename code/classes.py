import uuid

'''
Class to generate a unique id by saving them in a dictionary to compare if they are already in use
'''
class UniqueIDGenerator:
    def __init__(self):
        self.ids_dic = []

    def unique_id(self):
        new_id = uuid.uuid4()
        if new_id in self.ids_dic:
            return self.unique_id()
        else:
            self.ids_dic.append(new_id)
            return new_id