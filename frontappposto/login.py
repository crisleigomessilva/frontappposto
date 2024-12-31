import flet as ft
import httpx
import asyncio
import json
import os

# Carregar as configurações do config.json
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config.json')


def load_config():
    try:
        with open(CONFIG_PATH, 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print(f"Erro: O arquivo {CONFIG_PATH} não foi encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"Erro: Falha ao decodificar o JSON em {CONFIG_PATH}.")
        return None

# Carregue as configurações na inicialização
config = load_config()
if not config:
    raise Exception("Erro ao carregar o arquivo de configuração. Verifique o config.json.")

# Variável global para armazenar o token JWT
jwt_token = None

def main(page: ft.Page):
    global jwt_token  # Declarar como global para armazenar o token

    page.title = "Tela de Login"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "white"

    email_field = ft.TextField(
        label="Email",
        hint_text="Digite seu email",
        autofocus=True,
        width=300,
    )

    password_field = ft.TextField(
        label="Senha",
        hint_text="Digite sua senha",
        password=True,
        can_reveal_password=True,
        width=300,
    )

    async def authenticate_user(email, password):
        try:
            async with httpx.AsyncClient() as client:
                # Usar os valores do config.json
                api_base_url = config.get("api_base_url")
                login_endpoint = config.get("login_endpoint")
                
                if not api_base_url or not login_endpoint:
                    raise ValueError("Configuração inválida. Verifique api_base_url e login_endpoint no config.json.")

                url = f"{api_base_url}{login_endpoint}"
                params = {"email": email, "password": password}

                print(f"Enviando requisição para: {url}")
                print(f"Query Parameters: {params}")

                # Envia os dados como query parameters
                response = await client.post(url, params=params)
                response.raise_for_status()
                return {"success": True, "data": response.json()}
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 422:
                return {"success": False, "error": "Dados inválidos. Verifique email e senha."}
            if exc.response.status_code == 401:
                return {"success": False, "error": "Email ou senha incorretos."}
            else:
                return {"success": False, "error": f"Erro HTTP: {exc.response.status_code}"}
        except httpx.RequestError as exc:
            return {"success": False, "error": f"Erro de conexão: {exc}"}
        except ValueError as exc:
            return {"success": False, "error": str(exc)}

    async def handle_login():
        email = email_field.value.strip()
        password = password_field.value.strip()

        if not email or not password:
            dialog = ft.AlertDialog(
                title=ft.Text("Erro"),
                content=ft.Text("Por favor, preencha todos os campos."),
                actions=[ft.TextButton("Fechar", on_click=lambda _: close_dialog(dialog))],
                open=True,
            )
            page.overlay.append(dialog)
            page.update()
            return

        dialog = ft.AlertDialog(
            title=ft.Text("Autenticando..."),
            open=True,
        )
        page.overlay.append(dialog)
        page.update()

        result = await authenticate_user(email, password)

        if result.get("success"):
            global jwt_token  # Declaração explícita para modificar a variável global
            jwt_token = result["data"].get("access_token", "Token não encontrado")

            dialog.title = ft.Text("Sucesso")
            dialog.content = ft.Text(f"Login bem-sucedido!")
            dialog.actions = [ft.TextButton("Fechar", on_click=lambda _: close_dialog(dialog))]
        else:
            error_message = result.get("error", "Erro inesperado")
            dialog.title = ft.Text("Erro")
            dialog.content = ft.Text(error_message)
            dialog.actions = [ft.TextButton("Fechar", on_click=lambda _: close_dialog(dialog))]

        dialog.open = True
        page.update()

    def close_dialog(dialog):
        dialog.open = False
        page.update()

    login_button = ft.ElevatedButton(
        text="Entrar",
        on_click=lambda _: asyncio.run(handle_login()),
        width=300,
    )

    page.add(
        ft.Column(
            [
                ft.Text(
                    "Login do Sistema",
                    size=24,
                    weight="bold",
                    color="black",
                    text_align=ft.TextAlign.CENTER,
                ),
                email_field,
                password_field,
                login_button,
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

ft.app(target=main, view=ft.AppView.WEB_BROWSER)
