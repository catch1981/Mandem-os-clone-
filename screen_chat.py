import argparse
import os
import sys

# Add the 'OK workspaces' directory to sys.path
repo_dir = os.path.dirname(os.path.abspath(__file__))
work_dir = os.path.join(repo_dir, 'OK workspaces')
if work_dir not in sys.path:
    sys.path.insert(0, work_dir)

from hecate import Hecate


def main():
    parser = argparse.ArgumentParser(description="Simple on-screen chat with Hecate")
    parser.add_argument("--speak", action="store_true", help="Speak responses aloud")
    args = parser.parse_args()

    bot = Hecate()
    intro = bot.startup_message()
    if intro:
        print(intro)
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not user_input:
            continue
        if user_input.lower() in {"quit", "exit"}:
            break
        reply = bot.respond(user_input)
        print(reply)
        if args.speak:
            try:
                import subprocess
                subprocess.run(["espeak", reply], check=True)
            except Exception:
                pass


if __name__ == "__main__":
    main()
