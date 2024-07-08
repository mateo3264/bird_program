import pandas as pd
from registers import read_bird_names

def get_birds_by_string_length():
    birds = read_bird_names()

    #chosen_birds = [random.choice(birds) for i, bird in enumerate(birds) if i <= 1]


    df = pd.DataFrame({'Especie':birds})
    new_idx = df.Especie.str.len().sort_values().index
    new_df = df.reindex(new_idx)
    chosen_birds = []
    for row in new_df.head().iterrows():
        chosen_birds.append(row[1]['Especie'])

    return chosen_birds