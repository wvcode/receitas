# -*- coding: utf-8 -*-
import os
import traceback
from taipy.gui import Gui, notify, Markdown
from dotenv import load_dotenv
import tiktoken


load_dotenv()


import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

from llama_index import (
    OpenAIEmbedding,
    PromptHelper,
    VectorStoreIndex,
    SimpleDirectoryReader,
)
from llama_index import ServiceContext
from llama_index.llms import OpenAI


def prep_genai():
    llm = OpenAI(model="gpt-3.5-turbo", temperature=0, max_tokens=256)
    embed_model = OpenAIEmbedding()
    prompt_helper = PromptHelper(
        context_window=4096,
        num_output=256,
        chunk_overlap_ratio=0.1,
        chunk_size_limit=None,
    )

    service_context = ServiceContext.from_defaults(
        llm=llm, embed_model=embed_model, prompt_helper=prompt_helper
    )

    documents = SimpleDirectoryReader(os.getenv("PDF_FOLDER")).load_data()
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine(service_context=service_context)
    return query_engine


def send_question2(state, id, action):
    try:
        state.prompt = f"""Descreva a receita de {state.prompt_simples}.
As vezes, o nome do autor está entre parenteses proximo ao nome da receita ou está no próprio título
Quando não for especificado um autor no contexto, tente utilizar o nome da pessoa no documento
Todas as unidades de medida de ingredientes solidos devem ser convertidas para gramas
Todas as unidades de medida de ingredientes liquidos deven ser convertidas para militros
No modo de preparo, cada verbo deve iniciar um novo passo
Mostrar a receita utilizando o seguinte formato:
<Titulo da Receita>
Por <Autor da Receita>
Ingredientes:
<Lista de Ingredientes>

Modo de Preparo:
<Passos para preparar a receita>

Observações:
<Toda a informação que não seja lista de ingredientes ou modo de preparo>        """
        response = state.engine.query(state.prompt)
        state.resultado = str(response)
        notify(state, "sucesso", "Receita extraída e formatada!")
    except:
        print(traceback.format_exc())
        notify(state, "error", "Receita não extraída!")


def send_question1(state, id, action):
    try:
        state.prompt = f"Liste a receita {state.prompt_simples}"
        response = state.engine.query(state.prompt)
        state.resultado = str(response)
        notify(state, "sucesso", "Receita extraída!")
    except:
        print(traceback.format_exc())
        notify(state, "error", "Receita não extraída!")


def send_question3(state, id, action):
    try:
        response = state.engine.query(state.prompt)
        state.resultado = str(response)
        notify(state, "sucesso", "Receita extraída!")
    except:
        print(traceback.format_exc())
        notify(state, "error", "Receita não extraída!")


# Definição de Variável
prompt_simples = ""

prompt = ""
resultado = ""

engine = prep_genai()

# Definição Pagina
gen_q_md = Markdown(
    """<|container|
    
<|layout|columns=1fr 250px|gap=5px|class_name=card|
<|c1|
**Extração**
|>
<|c2|
**Transformação**
|>
<|c3|
<|{prompt_simples}|input|label="Digite o nome de 1 receita:"|multiline=true|class_name=fullwidth|>
<br/>
<center><|Extrair|button|on_action=send_question1|><|Formatar|button|on_action=send_question2|></center>
|>
|>
---
<br/>
<|{prompt}|input|multiline|label=Prompt|class_name=fullwidth|>
<br/>
<center><|Gerar|button|on_action=send_question3|></center>
<br/>
<|{resultado}|input|multiline|label=Resultado|class_name=fullwidth|>
|>
"""
)
