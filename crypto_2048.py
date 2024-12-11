
import random
import curses

# Mapping of numbers to crypto symbols
CRYPTO_SYMBOLS = {
    2: "ETH",
    4: "BTC",
    8: "LTC",
    16: "DOGE",
    32: "ADA",
    64: "XRP",
    128: "SOL",
    256: "DOT",
    512: "AVAX",
    1024: "BNB",
    2048: "MATIC"
}

class Game2048:
    def __init__(self):
        self.board = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.spawn_new()
        self.spawn_new()

    def spawn_new(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.board[i][j] = 2 if random.random() < 0.9 else 4

    def slide_and_merge(self, row):
        new_row = [num for num in row if num != 0]
        for i in range(len(new_row) - 1):
            if new_row[i] == new_row[i + 1]:
                new_row[i] *= 2
                self.score += new_row[i]
                new_row[i + 1] = 0
        new_row = [num for num in new_row if num != 0]
        return new_row + [0] * (4 - len(new_row))

    def move(self, direction):
        rotated = False
        moved = False

        if direction in ('UP', 'DOWN'):
            self.board = list(zip(*self.board))
            rotated = True

        if direction in ('RIGHT', 'DOWN'):
            self.board = [row[::-1] for row in self.board]

        new_board = [self.slide_and_merge(row) for row in self.board]
        if new_board != self.board:
            moved = True

        self.board = new_board

        if direction in ('RIGHT', 'DOWN'):
            self.board = [row[::-1] for row in self.board]

        if rotated:
            self.board = list(zip(*self.board))

        if moved:
            self.spawn_new()

        return moved

    def is_game_over(self):
        if any(0 in row for row in self.board):
            return False

        for i in range(4):
            for j in range(4):
                if i + 1 < 4 and self.board[i][j] == self.board[i + 1][j]:
                    return False
                if j + 1 < 4 and self.board[i][j] == self.board[i][j + 1]:
                    return False

        return True

    def draw(self, stdscr):
        stdscr.clear()
        stdscr.addstr(f"Score: {self.score}\n\n")
        for row in self.board:
            stdscr.addstr("\t".join(CRYPTO_SYMBOLS.get(num, "    ").rjust(4) if num != 0 else "    " for num in row) + "\n")
        stdscr.addstr("\nUse arrow keys to play. Press 'q' to quit.")


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    game = Game2048()

    while True:
        game.draw(stdscr)
        key = stdscr.getch()

        if key == curses.KEY_UP:
            game.move('UP')
        elif key == curses.KEY_DOWN:
            game.move('DOWN')
        elif key == curses.KEY_LEFT:
            game.move('LEFT')
        elif key == curses.KEY_RIGHT:
            game.move('RIGHT')
        elif key == ord('q'):
            break

        if game.is_game_over():
            stdscr.clear()
            stdscr.addstr(f"Game Over! Final Score: {game.score}\n")
            stdscr.addstr("Press 'q' to quit.")
            while stdscr.getch() != ord('q'):
                pass
            break

if __name__ == "__main__":
    curses.wrapper(main)
