from ..game.game_engine import gameEngine
from ..game.player import Player
def run_cli():
    print("Farkle CLI Prototype")
    playerNames = Player.getPlayers()
    game = gameEngine(playerNames)
    game.startGame()
    
