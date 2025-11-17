import mysql.connector
from mysql.connector import Error
from src.game.game_engine import gameEngine
from contextlib import contextmanager

class RDSManager:
    def __init__(self, host, user, password, port=3306):
        self.conn = mysql.connector.connect(
            host = host,
            database = "FarkleDB",
            user = user,
            password = password,
            port = port
        )
    
    def get_connection(self):
        conn = None
        try:
            conn = mysql.connector.connect(**self.config)
            yield conn
        finally:
            if conn:
                conn.close()
            
    def save_game(self, engine: gameEngine, game_name: str) -> int:
        try:
            cur = self.conn.cursor()
            #insert new save
            cur.execute(
                "INSERT INTO game_saves (game_name, current_player_index) VALUES (%s, %s)",
                (game_name, engine.current_player_index)
            )
            save_id = cur.lastrowid
            
            #insert players
            for player in engine.players:
                cur.execute(
                    "INSERT INTO players (save_id, player_name, player_data) VALUES (%s, %s, %s)",
                    (save_id, player.name, player.serialize())
                )
                
            self.conn.commit()
            return save_id
        except Error as e:
            print(f"Error saving game: {e}")
            self.conn.rollback()
            return -1
        finally:
            cur.close()
    
    def load_game(self, save_id: int) -> gameEngine | None:
        try:
            cur = self.conn.cursor(dictionary=True)
            
            #load turn state
            cur.execute(
                "SELECT current_player_index FROM game_saves WHERE save_id = %s",
                (save_id,)
            )
            save_row = cur.fetchone()
            if not save_row:
                return None
            
            #get players
            cur.execute(
                "SELECT player_name, score FROM players WHERE save_id = %s ORDER BY player_id",
                (save_id,)
            )
            players = cur.fetchall()
            
            #reconstruct game engine
            engine = gameEngine(players=[p["name"]for p in players])
            for idx, p in enumerate(players):
                engine.players[idx].score = p["score"]
            
            engine.current_player_index = save_row["current_player_index"]
            return engine
        except Error as e:
            print(f"Error loading game: {e}")
            return None
        finally:
            cur.close()
        
    def list_saves(self) -> list[int]:
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT save_id FROM game_saves ORDER BY created_at DESC")
            return [row[0] for row in cur.fetchall()]
        except Error as e:
            print(f"Error listing saves: {e}")
            return []
        finally:
            cur.close()