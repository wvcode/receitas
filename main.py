# -*- coding: utf-8 -*-
import os

from taipy.gui import Gui
from dotenv import load_dotenv

load_dotenv()

from pages.generate import gen_q_md, on_init as gen_on_init
from pages.buscar import buscar_md, on_init as bsc_on_init


def on_init(state):
    gen_on_init(state)
    bsc_on_init(state)


pages = {
    "/": "<center><|navbar|></center>",
    "Receitas": buscar_md,
    "Playground": gen_q_md,
}


# ----------------------------------------------------------------
# Main
# ----------------------------------------------------------------
if __name__ == "__main__":
    Gui(pages=pages).run(
        title="Receitas da Vó Mainha",
        host="0.0.0.0",
        port=os.getenv("PORT"),
        use_reloader=True,
    )
