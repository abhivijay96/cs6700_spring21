#include <iostream>
#include <vector>
#include "game.hpp"

using namespace std;

int wins = 0;
int draws = 0;

void generate_positive_points(game* current_game, int shape)
{
    int board_size = current_game->get_board_size();
    int idx;
    int* state;
    
    for(idx = 0; idx < board_size; ++idx)
    {
        state = current_game->init_next_board_state();
        if(state[idx] != SHAPE_X && state[idx] != SHAPE_O)
        {
            state[idx] = shape;
            // current_game->print_states_of_game();
            if(current_game->is_game_over())
            {
                // current_game->print_states_of_game();
                current_game->print_data_points();
                ++wins;
            }
            else if(!current_game->is_board_full())
            {
                generate_positive_points(
                    current_game, 
                    shape == SHAPE_O ? SHAPE_X: SHAPE_O);
            }
            else
            {
                draws += 1;
            }
        }
        current_game->remove_next_board_state();
    }    
}

void log(string text)
{
    cout << "[LOG]: " << text << endl;
}

int main(int argc, char* argv[])
{ 
    int board_size;
    if(argc < 2)
    {
        cout << "Usage: ./generate <board_size>" << endl;
        return 1;
    }
    board_size = atoi(argv[1]);
    // log("Generating game with " + std::to_string(board_size) + "x" + std::to_string(board_size));
    game* new_game = new game(board_size);
    generate_positive_points(new_game, SHAPE_X);
    // log("Total wins: " + std::to_string(wins));
    // log("Total draws: " + std::to_string(draws));
    // log("Total games: " + std::to_string(draws + wins));
    draws = 0;
    wins = 0;
    // generate_positive_points(new_game, SHAPE_O);
    // log("Total wins: " + std::to_string(wins));
    // log("Total draws: " + std::to_string(draws));
    // log("Total games: " + std::to_string(draws + wins));
}