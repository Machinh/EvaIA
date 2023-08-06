import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import json
import unidecode

class EneAssistant(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Assistente Ene")
        self.set_default_size(400, 300)

        vbox = Gtk.VBox(spacing=10)
        self.add(vbox)

        # Text View to display the conversation
        self.conversation_view = Gtk.TextView()
        vbox.pack_start(self.conversation_view, True, True, 0)

        # Text Entry for user input
        self.user_input_entry = Gtk.Entry()
        self.user_input_entry.connect("activate", self.on_user_input_enter)
        vbox.pack_start(self.user_input_entry, False, False, 0)

        # Load responses from JSON file
        with open('memories.json', 'r', encoding='utf-8') as file:
            self.responses = json.load(file)

    def on_user_input_enter(self, entry):
        user_input = entry.get_text()
        self.add_to_conversation("Você: " + user_input)

        # Get response from Ene chatbot
        response = self.get_ene_response(user_input)
        self.animate_text("Ene: ", response)

        # Clear user input entry
        entry.set_text("")

    def add_to_conversation(self, text):
        buffer = self.conversation_view.get_buffer()
        end_iter = buffer.get_end_iter()
        buffer.insert(end_iter, text + "\n")

    def animate_text(self, prefix, text):
        # Function to remove accents and convert to lowercase
        def normalize_string(s):
            return unidecode.unidecode(s).lower()

        # Normalize user input and search for matching question in responses
        user_input_normalized = normalize_string(text)
        for item in self.responses:
            if normalize_string(item["pergunta"]) == user_input_normalized:
                response = item["resposta"]
                break
        else:
            response = "Desculpe, não entendi. Pode reformular sua pergunta?"

        # Animate the typing effect
        words = response.split()
        self.animate_typing(prefix, words)

    def animate_typing(self, prefix, words):
        buffer = self.conversation_view.get_buffer()
        end_iter = buffer.get_end_iter()
        buffer.insert(end_iter, prefix)

        def typing_animation():
            try:
                word = words.pop(0)
                buffer.insert(end_iter, word + " ")
                GLib.timeout_add(300, typing_animation)  # Change the delay here for typing speed
            except IndexError:
                buffer.insert(end_iter, "\n")

        typing_animation()

    def get_ene_response(self, user_input):
        # ... (Rest of your code remains the same)

win = EneAssistant()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
