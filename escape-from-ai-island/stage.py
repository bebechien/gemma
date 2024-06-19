class IStage:
    preamble = ""
    intro = ""
    bot = None
    cmd_exit = "bye"

    def __init__(self):
        pass

    def process(self):
        pass

    def pass_check(self):
        return False

    def next(self):
        return None

