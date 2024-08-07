from gemma import GemmaBot
admin_bot = GemmaBot("You are an advanced AI who rules this escape game. Summarize the conversation above.")

import StageIntro
current_stage = StageIntro.StageIntro()

def game_loop():
    if current_stage.bot is None:
        # stage type that has no bot
        current_stage.process()
        return

    resp = ""
    print("-"*80)
    print(f"Type \"{current_stage.cmd_exit}\" if you want to end the conversation.")
    print("-"*80)

    if current_stage.preamble != "":
        print(current_stage.preamble)

    while resp != current_stage.cmd_exit:
        if resp == "":
            text = current_stage.intro
            current_stage.bot.add_to_history_as_model(text)
        else:
            text = current_stage.bot.ask(resp)

        print(text)
        resp = input("\n> ")

    print(admin_bot.judge(current_stage.bot.get_history()))

def check_end_condition():
    if not current_stage.pass_check():
        check = admin_bot.end_of_game()
        print("Succeed to escape?")
        print(check)
        if check.lower().startswith("true"):
            print("Congratulations! You escaped the island.")
            exit(0)

    next_stage = current_stage.next()
    if next_stage is None:
        print("End Of Game")
        exit(0)

    return next_stage

while True:
    game_loop()
    current_stage = check_end_condition()
    input("Press ENTER to move forward")

