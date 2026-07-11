import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from PokePY.app import Game

if __name__ == "__main__":
    Game().run()
