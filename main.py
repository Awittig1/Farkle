from src.cli.cli_ui import run_cli
from src.gui.pygame_ui import run_pygame
import sys

def main():
    # Check command line arguments to choose interface
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        print("Starting Farkle with PyGame cli...")
        run_cli()
    else:
        print("Starting Farkle with gui interface...")
        run_pygame()

if __name__ == "__main__":
    main()