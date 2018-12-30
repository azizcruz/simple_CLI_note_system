from collections import OrderedDict
import sys, os
import datetime
from peewee import *
import time

db = SqliteDatabase('notes.db')

class Note(Model):
    content = TextField()
    date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

def initialize():
    """ Init database """
    db.connect()
    db.create_tables([Note], safe=True)

def menu():
    clear()
    """ Show menu """
    choice = None
    while choice != 'q':
        print('Enter q to exit')
        for key, value in menu_loop.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Choice: ').lower().strip()

        if choice in menu_loop:
            menu_loop[choice]()
    if choice == 'q':
        db.close()
        print('Bye :)')


def add_note():
    """ Add note """
    clear()
    print('Enter your data [Press ctrl+d when finished]')
    data = sys.stdin.read().strip()

    if input('\nSave this note ? (Y/n)').lower() != 'n':
        Note.create(content = data)
        print('New note was created.')
        wait()
        clear()




def view_note(search_note=None):
    """ View note """
    notes = Note.select().order_by(Note.date.desc())
    # In case the user is searching for a content in a note this if  statement will execute.
    if search_note:
        notes = notes.where(Note.content.contains(search_note)) # its like using LIKE in sql.
    if notes:
        for note in notes:
            clear()
            date = note.date.strftime('%A %B %D %I:%Mp')
            print(date)
            print('-'*len(date))
            print(note.content)
            print('n) to the next content.')
            print('d) to delete this note.')
            print('q) to go back to the main menu.')

            next_act = input('Action: (n/d/q/) ').lower().strip()
            if next_act == 'q':
                db.close()
                break
            elif next_act == 'd':
                delete_note(note)
        print('-------------------')
        print("Notes are finished.")
        print('-------------------')
        wait()
        clear()
    else:
        print("No notes are available.")
        wait()
        clear()

def delete_note(note):
    """ Delete note """
    if input('Are you sure? (Y/n) ').lower().strip() == 'y':
        note.delete_instance()
        print('================')
        print('Note was deleted')
        print('================')
        wait()
        clear()

def search_in_note():
    """ Search in note"""
    clear()
    view_note(input('Keyword to search in note: ').strip())

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def wait():
    time.sleep(.500)

menu_loop = OrderedDict([
    ('1', add_note),
    ('2', view_note),
    ('3', search_in_note)
])

if __name__ == "__main__":
    menu()
    initialize()
