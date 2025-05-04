import pygame
import time

# Инициализация pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 400, 300  # Расширили для интерфейса
C_SIZE = 300 // 3
I_WIDTH = 100
L_COLOR = (0, 0, 0)
BG_COLOR = (255, 255, 255)
X_COLOR = (200, 0, 0)
O_COLOR = (0, 0, 200)
T_COLOR = (255, 215, 0)
L_WIDTH = 5
F_WIDTH = 8
F_COLOR = (150, 150, 150)  # Цвет для подсветки исчезающей фигуры
W_COLOR = (0, 0, 0, 180)  # Полупрозрачный фон для текста победы

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Динамические крестики нолики")
screen.fill(BG_COLOR)

font = pygame.font.Font(None, 40)
win_font = pygame.font.Font(None, 60)


class DynamicTicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.moves = {'X': [], 'O': []}
        self.current = 'X'
        self.scores = {'X': 0, 'O': 0}
        self.win = None

    def draw(self):
        screen.fill(BG_COLOR)

        for i in range(1, 3):
            pygame.draw.line(screen, L_COLOR, (100, i * C_SIZE),
                             (400, i * C_SIZE), L_WIDTH)
            pygame.draw.line(screen, L_COLOR, (100 + i * C_SIZE, 0),
                             (100 + i * C_SIZE, 300), L_WIDTH)

        for r in range(3):
            for c in range(3):
                fig_col = X_COLOR if self.board[r][c] == 'X' else O_COLOR
                if (r, c) in self.moves[self.current][:1]:
                    fig_col = F_COLOR

                if self.board[r][c] == 'X':
                    pygame.draw.line(screen, fig_col,
                                     (100 + c * C_SIZE + 30, r * C_SIZE + 30),
                                     (100 + (c + 1) * C_SIZE - 30,
                                      (r + 1) * C_SIZE - 30), F_WIDTH)
                    pygame.draw.line(screen, fig_col,
                                     (100 + (c + 1) * C_SIZE - 30,
                                      r * C_SIZE + 30),
                                     (100 + c * C_SIZE + 30, (r + 1)
                                      * C_SIZE - 30), F_WIDTH)
                elif self.board[r][c] == 'O':
                    pygame.draw.circle(screen, fig_col,
                                       (100 + c * C_SIZE + C_SIZE // 2,
                                        r * C_SIZE + C_SIZE // 2),
                                       C_SIZE // 3, F_WIDTH)

        pygame.draw.rect(screen, (200, 200, 200),
                         (0, 0, I_WIDTH, HEIGHT))
        player_text = font.render(self.current, True,
                                  X_COLOR if self.current == 'X' else O_COLOR)
        screen.blit(player_text, (30, 50))
        score_text = font.render(f"{self.scores['X']} - {self.scores['O']}",
                                 True, (0, 0, 0))
        screen.blit(score_text, (15, 100))

        if self.win:
            win_text = win_font.render("WIN!", True, T_COLOR)
            rect = win_text.get_rect(center=(250, HEIGHT // 2))
            bg = pygame.Rect(rect.left - 10, rect.top - 10,
                             rect.width + 20, rect.height + 20)
            pygame.draw.rect(screen, (0, 0, 0), bg)
            screen.blit(win_text, rect.topleft)

        pygame.display.flip()

    def check(self):
        for r in self.board:
            if r.count(r[0]) == 3 and r[0] != ' ':
                return r[0]
        for c in range(3):
            if self.board[0][c] == self.board[1][c] == self.board[2][c] != ' ':
                return self.board[0][c]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]
        return None

    def move(self, r, c):
        if self.board[r][c] == ' ' and not self.win:
            self.board[r][c] = self.current
            self.moves[self.current].append((r, c))

            if len(self.moves[self.current]) > 3:
                old_r, old_c = self.moves[self.current].pop(0)
                self.board[old_r][old_c] = ' '

            self.win = self.check()
            if self.win:
                self.scores[self.win] += 1
                self.draw()
                pygame.display.flip()
                time.sleep(2)
                self.reset()
            else:
                self.current = 'O' if self.current == 'X' else 'X'

            self.draw()

    def reset(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.moves = {'X': [], 'O': []}
        self.current = 'O' if self.win == 'X' else 'X'
        self.win = None

    def cell(self, pos):
        return pos[1] // C_SIZE, (pos[0] - 100) // C_SIZE

    def play(self):
        running = True
        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                elif e.type == pygame.MOUSEBUTTONDOWN and e.pos[0] > 100:
                    r, c = self.cell(e.pos)
                    if 0 <= r < 3 and 0 <= c < 3:
                        self.move(r, c)
        pygame.quit()


if __name__ == "__main__":
    game = DynamicTicTacToe()
    game.draw()
    game.play()

