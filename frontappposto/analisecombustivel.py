import flet as ft
import httpx
from config_loader import load_config

# Carrega as configurações
config = load_config()

# Endpoint completo
API_URL = config["api_base_url"] + config["densidade_endpoint"]

def AnaliseCombustivel(page: ft.Page):
    # Paleta de cores
    PRIMARY_COLOR = "#FFA726"
    TEXT_COLOR = "#37474F"

    # Campos de entrada
    tipo_combustivel = ft.Dropdown(
        label="Tipo de Combustível",
        options=[
            ft.dropdown.Option("Gasolina Comum", "Gasolina Comum"),
            ft.dropdown.Option("Gasolina Aditivada", "Gasolina Aditivada"),
            ft.dropdown.Option("Gasolina Podium", "Gasolina Podium"),
            ft.dropdown.Option("Etanol", "Etanol"),
            ft.dropdown.Option("Etanol Premium", "Etanol Premium"),
            ft.dropdown.Option("Diesel S10", "Diesel S10"),
            ft.dropdown.Option("Diesel S10 Aditivado", "Diesel S10 Aditivado"),
            ft.dropdown.Option("Diesel S500", "Diesel S500"),
            ft.dropdown.Option("Diesel S500 Aditivado", "Diesel S500 Aditivado"),
        ],
    )

    temperatura_observada = ft.TextField(
        label="Temperatura Observada (°C)",
        keyboard_type=ft.KeyboardType.NUMBER,
        color=TEXT_COLOR,
        text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
    )

    densidade_observada = ft.TextField(
        label="Densidade Observada (kg/m³)",
        keyboard_type=ft.KeyboardType.NUMBER,
        color=TEXT_COLOR,
        text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
    )

    # Exibição dos resultados
    resultado = ft.Column()

    # Função para enviar os dados para a API
    async def calcular(e):
        resultado.controls.clear()  # Limpa os resultados anteriores
        try:
            # Prepara os dados para envio
            dados = {
                "temperatura_observada": float(temperatura_observada.value),
                "densidade_observada": float(densidade_observada.value),
                "tipo_combustivel": tipo_combustivel.value,
            }

            # Envia a requisição para a API
            async with httpx.AsyncClient() as client:
                response = await client.post(API_URL, json=dados)
                response.raise_for_status()

            # Exibe os resultados
            dados_response = response.json()
            resultado.controls.append(ft.Text(f"Temperatura Lida: {dados_response['temperatura_lida']} °C", color=TEXT_COLOR))
            resultado.controls.append(ft.Text(f"Densidade Lida: {dados_response['densidade_lida']} kg/m³", color=TEXT_COLOR))
            resultado.controls.append(ft.Text(f"Densidade Corrigida: {dados_response['densidade_corrigida']} kg/m³", color=TEXT_COLOR))
            
            if dados_response['teor_alcoolico'] is not False:
                resultado.controls.append(ft.Text(f"Teor Alcoólico: {dados_response['teor_alcoolico']}%", color=TEXT_COLOR))
            
            resultado.controls.append(ft.Text(f"Status: {dados_response['status']}", color=TEXT_COLOR, weight="bold"))
        except httpx.HTTPStatusError as http_error:
            # Trata erros de status HTTP retornados pela API
            resultado.controls.append(ft.Text(f"Erro: {http_error.response.json().get('detail', 'Erro desconhecido')}", color="red"))
        except Exception as ex:
            # Trata outros erros, como problemas de conexão
            resultado.controls.append(ft.Text(f"Erro ao calcular: {ex}", color="red"))
        finally:
            page.update()

    # Retorna o layout da tela
    return ft.Column(
        [
            ft.Text("Análise de Combustível", size=24, weight="bold", color=TEXT_COLOR),
            tipo_combustivel,  # Tipo de combustível como primeiro campo
            temperatura_observada,  # Temperatura como segundo campo
            densidade_observada,  # Densidade como terceiro campo
            ft.ElevatedButton("Calcular", on_click=calcular, bgcolor=PRIMARY_COLOR, color="white"),
            ft.Divider(),
            resultado,
        ],
        expand=True,
    )
