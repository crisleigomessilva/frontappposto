import flet as ft
from analisecombustivel import AnaliseCombustivel

# Simulando o nome do usuário logado
LOGGED_USER = "Crislei Sousa"

def main(page: ft.Page):
    # Paleta de cores
    PRIMARY_COLOR = "#FFA726"
    BACKGROUND_COLOR = "#ECEFF1"
    DRAWER_BG_COLOR = "#F5F5F5"
    TEXT_COLOR = "#37474F"

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = BACKGROUND_COLOR

    # Conteúdo inicial da página
    content = ft.Column(
        [ft.Text("Bem-vindo ao Sistema de Análise", size=20, weight="bold", color=TEXT_COLOR)],
        expand=True,
    )

    # Função para alterar o conteúdo principal
    def change_content(new_content):
        content.controls.clear()
        content.controls.append(new_content)
        page.update()

    # Configuração do NavigationDrawer
    drawer = ft.NavigationDrawer(
        on_change=lambda e: change_content(AnaliseCombustivel(page)) if e.control.selected_index == 0 else None,
        bgcolor=DRAWER_BG_COLOR,
        controls=[
            ft.NavigationDrawerDestination(
                label="Análise de Combustível",
                icon=ft.Icons.ANALYTICS_OUTLINED,
                selected_icon=ft.Icons.ANALYTICS,
            ),
        ],
    )

    # Configuração do AppBar
    page.appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.MENU,
            on_click=lambda e: page.open(drawer),
        ),
        title=ft.Text(f"Bem-vindo, {LOGGED_USER}", color=TEXT_COLOR),
        center_title=True,
        bgcolor=PRIMARY_COLOR,
    )

    # Adicionando o conteúdo principal
    page.add(content)

ft.app(target=main, view=ft.AppView.WEB_BROWSER)
