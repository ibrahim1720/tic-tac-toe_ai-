import pygame
from Ai_Algorithms import AiAlgorithms


class UI:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 600, 600
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.grid_size = 400
        self.margin_x = (self.WIDTH - self.grid_size) // 2
        self.margin_y = (self.HEIGHT - self.grid_size) // 2
        self.cell_size = self.grid_size // 3
        self.draw_board()
        self.x_image = pygame.image.load("x_image.png")
        self.x_image = pygame.transform.scale(self.x_image, (self.cell_size - 2 * 5, self.cell_size - 2 * 5))
        self.recolor_image(self.x_image, (0, 0, 0))
        self.o_image = pygame.image.load("o_image.png")
        self.o_image = pygame.transform.scale(self.o_image, (self.cell_size - 2 * 5, self.cell_size - 2 * 5))
        self.recolor_image(self.o_image, (0, 0, 0))
        self.grid = [[None for _ in range(3)] for _ in range(3)]
        self.ai = AiAlgorithms()
        self.algorithm = None
        self.play = True
        self.exit = False
        self.game_over = False
        self.algorithm_selection_screen()

    def algorithm_selection_screen(self):
        font = pygame.font.SysFont("Arial", 16)

        while not self.exit:

            self.window.fill((30, 30, 30))
            title = font.render("Choose AI Algorithm", True, (255, 255, 255))
            self.window.blit(title, (self.WIDTH // 2 - title.get_width() // 2, 50))

            minimax_button = pygame.Rect(self.WIDTH // 2 - 155, 150, 300, 40)
            pygame.draw.rect(self.window, (50, 50, 50), minimax_button)
            minimax_text = font.render("Minimax Algorithm", True, (255, 255, 255))
            self.window.blit(minimax_text, (self.WIDTH // 2 - minimax_text.get_width() // 2, 160))

            minimax_depth_button = pygame.Rect(self.WIDTH // 2 - 155, 200, 300, 40)
            pygame.draw.rect(self.window, (50, 50, 50), minimax_depth_button)
            minimax_depth_text = font.render("Minimax with Depth", True, (255, 255, 255))
            self.window.blit(minimax_depth_text, (self.WIDTH // 2 - minimax_depth_text.get_width() // 2, 210))

            minimax_sym_button = pygame.Rect(self.WIDTH // 2 - 155, 250, 300, 40)
            pygame.draw.rect(self.window, (50, 50, 50), minimax_sym_button)

            minimax_sym_text = font.render("heuristic reduction minimax", True, (255, 255, 255))
            self.window.blit(minimax_sym_text, (self.WIDTH // 2 - minimax_sym_text.get_width() // 2, 255))

            alpha_beta_button = pygame.Rect(self.WIDTH // 2 - 155, 300, 300, 40)
            pygame.draw.rect(self.window, (50, 50, 50), alpha_beta_button)
            alpha_beta_text = font.render("Alpha Beta", True, (255, 255, 255))
            self.window.blit(alpha_beta_text, (self.WIDTH // 2 - alpha_beta_text.get_width() // 2, 310))

            alpha_beta_depth_button = pygame.Rect(self.WIDTH // 2 - 155, 350, 300, 40)
            pygame.draw.rect(self.window, (50, 50, 50), alpha_beta_depth_button)
            alpha_beta_depth_text = font.render("Alpha Beta with depth", True, (255, 255, 255))
            self.window.blit(alpha_beta_depth_text, (self.WIDTH // 2 - alpha_beta_depth_text.get_width() // 2, 360))

            alpha_beta_sym_button = pygame.Rect(self.WIDTH // 2 - 155, 400, 300, 40)
            pygame.draw.rect(self.window, (50, 50, 50), alpha_beta_sym_button)
            alpha_beta_sym_text = font.render("Alpha Beta with Symmetry", True, (255, 255, 255))
            self.window.blit(alpha_beta_sym_text, (self.WIDTH // 2 - alpha_beta_sym_text.get_width() // 2, 410))

            one_move_button = pygame.Rect(self.WIDTH // 2 - 155, 450, 300, 40)
            pygame.draw.rect(self.window, (50, 50, 50), one_move_button)
            one_move_text = font.render("One Move Heuristic", True, (255, 255, 255))
            self.window.blit(one_move_text, (self.WIDTH // 2 - one_move_text.get_width() // 2, 460))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if minimax_button.collidepoint(mouse_pos):
                        self.algorithm = 'minimax'
                        self.run_game()
                    elif minimax_depth_button.collidepoint(mouse_pos):
                        self.algorithm = 'minimax_depth'
                        self.run_game()
                    elif minimax_sym_button.collidepoint(mouse_pos):
                        self.algorithm = 'minimax_heuristic_reduction'
                        self.run_game()
                    elif alpha_beta_button.collidepoint(mouse_pos):
                        self.algorithm = 'alpha_beta'
                        self.run_game()
                    elif alpha_beta_depth_button.collidepoint(mouse_pos):
                        self.algorithm = 'alpha_beta_depth'
                        self.run_game()
                    elif alpha_beta_sym_button.collidepoint(mouse_pos):
                        self.algorithm = 'alpha_beta_symmetry'
                        self.run_game()
                    elif one_move_button.collidepoint(mouse_pos):
                        self.algorithm = 'one_move_heuristic'
                        self.run_game()

            pygame.display.flip()

    def run_game(self):
        # This method will handle the Tic-Tac-Toe gameplay logic
        while not self.exit:
            if not self.game_over:
                self.draw_board()
                self.track_events()
                self.draw_x_or_y()

            self.check_winner_or_tie()
            pygame.display.flip()

    def draw_board(self):
        self.window.fill((0, 0, 0))
        line_color = (0, 0, 0)
        grid_color = (169, 169, 169)
        pygame.draw.rect(self.window, grid_color, (self.margin_x, self.margin_y, self.grid_size, self.grid_size))
        for x in range(1, 3):
            pygame.draw.line(
                self.window,
                line_color,
                (self.margin_x + x * self.cell_size, self.margin_y),
                (self.margin_x + x * self.cell_size, self.margin_y + self.grid_size),
                2,
            )

        for y in range(1, 3):
            pygame.draw.line(
                self.window,
                line_color,
                (self.margin_x, self.margin_y + y * self.cell_size),
                (self.margin_x + self.grid_size, self.margin_y + y * self.cell_size),
                2,
            )

    def get_cell(self, pos):
        x, y = pos
        if not (
                self.margin_x <= x <= self.margin_x + self.grid_size and self.margin_y <= y <= self.margin_y + self.grid_size):
            return None, None
        col = (x - self.margin_x) // self.cell_size
        row = (y - self.margin_y) // self.cell_size
        return row, col

    def track_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit = True
            if self.play:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    row, col = self.get_cell(mouse_pos)
                    if row is not None and col is not None and self.grid[row][col] is None:
                        self.grid[row][col] = "x"
                    self.play = False
            else:
                choice = None
                if self.algorithm == 'minimax':
                    choice = self.ai.minimax(self.grid, True, 'o')[0]
                elif self.algorithm == 'minimax_heuristic_reduction':
                    choice = self.ai.minimax_heuristic_reduction(self.grid, 0, True, 'o')[0]
                elif self.algorithm == 'minimax_depth':
                    choice = self.ai.minimax_depth(self.grid, 0, True, '0')[0]

                elif self.algorithm == 'alpha_beta':
                    choice = self.ai.alpha_beta(self.grid, -20, 20, True, 'o')[0]
                elif self.algorithm == 'alpha_beta_depth':
                    choice = self.ai.alpha_beta_depth(self.grid, 0, -20, 20, True, 'o')[0]
                elif self.algorithm == 'alpha_beta_symmetry':
                    choice = self.ai.alpha_beta_symmetry(self.grid, 0, -20, 20, True, 'o')[0]
                elif self.algorithm == 'one_move_heuristic':
                    choice = self.ai.one_move_heuristic(self.grid, 'o')[0]

                row = choice['row']
                col = choice['col']
                if row is not None and col is not None and self.grid[row][col] is None:
                    self.grid[row][col] = "o"
                self.play = True

    def draw_x_or_y(self):
        for r in range(3):
            for c in range(3):
                if self.grid[r][c] == "x":
                    self.place_image(r, c, self.x_image)
                if self.grid[r][c] == "o":
                    self.place_image(r, c, self.o_image)

    def place_image(self, row, col, image, padding=5):
        x_pos = self.margin_x + col * self.cell_size + padding
        y_pos = self.margin_y + row * self.cell_size + padding
        self.window.blit(image, (x_pos, y_pos))

    def recolor_image(self, image, color):
        width, height = image.get_size()
        for x in range(width):
            for y in range(height):
                alpha = image.get_at((x, y)).a  # Preserve alpha transparency
                if alpha > 0:  # Only recolor non-transparent pixels
                    image.set_at((x, y), (*color, alpha))

    def check_winner_or_tie(self):
        winner = self.ai.is_game_over(self.grid)
        if winner[0] and winner[1] != 'tie':
            self.display_winner(winner[1])
            self.game_over = True
        elif winner[0] and winner[1] == 'tie':
            self.display_tie()
            self.game_over = True

    def display_winner(self, winner):
        # Display a message when someone wins
        font = pygame.font.SysFont("Arial", 50)
        if winner == 'o':
            text = font.render(f"You lost!", True, (255, 0, 0))
        else:
            text = font.render(f"You won!", True, (0, 0, 255))
        self.window.blit(text, (self.WIDTH // 2 - text.get_width() // 2, 20))
        self.retry_btn()

    def display_tie(self):
        # Display a message when there's a tie
        font = pygame.font.SysFont("Arial", 50)
        text = font.render("It's a tie!", True, (0, 255, 0))

        # Position the text at the top of the screen
        self.window.blit(text, (self.WIDTH // 2 - text.get_width() // 2, 20))  # Y-coordinate set to 20 for the top
        self.retry_btn()

    def retry_btn(self):
        font = pygame.font.SysFont("Arial", 30)
        retry_button = pygame.Rect(self.WIDTH // 2 - 155, 510, 300, 70)
        pygame.draw.rect(self.window, (50, 50, 50), retry_button)
        retry_text = font.render("Retry", True, (255, 255, 255))
        self.window.blit(retry_text, (self.WIDTH // 2 - retry_text.get_width() // 2, 525))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if retry_button.collidepoint(mouse_pos):
                    self.reset_game()
                    self.algorithm_selection_screen()

    def reset_game(self):
        self.grid = [[None for _ in range(3)] for _ in range(3)]
        self.play = True
        self.game_over = False
        self.algorithm = None
