# demo_simple.py - Versão simplificada da interface com botão de valores aleatórios
# -*- coding: utf-8 -*-

import flet as ft
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import io
import base64
from datetime import datetime
import numpy as np
import random

# Cores simplificadas
COLORS = {
    'primary': '#2E7D32',
    'secondary': '#4CAF50', 
    'accent': '#81C784',
    'background': '#F5F5F5',
    'surface': '#FFFFFF',
    'text_primary': '#212121',
    'text_secondary': '#757575',
    'success': '#4CAF50',
    'warning': '#FF9800',
    'danger': '#F44336',
    'info': '#2196F3'
}

# Variáveis globais para os controles
texto_concentracao = None
texto_pm25 = None
texto_pm10 = None
texto_temperatura = None
texto_umidade = None
texto_qualidade = None
descricao_qualidade = None
icone_qualidade = None
controle_imagem_plot = None
timestamp_text = None
progress_concentracao = None
progress_pm25 = None
progress_pm10 = None

def gerar_valores_aleatorios():
    """Gera valores aleatórios realistas para as métricas."""
    return {
        'concentracao': round(random.uniform(50, 800), 1),
        'pm25': round(random.uniform(5, 60), 1),
        'pm10': round(random.uniform(10, 120), 1),
        'temperatura': round(random.uniform(15, 35), 1),
        'umidade': round(random.uniform(30, 90), 1)
    }

def determinar_qualidade_ar(concentracao, pm25, pm10):
    """Determina a qualidade do ar baseada nos valores."""
    # Critérios simplificados
    if concentracao < 200 and pm25 < 12 and pm10 < 25:
        return 'Excelente', ft.Icons.SENTIMENT_VERY_SATISFIED, COLORS['success']
    elif concentracao < 400 and pm25 < 25 and pm10 < 50:
        return 'Bom', ft.Icons.SENTIMENT_SATISFIED, COLORS['success']
    elif concentracao < 600 and pm25 < 35 and pm10 < 75:
        return 'Moderado', ft.Icons.SENTIMENT_NEUTRAL, COLORS['warning']
    else:
        return 'Ruim', ft.Icons.SENTIMENT_DISSATISFIED, COLORS['danger']

def get_qualidade_description(qualidade):
    """Retorna a descrição baseada na qualidade do ar."""
    desc_map = {
        'Excelente': 'Qualidade do ar ideal para atividades ao ar livre',
        'Bom': 'Qualidade do ar aceitável para a maioria das pessoas',
        'Moderado': 'Algumas pessoas podem ser sensíveis',
        'Ruim': 'Evite atividades ao ar livre prolongadas'
    }
    return desc_map.get(qualidade, 'Status desconhecido')

def create_metric_card(title: str, value_text: ft.Text, unit: str, icon: str, color: str) -> ft.Card:
    """Cria um card de métrica simples."""
    return ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(icon, color=color, size=24),
                    ft.Text(title, size=16, weight=ft.FontWeight.BOLD, color=COLORS['text_primary'])
                ]),
                ft.Container(height=10),
                ft.Row([
                    value_text,
                    ft.Container(width=5),
                    ft.Text(unit, size=14, color=COLORS['text_secondary'])
                ], alignment=ft.MainAxisAlignment.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            alignment=ft.alignment.center
        ),
        elevation=3,
        color=COLORS['surface']
    )

def create_status_badge(status: str, color: str) -> ft.Container:
    """Cria um badge de status simples."""
    return ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.CIRCLE, size=8, color=color),
            ft.Text(status, size=12, color=color)
        ], spacing=5),
        padding=ft.padding.symmetric(horizontal=10, vertical=5),
        border_radius=10,
        bgcolor=f"{color}20"
    )

def create_progress_bar(value: float, max_value: float, color: str) -> ft.Container:
    """Cria uma barra de progresso simples."""
    percentage = min((value / max_value) * 100, 100) if max_value > 0 else 0
    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text(f"{value:.1f}", size=12, weight=ft.FontWeight.BOLD),
                ft.Text(f"/ {max_value:.1f}", size=10, color=COLORS['text_secondary'])
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(height=2),
            ft.Container(
                content=ft.Container(
                    width=percentage,
                    bgcolor=color,
                    border_radius=1
                ),
                width=80,
                height=4,
                bgcolor='#E0E0E0',
                border_radius=2
            )
        ]),
        padding=4
    )

def gerar_grafico_demo(dados) -> str:
    """Gera um gráfico de demonstração com dados atuais."""
    figura_matplotlib = Figure(figsize=(10, 5), dpi=100, facecolor='white')
    eixos = figura_matplotlib.add_subplot(111)
    
    # Dados simulados baseados nos valores atuais
    horas = range(24)
    concentracao_base = dados['concentracao']
    pm25_base = dados['pm25']
    pm10_base = dados['pm10']
    
    # Gerar previsão com variação baseada no valor atual
    concentracao = [concentracao_base + np.random.normal(0, concentracao_base * 0.1) for _ in horas]
    pm25 = [pm25_base + np.random.normal(0, pm25_base * 0.15) for _ in horas]
    pm10 = [pm10_base + np.random.normal(0, pm10_base * 0.12) for _ in horas]
    
    eixos.plot(horas, concentracao, label='Concentração PPM', linewidth=2, color=COLORS['primary'])
    eixos.plot(horas, pm25, label='PM2.5 µg/m³', linewidth=2, color=COLORS['secondary'])
    eixos.plot(horas, pm10, label='PM10 µg/m³', linewidth=2, color=COLORS['accent'])

    eixos.legend(prop={'size': 10, 'weight': 'bold'})
    eixos.set_title("Previsão - Próximas 24 Horas", color=COLORS['text_primary'], size=14, weight='bold')
    eixos.grid(True, alpha=0.2)
    eixos.set_xlabel('Horas', color=COLORS['text_primary'], size=12)
    eixos.set_ylabel('Concentração', color=COLORS['text_primary'], size=12)
    
    for spine in eixos.spines.values():
        spine.set_edgecolor('#E0E0E0')

    figura_matplotlib.tight_layout(pad=2.0)
    buf = io.BytesIO()
    figura_matplotlib.savefig(buf, format="png", transparent=False, bbox_inches='tight', dpi=100)
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def atualizar_interface(page: ft.Page, dados):
    """Atualiza todos os elementos da interface com novos dados."""
    global texto_concentracao, texto_pm25, texto_pm10, texto_temperatura, texto_umidade
    global texto_qualidade, descricao_qualidade, icone_qualidade, controle_imagem_plot, timestamp_text
    global progress_concentracao, progress_pm25, progress_pm10
    
    # Atualizar valores dos cards
    if texto_concentracao:
        texto_concentracao.value = f"{dados['concentracao']:.1f}"
    if texto_pm25:
        texto_pm25.value = f"{dados['pm25']:.1f}"
    if texto_pm10:
        texto_pm10.value = f"{dados['pm10']:.1f}"
    if texto_temperatura:
        texto_temperatura.value = f"{dados['temperatura']:.1f}"
    if texto_umidade:
        texto_umidade.value = f"{dados['umidade']:.1f}"
    
    # Determinar qualidade do ar
    qualidade, icone, cor = determinar_qualidade_ar(dados['concentracao'], dados['pm25'], dados['pm10'])
    if texto_qualidade:
        texto_qualidade.value = qualidade.upper()
    if descricao_qualidade:
        descricao_qualidade.value = get_qualidade_description(qualidade)
    if icone_qualidade:
        icone_qualidade.name = icone
        icone_qualidade.color = cor
    
    # Atualizar timestamp
    if timestamp_text:
        timestamp_text.value = f"Última atualização: {datetime.now().strftime('%H:%M:%S')}"
    
    # Atualizar gráfico
    if controle_imagem_plot:
        controle_imagem_plot.src_base64 = gerar_grafico_demo(dados)
    
    # Atualizar barras de progresso (simplificado para evitar erros)
    # As barras de progresso serão recriadas a cada atualização
    
    page.update()

def gerar_novos_dados(e):
    """Callback do botão para gerar novos dados."""
    dados = gerar_valores_aleatorios()
    atualizar_interface(e.page, dados)

def main(page: ft.Page):
    """Interface principal com botão de valores aleatórios."""
    global texto_concentracao, texto_pm25, texto_pm10, texto_temperatura, texto_umidade
    global texto_qualidade, descricao_qualidade, icone_qualidade, controle_imagem_plot, timestamp_text
    global progress_concentracao, progress_pm25, progress_pm10
    
    page.title = "Sentinela Verde - Demonstração Interativa"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = COLORS['background']
    page.padding = 20
    page.spacing = 20
    
    # Dados iniciais
    dados = {
        'concentracao': 245.7,
        'pm25': 18.3,
        'pm10': 32.1,
        'temperatura': 24.5,
        'umidade': 65.2
    }
    
    # Status badge
    status_indicator = create_status_badge("Conectado", COLORS['success'])
    timestamp_text = ft.Text(f"Última atualização: {datetime.now().strftime('%H:%M:%S')}", 
                           size=12, color=COLORS['text_secondary'])
    
    # Textos dos valores (serão atualizados)
    texto_concentracao = ft.Text(f"{dados['concentracao']:.1f}", size=32, weight=ft.FontWeight.BOLD, color=COLORS['text_primary'])
    texto_pm25 = ft.Text(f"{dados['pm25']:.1f}", size=32, weight=ft.FontWeight.BOLD, color=COLORS['text_primary'])
    texto_pm10 = ft.Text(f"{dados['pm10']:.1f}", size=32, weight=ft.FontWeight.BOLD, color=COLORS['text_primary'])
    texto_temperatura = ft.Text(f"{dados['temperatura']:.1f}", size=32, weight=ft.FontWeight.BOLD, color=COLORS['text_primary'])
    texto_umidade = ft.Text(f"{dados['umidade']:.1f}", size=32, weight=ft.FontWeight.BOLD, color=COLORS['text_primary'])
    
    # Cards de métricas
    card_concentracao = create_metric_card("Concentração Geral", texto_concentracao, "ppm", ft.Icons.AIR, COLORS['primary'])
    card_pm25 = create_metric_card("PM2.5", texto_pm25, "µg/m³", ft.Icons.CLOUD, COLORS['secondary'])
    card_pm10 = create_metric_card("PM10", texto_pm10, "µg/m³", ft.Icons.CLOUD_QUEUE, COLORS['accent'])
    card_temperatura = create_metric_card("Temperatura", texto_temperatura, "°C", ft.Icons.THERMOSTAT, COLORS['warning'])
    card_umidade = create_metric_card("Umidade", texto_umidade, "%", ft.Icons.WATER_DROP, COLORS['info'])

    # Qualidade do ar inicial
    qualidade, icone, cor = determinar_qualidade_ar(dados['concentracao'], dados['pm25'], dados['pm10'])
    texto_qualidade = ft.Text(qualidade.upper(), size=24, weight=ft.FontWeight.BOLD, color=COLORS['text_primary'])
    descricao_qualidade = ft.Text(get_qualidade_description(qualidade), size=14, color=COLORS['text_secondary'])
    icone_qualidade = ft.Icon(icone, size=48, color=cor)
    
    # Barras de progresso
    progress_concentracao = create_progress_bar(dados['concentracao'], 1000, COLORS['primary'])
    progress_pm25 = create_progress_bar(dados['pm25'], 50, COLORS['secondary'])
    progress_pm10 = create_progress_bar(dados['pm10'], 100, COLORS['accent'])
    
    # Card de qualidade do ar
    card_qualidade_ar = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.AIR, color=COLORS['primary'], size=24),
                    ft.Text("Qualidade do Ar (IA)", size=16, weight=ft.FontWeight.BOLD, color=COLORS['text_primary'])
                ]),
                ft.Container(height=20),
                ft.Column([
                    icone_qualidade,
                    ft.Container(height=10),
                    texto_qualidade,
                    ft.Container(height=8),
                    descricao_qualidade,
                    ft.Container(height=16),
                    # Indicadores de progresso
                    ft.Column([
                        ft.Row([
                            ft.Text("Concentração:", size=12, color=COLORS['text_secondary']),
                            ft.Container(width=8),
                            progress_concentracao
                        ]),
                        ft.Container(height=4),
                        ft.Row([
                            ft.Text("PM2.5:", size=12, color=COLORS['text_secondary']),
                            ft.Container(width=8),
                            progress_pm25
                        ]),
                        ft.Container(height=4),
                        ft.Row([
                            ft.Text("PM10:", size=12, color=COLORS['text_secondary']),
                            ft.Container(width=8),
                            progress_pm10
                        ])
                    ])
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=25,
            alignment=ft.alignment.center
        ),
        elevation=3,
        color=COLORS['surface']
    )

    # Gráfico inicial
    controle_imagem_plot = ft.Image(
        src_base64=gerar_grafico_demo(dados),
        fit=ft.ImageFit.CONTAIN, 
        expand=True
    )

    # Botão para gerar novos dados
    botao_gerar_dados = ft.ElevatedButton(
        content=ft.Row([
            ft.Icon(ft.Icons.REFRESH, color=COLORS['surface']),
            ft.Text("Gerar Novos Dados", color=COLORS['surface'], weight=ft.FontWeight.BOLD)
        ], spacing=8),
        style=ft.ButtonStyle(
            bgcolor=COLORS['primary'],
            padding=ft.padding.symmetric(horizontal=20, vertical=12)
        ),
        on_click=gerar_novos_dados
    )

    # Header
    header = ft.Container(
        content=ft.Row([
            ft.Column([
                ft.Text("🌳 Sentinela Verde", size=28, weight=ft.FontWeight.BOLD, color=COLORS['primary']),
                ft.Text("Monitoramento Inteligente da Qualidade do Ar", size=14, color=COLORS['text_secondary'])
            ], expand=True),
            ft.Column([
                status_indicator,
                ft.Container(height=10),
                botao_gerar_dados
            ], horizontal_alignment=ft.CrossAxisAlignment.END)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.only(bottom=20)
    )

    # Seção de métricas
    metrics_section = ft.Container(
        content=ft.Column([
            ft.Text("Métricas em Tempo Real", size=20, weight=ft.FontWeight.BOLD, color=COLORS['text_primary']),
            ft.Container(height=15),
            ft.Row([
                card_concentracao, card_pm25, card_pm10
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=15),
            ft.Row([
                card_temperatura, card_umidade
            ], alignment=ft.MainAxisAlignment.CENTER)
        ]),
        padding=ft.padding.only(bottom=20)
    )

    # Seção de análise
    analysis_section = ft.Container(
        content=ft.Column([
            ft.Text("Análise Preditiva", size=20, weight=ft.FontWeight.BOLD, color=COLORS['text_primary']),
            ft.Container(height=15),
            ft.Row([
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Previsão de Qualidade", size=16, weight=ft.FontWeight.BOLD, color=COLORS['text_primary']),
                            ft.Container(height=10),
                            controle_imagem_plot
                        ]),
                        padding=20
                    ),
                    elevation=3,
                    color=COLORS['surface'],
                    expand=3
                ),
                ft.Container(width=20),
                card_qualidade_ar
            ], alignment=ft.MainAxisAlignment.CENTER)
        ]),
        padding=ft.padding.only(bottom=20)
    )

    # Footer
    footer = ft.Container(
        content=ft.Row([
            timestamp_text,
            ft.Container(expand=True),
            ft.Text("Demonstração Interativa", size=12, color=COLORS['text_secondary'])
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.only(top=10)
    )

    # Layout principal
    main_layout = ft.Column([
        header,
        metrics_section,
        analysis_section,
        footer
    ], scroll=ft.ScrollMode.AUTO, expand=True, spacing=0)

    page.add(main_layout)

if __name__ == "__main__":
    ft.app(target=main) 