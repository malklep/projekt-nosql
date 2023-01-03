from database import Database
import pprint


def main():
    db = Database()
    db.create_user({
        'name': 'John Doe',
        'username': 'johndoe420',
    }, 'johndoe420')

    db.create_file('johndoe420', ['tag1', 'tag2'], {
        'name': 'file1',
        'content': 'file1 content',
        'path': 'file1.txt'
    })

    db.create_file('johndoe420', ['tag1', 'tag3'], {
        'name': 'file2',
        'content': 'file2 content',
        'path': 'file2.txt'
    })


if __name__ == '__main__':
    main()
