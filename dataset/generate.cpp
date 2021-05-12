#include <iostream>
#include <vector>
#include "game.hpp"

using namespace std;

int print_interlval = 10000;
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
                // current_game->print_data_points();
                ++wins;
                if(wins % print_interlval == 0)
                {
                    // cout << "Total wins: " << std::to_string(wins) << endl;
                }
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
    game* new_game = new game(3);
    generate_positive_points(new_game, SHAPE_X);
    log("Total wins: " + std::to_string(wins));
    log("Total draws: " + std::to_string(draws));
    log("Total games: " + std::to_string(draws + wins));
    draws = 0;
    wins = 0;
    generate_positive_points(new_game, SHAPE_O);
    log("Total wins: " + std::to_string(wins));
    log("Total draws: " + std::to_string(draws));
    log("Total games: " + std::to_string(draws + wins));
}