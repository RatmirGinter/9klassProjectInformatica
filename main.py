import pygame
import time

# Инициализация pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 400, 300  # Расширили для интерфейса
CELL_SIZE = 300 // 3
INFO_WIDTH = 100
LINE_COLOR = (0, 0, 0)
BG_COLOR = (255, 255, 255)
X_COLOR = (200, 0, 0)
O_COLOR = (0, 0, 200)
TEXT_COLOR = (255, 215, 0)
LINE_WIDTH = 5
FIGURE_WIDTH = 8
FADED_COLOR = (150, 150, 150)  # Цвет для подсветки исчезающей фигуры
WIN_BG_COLOR = (0, 0, 0, 180)  # Полупрозрачный фон для текста победы

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dynamic Tic Tac Toe")
screen.fill(BG_COLOR)

font = pygame.font.Font(None, 40)
win_font = pygame.font.Font(None, 60)


class DynamicTicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.moves = {'X': [], 'O': []}
        self.current_player = 'X'
        self.scores = {'X': 0, 'O': 0}
        self.winner = None

    def draw_board(self):
        screen.fill(BG_COLOR)

        # Поле
        for i in range(1, 3):
            pygame.draw.line(screen, LINE_COLOR, (100, i * CELL_SIZE), (400, i * CELL_SIZE), LINE_WIDTH)
            pygame.draw.line(screen, LINE_COLOR, (100 + i * CELL_SIZE, 0), (100 + i * CELL_SIZE, 300), LINE_WIDTH)

        for row in range(3):
            for col in range(3):
                figure_color = X_COLOR if self.board[row][col] == 'X' else O_COLOR
                if (row, col) in self.moves[self.current_player][:1]:  # Подсветка следующей удаляемой фигуры
                    figure_color = FADED_COLOR

                if self.board[row][col] == 'X':
                    pygame.draw.line(screen, figure_color, (100 + col * CELL_SIZE + 30, row * CELL_SIZE + 30),
                                     (100 + (col + 1) * CELL_SIZE - 30, (row + 1) * CELL_SIZE - 30), FIGURE_WIDTH)
                    pygame.draw.line(screen, figure_color, (100 + (col + 1) * CELL_SIZE - 30, row * CELL_SIZE + 30),
                                     (100 + col * CELL_SIZE + 30, (row + 1) * CELL_SIZE - 30), FIGURE_WIDTH)
                elif self.board[row][col] == 'O':
                    pygame.draw.circle(screen, figure_color,
                                       (100 + col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                                       CELL_SIZE // 3, FIGURE_WIDTH)

        # Интерфейс
        pygame.draw.rect(screen, (200, 200, 200), (0, 0, INFO_WIDTH, HEIGHT))
        current_text = font.render(self.current_player, True, X_COLOR if self.current_player == 'X' else O_COLOR)
        screen.blit(current_text, (30, 50))
        score_text = font.render(f"{self.scores['X']} - {self.scores['O']}", True, (0, 0, 0))
        screen.blit(score_text, (15, 100))

        # Победа
        if self.winner:
            win_text = win_font.render("WIN!", True, TEXT_COLOR)
            text_rect = win_text.get_rect(center=(250, HEIGHT // 2))  # Центрируем по игровому полю

            # Фон под текстом победы
            bg_rect = pygame.Rect(text_rect.left - 10, text_rect.top - 10, text_rect.width + 20, text_rect.height + 20)
            pygame.draw.rect(screen, (0, 0, 0), bg_rect)  # Черный фон
            screen.blit(win_text, text_rect.topleft)

        pygame.display.flip()

    def check_winner(self):
        for row in self.board:
            if row.count(row[0]) == 3 and row[0] != ' ':
                return row[0]
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                return self.board[0][col]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]
        return None

    def make_move(self, row, col):
        if self.board[row][col] == ' ' and not self.winner:
            self.board[row][col] = self.current_player
            self.moves[self.current_player].append((row, col))

            if len(self.moves[self.current_player]) > 3:
                old_row, old_col = self.moves[self.current_player].pop(0)
                self.board[old_row][old_col] = ' '

            self.winner = self.check_winner()
            if self.winner:
                self.scores[self.winner] += 1
                self.draw_board()
                pygame.display.flip()
                time.sleep(2)
                self.reset_board()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'

            self.draw_board()

    def reset_board(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.moves = {'X': [], 'O': []}
        self.current_player = 'O' if self.winner == 'X' else 'X'
        self.winner = None

    def get_cell(self, pos):
        return pos[1] // CELL_SIZE, (pos[0] - 100) // CELL_SIZE

    def play(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.pos[0] > 100:
                    row, col = self.get_cell(event.pos)
                    if 0 <= row < 3 and 0 <= col < 3:
                        self.make_move(row, col)
        pygame.quit()


if __name__ == "__main__":
    game = DynamicTicTacToe()
    game.draw_board()
    game.play()

