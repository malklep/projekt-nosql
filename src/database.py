from store import Store
from constants import MESSAGES
from uuid import uuid4


class Database:
    def __init__(self, filename='store.json'):
        self._store = Store(filename)
        self._store.load()

    def drop_database(self):
        '''
            Usuwa wszystkie dane z bazy danych.
        '''

        self._store = Store(self._store._filename)
        self._store.save()

    def create_user(self, document: dict, key: str):
        '''
            Tworzy nowego użytkownika.
            Jeśli użytkownik o podanym kluczu już istnieje, zwraca odpowiedni komunikat.
        '''

        result = self._store.get(key, namespace='users')

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
        '''
            Zwraca użytkownika o podanym kluczu jeżeli ten istnieje.
        '''

        result = self._store.get(key, namespace='users')
        if result['code'] != MESSAGES.OK_CODE:
            return MESSAGES.USER_NOT_FOUND
        else:
            return MESSAGES.ok(result['value'], result['guard'])

    def update_user(self, key: str, document: dict):
        '''
            Aktualizuje dane użytkownika o podanym kluczu.
        '''

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
        '''
            Usuwa użytkownika o podanym kluczu.
        '''

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

    def create_file(self, user_key: str, tags: list[str], document: dict):
        '''
            Tworzy nowy plik dla użytkownika o podanym kluczu.
            Plik zostaje zapisany pod każdym tagiem z podanej listy.
        '''

        result = self.get_user(user_key)
        if result['code'] == MESSAGES.USER_NOT_FOUND_CODE:
            return MESSAGES.USER_NOT_FOUND
        else:
            if not tags:
                return MESSAGES.AT_LEAST_ONE_TAG_REQUIRED

            document['id'] = str(uuid4())
            for tag in tags:
                tag_key = f'{user_key}:{tag}'
                tag_value = self._store.get(tag_key, namespace='files')
                if tag_value['code'] == MESSAGES.OK_CODE:
                    tag_value['value'].append(document)
                    result = self._store.put(tag_key, tag_value['value'], namespace='files', guard=tag_value['guard'])
                else:
                    result = self._store.put(tag_key, [document], namespace='files')
                if result['code'] != MESSAGES.OK_CODE:
                    return result

            self._store.save()
            return MESSAGES.FILE_CREATED

    def get_file(self, user_key: str, filename: str, tag: str = None):
        '''
            Zwraca plik o podanej nazwie dla użytkownika o podanym kluczu.
            Jeśli podano tag, zwraca plik tylko z tego tagu, w przeciwnym wypadku
            zwraca pierwszy napotkany plik (spod dowolnego tagu).
        '''

        result = self.get_user(user_key)
        if result['code'] == MESSAGES.USER_NOT_FOUND_CODE:
            return MESSAGES.USER_NOT_FOUND
        else:
            if tag:
                tag_data = self.get_tag(user_key, tag)
                if tag_data['code'] == MESSAGES.OK_CODE:
                    for f in tag_data['value']:
                        if f['name'] == filename:
                            return MESSAGES.ok(f, tag_data['guard'])
                    return MESSAGES.FILE_NOT_FOUND
                else:
                    return MESSAGES.TAG_NOT_FOUND
            else:
                for tag in self.get_tags(user_key)['value']:
                    tag_data = self.get_tag(user_key, tag)
                    if tag_data['code'] == MESSAGES.OK_CODE:
                        for f in tag_data['value']:
                            if f['name'] == filename:
                                return MESSAGES.ok(f, tag_data['guard'])
                return MESSAGES.FILE_NOT_FOUND

    def get_files_by_tag(self, user_key: str, tags: list[str]):
        '''
            Zwraca wszystkie pliki spod podanego tagu dla użytkownika o podanym kluczu.
            Jeżeli plik występuje pod kilkoma tagami, zwracany jest tylko raz.
        '''

        result = self.get_user(user_key)
        if result['code'] == MESSAGES.USER_NOT_FOUND_CODE:
            return MESSAGES.USER_NOT_FOUND
        else:
            if not tags:
                return MESSAGES.AT_LEAST_ONE_TAG_REQUIRED

            files = []
            for tag in tags:
                tag_data = self.get_tag(user_key, tag)
                if tag_data['code'] == MESSAGES.OK_CODE:
                    files.extend(tag_data['value'])

            deduplicated_files = dict((v['id'], v) for v in files).values()
            return MESSAGES.ok(list(deduplicated_files))

    def delete_file_from_tags(self, user_key: str, tags: list[str], filename: str):
        '''
            Usuwa plik o podanej nazwie z podanych tagów dla użytkownika o podanym kluczu.
            Jeżeli pod danym tagiem nie ma już żadnych plików, ten tag zostanie usunięty.
        '''

        result = self.get_user(user_key)
        if result['code'] == MESSAGES.USER_NOT_FOUND_CODE:
            return MESSAGES.USER_NOT_FOUND
        else:
            if not tags:
                return MESSAGES.AT_LEAST_ONE_TAG_REQUIRED

            deleting_result = None
            for tag in tags:
                tag_key = f'{user_key}:{tag}'
                tag_data = self.get_tag(user_key, tag)

                if tag_data['code'] == MESSAGES.OK_CODE:
                    files_count = len(tag_data['value'])
                    tag_data['value'] = [f for f in tag_data['value'] if f['name'] != filename]
                    if files_count == len(tag_data['value']):
                        deleting_result = MESSAGES.FILE_NOT_FOUND
                    else:
                        result = self._store.put(tag_key, tag_data['value'], namespace='files', guard=tag_data['guard'])
                        if result['code'] != MESSAGES.OK_CODE:
                            return result
                        else:
                            if len(tag_data['value']) == 0:
                                result = self.delete_tag(user_key, tag)
                                if result['code'] != MESSAGES.TAG_DELETED_CODE:
                                    return result
                        deleting_result = MESSAGES.FILE_DELETED
                else:
                    deleting_result = MESSAGES.TAG_NOT_FOUND

            self._store.save()
            return deleting_result

    def get_tag(self, user_key: str, tag: str):
        '''
            Zwraca tag dla użytkownika o podanym kluczu.
        '''

        result = self.get_user(user_key)
        if result['code'] == MESSAGES.USER_NOT_FOUND_CODE:
            return MESSAGES.USER_NOT_FOUND
        else:
            tag_key = f'{user_key}:{tag}'
            result = self._store.get(tag_key, namespace='files')
            if result['code'] != MESSAGES.OK_CODE:
                return MESSAGES.TAG_NOT_FOUND
            else:
                return MESSAGES.ok(result['value'], result['guard'])

    def get_tags(self, user_key: str):
        '''
            Zwraca listę tagów dla użytkownika o podanym kluczu.
        '''

        result = self.get_user(user_key)
        if result['code'] == MESSAGES.USER_NOT_FOUND_CODE:
            return MESSAGES.USER_NOT_FOUND
        else:
            tags = []
            if not 'files' in self._store._store:
                return MESSAGES.ok(tags)

            for key in self._store._store['files']:
                key_data = key.split(':')
                if key_data[0] == user_key:
                    tags.append(key_data[1])
            return MESSAGES.ok(tags)

    def delete_tag(self, user_key: str, tag: str):
        '''
            Usuwa tag dla użytkownika o podanym kluczu.
            Wraz z usuwanym tagiem, usuwane są wszystkie pliki z tego tagu.
        '''

        result = self.get_user(user_key)
        if result['code'] == MESSAGES.USER_NOT_FOUND_CODE:
            return MESSAGES.USER_NOT_FOUND
        else:
            tag_key = f'{user_key}:{tag}'
            tag = self.get_tag(user_key, tag)
            if tag['code'] == MESSAGES.TAG_NOT_FOUND_CODE:
                return MESSAGES.TAG_NOT_FOUND
            else:
                result = self._store.delete(tag_key, namespace='files', guard=tag['guard'])
                if result['code'] != MESSAGES.OK_CODE:
                    return result
                else:
                    self._store.save()
                    return MESSAGES.TAG_DELETED
