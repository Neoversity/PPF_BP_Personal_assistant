# from kivy.uix.widget import Widget

# from kivymd.app import MDApp
# from kivymd.uix.button import MDFlatButton
# from kivymd.uix.dialog import MDDialog

from models import Note

# from sqlalchemy.orm import sessionmaker


class CommandLineProcessor:
    def __init__(self, address_book_app, **kwargs):
        super().__init__(**kwargs)
        self.address_book_app = address_book_app
        self.commands = {
            "home": self.go_to_home,
            "add": self.add_contact,
            "change": self.change_contact,
            "phone": self.phone_search,
            "all": self.show_all_contacts,
            "add-birthday": self.add_birthday,
            "show-birthday": self.show_birthday,
            "birthdays": self.show_all_birthdays,
            "hello": self.say_hello,
            "close": self.close_app,
            "exit": self.close_app,
            "add_note": self.add_note,            
            "all_note": self.show_all_note,
            "delete_note": self.delete_note,
        }
        self.waiting_for_note = False  # Нова змінна для відстеження стану

    def on_command_entered(self, command):
        if command in self.commands:
            if command == "exit" or command == "close":
                self.address_book_app.close_app()
            else:
                self.commands[command]()
                self.address_book_app.root.ids.command_output.text = (
                    "Results of the command: " + command
                )
        else:
            self.address_book_app.root.ids.command_output.text = "Unknown command!"

    def add_contact(self):
        # Implement logic to add a new contact
        pass

    def change_contact(self):
        # Implement logic to change a contact
        pass

    def phone_search(self):
        # Implement logic to search for a contact by phone
        pass

    def show_all_contacts(self):
        # Implement logic to show all contacts
        pass

    def add_birthday(self):
        # Implement logic to add a birthday
        pass

    def show_birthday(self):
        # Implement logic to show a birthday
        pass

    def show_all_birthdays(self):
        # Implement logic to show all birthdays
        pass

    def add_note(self):
        self.address_book_app.root.ids.command_output_result.text = (
            "Please enter tag and description for the note: <tag> <description>"
        )
        self.address_book_app.root.ids.command_input.bind(
            on_text_validate=self.process_note_input
        )
        self.address_book_app.root.ids.command_input.text = ""

    def process_note_input(self, instance):
        input_text = instance.text
        if input_text.lower() == "home":
            self.go_to_home()
            return True  # Повертаємо True, щоб припинити обробку події
        words = input_text.split()
        if len(words) < 2:
            self.address_book_app.root.ids.command_output_result.text = "Please enter both tag and description for the note: <tag> <description>"
            return True  # Повертаємо True, щоб припинити обробку події
        tag = words[0]
        description = " ".join(words[1:])
        Note.add(tag, description)
        self.address_book_app.root.ids.command_output_result.text = (
            "Note added successfully. \nTag: {} \nDescription: {}".format(
                tag, description
            )
        )
        self.address_book_app.root.ids.command_input.text = ""
        # Встановимо обробник on_text_validate знову
        self.address_book_app.root.ids.command_input.bind(
            on_text_validate=self.process_note_input
        )
        return True  # Повертаємо True, щоб припинити обробку події

    def show_all_note(self):
        all_notes = Note.all()
        if all_notes:
            note_list = "\n".join(
                [
                    f"{note.id}: Tag: {note.tag}, Description: {note.description}"
                    for note in all_notes
                ]
            )
            self.address_book_app.root.ids.command_output_result.text = (
                f"All notes:\n{note_list}"
            )
        else:
            self.address_book_app.root.ids.command_output_result.text = (
                "No notes found."
            )
        self.address_book_app.root.ids.command_input.text = ""

    def delete_note(self):
        self.address_book_app.root.ids.command_output_result.text = (
            "Please enter the ID of the note you want to delete: <id>"
        )
        self.address_book_app.root.ids.command_input.bind(
            on_text_validate=self.process_delete_note_input
        )

    def process_delete_note_input(self, instance):
        input_text = instance.text
        try:
            note_id = int(input_text)
            if Note.delete_note_by_id(note_id):
                self.address_book_app.root.ids.command_output_result.text = (
                    f"Note with ID {note_id} has been deleted."
                )
            else:
                self.address_book_app.root.ids.command_output_result.text = (
                    f"Note with ID {note_id} does not exist."
                )
        except ValueError:
            self.address_book_app.root.ids.command_output_result.text = (
                "Invalid input. Please enter a valid note ID."
            )
        self.address_book_app.root.ids.command_input.text = ""
        # Відмінюємо обробник події on_text_validate після додавання нотатки
        self.address_book_app.root.ids.command_input.unbind(
            on_text_validate=self.process_delete_note_input
        )
        return True

    def say_hello(self):
        self.address_book_app.root.ids.command_output_result.text = "Hello!"
        self.address_book_app.root.ids.command_input.text = ""

    def close_app(self):
        pass

    def go_to_home(self):
        # Повертаємо до початкового стану для вибору команди
        self.address_book_app.root.ids.command_output_result.text = (
            "You are returned to the main screen"
        )
        self.address_book_app.root.ids.command_input.text = ""
        # Відмінюємо обробник події on_text_validate, якщо він був встановлений
        self.address_book_app.root.ids.command_input.unbind(
            on_text_validate=self.process_note_input
        )
        self.waiting_for_note = (
            False  # Змінюємо стан, що користувач більше не очікує введення нотатки
        )