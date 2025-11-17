from src.storage.RDSManager import RDSManager
from src.storage.serializers import gameEngine

class SaveRepository:
    def __init__(self, rds_config):
        self.db.save_game = RDSManager(**rds_config)
        
    def save(self, engine: gameEngine, gameName: str) -> int:
        return self.rds_manager.save_game(engine, gameName)
    
    def load(self, save_id: int) -> gameEngine | None:
        return self.rds_manager.load_game(save_id)
    
    def list_saves(self) -> list[int]:
        return self.rds_manager.list_saves()
        