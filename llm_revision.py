from langchain_openai import ChatOpenAI
from langchain_community.callbacks import get_openai_callback
from dotenv import load_dotenv
from registers import read_json_file
from configurations import FILENAME_BIRD_TEXTS
from langchain_core.prompts import ChatPromptTemplate
import tiktoken
from registers import read_json_file
from typing import Dict

load_dotenv()

def get_num_tokens(string: str, encoding_name: str):
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


# ToDo: Don't create new instances each time this function is called
def get_score_from_llm(json_bird_texts: Dict, bird_name: str, user_response: str, model_name: str ='gpt-4o-mini', verbose: bool = False):
    
    

    # print(json_text_files[bird])

    
    llm = ChatOpenAI(model=model_name)

    

    #print('Num tokens: ', get_num_tokens(user_response, model_name))

    template_en = '''You are an excellent ornithologist and educator. Given the description of the {bird} provided by the user, and the correct description given to you (In both english and spanish) qualify from 0 to 10 the description of the user based on the similarity with the correct description. Only focus on the anatomy. Just answer with the number nothing else.
    correct_description: {correct_description}
    user_response: {user_response}

    Qualification (from 0 to 10):
    '''

    template_es = '''Eres un excelente ornitólogo y educador. Dada la descripción del {bird} proporcionada por el usuario, y la descripción correcta que se te ha proporcionado (tanto en inglés como en español), califica de 0 a 10 la descripción del usuario basándote en la similitud con la descripción correcta. Enfócate solo en la anatomía (no habitat o dieta). Si el peso y tamaño son cercanos (+-2cm, +-2gramos) considéralo correcto. En general no seas tan exigente y si usa términos sinónimos aceptalos. Responde únicamente con el número y explica brevement que faltó.
    descripción_correcta: {correct_description}
    respuesta_del_usuario: {user_response}
    Calificación (de 0 a 10):'''

    prompt = ChatPromptTemplate.from_template(template_es)
    chain = prompt | llm

    with get_openai_callback() as c:
        response = chain.invoke({'bird':bird_name, 'correct_description':json_bird_texts[bird_name], 'user_response':user_response})
        if verbose:
            print(response.content)
            print(c)
    
    return response.content

if __name__ == '__main__':
    file = read_json_file(FILENAME_BIRD_TEXTS)
    user_response = input(f'Escribe las características del {bird_name}: ')
    get_score_from_llm(file, 'Icterus chrysater', user_response)