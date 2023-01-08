from database import Database
from pprint import pprint


def main():
    db = Database()
    db.drop_database()  # czyścimy bazę aby nie śmiecić w pliku store.json (aby otrzymać ten sam wynik)

    db.create_user({
        'name': 'Gosia Klepczarek',
        'username': 'malklep',
    }, 'malklep')

    db.create_file('malklep', ['tag1', 'tag2'], {
        'name': 'file1',
        'path': 'file1.txt'
    })

    db.create_file('malklep', ['tag1', 'tag3'], {
        'name': 'file2',
        'path': 'file2.txt'
    })

    db.create_file('malklep', ['tag1', 'tag2', 'tag3'], {
        'name': 'file3',
        'path': 'file3.txt'
    })

    pprint(db.get_files_by_tag('malklep', ['tag1', 'tag2']))

    pprint(db.get_tag('malklep', 'tag1'))  # stan przed usunięciem pliku
    db.delete_file_from_tags('malklep', ['tag1'], 'file3')
    pprint(db.get_tag('malklep', 'tag1'))  # stan po usunięciu pliku

    db.delete_file_from_tags('malklep', ['tag2', 'tag3'], 'file1')

    pprint(db.get_tags('malklep'))
    db.delete_tag('malklep', 'tag1')
    pprint(db.get_tags('malklep'))


if __name__ == '__main__':
    main()
