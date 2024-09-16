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
