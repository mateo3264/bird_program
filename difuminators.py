import random 

def difuminate(text, rate_of_difumination=1):
    difuminations = [text]
    text = list(text)
    left_to_difuminate = {i for i in range(len(text))}
    space_idxs = {i for i in range(len(text)) if text[i] == ' '}
    left_to_difuminate = left_to_difuminate - space_idxs
    
    
    while len(left_to_difuminate) > 0:
        for i in range(rate_of_difumination):
            if len(left_to_difuminate) > 0:
                idx_of_character_to_remove = random.choice(list(left_to_difuminate))
            
                if text[idx_of_character_to_remove] != ' ':
                    left_to_difuminate.remove(idx_of_character_to_remove)
                    text[idx_of_character_to_remove] = '_'
        difuminations.append(''.join(text))
        
    
    if len(left_to_difuminate) == 1:
        text[left_to_difuminate[0]] = '_'
        
            
        
    return difuminations


