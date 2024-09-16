# Caderninho de Visitantes :D

Este projeto é uma aplicação web simples desenvolvida com **FastHTML** para criar um "Caderno de Visitantes" onde os usuários podem deixar mensagens e vê-las em tempo real. A aplicação utiliza o **Supabase** como backend para armazenar e recuperar as mensagens enviadas pelos visitantes.

## Tecnologias Utilizadas

- **FastHTML**: Biblioteca Python para criar aplicações web usando apenas código Python.
- **Supabase**: Banco de dados como serviço baseado em PostgreSQL para gerenciamento de dados.
- **pytz**: Biblioteca para trabalhar com fusos horários.
- **dotenv**: Gerenciamento de variáveis de ambiente de forma segura.

## Funcionalidades

- **Registro de Mensagens**: Os visitantes podem deixar mensagens com seus nomes e as mensagens são salvas no banco de dados Supabase.
- **Exibição em Tempo Real**: As mensagens são exibidas em tempo real, sendo atualizadas dinamicamente na página.
- **Formulário Interativo**: Um formulário permite ao usuário enviar mensagens com um simples clique.

## Instalação

1. Clone o repositório para o seu ambiente local:

    ```bash
    git clone https://github.com/seu-usuario/nome-do-repositorio.git
    cd nome-do-repositorio
    ```

2. Instale as dependências necessárias:

    ```bash
    pip install fasthtml supabase-python pytz python-dotenv
    ```

3. Crie um arquivo `.env` com as credenciais do Supabase:

    ```
    SUPABASE_URL=sua_url_supabase
    SUPABASE_KEY=sua_chave_supabase
    ```

4. Execute o aplicativo:

    ```bash
    python nome_do_arquivo.py
    ```

5. Acesse o aplicativo no navegador:

    ```
    http://localhost:8000
    ```

## Estrutura do Projeto

- **`main.py`**: Arquivo principal que contém toda a lógica da aplicação.
- **Supabase**: Utilizado para persistir as mensagens enviadas pelos visitantes.
- **FastHTML**: Responsável pela renderização dos elementos HTML e pelo roteamento das páginas.

## Como Funciona

### 1. **Formulário de Envio**

Os usuários podem enviar suas mensagens através de um formulário simples:

```python
Form(
    Fieldset(
        Input(type="text", name="name", placeholder="Seu nome", required="True", maxlength=15),
        Input(type="text", name="menssage", placeholder="Mensagem até 50 letras", required="True", maxlength=50),
        Button("Enviar", type="submit")
    ),
    method="post",
    hx_post="submit-menssage",
    hx_target="#menssage-list",
    hx_swap="outerHTML",
    hx_on__after_request="this.reset()"
)
```

### 2. **Armazenamento de Mensagens**

As mensagens são salvas no Supabase com um timestamp formatado de acordo com o fuso horário CET:

```python
def add_menssage(name, menssage):
    timestamp = get_cet_time().strftime(TIMESTAMP_FMT)
    supabase.table("MeusVisitantesLivrados").insert(
        {"name": name, "menssage": menssage, "timestamp": timestamp}
    ).execute()
```

### 3. **Exibição das Mensagens**

As mensagens são renderizadas em tempo real na interface da aplicação:

```python
def render_menssage_list():
    messages = get_menssages()
    return Div(*[render_menssage(entry) for entry in messages], id="menssage-list")
```

## Variáveis de Ambiente

As seguintes variáveis de ambiente são necessárias para o funcionamento do projeto:

- **SUPABASE_URL**: URL da instância do Supabase.
- **SUPABASE_KEY**: Chave de API para acessar o banco de dados do Supabase.

### Explicação do Código

#### Importações

```python
import os
from datetime import datetime
import pytz
from supabase import create_client
from dotenv import load_dotenv
from fasthtml.common import *
```

As bibliotecas utilizadas aqui são:

- **os**: para acessar variáveis de ambiente, como chaves de API e URL.
- **datetime**: usada para trabalhar com datas e horas, particularmente para timestamps.
- **pytz**: fornece suporte para fusos horários (nesse caso, estamos lidando com o fuso horário CET).
- **supabase**: é o cliente que permite conexão e interação com o banco de dados Supabase.
- **dotenv**: carrega as variáveis de ambiente a partir de um arquivo `.env` para proteger informações sensíveis, como chaves de API.
- **fasthtml**: biblioteca que permite construir o frontend da aplicação com Python.

#### Carregar Variáveis de Ambiente

```python
load_dotenv()
```

O `dotenv` carrega variáveis sensíveis (como chaves de API) a partir de um arquivo `.env`. Esse arquivo `.env` deve conter:

```
SUPABASE_URL=sua_url_supabase
SUPABASE_KEY=sua_chave_supabase
```

#### Inicializar o Cliente do Supabase

```python
supabase= create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
```

Aqui, o cliente do **Supabase** é inicializado usando as variáveis de ambiente carregadas. Isso cria a conexão com o banco de dados, permitindo realizar operações como inserções e seleções de dados.

#### Função de Tempo CET

```python
def get_cet_time():
    cet_tz = pytz.timezone("CET")
    return datetime.now(cet_tz)
```

Essa função obtém a hora atual no fuso horário **CET** (Central European Time). Isso é usado para marcar cada mensagem com um timestamp na hora certa.

#### Inserir Mensagem no Banco de Dados

```python
def add_menssage(name, menssage):
    timestamp = get_cet_time().strftime(TIMESTAMP_FMT)
    supabase.table("MeusVisitantesLivrados").insert(
        {"name": name, "menssage": menssage, "timestamp": timestamp}
    ).execute()
```

Aqui, a função `add_menssage` insere um novo registro no banco de dados com o nome do usuário, a mensagem e o timestamp. Isso é feito chamando o método `insert` na tabela `MeusVisitantesLivrados` e passando os dados como um dicionário.

#### Buscar Mensagens do Banco de Dados

```python
def get_menssages():
    response = (
        supabase.table("MeusVisitantesLivrados").select("*").order("id", desc=True).execute()
    )
    return response.data
```

Essa função busca todas as mensagens armazenadas no banco de dados, ordenando-as por `id` em ordem decrescente (ou seja, as mensagens mais recentes vêm primeiro). O resultado da consulta é retornado como `response.data`.

#### Renderizar Mensagens

```python
def render_menssage(entry):
    return Article(
            Header(f"Nome: {entry['name']}"),
            P(entry['menssage']),
            Footer(Small(Em(f"Postado: {entry['timestamp']}"))),
        ),
```

A função `render_menssage` recebe uma entrada (uma mensagem) e constrói um componente HTML usando FastHTML. Ela renderiza o nome do usuário, a mensagem e a data de postagem, formatando isso com os componentes `Article`, `Header`, `P`, e `Footer`.

#### Lista de Mensagens

```python
def render_menssage_list():
    messages = get_menssages()
    return Div(
        *[render_menssage(entry) for entry in messages],
        id="menssage-list",
    )
```

Essa função chama `get_menssages` para obter todas as mensagens e, em seguida, usa um loop para renderizar cada uma delas dentro de um `Div`. O resultado é uma lista de mensagens formatadas.

#### Página de Conteúdo

```python
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
```

Aqui é criada a página de conteúdo principal. O formulário HTML permite ao usuário enviar um nome e uma mensagem, e a função usa **htmx** para que, quando o formulário for enviado, a lista de mensagens na página seja atualizada sem precisar recarregar.

### Roteamento

#### Submissão da Mensagem

```python
@routes("/submit-menssage")
def post(name: str, menssage: str):
    add_menssage(name, menssage)
    return render_menssage_list()
```

Quando o usuário envia o formulário, os dados (nome e mensagem) são enviados para a rota `"/submit-menssage"`. A função `post` chama `add_menssage` para adicionar a mensagem ao banco de dados e, em seguida, renderiza a lista de mensagens novamente para atualizar a página com a nova mensagem.

#### Página Principal

```python
@routes("/")
def get():
    return Titled("Caderninho de Visitantes :D", render_content())
```

Essa rota é a página principal, onde todo o conteúdo, incluindo o formulário e a lista de mensagens, é exibido.

#### Executar a Aplicação

```python
serve()
```

Esse comando inicia o servidor FastHTML e coloca a aplicação no ar, pronta para receber visitas e processar as mensagens.
