### ファイル: qlearning_ai.py
import pickle
import random
import os
import argparse
from game import Game

ACTIONS = ['Up', 'Down', 'Left', 'Right']

def rotate_board(board):
    return [list(row) for row in zip(*board[::-1])]

def normalize_state(state):
    board = [list(state[i*4:(i+1)*4]) for i in range(4)]
    boards = []
    b = board
    for _ in range(4):
        boards.append(tuple(tile for row in b for tile in row))
        b = rotate_board(b)
    return max(boards)

def choose_action(q_table, state, epsilon):
    if random.random() < epsilon:
        return random.choice(ACTIONS)
    values = [q_table.get((state, a), 0.0) for a in ACTIONS]
    max_v = max(values)
    best = [a for a, v in zip(ACTIONS, values) if v == max_v]
    return random.choice(best)

def update_q(q_table, state, action, reward, next_state, alpha, gamma):
    max_next = max(q_table.get((next_state, a), 0.0) for a in ACTIONS)
    old = q_table.get((state, action), 0.0)
    q_table[(state, action)] = old + alpha * (reward + gamma * max_next - old)

def train_q_learning(episodes=1000, epsilon=0.1, alpha=0.1, gamma=0.9, save_path='qtable.pkl'):
    if os.path.exists(save_path):
        with open(save_path, 'rb') as f:
            q_table = pickle.load(f)
        print(f"Loaded existing Q-table from {save_path}")
    else:
        q_table = {}
    for ep in range(1, episodes + 1):
        game = Game()
        state = normalize_state(game.get_state())
        done = False
        while not done:
            action = choose_action(q_table, state, epsilon)
            reward, done = game.step(action)
            next_state = normalize_state(game.get_state())
            update_q(q_table, state, action, reward, next_state, alpha, gamma)
            state = next_state
        if ep % 100 == 0:
            print(f"Episode {ep} finished. Score: {game.score}, Max Tile: {game.max_tile()}")
    with open(save_path, 'wb') as f:
        pickle.dump(q_table, f)
    print(f"Q-table saved to {save_path}")

### ファイル: q_ai.py
import pickle
from game import Game

class QAI:
    def __init__(self, qtable_path='qtable.pkl'):
        with open(qtable_path, 'rb') as f:
            self.q_table = pickle.load(f)
        self.actions = ['Up', 'Down', 'Left', 'Right']

    def normalize_state(self, state):
        board = [list(state[i*4:(i+1)*4]) for i in range(4)]
        boards = []
        b = board
        for _ in range(4):
            boards.append(tuple(tile for row in b for tile in row))
            b = [list(row) for row in zip(*b[::-1])]
        return max(boards)

    def choose_move(self, game):
        state = self.normalize_state(game.get_state())
        values = [self.q_table.get((state, a), 0.0) for a in self.actions]
        max_v = max(values)
        best_actions = [a for a, v in zip(self.actions, values) if v == max_v]
        return best_actions[0], f"Q-value: {max_v:.2f}"  # 説明文も返す

### main.py側の変更（例）
# from ai import SimpleAI → from q_ai import QAI
# self.ai = QAI() に差し替え

# また、AIに連続試行させる関数などで ai.choose_move(game) を呼び出せば、
# Q学習済みのAIが行動選択を行い続けます。

# 学習はコマンドで: python qlearning_ai.py --episodes 5000 など
# その後に main.py を起動すれば、GUIで Q 学習済み AI がプレイします。

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train 2048 Q-learning AI')
    parser.add_argument('--episodes', type=int, default=1000,
                        help='number of training episodes')
    parser.add_argument('--epsilon', type=float, default=0.1,
                        help='epsilon for epsilon-greedy')
    parser.add_argument('--alpha', type=float, default=0.1,
                        help='learning rate')
    parser.add_argument('--gamma', type=float, default=0.9,
                        help='discount factor')
    parser.add_argument('--qtable', default='qtable.pkl',
                        help='path to save/load Q-table')
    args = parser.parse_args()

    train_q_learning(episodes=args.episodes, epsilon=args.epsilon,
                     alpha=args.alpha, gamma=args.gamma,
                     save_path=args.qtable)
