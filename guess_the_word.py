import re
from transformers import AutoTokenizer, AutoModelForCausalLM

model_path = "google/gemma-1.1-2b-it"

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

class ChatState():
  """
  Manages the conversation history for a turn-based chatbot
  Follows the turn-based conversation guidelines for the Gemma family of models
  documented at https://ai.google.dev/gemma/docs/formatting
  """

  __START_TURN_USER__ = "<start_of_turn>user\n"
  __START_TURN_MODEL__ = "<start_of_turn>model\n"
  __END_TURN__ = "<end_of_turn>\n"

  def __init__(self, system=""):
    """
    Initializes the chat state.

    Args:
        system: (Optional) System instructions or bot description.
    """
    self.system = system
    self.history = []

  def add_to_history_as_user(self, message):
      """
      Adds a user message to the history with start/end turn markers.
      """
      self.history.append(self.__START_TURN_USER__ + message + self.__END_TURN__
)

  def add_to_history_as_model(self, message):
      """
      Adds a model response to the history with start/end turn markers.
      """
      self.history.append(self.__START_TURN_MODEL__ + message + self.__END_TURN_
_)

  def get_history(self):
      """
      Returns the entire chat history as a single string.
      """
      return "".join([*self.history])

  def get_full_prompt(self):
    """
    Builds the prompt for the language model, including history and system descr
iption.
    """
    prompt = self.get_history() + self.__START_TURN_MODEL__
    if len(self.system)>0:
      prompt = self.system + "\n" + prompt
    return prompt

  def send_message(self, message):
    """
    Handles sending a user message and getting a model response.

    Args:
        message: The user's message.

    Returns:
        The model's response.
    """
    self.add_to_history_as_user(message)
    prompt = self.get_full_prompt()
    input_tokens = tokenizer(prompt, return_tensors="pt")
    generate_ids = model.generate(**input_tokens, max_new_tokens=512, do_sample=
True)
    response = tokenizer.batch_decode(generate_ids)[0]
    result = response.replace(prompt, "")  # Extract only the new response
    result = re.sub("(<bos>|<eos>)", "", result)
    self.add_to_history_as_model(result)
    return result

from terminaltexteffects.effects.effect_beams import Beams

def beams_animated_prompt(prompt_text: str):
    effect = Beams(prompt_text)
    effect.effect_config.final_gradient_frames = 1
    effect.terminal_config.wrap_text = True
    with effect.terminal_output() as terminal:
        for frame in effect:
            terminal.print(frame)

theme = input("Choose your theme: ")
setup_message = f"Generate a random single word from {theme}."

chat = ChatState()
answer = chat.send_message(setup_message).split()[0]
chat.history.clear()
cmd_exit = "quit"
question = f"Describe the word \"{answer}\" without saying it."

resp = ""
while resp.lower() != answer.lower() and resp != cmd_exit:
    text = chat.send_message(question)
    if resp == "":
        print(f"Guess what I'm thinking.\nType \"{cmd_exit}\" if you want to qui
t.")
    remove_answer = re.compile(re.escape(answer), re.IGNORECASE)
    text = remove_answer.sub("XXXX", text)
    beams_animated_prompt(text)
    resp = input("\n> ")

if resp == cmd_exit:
    print(f"The answer was {answer}.\n")
else:
    print("Correct!")
