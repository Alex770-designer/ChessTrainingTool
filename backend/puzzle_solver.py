import chess
import json


def load_puzzle():

    with open("analysis.json") as file:
        puzzles = json.load(file)

    for puzzle in puzzles:

        if puzzle["category"] == "BLUNDER":
            return puzzle

    return None



def play_puzzle(puzzle):

    board = chess.Board(
        puzzle["fen"]
    )

    print(board)

    print("\nFind the best move!")

    user_move = input("Your move (example e2e4): ")

    correct_move = puzzle["best_move"]


    if user_move == correct_move:
        print("\nCorrect! 🎯")
    else:
        print("\nIncorrect.")
        print("Best move:", correct_move)



puzzle = load_puzzle()

if puzzle:
    play_puzzle(puzzle)

else:
    print("No puzzles found.")