
import tkinter as tk
from game import Game
from simple_ai_qlearn import SimpleAIQ

class GameUI:
    def __init__(self, root):
        self.root = root
        self.game = Game()
        self.ai = SimpleAIQ('qtable.pkl')
        self.auto_job = None

        self.root.title("2048 Q学習AI")
        self.cells = []
        for r in range(4):
            row = []
            for c in range(4):
                lbl = tk.Label(root, text='', width=4, height=2,
                               font=('Helvetica', 24), borderwidth=2, relief='solid')
                lbl.grid(row=r, column=c, padx=5, pady=5)
                row.append(lbl)
            self.cells.append(row)

        self.score_label = tk.Label(root, text='Score: 0')
        self.score_label.grid(row=4, column=0, columnspan=4)

        self.comment_label = tk.Label(root, text='', wraplength=300, justify='left')
        self.comment_label.grid(row=5, column=0, columnspan=4)

        self.auto_btn = tk.Button(root, text='Auto Play', command=self.start_auto)
        self.auto_btn.grid(row=6, column=0, columnspan=1)

        self.reset_btn = tk.Button(root, text='Restart', command=self.reset_game)
        self.reset_btn.grid(row=6, column=1, columnspan=1)

        self.stop_btn = tk.Button(root, text='Stop', command=self.stop_auto)
        self.stop_btn.grid(row=6, column=2, columnspan=1)

        self.update_ui()

    def reset_game(self):
        self.game.reset()
        self.update_ui()
        self.comment_label.config(text='Restarted.')

    def start_auto(self):
        if self.auto_job is None:
            self.auto_step()

    def stop_auto(self):
        if self.auto_job:
            self.root.after_cancel(self.auto_job)
            self.auto_job = None
            self.comment_label.config(text='Auto play stopped.')

    def auto_step(self):
        direction, explanation = self.ai.choose_move(self.game)
        self.comment_label.config(text=explanation)
        if direction is None:
            self.stop_auto()
            return
        moved, _ = self.game.move(direction)
        if moved:
            self.game.add_random_tile()
            self.update_ui()
            if self.game.can_move():
                self.auto_job = self.root.after(300, self.auto_step)
            else:
                self.comment_label.config(text='Game Over.')

    def update_ui(self):
        for r in range(4):
            for c in range(4):
                value = self.game.board[r][c]
                self.cells[r][c]['text'] = str(value) if value else ''
        self.score_label.config(text='Score: {}'.format(self.game.score))

if __name__ == '__main__':
    root = tk.Tk()
    ui = GameUI(root)
    root.mainloop()
