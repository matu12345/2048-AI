
import random

class Game:
    def __init__(self, size=4):
        self.size = size
        self.score = 0
        self.board = [[0]*size for _ in range(size)]
        self.add_random_tile()
        self.add_random_tile()

    def get_state(self):
        """Return the current board flattened as a tuple."""
        return tuple(tile for row in self.board for tile in row)

    def reset(self):
        self.score = 0
        self.board = [[0]*self.size for _ in range(self.size)]
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        empties = [
            (r, c)
            for r in range(self.size)
            for c in range(self.size)
            if self.board[r][c] == 0
        ]
        if not empties:
            return
        r, c = random.choice(empties)
        self.board[r][c] = 4 if random.random() < 0.1 else 2

    def _move_row_left(self, row):
        new_row = [i for i in row if i != 0]
        score = 0
        i = 0
        while i < len(new_row) - 1:
            if new_row[i] == new_row[i+1]:
                new_row[i] *= 2
                score += new_row[i]
                new_row.pop(i+1)
                i += 1
            else:
                i += 1
        new_row += [0] * (self.size - len(new_row))
        changed = new_row != row
        return new_row, score, changed

    def move(self, direction):
        changed_any = False
        total_score = 0
        board = self.board
        for _ in range({'Left': 0, 'Up': 3, 'Right': 2, 'Down': 1}[direction]):
            board = [list(row) for row in zip(*board[::-1])]
        new_board = []
        for row in board:
            new_row, score, changed = self._move_row_left(list(row))
            new_board.append(new_row)
            total_score += score
            if changed:
                changed_any = True
        for _ in range({'Left': 0, 'Up': 1, 'Right': 2, 'Down': 3}[direction]):
            new_board = [list(row) for row in zip(*new_board[::-1])]
        if changed_any:
            self.board = new_board
            self.score += total_score
        return changed_any, total_score

    def step(self, direction):
        """Apply a move and add a random tile. Return reward and done flag."""
        changed, reward = self.move(direction)
        if changed:
            self.add_random_tile()
        done = not self.can_move()
        return reward, done

    def max_tile(self):
        return max(max(row) for row in self.board)

    def can_move(self):
        if any(0 in row for row in self.board):
            return True
        for r in range(self.size):
            for c in range(self.size - 1):
                if self.board[r][c] == self.board[r][c + 1]:
                    return True
        for c in range(self.size):
            for r in range(self.size - 1):
                if self.board[r][c] == self.board[r + 1][c]:
                    return True
        return False
