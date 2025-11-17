import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import random
from game.scoring import Scoring
from game.dice import Dice

##one and 5 test
print(f"\nDice roll: [1] => Score: {Scoring.calculateScore([1])}")
print(f"\nDice roll: [5] => Score: {Scoring.calculateScore([5])}")

##three of a kind test
print("\nThree of a kind tests:")
for i in range(6):
    n = i + 1
    threePairRoll = [n, n, n]
    print(f"Dice roll: {threePairRoll} => Score: {Scoring.calculateScore(threePairRoll)}")

##four of a kind test
print("\nFour of a kind tests:")
for i in range(6):
    n = i + 1
    fourPairRoll = [n, n, n, n]
    print(f"Dice roll: {fourPairRoll} => Score: {Scoring.calculateScore(fourPairRoll)}")

##five of a kind test
print("\nFive of a kind tests:")
for i in range(6):
    n = i + 1
    fivePairRoll = [n, n, n, n, n]
    print(f"Dice roll: {fivePairRoll} => Score: {Scoring.calculateScore(fivePairRoll)}")

##six of a kind test
print("\nSix of a kind tests:")
for i in range(6):
    n = i + 1
    sixPairRoll = [n, n, n, n, n, n]
    print(f"Dice roll: {sixPairRoll} => Score: {Scoring.calculateScore(sixPairRoll)}")

#straight test
print("\nStraight test:")
print(f"Dice roll: [1, 2, 3, 4, 5, 6] => Score: {Scoring.calculateScore([1, 2, 3, 4, 5, 6])}")

#two sets of three test
print("\nTwo sets of three test:")
for i in range(1, 7):
    for j in range(1, 7):
        if i != j:
            twoSetsRoll = [i, i, i, j, j, j]
            print(f"Dice roll: {twoSetsRoll} => Score: {Scoring.calculateScore(twoSetsRoll)}")

##bad dice roll check
print("\nBad dice roll tests:")
for i in range(50):
    dice_roll = Dice.roll(random.randint(3,6))
    score = Scoring.calculateScore(dice_roll)
    print(f"Dice roll: {dice_roll} => Score: {score}")