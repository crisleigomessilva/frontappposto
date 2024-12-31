import flet as ft
import httpx
import asyncio

API_BASE_URL = "http://217.77.0.239:8081"
LOGIN_ENDPOINT = "/auth/login"

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
                url = f"{API_BASE_URL}{LOGIN_ENDPOINT}"
                params = {"email": email, "password": password}

                print(f"Enviando requisição para: {url}")
                print(f"Query Parameters: {params}")

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
