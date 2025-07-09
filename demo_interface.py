# demo_interface.py - Demonstração da interface melhorada
# -*- coding: utf-8 -*-

import flet as ft
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import io
import base64
from datetime import datetime, timedelta
import numpy as np

# Importar estilos
from styles import COLORS, TEXT_STYLES, CARD_STYLES, create_title, create_metric_card, create_status_badge, apply_theme_to_page

def create_demo_data():
    """Cria dados simulados para demonstração."""
    # Dados atuais simulados
    current_data = {
        'Concentracao_Geral_PPM': 245.7,
        'PM2.5_ug_m3': 18.3,
        'PM10_ug_m3': 32.1,
        'Temperatura_C': 24.5,
        'Umidade_Relativa_percent': 65.2,
        'qualidade_ar': 'Bom'
    }
    
    # Dados de previsão simulados
    hours = pd.date_range(start=datetime.now(), periods=24, freq='H')
    forecast_data = {
        'Concentracao_Geral_PPM': np.random.normal(250, 30, 24),
        'PM2.5_ug_m3': np.random.normal(20, 5, 24),
        'PM10_ug_m3': np.random.normal(35, 8, 24)
    }
    df_forecast = pd.DataFrame(forecast_data, index=hours)
    
    return current_data, df_forecast

def create_progress_bar(value: float, max_value: float, color: str = COLORS['primary']) -> ft.Container:
    """Cria uma barra de progresso customizada."""
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
                bgcolor=COLORS['border'],
                border_radius=2
            )
        ]),
        padding=4
    )

def gerar_grafico_demo(df_forecast: pd.DataFrame) -> str:
    """Gera um gráfico de demonstração."""
    figura_matplotlib = Figure(figsize=(12, 6), dpi=100, facecolor='white')
    eixos = figura_matplotlib.add_subplot(111)
    
    figura_matplotlib.set_facecolor(COLORS['surface'])
    eixos.set_facecolor(COLORS['surface'])

    cores = [COLORS['primary'], COLORS['secondary'], COLORS['accent']]
    for i, col in enumerate(df_forecast.columns):
        label = col.replace('_PPM', ' PPM').replace('_ug_m3', ' µg/m³')
        eixos.plot(df_forecast.index, df_forecast[col], 
                  label=label, linewidth=3, color=cores[i % len(cores)])

    eixos.legend(prop={'size': 11, 'weight': 'bold'}, 
                frameon=True, fancybox=True, shadow=True, loc='upper right')
    eixos.set_title("Previsão - Próximas 24 Horas", 
                   color=COLORS['text_primary'], size=16, weight='bold', pad=25)
    eixos.grid(True, alpha=0.2, linestyle='-', linewidth=0.5)

    eixos.tick_params(axis='x', colors=COLORS['text_primary'], rotation=45, labelsize=11)
    eixos.tick_params(axis='y', colors=COLORS['text_primary'], labelsize=11)
    eixos.set_xlabel('Horas', color=COLORS['text_primary'], size=13, weight='bold')
    eixos.set_ylabel('Concentração', color=COLORS['text_primary'], size=13, weight='bold')
    
    for spine in eixos.spines.values():
        spine.set_edgecolor(COLORS['border'])
        spine.set_linewidth(1)

    figura_matplotlib.tight_layout(pad=2.5)
    buf = io.BytesIO()
    figura_matplotlib.savefig(buf, format="png", transparent=False, 
                             bbox_inches='tight', dpi=120)
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def main(page: ft.Page):
    """Demonstração da interface melhorada."""
    # Aplicar tema personalizado
    apply_theme_to_page(page)
    page.title = "Sentinela Verde - Demonstração da Interface"
    
    # Criar dados de demonstração
    current_data, df_forecast = create_demo_data()
    
    # Status badge
    status_indicator = create_status_badge("Conectado", COLORS['success'])
    timestamp_text = ft.Text(f"Última atualização: {datetime.now().strftime('%H:%M:%S')}", **TEXT_STYLES['caption'])
    
    # Cards de métricas
    card_concentracao = create_metric_card(
        "Concentração Geral", 
        f"{current_data['Concentracao_Geral_PPM']:.1f}", 
        "ppm", 
        ft.Icons.AIR, 
        COLORS['primary']
    )
    
    card_pm25 = create_metric_card(
        "PM2.5", 
        f"{current_data['PM2.5_ug_m3']:.1f}", 
        "µg/m³", 
        ft.Icons.CLOUD, 
        COLORS['secondary']
    )
    
    card_pm10 = create_metric_card(
        "PM10", 
        f"{current_data['PM10_ug_m3']:.1f}", 
        "µg/m³", 
        ft.Icons.CLOUD_QUEUE, 
        COLORS['accent']
    )
    
    card_temperatura = create_metric_card(
        "Temperatura", 
        f"{current_data['Temperatura_C']:.1f}", 
        "°C", 
        ft.Icons.THERMOSTAT, 
        COLORS['warning']
    )
    
    card_umidade = create_metric_card(
        "Umidade", 
        f"{current_data['Umidade_Relativa_percent']:.1f}", 
        "%", 
        ft.Icons.WATER_DROP, 
        COLORS['info']
    )

    # Card de qualidade do ar
    qualidade = current_data['qualidade_ar']
    icone_qualidade = ft.Icons.SENTIMENT_SATISFIED if qualidade == 'Bom' else ft.Icons.HELP_OUTLINE
    cor_qualidade = COLORS['good'] if qualidade == 'Bom' else COLORS['text_muted']
    
    card_qualidade_ar = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.AIR, color=COLORS['primary'], size=28),
                    ft.Text("Qualidade do Ar (IA)", **TEXT_STYLES['h4'])
                ], alignment=ft.MainAxisAlignment.START),
                ft.Container(height=20),
                ft.Column([
                    ft.Icon(icone_qualidade, size=48, color=cor_qualidade),
                    ft.Container(height=12),
                    ft.Text(qualidade.upper(), **TEXT_STYLES['h2']),
                    ft.Container(height=8),
                    ft.Text("Qualidade do ar aceitável para a maioria das pessoas", **TEXT_STYLES['body']),
                    ft.Container(height=16),
                    # Indicadores de progresso
                    ft.Column([
                        ft.Row([
                            ft.Text("Concentração:", size=12, color=COLORS['text_secondary']),
                            ft.Container(width=8),
                            create_progress_bar(current_data['Concentracao_Geral_PPM'], 1000, COLORS['primary'])
                        ]),
                        ft.Container(height=4),
                        ft.Row([
                            ft.Text("PM2.5:", size=12, color=COLORS['text_secondary']),
                            ft.Container(width=8),
                            create_progress_bar(current_data['PM2.5_ug_m3'], 50, COLORS['secondary'])
                        ]),
                        ft.Container(height=4),
                        ft.Row([
                            ft.Text("PM10:", size=12, color=COLORS['text_secondary']),
                            ft.Container(width=8),
                            create_progress_bar(current_data['PM10_ug_m3'], 100, COLORS['accent'])
                        ])
                    ])
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            **CARD_STYLES['featured']
        ),
        **CARD_STYLES['featured']
    )

    # Gráfico
    controle_imagem_plot = ft.Image(
        src_base64=gerar_grafico_demo(df_forecast),
        fit=ft.ImageFit.CONTAIN, 
        expand=True
    )

    # Header
    header = ft.Container(
        content=ft.Row([
            ft.Column([
                ft.Text("🌳 Sentinela Verde", **TEXT_STYLES['h1']),
                ft.Text("Monitoramento Inteligente da Qualidade do Ar", **TEXT_STYLES['body'])
            ], expand=True),
            status_indicator
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.only(bottom=20)
    )

    # Seção de métricas
    metrics_section = ft.Container(
        content=ft.Column([
            create_title("Métricas em Tempo Real", 'h3'),
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
            create_title("Análise Preditiva", 'h3'),
            ft.Container(height=15),
            ft.Row([
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Previsão de Qualidade", **TEXT_STYLES['h4']),
                            ft.Container(height=10),
                            controle_imagem_plot
                        ]),
                        padding=24
                    ),
                    **CARD_STYLES['default'],
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
            ft.Text("Demonstração", **TEXT_STYLES['caption'])
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