from enum import Enum

class Winner(Enum):
    NOONE = '0'
    BLACK = '1'
    WHITE = '2'


class Game:
    def __init__(self, field: str):
        self.field = list(map(lambda row: list(row), filter(lambda row: row != '',field.split('\n'))))
        self.winning_count = 5
        self.winner = Winner.NOONE
        self.winning_stone = None
        self.compute_winner()


    def compute_winner(self):
        for i in range(len(self.field)):
            for j in range(len(self.field[i])):
                possible_winner = self.field[i][j]

                if possible_winner == Winner.NOONE.value:
                    continue

                if self.__check_row(i, j, possible_winner) or self.__check_column(i, j, possible_winner) or self.__check_diagonal_main(i, j, possible_winner) or self.__check_diagonal_secondary(i, j, possible_winner):
                    self.winner = Winner(possible_winner)
                    self.winning_stone = (i, j)
                    return


    def __check_row(self, i: int, j: int, possible_winner: Winner) -> bool:
        for x in range(i, i + self.winning_count):
            if x >= 19:
                return False

            if self.field[x][j] != possible_winner:
                return False

        # More than 5 stone checks
        if i - 1 >= 0 and self.field[i - 1][j] == possible_winner:
            return False
        if i + self.winning_count < 19 and self.field[i + self.winning_count][j] == possible_winner:
            return False

        return True

    def __check_column(self, i: int, j: int, possible_winner: Winner) -> bool:
        for y in range(j, j + self.winning_count):
            if y >= 19:
                return False

            if self.field[i][y] != possible_winner:
                return False

        # More than 5 stone checks
        if j - 1 >= 0 and self.field[i][j - 1] == possible_winner:
            return False
        if j + self.winning_count < 19 and self.field[i][j + self.winning_count] == possible_winner:
            return False

        return True


    def __check_diagonal_main(self, i: int, j: int, possible_winner: Winner) -> bool:
        for x in range(i, i + self.winning_count):
            if x >= 19:
                return False

            y = j + (x - i)
            if y >= 19:
                return False

            if self.field[x][y] != possible_winner:
                return False

        # More than 5 stone checks
        if i - 1 >= 0 and j - 1 >= 0 and self.field[i - 1][j - 1] == possible_winner:
            return False
        if i + self.winning_count < 19 and j + self.winning_count < 19 and self.field[i + self.winning_count][j + self.winning_count] == possible_winner:
            return False

        return True


    def __check_diagonal_secondary(self, i: int, j: int, possible_winner: Winner) -> bool:
        for x in range(i, i - self.winning_count, -1):
            if x < 0:
                return False

            y = j + (i - x)
            if y >= 19:
                return False

            if self.field[x][y] != possible_winner:
                return False

        # More than 5 stone checks
        if i + 1 < 19 and j - 1 >= 0 and self.field[i + 1][j - 1] == possible_winner:
            return False
        if i - self.winning_count >= 0 and j + self.winning_count < 19 and self.field[i - self.winning_count][j + self.winning_count] == possible_winner:
            return False

        return True


    def get_winner(self):
        return self.winner

    def get_winning_stone(self):
        return self.winning_stone


def main():
    output = []
    with open('input.txt', 'r') as file:
        test_cases_count = int(file.readline())
        if test_cases_count < 1 or test_cases_count > 11:
            print('Invalid test cases number')
            return

        content = list(filter(lambda line: line != '', file.readlines()))

        for i in range(test_cases_count):
            field = '\n'.join(content[i * 19: (i + 1) * 19 - 1])
            game = Game(field)
            output.append(game.get_winner().value)

            winning_stone = game.get_winning_stone()
            if winning_stone is not None:
                output.append(f'{winning_stone[0]} {winning_stone[1]}')

    with open('output.txt', 'w') as file:
        file.write('\n'.join(output))


if __name__ == '__main__':
    main()