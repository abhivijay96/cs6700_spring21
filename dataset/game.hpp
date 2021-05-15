#include <vector>

#ifndef GAME
#define GAME

using namespace std;

#define SHAPE_O -1
#define SHAPE_X 1

class game
{
private:
    int board_size;
    int total_elems;
    // Each board state is an array of ints (-1 -> empty, 0 -> X, 1 -> O)
    
    // Example board of size 3 x 3, indeces of the corresponding element in the array
    // [0 1 2]
    // [3 4 5]
    // [6 7 8]

    // Exaple board of size 4 x 4
    // [0 1 2 3]
    // [4 5 6 7]
    // [8 9 10 11]
    // [12 13 14 15]

    // States is a list of board states
    vector<int*> states; 
    void print_one_state(int* state);
public:
    game(int board_size);
    ~game();

    // returns board size
    int get_board_size();

    // Initializes and returns the net board state which can be played on
    int* init_next_board_state();
    // Destroys the current board state which has been played on
    void remove_next_board_state();
    
    // returns true if the game is done (one of the player has won), false otherwise
    bool is_game_over();
    // returns true if the board is full, false otherwise
    bool is_board_full();
    // prints the board states, can be used to debug
    void print_states_of_game();
    // prints the states of game which is stored in the dataset file
    void print_data_points();
};

#endif