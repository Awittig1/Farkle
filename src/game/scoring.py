class Scoring:
    @staticmethod
    def calculateScore(dice: list[int]) -> int:
        dlen = len(dice)
        score = 0
        
        #
        #    How most of this worsks is two principals:
        #1. Check for the length of dice being scored 
        #    ie : 3 dice can only be 3 of a kind where 6 can be multiple things
        #
        #2. Check for what the dice actually are
        #    this works by mainly ensuring the length of the list in set form is 1,
        #    ensuring
        #
        
        #1 or 5
        if dlen == 1:
            if dice == [1]:
                score += 100
            elif dice == [5]:
                score += 50
            else:
                score = 0

        #three of a kind
        elif dlen == 3 and len(set(dice)) == 1:
             if len(set(dice)) == 1:
                if dice[0] == 1:
                    score += 1000
                else:
                    score += (dice[0] * 100)  

        #four of a kind
        elif dlen == 4 and len(set(dice)) == 1:
            if len(set(dice)) == 1:
                if dice[0] == 1:
                    score += 2000
                else:
                    score += (dice[0] * 100) * 2

        #five of a kind
        elif dlen == 5 and len(set(dice)) == 1:
            if len(set(dice)) == 1:
                if dice[0] == 1:
                    score += 3000
                else:
                    score += (dice[0] * 100) * 3

        #six dice
        elif dlen == 6:           

            #six of a kind
            if len(set(dice)) == 1:
                if dice[0] == 1:
                    score += 4000
                else:
                    score += (dice[0] * 100) * 4  
                             
            #straight
            elif sum(set(dice)) == 21 and len(set(dice)) == 6:
                score += 1500                

            #2 sets of 3
            elif len(set(dice)) == 2 and all(dice.count(x) == 3 for x in set(dice)):
                score += 2500

        #bad roll        
        else:
            score = 0


        return score