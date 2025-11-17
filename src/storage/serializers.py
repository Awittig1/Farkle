import json
from src.game.game_engine import gameEngine

def serialize_game_state(engine: gameEngine) -> bytes:
    data = {
        "players": [
            {
                "name": player.name,
                "score": player.score,
            } 
            for player in engine.players
        ],
        "current_player_index": engine.current_player_index,
    }
    return json.dumps(data, indent=4).encode('utf-8')

def deserialize_game_state(data: bytes) -> gameEngine:
    raw = json.loads(payload.decode('utf-8'))
    
    #Build engine
    engine = gameEngine(players=[p["name"] for p in raw["players"]])
    
    #restore player scores
    for idx, p in enumerate(raw["players"]):
        engine.players[idx].score = p["score"]
        
    #restore turn state
    engine.current_player_index = raw["current_player_index"]
    
    return engine
    