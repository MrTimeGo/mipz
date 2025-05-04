from game import Game

MIN_TEST_CASE_COUNT = 1
MAX_TEST_CASE_COUNT = 11

FIELD_SIZE = 19

INPUT_FILE_NAME = 'input.txt'
OUTPUT_FILE_NAME = 'output.txt'


def read_input_file(file_name):
    output = []
    with open(file_name, 'r') as file:
        test_cases_count = int(file.readline())
        if test_cases_count < MIN_TEST_CASE_COUNT or test_cases_count > MAX_TEST_CASE_COUNT:
            print('Invalid test cases number')
            return

        content = list(filter(lambda line: line != '', file.readlines()))

        for i in range(test_cases_count):
            field = '\n'.join(content[i * FIELD_SIZE: (i + 1) * FIELD_SIZE - 1])
            game = Game(field, FIELD_SIZE)
            output.append(game.get_winner().value)

            winning_stone = game.get_winning_stone()
            if winning_stone is not None:
                output.append(f'{winning_stone[0]} {winning_stone[1]}')
    return output


def write_to_output_file(file_name, output):
    with open(file_name, 'w') as file:
        file.write('\n'.join(output))


def main():
    output = read_input_file(INPUT_FILE_NAME)

    write_to_output_file(OUTPUT_FILE_NAME, output)


if __name__ == '__main__':
    main()