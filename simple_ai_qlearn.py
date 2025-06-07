
import pickle

ACTIONS = ['Up', 'Down', 'Left', 'Right']

class SimpleAIQ:
    def __init__(self, qtable_path='qtable.pkl'):
        with open(qtable_path, 'rb') as f:
            self.q_table = pickle.load(f)

    def normalize_state(self, board):
        def rotate(b): return [list(row) for row in zip(*b[::-1])]
        boards = []
        b = [list(board[i*4:(i+1)*4]) for i in range(4)]
        for _ in range(4):
            boards.append(tuple(tile for row in b for tile in row))
            b = rotate(b)
        return max(boards)

    def choose_move(self, game):
        state = self.normalize_state(game.get_state())
        best = None
        best_value = -float('inf')
        for a in ACTIONS:
            v = self.q_table.get((state, a), 0.0)
            if v > best_value:
                best_value = v
                best = a
        return best, f'Q値に基づく選択: {best} (value={best_value})'
