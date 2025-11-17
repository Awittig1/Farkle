class turnCheck:
    def turnCheck(players, turn):
        pCount = len(players)
        if turn + 1 >= pCount:
            turn = 0
        else:
            turn += 1
        return turn