from blocks import new_blocks, Tetromino


class Tetris:

    def __init__(self, columns=10, rows=20):
        """
        Used to represent the Tetris engine and its rules.
        :param columns: (int) number of columns on the board
        :param rows: (int) number of rows on the board
        """
        self.columns = columns
        self.rows = rows
        self.board = [[0 for _ in range(columns)] for _ in range(rows)]
        self.current = None
        self.piece_next = None
        self.previous = None

        self.level = 1
        self.score = 0
        self.cleared_count = 0

        self.SCORE_MAP = {
            0: 0,
            1: 40 * self.level,
            2: 100 * self.level,
            3: 300 * self.level,
            4: 1200 * self.level,
        }

        self.TO_STR_MAP = {
            1: "I",
            2: "O",
            3: "T",
            4: "S",
            5: "Z",
            6: "J",
            7: "L"
        }

        self.bag = new_blocks()
        self.pull()

    def pull(self):
        if self.piece_next is not None:
            self.current = self.piece_next
        else:
            self.current = self.bag.pop()

        self.current.translate(int(self.columns / 2), 0)
        self.piece_next = self.bag.pop()

        if not self.bag:
            self.bag = new_blocks()

    def solidify(self):
        coords = self.current.get_coods()

        if any(x < 0 or x >= self.columns or y < 0 or y >= self.rows or self.board[y][x] != 0 for x, y in
               coords):
            return False

        for x, y in coords:
            self.board[y][x] = self.current.shape.ind

        self.previous = self.current
        self.current = None
        return True

    def is_valid_translation(self, dir_x, dir_y):
        for x, y in self.current.get_coods():
            next_x = x + dir_x
            next_y = y + dir_y
            if next_x < 0 or next_x >= self.columns or next_y < 0 or next_y >= self.rows:
                return False
            if self.board[next_y][next_x] != 0:
                return False
        return True

    def translate_current(self, x):
        if self.current is None:
            return False

        if not self.is_valid_translation(x, 0):
            return False

        self.current.translate(x, 0)
        return True

    def is_game_over(self):
        return self.current is not None and not self.is_valid_translation(0, 0)

    def is_row(self, y):
        return 0 not in self.board[y]

    def remove_row(self, y):
        removed_row = self.board.pop(y)
        self.board.insert(0, [0 for _ in range(self.columns)])
        return removed_row

    def combined_moves(self, x, rotation):
        if self.current is None:
            return False

        self.current.rotate(rotation)

        return self.is_valid_translation(0, 0) and self.translate_current(-self.current.x + x) and self.drop()

    def drop(self):
        if self.current is None:
            return False

        while self.is_valid_translation(0, 1):
            self.current.translate(0, 1)

        return self.solidify()

    def insert_row(self, y, row):
        self.board.pop(0)
        self.board.insert(y, row)

    def generate_possible_states(self):
        """
        Returns the possible tuples of ((x translation, rotation), [property1, property2, ...])
        """
        if self.current is None:
            return []

        states = []

        last_piece = self.previous

        for rotation in range(self.current.shape.rotations):
            for translation in range(self.columns + 1):
                piece = Tetromino(self.current.x, self.current.y, self.current.shape, self.current.rotation)
                if self.combined_moves(translation, rotation):
                    rows_cleared = self.get_possible_cleared_rows()
                    removed = []
                    for y in rows_cleared:
                        removed.append((y, self.remove_row(y)))

                    # Represent a state as tuple(tuple(x translation, rotation), List[properties])
                    states.append(((translation, rotation), self.get_properties(rows_cleared)))

                    for ind, row in reversed(removed):
                        self.insert_row(ind, row)
                    for x, y in self.previous.get_coods():
                        self.board[y][x] = 0
                self.current = piece
                self.previous = last_piece
        return states

    def row_clean(self):
        rows = []
        if self.is_game_over():
            return rows

        if self.current is None:
            self.pull()
            rows = self.get_possible_cleared_rows()
            if rows:
                for row in rows:
                    self.remove_row(row)
                self.score += self.compute_score_bonus(len(rows))
                self.cleared_count += len(rows)
                if self.cleared_count >= self.level * 10:
                    self.level += 1
        return rows

    def compute_score_bonus(self, number_rows_cleared):
        return self.SCORE_MAP.get(number_rows_cleared, 0)

    def get_bumpiness(self):
        return sum([abs(col2 - col1) for col1, col2 in zip(self.get_peaks()[:-1], self.get_peaks()[1:])])

    def get_total_peaks(self):
        return sum(self.get_peaks())

    def get_peaks(self):
        peaks = []
        for col in range(self.columns):
            for row in range(self.rows):
                if self.board[row][col] != 0:
                    peaks.append(self.rows - row)
                    break

                if row == self.rows - 1:
                    peaks.append(0)

        return peaks

    def get_holes(self):
        board = self.board
        holes = 0
        for column in zip(*board):
            i = 0
            while i < self.rows and column[i] == 0:
                i += 1
            holes += len([x for x in column[i+1:] if x == 0])
        return holes

    def get_properties(self, r):
        return [len(r), self.get_holes(), self.get_bumpiness(), self.get_total_peaks()]

    def get_possible_cleared_rows(self):
        res = []
        for row in range(self.rows):
            if self.is_row(row):
                res.append(row)
        return res

    def __str__(self):
        vert_borders = "+" + "-" * self.columns + "+\n"
        display = vert_borders
        for row in range(self.rows):
            display += ":"
            for col in range(self.columns):
                if self.board[row][col] == 0:
                    display += " "
                else:
                    display += self.TO_STR_MAP[self.board[row][col]]
            display += ":\n"
        display += vert_borders
        return str(display)
