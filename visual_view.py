import pygame
from engine import Tetris
from assets.visuals import visuals


class Visual:
    def __init__(self, model: Tetris, window=None, fps=60):
        if model is None:
            model = Tetris()
        if window is None:
            window = pygame.display.set_mode((500, 550))

        self.model = model
        self.window = window
        self.fps = fps

        self.main_game_rect_border = (0, 0, 270, 550)
        self.main_game_rect = (20, 20, 230, 510)
        self.next_rect = (self.main_game_rect_border[2] - 20, 80, 250, 200)

        self.x1, self.y1, self.x2, self.y2 = self.main_game_rect_border

        self.clock = pygame.time.Clock()

    def render(self):
        """Render the visual view given an engine"""
        # First, advance the clock one frame and fill the window.
        self.clock.tick(self.fps)
        self.window.fill(visuals.white)

        self.draw_board()
        self.draw_next(self.model.piece_next)
        self.draw_info(self.model.level, self.model.score, self.model.cleared_count)
        pygame.display.update()

        if self.model.is_game_over():
            # TODO: Real game over screen
            print("Final Score: {}".format(str(self.model.score)))

    def draw_board(self):
        pygame.draw.rect(self.window, visuals.black, self.main_game_rect_border)
        x1, y1, x2, y2 = self.main_game_rect
        dx = x2 / self.model.columns
        dy = y2 / self.model.rows

        pygame.draw.rect(self.window, visuals.grey_2, self.main_game_rect)

        for square_y in range(self.model.rows):
            for square_x in range(self.model.columns):
                ind = self.model.board[square_y][square_x]
                if ind != 0:
                    x = x1 + square_x * dx
                    y = y1 + square_y * dy
                    self.draw_tile((x, y, dx, dy), ind)

        if self.model.current is not None:
            explorer_y = 0
            while self.model.is_valid_translation(0, explorer_y + 1):
                explorer_y += 1

            for board_x, board_y in self.model.current.get_coods():
                x = x1 + board_x * dx
                y = y1 + board_y * dy
                ind = self.model.current.shape.ind
                self.draw_tile((x, y, dx, dy), ind)

                if explorer_y != 0:
                    temp = (x, y + explorer_y * dy, dx, dy)

                    surface = pygame.Surface(temp[2:])
                    surface.fill(visuals.grey_3)
                    self.window.blit(surface, temp[:2])

        self.draw_grid(self.main_game_rect, self.model.rows, self.model.columns, 2)

    def draw_tile(self, square, ind):
        pygame.draw.rect(self.window, visuals.COLOR_MAP[ind], square)

    def draw_next(self, block_next):
        self.draw_piece(block_next, self.next_rect)
        next_text = visuals.font_bold.render('Next', True, visuals.grey_1)
        self.window.blit(next_text, (self.next_rect[0] + 45, self.next_rect[3] - 50))

    def draw_grid(self, rect, rows, columns, line):
        x1, y1, x2, h2 = rect
        tile_w = x2 / columns
        tile_h = h2 / rows
        half_line = line / 2

        for relx in range(columns + 1):
            x = x1 + relx * tile_w - line / 2
            y = y1 - half_line
            pygame.draw.rect(self.window, visuals.black, (x, y, line, h2 + line))

        for rely in range(rows + 1):
            y = y1 + rely * tile_h - half_line
            x = (x1 - half_line)
            pygame.draw.rect(self.window, visuals.black, (x, y, x2 + line, line))

    def draw_piece(self, block, rect):
        if block is None:
            return
        x1, y1, x2, y2 = rect
        cell_width = 24
        cell_height = 24
        x1 += x2 / 2 + 12
        y1 += 12

        ind = block.shape.ind
        dx, dy = visuals.OFFSET_MAP[ind]

        for relx, rely in block.get_coods():
            x = x1 + (relx + dx) * cell_width
            y = y1 + (rely + dy) * cell_height
            self.draw_tile((x, y, cell_width, cell_height), ind)

    def draw_info(self, level, score, cleared):
        score_text = visuals.font_light.render('Score ' + str(score), True, visuals.grey_1)
        self.window.blit(score_text, (self.x1 + self.x2 + 25, self.y1 + 200))
        levels_text = visuals.font_light.render('Level ' + str(level), True, visuals.grey_1)
        self.window.blit(levels_text, (self.x1 + self.x2 + 25, self.y1 + 250))
        lines_text = visuals.font_light.render('Lines  ' + str(cleared), True, visuals.grey_1)
        self.window.blit(lines_text, (self.x1 + self.x2 + 25, self.y1 + 300))
