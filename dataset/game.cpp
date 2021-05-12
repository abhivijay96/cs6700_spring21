#include <iostream>
#include "game.hpp"

using namespace std;

game::game(int board_size)
{
    this->board_size = board_size;
    this->total_elems = board_size * board_size;
}

game::~game()
{
    int idx;
    for(idx = 0; idx < this->states.size(); ++idx)
    {
        delete this->states[idx];
    }
}

int game::get_board_size()
{
    return this->total_elems;
}

int* game::init_next_board_state()
{
    int idx;
    int* state = new int[this->total_elems];
    for(idx = 0; idx < this->total_elems; ++idx)
    {
        if(this->states.size() == 0)
        {
            state[idx] = -1;
        }
        else
        {
            state[idx] = (this->states.back())[idx];
        }
    }
    this->states.push_back(state);
    return state;
}

void game::remove_next_board_state()
{
    int* state = this->states.back();
    this->states.pop_back();
    delete state;
}

bool game::is_game_over()
{
    int row_num;
    int col_num;
    int diagonal_num;
    int start_idx;
    int end_idx;
    int value;
    bool result;

    int* state = this->states.back();

    // check rows
    // cout << "Checking rows" << endl;
    for(row_num = 0; row_num < this->board_size; ++row_num)
    {
        start_idx = row_num * this->board_size;
        end_idx = start_idx + this->board_size;
        value = -2;
        result = true;
        for(; start_idx < end_idx; ++start_idx)
        {
            if(value == -2)
            {
                value = state[start_idx];
            }
            else if(value != state[start_idx])
            {
                result = false;
                break;
            }
        }
        if(result && (value == SHAPE_X || value == SHAPE_O)) 
        {

        // cout << "Won by row" << endl;
            return result;
        }
    }

    // check columns
    // cout << "Checking cols" << endl;
    for(col_num = 0; col_num < this->board_size; ++col_num)
    {
        start_idx = col_num;
        end_idx = (col_num + (this->board_size - 1) * this->board_size) + 1;
        value = -2;
        result = true;

        for(; start_idx < end_idx; start_idx += this->board_size)
        {
            if(value == -2)
            {
                value = state[start_idx];
            }
            else if(value != state[start_idx])
            {
                result = false;
                break;
            }
        }
        if(result && (value == SHAPE_X || value == SHAPE_O))
        {

        // cout << "Won by col" << endl;
            return result;
        }
    }
    
    // check diagonal (1)
    // cout << "Checking diag1" << endl;
    start_idx = 0;
    end_idx = this->total_elems;
    value = -2;
    result = true;
    for(; start_idx < end_idx; start_idx += (this->board_size + 1))
    {
        if(value == -2)
        {
            value = state[start_idx];
        }
        else if(value != state[start_idx])
        {
            result = false;
            break;
        }
    }
    if(result && (value == SHAPE_X || value == SHAPE_O))
    {
        // cout << "Won by daig 1" << endl;
        return result;
    }    

    // check diagonal (2)
    // cout << "Checking diag2" << endl;
    start_idx = this->board_size - 1;
    end_idx = (this->board_size * (this->board_size - 1)) + 1;
    value = -2;
    result = true;
    for(; start_idx < end_idx; start_idx += (this->board_size - 1))
    {
        if(value == -2)
        {
            value = state[start_idx];
        }
        else if(value != state[start_idx])
        {
            result = false;
            break;
        }
    }

    if(result && (value == SHAPE_X || value == SHAPE_O))
    {
        // cout << "Won by daig 2" << endl;
        return result;
    }
    return false;
}

bool game::is_board_full()
{
    bool result = true;
    int* state = this->states.back();
    int idx;

    for(idx = 0; idx < this->total_elems; ++idx)
    {
        if(state[idx] == -1)
        {
            result = false;
        }
    }
    
    return result;
}

void game::print_states_of_game()
{
    int* state;
    int state_idx;
    int row_idx;
    int col_idx;

    for(state_idx = 0; state_idx < this->states.size(); ++state_idx)
    {
        state = this->states[state_idx];
        cout << "==========" << endl;
        for(row_idx = 0; row_idx < this->total_elems; row_idx += this->board_size)
        {  
            cout << "[";
            for(col_idx = row_idx; col_idx < row_idx + this->board_size; ++col_idx)
            {
                cout << std::to_string(state[col_idx]) << ",";
            }
            cout << "]" << endl;
        }
    }
}

void game::print_one_state(int* state)
{
    int print_idx;
    for(print_idx = 0; print_idx < this->total_elems; ++print_idx)
    {
        cout << std::to_string(state[print_idx]);
        if(print_idx != this->total_elems - 1)
        {
            cout << ",";
        }
    }
}

void game::print_data_points()
{
    int* current_state;
    int* next_state;
    int state_idx;

    for(state_idx = 0; state_idx < this->states.size() - 1; ++state_idx)
    {
        current_state = this->states[state_idx];
        next_state = this->states[state_idx + 1];

        print_one_state(current_state);
        cout << "|";
        print_one_state(next_state);
        cout << endl;
    }
}