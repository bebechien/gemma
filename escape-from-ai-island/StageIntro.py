from stage import IStage
from StageArrival import StageArrival

class StageIntro(IStage):
    def process(self):
        f = open("title.txt", "r")
        title = f.read()
        f.close()
        f = open("intro.txt", "r")
        intro = f.read()
        f.close()

        print(title)
        print(intro)

    def pass_check(self):
        return True

    def next(self):
        return StageArrival()

