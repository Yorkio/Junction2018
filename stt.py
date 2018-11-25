import pyaudio
import speech_recognition as sr
import phrase2action
import glasses_and_hats
import random
from enum import Enum

class InputType(Enum):
    NONE = 0
    SPEECH = 1
    TEXT = 2


def payment():
    print('You successfully purchased the product! You can eithet quit now or continue experience.')


def main():
    print("Welcome to our STT shop.")
    input_type = InputType.NONE
    action = phrase2action.Actions.NONE
    while action is not phrase2action.Actions.EXIT:
        if input_type is InputType.NONE:
            print("""Do you want to use stt for this action?(Y/n). You can later switch input method via "change input method" command""")
            response = input()
            if 'y' in response.lower():
                input_type = InputType.SPEECH
            else:
                input_type = InputType.TEXT
        query = ''
        if input_type is InputType.SPEECH:
            r = sr.Recognizer()
            audio = None
            with sr.Microphone() as source:
                print("Speak now\n")
                audio = r.listen(source)
            try:
                query = r.recognize_google(audio)
                print(query)
            except (LookupError, sr.UnknownValueError):
                pass
        else:
            query = input()
        action = phrase2action.find_action(query)
        if action[1] == phrase2action.Actions.EXIT:
            print(phrase2action.reply[action[1]][random.randrange(len(phrase2action.reply[action[1]]))])
            exit()

        if action[1] == phrase2action.Actions.INP_CH:
            if input_type is InputType.SPEECH:
                input_type = InputType.TEXT
                print('input type switched to text')
            else:
                input_type = InputType.SPEECH
                print('input type switched to speech')

        if action[1] == phrase2action.Actions.GREET:
            print(phrase2action.reply[action[1]][random.randrange(len(phrase2action.reply[action[1]]))])

        if action[1] == phrase2action.Actions.WAR_PER:
            print(phrase2action.reply[action[1]][random.randrange(len(phrase2action.reply[action[1]]))])

        if action[1] == phrase2action.Actions.TIME_SHIP:
            print(phrase2action.reply[action[1]][random.randrange(len(phrase2action.reply[action[1]]))])

        if action[1] == phrase2action.Actions.NONE:
            print('What do you mean?')

        cnt = 0
        if action[1] == phrase2action.Actions.SHOW_GLASSES:
            print(phrase2action.reply[action[1]][random.randrange(len(phrase2action.reply[action[1]]))])
            print('You can press <- arrow if you don;t like them or -> right arrow if you do like. Simple Tinder like control :)')
            glass_templ = glasses_and_hats.load_resources('glass_resources')
            for t in glass_templ:
                response = glasses_and_hats.show_webcam(t, glasses_and_hats.add_glasses, 0)
                if response == phrase2action.Actions.Y:
                    print('Nice choice! Would you like to proceed to checkout?')
                    payment()
                    break
                else:
                    cnt += 1
                if cnt == len(glass_templ):
                    print('For now we donnt have more glasses options')
                    print('Would you like to get something else?')


        cnt = 0
        if action[1] == phrase2action.Actions.SHOW_HAT:
            print(phrase2action.reply[action[1]][random.randrange(len(phrase2action.reply[action[1]]))])
            print('You can press <- arrow if you don;t like them or -> right arrow if you do like. Simple Tinder like control :)')
            hat_templ = glasses_and_hats.load_resources('hat_resources')
            for t in hat_templ:
                response = glasses_and_hats.show_webcam(t, glasses_and_hats.add_hat, 0)
                if response == phrase2action.Actions.Y:
                    print('Nice choice! Would you like to proceed to checkout?')
                    payment()
                    break
                else:
                    cnt += 1
                if cnt == len(hat_templ):
                    print('For now we dont have more hat options')
                    print('Would you like to get something else?')


if __name__ == '__main__':
    main()
