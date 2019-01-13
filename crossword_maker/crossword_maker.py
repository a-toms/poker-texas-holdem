#! python3
# crossword_maker.py

HEIGHT = 15
WIDTH = 15


def create_board(vertical_length, horizontal_length):
    """Define the board dimensions"""
    outer = []
    for i in range(vertical_length * horizontal_length):
        inner = dict()
        inner[i] = '-'
        outer.append(inner)
    return outer

board = create_board(WIDTH, HEIGHT)


def display_data_structure(board):
    for i in range(len(board)):
        if i % HEIGHT != 0:
            print(board[i], end=' ')
        else:
            print(board[i])


def display_board_to_user(board):
    """print crossword positions"""
    for i in range(len(board)):
        if i % HEIGHT != 0:
            print(board[i][i], end=' ')
        else:
            print(board[i][i]) #  this prints a new line


class Word:
    pass

    # todo: add vertical words and horizontal word letter placeholders


# Adding words to test the board update process
word_1 = Word()
word_1.word, word_1.word_position_on_board = 'ATE', [2, 3, 4]

word_2 = Word()
word_2.word, word_2.word_position_on_board = \
    'REPENTENCE', [1, 16, 31, 46, 61, 76, 91, 106, 121, 136]


"""TODO: PLAN: Continue here by adding new words from a completed Guardian
or Times crossword. 
1. Create crossword board structure -> Add the words from the completed crossword  example to the data structure.
2. Define placeholders -> Change all of the words to be placeholders for vertical or horizontal words.
Name each of these words, e.g., 'vertical word 1' 
3. Write a test -> test that the placeholder names are valid
4. Get random letters that fit -> Write a function that gets a random word that fits each placeholder 
word's length and existing letters. 
To achieve 4:
    a. Get a list of english words
    b. parse the words 
    c. find words of the fitting length
    d. find words that have letters that accord with the existing letters
    in the data structuire
    e. replace the appropriate placeholder word's (e.g., 'vertical word 1')
    with the letters of the new hidden word
5. Add basic clues to the UI under the board -> Retrieve thesaurus words. Use 
regex to remove any of the basic clues containing the hidden word
6. Create user guessing and data structure update function"""






# Write a test for the below
def add_word_to_board(board, word_position, word):
    for position, counter in zip(word_position, range(len(word_position))):
        board[position] = {position: word[counter]} # Change this to update


add_word_to_board(board, word_1.word_position_on_board, word_1.word)
add_word_to_board(board, word_2.word_position_on_board, word_2.word)


#




"""
Blank board outline:
- - - - V - - - - -
- - - - V - - - - -
- H HV H HV H HV H - 
- - V - - - - V - -
- - V - - - - V - -
- - V - - - H HV H H


"""

display_data_structure(board)

display_board_to_user(board)