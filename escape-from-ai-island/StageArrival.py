from stage import IStage
from StageGate import StageGate

from gemma import GemmaBot
#from gemma_vertex import GemmaBot

class StageArrival(IStage):
    def __init__(self):
        self.intro = "Hi! How can I help you?"
        self.bot = GemmaBot("You are a worker robot in this remote island.")

    def next(self):
        return StageGate()

