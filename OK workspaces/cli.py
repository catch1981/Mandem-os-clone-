from hecate import Hecate
import argparse
import speech_recognition as sr
import subprocess

def speak(text):
    try:
        subprocess.run(["espeak", text], check=True)
    except Exception:
        pass


def voice_chat(bot, speak_output=False):
    """Continuous microphone input loop."""
    r = sr.Recognizer()
    mic = sr.Microphone()
    print("Speak into the microphone. Press Ctrl+C to exit.")
    while True:
        try:
            with mic as source:
                audio = r.listen(source)
            try:
                text = r.recognize_google(audio)
            except Exception as e:
                print(f"[error] {e}")
                continue
            print(f'You: {text}')
            reply = bot.respond(text)
            print(reply)
            if speak_output:
                speak(reply)
        except KeyboardInterrupt:
            print()
            break


def text_chat(bot, speak_output=False):
    print("Type your message. Enter 'quit' to exit.")
    while True:
        try:
            user_input = input('You: ').strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not user_input:
            continue
        if user_input.lower() in {'quit', 'exit'}:
            break
        reply = bot.respond(user_input)
        print(reply)
        if speak_output:
            speak(reply)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Hecate CLI")
    parser.add_argument("--voice", action="store_true", help="Use microphone input")
    parser.add_argument("--speak", action="store_true", help="Speak responses aloud")
    args = parser.parse_args()

    bot = Hecate()
    intro = bot.startup_message()
    if intro:
        print(intro)
        if args.speak:
            speak(intro)
    if args.voice:
        voice_chat(bot, speak_output=args.speak)
    else:
        text_chat(bot, speak_output=args.speak)
