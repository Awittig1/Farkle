class turnCheck:
    @staticmethod
    def turnCheck(players, turn):
        return (turn + 1) % len(players)