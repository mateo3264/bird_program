from schedulers import get_birds_by_string_length
from retrievers import Retriever
from presenters import TkinterPresenter


def main():
    chosen_birds = get_birds_by_string_length(10, order='random')
    tp = TkinterPresenter(Retriever(chosen_birds, 'image-audio'))
    tp.present()

if __name__ == '__main__':
    main()