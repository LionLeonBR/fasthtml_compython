import os

from datetime import datetime

import pytz
from supabase import create_client
from dotenv import load_dotenv
from fasthtml.common import *

#carregar o ambiente
load_dotenv()


TIMESTAMP_FMT = "%Y-%m-%d %I:%M:%S %p CET"




#inicializar o supabase cliente
supabase= create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

app, routes = fast_app(
    hdrs=(Link(rel="icon", type="assets/x-icon", href="/assets/legoshi.jpeg"),),    
)


def get_cet_time():
    cet_tz = pytz.timezone("CET")
    return datetime.now(cet_tz)

def add_menssage(name, menssage):
    timestamp = get_cet_time().strftime(TIMESTAMP_FMT)
    supabase.table("MeusVisitantesLivrados").insert(
        {"name": name, "menssage": menssage, "timestamp": timestamp}
    ).execute()


def get_menssages():
    response = (
        supabase.table("MeusVisitantesLivrados").select("*").order("id", desc=True).execute()
    )
    return response.data


def render_menssage(entry):
    return Article(
            Header(f"Nome: {entry['name']}"),
            P(entry['menssage']),
            Footer(Small(Em(f"Postado: {entry['timestamp']}"))),
        ),

def render_menssage_list():
    messages = get_menssages()
    return Div(
        *[render_menssage(entry) for entry in messages],
        id="menssage-list",
    )

def render_content():
    form = Form(
        Fieldset(
            Input(
                type="text",
                name="name",
                placeholder="Seu nome",
                required="True",
                maxlength=15,
            ),
            Input(
                type="text",
                name="menssage",
                placeholder="Mensagem até 50 letras",
                required="True",
                maxlength=50,
            ),
            Button("Enviar", type="submit"),
            role="group",
        ),
        method="post",
        hx_post="submit-menssage",
        hx_target="#menssage-list",
        hx_swap="outerHTML",
        hx_on__after_request="this.reset()",
    )
    return Div(
        P(Em("Escreva alguma coisa!")),
        form,
        Div(
            f"Feito com DOR E LÁGRIMAS por ",
            A("Leo", href="https://github.com/LionLeonBR", target="_blank"),
        ),
        Hr(),
        render_menssage_list(),
    )


@routes("/submit-menssage")
def post(name: str, menssage: str):
    add_menssage(name, menssage)
    return render_menssage_list()

@routes("/")
def get():
    return Titled("Caderninho de Visitantes :D", render_content())


serve()