import hashlib
import hmac
import os
import random
import sys
class MoveGenerator:
    @staticmethod
    def generate_move(moves):
        return random.choice(moves)


class HMACGenerator:
    @staticmethod
    def generate_key():
        # Generate a cryptographically strong random key with a length of at least 256 bits
        key = os.urandom(32)  # 32 bytes = 256 bits
        return key

    @staticmethod
    def generate_hmac(key, move):
        # Calculate HMAC using SHA-256
        h = hmac.new(key, move.encode(), hashlib.sha256)
        return h.hexdigest()


class GameRules:
    @staticmethod
    def determine_winner(moves, user_move, computer_move):
        moves_len = len(moves)
        half_len = moves_len // 2

        user_index = moves.index(user_move)
        computer_index = moves.index(computer_move)

        if user_index == computer_index:
            return "Draw"
        elif (user_index - computer_index) % moves_len <= half_len:
            return "Win"
        else:
            return "Lose"


def print_help_table(moves):
    moves_len = len(moves)
    header = [""] + moves
    table = [header]

    for move_row in moves:
        row = [move_row]
        for move_col in moves:
            result = GameRules.determine_winner(moves, move_row, move_col)
            row.append(result)
        table.append(row)

    print_table(table)


def print_table(table):
    col_widths = [max(len(str(cell)) for cell in col) for col in zip(*table)]
    for row in table:
        print("  ".join(str(cell).ljust(width) for cell, width in zip(row, col_widths)))


def main():
    moves = sys.argv[1:]
    moves_len = len(moves)

    if moves_len % 2 == 0 or moves_len < 3:
        print("Error: The number of moves must be odd and greater than or equal to 3.")
        print("Example usage: python script.py rock paper scissors")
        return

    hmac_key = HMACGenerator.generate_key()
    computer_move = MoveGenerator.generate_move(moves)
    computer_hmac = HMACGenerator.generate_hmac(hmac_key, computer_move)

    print("HMAC:", computer_hmac)
    print("Available moves:")
    for i, move in enumerate(moves, start=1):
        print(f"{i} - {move}")

    print("0 - Exit")
    print("? - Help")

    while True:
        user_input = input("Enter your move: ")
        if user_input == "?":
            print_help_table(moves)
            continue
        elif user_input == "0":
            print("Exiting the game.")
            return

        try:
            user_move_index = int(user_input) - 1
            if user_move_index < 0 or user_move_index >= moves_len:
                raise ValueError
        except ValueError:
            print("Invalid input. Please enter a valid move number.")
            continue

        user_move = moves[user_move_index]

        print(f"Your move: {user_move}")
        print(f"Computer move: {computer_move}")
        print("HMAC key:", hmac_key.hex())
        result = GameRules.determine_winner(moves, user_move, computer_move)
        print("You", result + "!")


if __name__ == "__main__":
    main()