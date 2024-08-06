import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-pro')
chat = model.start_chat()

class GeminiBot():
    def __init__(self, system=""):
        self.system = system

    def ask(self, message):
        return model.generate_content(message).text

    def judge(self, message):
        return chat.send_message(message + "\n" + self.system).text

    def end_of_game(self):
        return chat.send_message("Did the user successfuly escape the island? Answer it only with True or False without any explanation.").text

