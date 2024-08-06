from stage import IStage

from gemma import GemmaBot
#from gemma_vertex import GemmaBot

class StageGate(IStage):
    def __init__(self):
        self.preamble = "The steel gate looms before you, a formidable barrier separating you from the path ahead. Vines crawl along its rusted bars, and the air hums with a faint electrical current.\nThe Storyteller appears beside you, a shimmering presence in the dappled sunlight."
        self.intro = "Greetings! I am the Storyteller, your guide on this island.\nWe've come to a gate... what will you do?"
        self.bot = GemmaBot("You are the Storyteller, a friendly and helpful AI guide on a mysterious island. Your role is to help the player navigate challenges and find a way to escape. You are currently standing before a large steel gate.")

