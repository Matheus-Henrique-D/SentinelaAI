# frontend.py (versão moderna e melhorada com estilos customizados)
# -*- coding: utf-8 -*-

import flet as ft
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import io
import base64
from typing import Dict, Any
from datetime import datetime

# Importa o backend apenas para anotação de tipo, evitando importação circular.
from backend import SentinelaVerde
from styles import COLORS, TEXT_STYLES, CARD_STYLES, create_title, create_metric_card, create_status_badge, apply_theme_to_page

# --- Referências Globais a Controles Flet ---
# Cards principais
card_concentracao = None
card_pm25 = None
card_pm10 = None
card_temperatura = None
card_umidade = None
card_qualidade_ar = None

# Textos dos valores
texto_concentracao_geral = ft.Text("--", **TEXT_STYLES['metric_value'])
texto_pm25 = ft.Text("--", **TEXT_STYLES['metric_value'])
texto_pm10 = ft.Text("--", **TEXT_STYLES['metric_value'])
texto_temperatura = ft.Text("--", **TEXT_STYLES['metric_value'])
texto_umidade = ft.Text("--", **TEXT_STYLES['metric_value'])

# Unidades
unidade_concentracao = ft.Text("ppm", **TEXT_STYLES['metric_unit'])
unidade_pm25 = ft.Text("µg/m³", **TEXT_STYLES['metric_unit'])
unidade_pm10 = ft.Text("µg/m³", **TEXT_STYLES['metric_unit'])
unidade_temperatura = ft.Text("°C", **TEXT_STYLES['metric_unit'])
unidade_umidade = ft.Text("%", **TEXT_STYLES['metric_unit'])

# Qualidade do ar
icone_qualidade_ar = ft.Icon(ft.Icons.HELP_OUTLINE, size=48, color=COLORS['text_muted'])
texto_qualidade_ar = ft.Text("Aguardando...", **TEXT_STYLES['h2'])
descricao_qualidade = ft.Text("Análise em andamento", **TEXT_STYLES['body'])

# Gráfico
controle_imagem_plot = ft.Image(fit=ft.ImageFit.CONTAIN, expand=True)
indicador_carregamento = ft.ProgressRing(visible=False, width=32, height=32, color=COLORS['primary'])

# Status e timestamp
status_indicator = create_status_badge("Conectando...", COLORS['warning'])
timestamp_text = ft.Text("Última atualização: --", **TEXT_STYLES['caption'])

# Indicadores de progresso para qualidade do ar
progress_concentracao = None
progress_pm25 = None
progress_pm10 = None

def get_quality_color(quality: str) -> str:
    """Retorna a cor baseada na qualidade do ar."""
    color_map = {
        'Excelente': COLORS['excellent'],
        'Bom': COLORS['good'],
        'Moderado': COLORS['moderate'],
        'Ruim': COLORS['poor'],
        'IA não treinada': COLORS['info'],
        'Analisando...': COLORS['warning'],
        'Aguardando...': COLORS['text_muted']
    }
    return color_map.get(quality, COLORS['text_muted'])

def get_quality_icon(quality: str) -> str:
    """Retorna o ícone baseado na qualidade do ar."""
    icon_map = {
        'Excelente': ft.Icons.SENTIMENT_VERY_SATISFIED,
        'Bom': ft.Icons.SENTIMENT_SATISFIED,
        'Moderado': ft.Icons.SENTIMENT_NEUTRAL,
        'Ruim': ft.Icons.SENTIMENT_DISSATISFIED,
        'IA não treinada': ft.Icons.COMPUTER,
        'Analisando...': ft.Icons.HOURGLASS_EMPTY,
        'Aguardando...': ft.Icons.HOURGLASS_EMPTY
    }
    return icon_map.get(quality, ft.Icons.HELP_OUTLINE)

def get_quality_description(quality: str) -> str:
    """Retorna a descrição baseada na qualidade do ar."""
    desc_map = {
        'Excelente': 'Qualidade do ar ideal para atividades ao ar livre',
        'Bom': 'Qualidade do ar aceitável para a maioria das pessoas',
        'Moderado': 'Algumas pessoas podem ser sensíveis',
        'Ruim': 'Evite atividades ao ar livre prolongadas',
        'IA não treinada': 'Modelo de IA ainda em treinamento',
        'Analisando...': 'Processando dados dos sensores',
        'Aguardando...': 'Aguardando primeira leitura'
    }
    return desc_map.get(quality, 'Status desconhecido')

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

def gerar_imagem_grafico_base64(summary_data: Dict[str, Any], page_theme_mode: ft.ThemeMode) -> str:
    """Cria um gráfico de previsão moderno e o retorna como uma string base64."""
    figura_matplotlib = Figure(figsize=(12, 6), dpi=100, facecolor='white')
    eixos = figura_matplotlib.add_subplot(111)
    
    # Configuração do tema
    cor_texto = COLORS['text_primary'] if page_theme_mode == ft.ThemeMode.LIGHT else '#FFFFFF'
    cor_fundo = COLORS['surface'] if page_theme_mode == ft.ThemeMode.LIGHT else '#1E1E1E'
    
    figura_matplotlib.set_facecolor(cor_fundo)
    eixos.set_facecolor(cor_fundo)

    df_forecast = summary_data.get('previsoes')
    tem_dados = False
    
    if df_forecast is not None and not df_forecast.empty:
        cores = [COLORS['primary'], COLORS['secondary'], COLORS['accent']]
        for i, col in enumerate(df_forecast.columns):
            if pd.api.types.is_numeric_dtype(df_forecast[col]):
                tem_dados = True
                label = col.replace('_PPM', ' PPM').replace('_ug_m3', ' µg/m³')
                eixos.plot(df_forecast.index, df_forecast[col], 
                          label=label, linewidth=3, color=cores[i % len(cores)])

    if tem_dados:
        eixos.legend(prop={'size': 11, 'weight': 'bold'}, 
                    frameon=True, fancybox=True, shadow=True, loc='upper right')
        eixos.set_title("Previsão - Próximas 24 Horas", 
                       color=cor_texto, size=16, weight='bold', pad=25)
        eixos.grid(True, alpha=0.2, linestyle='-', linewidth=0.5)
    else:
        eixos.text(0.5, 0.5, "Dados insuficientes para previsão", 
                  ha='center', va='center', color=cor_texto, 
                  fontsize=14, style='italic')

    eixos.tick_params(axis='x', colors=cor_texto, rotation=45, labelsize=11)
    eixos.tick_params(axis='y', colors=cor_texto, labelsize=11)
    eixos.set_xlabel('Horas', color=cor_texto, size=13, weight='bold')
    eixos.set_ylabel('Concentração', color=cor_texto, size=13, weight='bold')
    
    for spine in eixos.spines.values():
        spine.set_edgecolor(COLORS['border'])
        spine.set_linewidth(1)

    figura_matplotlib.tight_layout(pad=2.5)
    buf = io.BytesIO()
    figura_matplotlib.savefig(buf, format="png", transparent=False, 
                             bbox_inches='tight', dpi=120)
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def atualizar_elementos_ui(page: ft.Page, sentinela_instance: 'SentinelaVerde'):
    """Função central que ATUALIZA a UI com os dados mais recentes do backend."""
    indicador_carregamento.visible = True
    page.update()

    summary = sentinela_instance.get_latest_data_summary()

    if summary:
        # Atualizar valores
        conc_geral = summary.get('Concentracao_Geral_PPM')
        texto_concentracao_geral.value = f"{conc_geral:.1f}" if conc_geral is not None else "--"

        pm25 = summary.get('PM2.5_ug_m3')
        texto_pm25.value = f"{pm25:.1f}" if pm25 is not None else "--"

        pm10 = summary.get('PM10_ug_m3')
        texto_pm10.value = f"{pm10:.1f}" if pm10 is not None else "--"

        temp = summary.get('Temperatura_C')
        texto_temperatura.value = f"{temp:.1f}" if temp is not None else "--"
        
        umid = summary.get('Umidade_Relativa_percent')
        texto_umidade.value = f"{umid:.1f}" if umid is not None else "--"
        
        # Atualizar qualidade do ar
        qualidade = summary.get('qualidade_ar', "Aguardando...")
        texto_qualidade_ar.value = qualidade.upper()
        descricao_qualidade.value = get_quality_description(qualidade)
        
        # Atualizar ícone e cor da qualidade
        icone_qualidade_ar.name = get_quality_icon(qualidade)
        icone_qualidade_ar.color = get_quality_color(qualidade)
        
        # Atualizar status
        status_indicator.content.controls[0].color = COLORS['success']
        status_indicator.content.controls[1].value = "Conectado"
        status_indicator.content.controls[1].color = COLORS['success']
        
        # Atualizar timestamp
        timestamp_text.value = f"Última atualização: {datetime.now().strftime('%H:%M:%S')}"
    
    # Atualizar gráfico
    controle_imagem_plot.src_base64 = gerar_imagem_grafico_base64(summary, page.theme_mode)

    indicador_carregamento.visible = False
    page.update()

def main(page: ft.Page, sentinela_instance: 'SentinelaVerde'):
    """
    Constrói a interface gráfica moderna e melhorada.
    """
    # Aplicar tema personalizado
    apply_theme_to_page(page)
    page.title = "Sentinela Verde - Monitoramento Inteligente"
    
    # Configurar callback de atualização
    sentinela_instance.page_update_callback = lambda: atualizar_elementos_ui(page, sentinela_instance)

    # Criar cards de métricas usando a função do styles.py
    global card_concentracao, card_pm25, card_pm10, card_temperatura, card_umidade, card_qualidade_ar
    
    card_concentracao = create_metric_card(
        "Concentração Geral", 
        texto_concentracao_geral.value, 
        unidade_concentracao.value, 
        ft.Icons.AIR, 
        COLORS['primary']
    )
    
    card_pm25 = create_metric_card(
        "PM2.5", 
        texto_pm25.value, 
        unidade_pm25.value, 
        ft.Icons.CLOUD, 
        COLORS['secondary']
    )
    
    card_pm10 = create_metric_card(
        "PM10", 
        texto_pm10.value, 
        unidade_pm10.value, 
        ft.Icons.CLOUD_QUEUE, 
        COLORS['accent']
    )
    
    card_temperatura = create_metric_card(
        "Temperatura", 
        texto_temperatura.value, 
        unidade_temperatura.value, 
        ft.Icons.THERMOSTAT, 
        COLORS['warning']
    )
    
    card_umidade = create_metric_card(
        "Umidade", 
        texto_umidade.value, 
        unidade_umidade.value, 
        ft.Icons.WATER_DROP, 
        COLORS['info']
    )

    # Card de qualidade do ar melhorado
    card_qualidade_ar = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.AIR, color=COLORS['primary'], size=28),
                    ft.Text("Qualidade do Ar (IA)", **TEXT_STYLES['h4'])
                ], alignment=ft.MainAxisAlignment.START),
                ft.Container(height=20),
                ft.Column([
                    icone_qualidade_ar,
                    ft.Container(height=12),
                    texto_qualidade_ar,
                    ft.Container(height=8),
                    descricao_qualidade,
                    ft.Container(height=16),
                    # Indicadores de progresso para cada métrica
                    ft.Column([
                        ft.Row([
                            ft.Text("Concentração:", size=12, color=COLORS['text_secondary']),
                            ft.Container(width=8),
                            create_progress_bar(0, 1000, COLORS['primary'])
                        ]),
                        ft.Container(height=4),
                        ft.Row([
                            ft.Text("PM2.5:", size=12, color=COLORS['text_secondary']),
                            ft.Container(width=8),
                            create_progress_bar(0, 50, COLORS['secondary'])
                        ]),
                        ft.Container(height=4),
                        ft.Row([
                            ft.Text("PM10:", size=12, color=COLORS['text_secondary']),
                            ft.Container(width=8),
                            create_progress_bar(0, 100, COLORS['accent'])
                        ])
                    ])
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            **CARD_STYLES['featured']
        ),
        **CARD_STYLES['featured']
    )

    # Header com título e status
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

    # Seção de métricas principais
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

    # Seção de análise e gráfico
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
                ft.Container(width=20),  # Espaçamento
                card_qualidade_ar
            ], alignment=ft.MainAxisAlignment.CENTER)
        ]),
        padding=ft.padding.only(bottom=20)
    )

    # Footer com informações
    footer = ft.Container(
        content=ft.Row([
            timestamp_text,
            ft.Container(expand=True),
            indicador_carregamento
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
    
    # Iniciar análise
    sentinela_instance.run_analysis()
