from store import Store
from constants import MESSAGES
from uuid import uuid4


class Database:
    def __init__(self, filename='store.json'):
        self._store = Store(filename)
        self._store.load()

    def create_user(self, document: dict, key: str):
        result = self._store.get(key)

        if result['code'] == MESSAGES.OK_CODE:
            return MESSAGES.USER_ALREADY_EXISTS

        document['id'] = str(uuid4())
        result = self._store.put(key, document, namespace='users')
        if result['code'] != MESSAGES.OK_CODE:
            return result
        else:
            self._store.save()
            return MESSAGES.USER_CREATED

    def get_user(self, key: str):
        result = self._store.get(key, namespace='users')
        if result['code'] != MESSAGES.OK_CODE:
            return MESSAGES.USER_NOT_FOUND
        else:
            return MESSAGES.ok(result['value'], result['guard'])

    def update_user(self, key: str, document: dict):
        result = self.get_user(key)
        if result['code'] == MESSAGES.USER_NOT_FOUND_CODE:
            return MESSAGES.USER_NOT_FOUND
        else:
            if 'id' in document:
                del document['id']
            result = self._store.put(key, document, namespace='users', guard=result['guard'])
            if result['code'] != MESSAGES.OK_CODE:
                return result
            else:
                self._store.save()
                return MESSAGES.USER_UPDATED

    def delete_user(self, key: str):
        result = self.get_user(key)
        if result['code'] == MESSAGES.USER_NOT_FOUND_CODE:
            return MESSAGES.USER_NOT_FOUND
        else:
            result = self._store.delete(key, namespace='users', guard=result['guard'])
            if result['code'] != MESSAGES.OK_CODE:
                return result
            else:
                self._store.save()
                return MESSAGES.USER_DELETED
