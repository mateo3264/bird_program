import pandas as pd
from registers import read_bird_names
import random


def get_birds_by_string_length(n_birds=5, order='ascending'):
    """This method returns a list of birds stored in the aves-de-cota-observadas.csv
    returns a list in an ascending order based on the name's length of the birds.
    """
    
        
    birds = read_bird_names()

    #chosen_birds = [random.choice(birds) for i, bird in enumerate(birds) if i <= 1]


    df = pd.DataFrame({'Especie':birds})
    
    if order == 'ascending':
        ascending = True
        new_idx = df.Especie.str.len().sort_values(ascending=ascending).index
        new_df = df.reindex(new_idx)
    elif order == 'descending':
        ascending = False
        new_idx = df.Especie.str.len().sort_values(ascending=ascending).index
        new_df = df.reindex(new_idx)
    else:
        new_df = df.sample(frac=1).reset_index(drop=True)
    
    
    chosen_birds = []

    for i, row in enumerate(new_df.iterrows()):
        if i < n_birds:
            chosen_birds.append(row[1]['Especie'])
    
    copy_chosen_birds = chosen_birds.copy()
    random.shuffle(copy_chosen_birds)
    chosen_birds.extend(copy_chosen_birds)
    print('chosen_birds: ', chosen_birds)
    return chosen_birds


