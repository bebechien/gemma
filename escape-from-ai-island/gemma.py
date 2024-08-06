# Gemma local

import keras
import keras_nlp

model_name = "gemma2_instruct_2b_en"

class GemmaBot():
  __START_TURN_USER__ = "<start_of_turn>user\n"
  __START_TURN_MODEL__ = "<start_of_turn>model\n"
  __END_TURN__ = "<end_of_turn>\n"

  def __init__(self, system=""):
    self.model = keras_nlp.models.GemmaCausalLM.from_preset(model_name)
    self.system = system
    self.history = []

  def add_to_history_as_user(self, message):
      self.history.append(self.__START_TURN_USER__ + message + self.__END_TURN__)

  def add_to_history_as_model(self, message):
      self.history.append(self.__START_TURN_MODEL__ + message)

  def get_history(self):
      return "".join([*self.history])

  def get_full_prompt(self):
    prompt = self.get_history() + self.__START_TURN_MODEL__
    if len(self.system)>0:
      prompt = self.system + "\n" + prompt
    return prompt

  def ask(self, message):
    self.add_to_history_as_user(message)
    prompt = self.get_full_prompt()
    response = self.model.generate(prompt, max_length=2048)
    result = response.replace(prompt, "")  # Extract only the new response
    self.add_to_history_as_model(result)
    return result

  def judge(self, message):
    self.history = []
    return self.ask(message + "\n" + self.system)

  def end_of_game(self):
    return self.ask("Did the user successfuly escape the island? Answer it only with True or False without any explanation.")
