import json

class Persistence:
    def __init__(self):
        try:
            with open('users.json') as file:
                self.users = json.load(file)
        except FileNotFoundError:
            # Initialize for first start
            self.users = {}

    def createUser(self, id, username = "should_not_happen"):
        id = str(id)
        if not self.isUser(id):
            self.users[id]={'searches': 0, 'username': username}
            self.save()

    def deleteUser(self, id):
        id = str(id)
        if self.isUser(id):
            del self.users[id]
            self.save()

    def isUser(self, id):
        id = str(id)
        return id in self.users

    def countSearch(self, id):
        id = str(id)
        self.createUser(id)
        self.users[id]['searches'] += 1
        self.save()

    def setSearchString(self, id, text):
        id = str(id)
        self.createUser(id)
        self.users[id]['search_string'] = text
        self.save()

    def getSearchString(self, id):
        id = str(id)
        self.createUser(id)
        return self.users[id].get('search_string', None)

    def setSearchIndex(self, id, idx):
        id = str(id)
        self.createUser(id)
        self.users[id]['search_index'] = idx
        self.save()

    def getSearchIndex(self, id):
        id = str(id)
        self.createUser(id)
        return self.users[id].get('search_index', 0)

    def allUsers(self):
        return self.users

    def getUser(self,id):
        id = str(id)
        if not self.isUser(id):
            return None
        return self.users[id]

    def save(self):
        with open('users.json', 'w') as outfile:
            json.dump(self.users, outfile)
