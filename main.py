# -*- coding: utf-8 -*-
import os

from taipy.gui import Gui
from dotenv import load_dotenv

load_dotenv()

from pages.generate import gen_q_md

pages = {"/": "<center><|navbar|></center>", "Receitas": gen_q_md}


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
