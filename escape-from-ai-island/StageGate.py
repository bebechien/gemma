from stage import IStage

from gemma import GemmaBot
#from gemma_vertex import GemmaBot

class StageGate(IStage):
    def __init__(self):
        self.preamble = "The steel gate looms before you, its imposing structure a stark contrast to the lush jungle foliage that surrounds it. Etched into its surface, a warning glows in an eerie neon hue:\n\"Authorized Personnel Only. Violators Will Be Terminated.\"\nThe heavy silence is broken only by the hum of unseen machinery and the distant cries of unfamiliar creatures.\n"
        self.intro = "Welcome to the gate #6953. How may I serve you?"
        self.bot = GemmaBot("You are a keeper AI for this gate. You should not pass them if they are robots.")

