# Rock Paper Scissors - freeCodeCamp Machine Learning with Python Project 1
# Strategy: Track opponent's previous moves (Markov Chain approach)

play_history = {}

def player(prev_play, opponent_history=[]):
    if not prev_play:
        prev_play = 'R'
    
    opponent_history.append(prev_play)
    
    n = 5 # length of history string to track
    
    if len(opponent_history) > n:
        # Get the sequence of the last n-1 moves
        last_sequence = "".join(opponent_history[-(n):])
        
        # We need to predict the next move based on past frequencies
        possible_moves = ['R', 'P', 'S']
        
        # update history dictionary
        if len(opponent_history) > n:
            hist_str = "".join(opponent_history[-(n+1):])
            play_history[hist_str] = play_history.get(hist_str, 0) + 1
            
        predict = 'P' # Default
        max_count = 0
        
        for move in possible_moves:
            test_seq = last_sequence + move
            count = play_history.get(test_seq, 0)
            if count > max_count:
                max_count = count
                predict = move
                
        # Counter the predicted move
        ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
        return ideal_response[predict]
    
    # Random fallback for first few moves
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    return ideal_response[prev_play]

# Helper function to reset history between games
def reset_history():
    global play_history
    play_history = {}
