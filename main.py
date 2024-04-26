import random
import hmac
import hashlib


class TableGenerator:
    def __init__(self, moves):
        self.moves = moves

    def generate_table(self):
        table = [[None] * (len(self.moves) + 1) for _ in range(len(self.moves) + 1)]
        table[0][0] = "Moves"
        for i in range(1, len(table)):
            table[i][0] = self.moves[i - 1]
            table[0][i] = self.moves[i - 1]

        for i in range(1, len(table)):
            for j in range(1, len(table[i])):
                table[i][j] = self.get_result(table[0][j], table[i][0])

        return table

    def get_result(self, move1, move2):
        n = len(self.moves)
        if move1 == move2:
            return "Draw"
        elif (self.moves.index(move2) - self.moves.index(move1)) % n <= n // 2:
            return "Win"
        else:
            return "Lose"


class MoveRules:
    def __init__(self, moves):
        self.moves = moves

    def get_result(self, move1, move2):
        n = len(self.moves)
        move1_index = self.moves.index(move1)
        move2_index = self.moves.index(move2)
        if move1_index == move2_index:
            return "Draw"
        elif (move2_index - move1_index) % n <= n // 2:
            return "Win"
        else:
            return "Lose"


class KeyGenerator:
    @staticmethod
    def generate_key():
        return hashlib.sha256(bytes(random.getrandbits(8) for _ in range(32))).hexdigest()


class MoveGenerator:
    def __init__(self, moves):
        self.moves = moves

    def generate_move(self):
        return random.choice(self.moves)


class RockPaperScissorsGame:
    def __init__(self, moves):
        self.moves = moves
        self.key = KeyGenerator.generate_key()
        self.move_generator = MoveGenerator(moves)
        self.move_rules = MoveRules(moves)
        self.table_generator = TableGenerator(moves)
        self.computer_move = None

    def calculate_hmac(self, move):
        return hmac.new(bytes.fromhex(self.key), move.encode(), hashlib.sha256).hexdigest()

    def display_help(self):
        table = self.table_generator.generate_table()
        for row in table:
            print(" | ".join(str(cell) for cell in row))

    def play(self):
        num_moves = len(self.moves)
        print(f"Number of moves: {num_moves}")
        print("HMAC key:", self.key)
        print()

        for i in range(num_moves):
            print(f"--- Game {i + 1} ---")

            print("Available moves:")
            for j, move in enumerate(self.moves, start=1):
                print(f"{j} - {move}")
            print("0 - Exit")
            print("? - Help")

            user_input = input("Enter your move: ")

            if user_input == "?":
                self.display_help()
                print()
                continue

            if user_input == "0":
                print("Exiting the game. Goodbye!")
                break

            try:
                user_move = self.moves[int(user_input) - 1]
            except (ValueError, IndexError):
                print("Invalid input. Please enter a valid move or ? for help.")
                print()
                continue

            self.computer_move = self.move_generator.generate_move()

            print(f"Your move: {user_move}")
            print(f"Computer move: {self.computer_move}")

            result = self.move_rules.get_result(user_move, self.computer_move)
            print(result + "!")
            print("HMAC:", self.calculate_hmac(self.move_generator.generate_move()))

    def check_computer_move(self):
        if self.computer_move is None:
            print("Computer move has not been generated yet.")
        else:
            print(f"Computer move: {self.computer_move}")

if __name__ == "__main__":
    moves = ["rock", "paper", "scissors", "lizard", "spock"]
    game = RockPaperScissorsGame(moves)
    game.play()
    game.check_computer_move()