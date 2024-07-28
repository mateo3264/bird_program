from schedulers import get_birds_by_string_length
from retrievers import Retriever
from guis import TkinterGUI
from configurations import ALL

def main():
    chosen_birds = get_birds_by_string_length(3, order='random') #['Turdus fuscater', 'Piranga rubra', 'Zonotrichia capensis']
    tp = TkinterGUI(Retriever(chosen_birds, ALL))
    tp.present()

if __name__ == '__main__':
    main()