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
    llm = OpenAI(model="gpt-3.5-turbo", temperature=0.05, max_tokens=1024)
    embed_model = OpenAIEmbedding()
    prompt_helper = PromptHelper(
        context_window=4096,
        num_output=1024,
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


def on_init(state):
    state.engine = prep_genai()


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
<Toda a informação que não seja lista de ingredientes ou modo de preparo>"""
        response = state.engine.query(state.prompt)
        state.resultado = str(response)
        notify(state, "sucesso", "Receita extraída e formatada!")
    except:
        print(traceback.format_exc())
        notify(state, "error", "Receita não extraída!")


# Definição de Variável
receitas = [
    "PASTEIZINHOS DE NATA DA VÓ MAROCA",
    "CROQUETES",
    "BOLINHOS DE NATA DA VÓ MAROCA",
    "BISCOITO RUSSO",
    "ROCAMBOLE DE BATATAS",
    "TORTA RUSSA DE GALINHA",
    "Panquecas",
    "Frango a Luiz XV",
    "Estrogonoff",
    "Pastelão de palmito e camarão",
    "Rocambole de carne",
    "Lasanha Recheada",
    "Massa para lasanha:",
    "Nhoque",
    "Arroz de Forno",
    "Pudim de Carne",
    "Suflê de Frango",
    "TORTA DA TIA NORMA",
    "Presunto Arlequim",
    "Molho de Escabeche",
    "Medalhões de Peixe",
    "18",
    "COQUETEL DE CAMARÃO",
    "Beterraba Agridoce",
    "Bolinhos de Bacalhau",
    "Croquetes de bacalhau",
    "Torta Salgada (Carmem)",
    "Patê de fígado de galinha",
    "Croquete de Lagosta",
    "Galinha à Francesa",
    "Lombos de porco agridoce",
    "Macarrão à alemã",
    "Camarão a La King",
    "Bacalhau a Maria do Céu",
    "Mousse de Atum",
    "Salpicon do Pai",
    "Lulas à Isabel Cristina (Carlos Reis)",
    "Suflê de Camarão",
    "Galinha ao molho pardo",
    "Saltimboca",
    "Língua Recheada (Sarita)",
    "Puchero",
    "Pudim Gaúcho",
    "Sopa de beterraba",
    "Laranjada da Dinda Cema",
    "Pudim se leite condensado",
    "Vinhos de peixe com batatas",
    "Galinha do saco",
    "Perdizes em Escabeche",
    "Molho de Escabeche",
    "Lagarto com molho",
    "Torta Fria (verônica) Sanduíche",
    "Sonhos de forno",
    "Rosquinhas de Londres",
    "Rapadurinhas Eda",
    "Balinhas de Nana",
    "Rosca doce",
    "Filés de Pão Receita da Ligia Megoulat",
    "Gelatina da Silvinha",
    "Doce de ameixa",
    "Gelatina de morango",
    "Salada Polize",
    "Pudinzinhos de Galinha (Salmão ou camarão)",
    "Coxinhas de Galinha",
    "Pão-de-ló salgado",
    "Coxinhas recheadas com camarão (Galinha)",
    "Cactus",
    "Ovos recheados",
    "Cachorinhos",
    "Croquetes Flamencos",
    "Empada fechadas (massa podre)",
    "Bolinhos de queijo (Dedi)",
    "Pasteizinhos de Nata",
    "Paezinhos para almoço",
    "Pão d'água tipo caseiro",
    "Pão doce caseiro",
    "Pão doce caseiro",
    'Bolo de pão (o famoso "Bread-cake")',
    "Pão de queijo",
    'Pãezinhos "relâmpago"',
    'Biscoitos "tender leaf" (para chá)',
    'Pãezinhos "trevo"',
    "Bolinhos de nata",
    "Ovos de amendoim",
    "Ovos de coco",
    "Ovos de chocolate",
    "Cuca",
    "Torta branca",
    "Torta Edith",
    "Torta Horacina",
    "Torta Moka",
    "Torta de Laranja",
    "Torta Olga",
    "Torta Tia Herminia",
    "Torta Estefania",
    "Coroa de Frankfort",
    "Torta de amendoim",
    "Torta de coco queimado",
    "Torta farroupilha",
    "Torta de bom-bocado",
    "Torta de maçã",
    "Torta de côco(Sueli)",
    "Torta de nozes",
    "Chajá",
    "Torta de café",
    "Torta de batata doce",
    "Torta de Castanha (Santa Cruz)",
    "Torta de castanhas",
    "Torta de coco com chocolate",
    "Torta de chocolate Jeny",
    "Torta Paulista",
    "Torta de Limão (5 camadas)",
    "Torta de maça (Livia)",
    "Torta papo de anjo",
    "Torta Caçador",
    "Torta General",
    "Torta de Canela",
    "Sonhos de Bilia",
    "Marshmallow",
    "Torta negra maluca",
    "Torta de Côco",
    "Mirbeteig",
    "Coquetel",
    "Ponche de Natal",
    "Laranjada",
    "Boule á moda da mãe",
    "Boule",
    "Boule Dinda Cema (Champagnota)",
    "Ambrosia madrinha Elcy",
    "Ovos moles",
    "Baba de moça",
    "Ambrosia",
    "Flan de leite ou de laranja",
    "Pudim de laranja",
    "Pudim de Queijo",
    "Pudim Malakof",
    "Gelatina",
    "Gelatina de morango (Tia Norma)",
    "Charlote Russa",
    "Pudim Getúlio Vargas",
    "Rei Alberto",
    "Gelatina Espuma",
    "Gelatina de Coco",
    "Gelatina de Limão",
    "Gelatina Maria Mole",
    "Molho dinda Cema",
    "Pudim de Pão",
    "Pudim da Rosinha",
    "Baba de Moça",
    "É Pra Já",
    "Creme de abacaxi ou banana",
    "Docinhos de Amendoas",
    "Carioquinhas",
    "97",
    "Bananinhas Vó Nina",
    "Brigadeiros",
    "Pudim de Pão",
    "Pudim de Laranja (D. Chichinha)",
    "Já-Já",
    "Fios de Ovos",
    "Perú a california",
    "BrIoche",
]
prompt_simples = ""
prompt = ""
resultado = ""
engine = None

# Definição Pagina
buscar_md = Markdown(
    """<|container|
    
<|layout|columns=1|gap=5px|class_name=card|
<|c1|
**Buscar Receita**
|>
<|c3|
Receita:
<|{prompt_simples}|selector|lov={receitas}|dropdown|class_name=fullwidth|>
<br/>
<center><|Buscar|button|on_action=send_question2|></center>
|>
|>
---
<br/>
<|{resultado}|input|multiline|label=Resultado|class_name=fullwidth|>
|>
"""
)
