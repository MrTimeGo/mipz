from winner import Winner


class Game:
    def __init__(self, field: str, field_size: int):
        self.field = list(map(lambda row: list(row), filter(lambda row: row != '',field.split('\n'))))
        self.winning_count = 5
        self.winner = Winner.NO_ONE
        self.winning_stone = None
        self.field_size = field_size
        self.compute_winner()



    def compute_winner(self):
        row_count, col_count = len(self.field), len(self.field[0])
        for i in range(row_count):
            for j in range(col_count):
                possible_winner = self.field[i][j]

                if possible_winner == Winner.NO_ONE.value:
                    continue

                if self.__check_row(i, j, possible_winner) or self.__check_column(i, j, possible_winner) or self.__check_diagonal_main(i, j, possible_winner) or self.__check_diagonal_secondary(i, j, possible_winner):
                    self.winner = Winner(possible_winner)
                    self.winning_stone = (i, j)
                    return


    def __check_row(self, i: int, j: int, possible_winner: Winner) -> bool:
        if i + self.winning_count >= self.field_size:
            return False

        for x in range(i, i + self.winning_count):
            if self.field[x][j] != possible_winner:
                return False

        return not ((i - 1 >= 0 and self.field[i - 1][j] == possible_winner) or (i + self.winning_count < self.field_size and self.field[i + self.winning_count][j] == possible_winner))

    def __check_column(self, i: int, j: int, possible_winner: Winner) -> bool:
        if j + self.winning_count >= self.field_size:
            return False

        for y in range(j, j + self.winning_count):
            if self.field[i][y] != possible_winner:
                return False

        return not ((j - 1 >= 0 and self.field[i][j - 1] == possible_winner) or (j + self.winning_count < self.field_size and self.field[i][j + self.winning_count] == possible_winner))


    def __check_diagonal_main(self, i: int, j: int, possible_winner: Winner) -> bool:
        for x in range(i, i + self.winning_count):
            if x >= self.field_size:
                return False

            y = j + (x - i)
            if y >= self.field_size:
                return False

            if self.field[x][y] != possible_winner:
                return False

        return not ((i - 1 >= 0 and j - 1 >= 0 and self.field[i - 1][j - 1] == possible_winner) or (i + self.winning_count < self.field_size and j + self.winning_count < self.field_size and self.field[i + self.winning_count][j + self.winning_count] == possible_winner))


    def __check_diagonal_secondary(self, i: int, j: int, possible_winner: Winner) -> bool:
        for x in range(i, i - self.winning_count, -1):
            if x < 0:
                return False

            y = j + (i - x)
            if y >= self.field_size:
                return False

            if self.field[x][y] != possible_winner:
                return False

        return not ((i + 1 < self.field_size and j - 1 >= 0 and self.field[i + 1][j - 1] == possible_winner) or (i - self.winning_count >= 0 and j + self.winning_count < self.field_size and self.field[i - self.winning_count][j + self.winning_count] == possible_winner))


    def get_winner(self):
        return self.winner

    def get_winning_stone(self):
        return self.winning_stone