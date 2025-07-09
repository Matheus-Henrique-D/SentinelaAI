# styles.py - Estilos customizados para o Sentinela Verde
# -*- coding: utf-8 -*-

import flet as ft

# Paleta de cores moderna e profissional
COLORS = {
    'primary': '#2E7D32',      # Verde escuro - cor principal
    'secondary': '#4CAF50',    # Verde médio - cor secundária
    'accent': '#81C784',       # Verde claro - cor de destaque
    'background': '#F8F9FA',   # Cinza muito claro - fundo
    'surface': '#FFFFFF',      # Branco - superfícies
    'text_primary': '#212121', # Preto suave - texto principal
    'text_secondary': '#757575', # Cinza médio - texto secundário
    'text_muted': '#9E9E9E',   # Cinza claro - texto mudo
    'success': '#4CAF50',      # Verde - sucesso
    'warning': '#FF9800',      # Laranja - aviso
    'danger': '#F44336',       # Vermelho - perigo
    'info': '#2196F3',         # Azul - informação
    'excellent': '#00C853',    # Verde excelente
    'good': '#4CAF50',         # Verde bom
    'moderate': '#FF9800',     # Laranja moderado
    'poor': '#F44336',         # Vermelho ruim
    'border': '#E0E0E0',       # Cinza claro - bordas
    'shadow': '#00000010',     # Preto transparente - sombras
}

# Estilos de texto
TEXT_STYLES = {
    'h1': {
        'size': 32,
        'weight': ft.FontWeight.BOLD,
        'color': COLORS['text_primary']
    },
    'h2': {
        'size': 24,
        'weight': ft.FontWeight.BOLD,
        'color': COLORS['text_primary']
    },
    'h3': {
        'size': 20,
        'weight': ft.FontWeight.BOLD,
        'color': COLORS['text_primary']
    },
    'h4': {
        'size': 16,
        'weight': ft.FontWeight.BOLD,
        'color': COLORS['text_primary']
    },
    'body': {
        'size': 14,
        'color': COLORS['text_primary']
    },
    'caption': {
        'size': 12,
        'color': COLORS['text_secondary']
    },
    'metric_value': {
        'size': 36,
        'weight': ft.FontWeight.BOLD,
        'color': COLORS['text_primary']
    },
    'metric_unit': {
        'size': 14,
        'color': COLORS['text_secondary']
    }
}

# Estilos de cards
CARD_STYLES = {
    'default': {
        'elevation': 2,
        'color': COLORS['surface'],
        # 'border_radius': 12,  # Removido daqui
        # 'padding': 20        # Removido daqui
    },
    'metric': {
        'elevation': 3,
        'color': COLORS['surface'],
        # 'border_radius': 16, # Removido daqui
        # 'padding': 24       # Removido daqui
    },
    'featured': {
        'elevation': 4,
        'color': COLORS['surface'],
        # 'border_radius': 20, # Removido daqui
        # 'padding': 28       # Removido daqui
    }
}

# Estilos de container para cards
CONTAINER_CARD_STYLES = {
    'default': {
        'border_radius': 12,
        'padding': 20
    },
    'metric': {
        'border_radius': 16,
        'padding': 24
    },
    'featured': {
        'border_radius': 20,
        'padding': 28
    }
}

# Estilos de botões
BUTTON_STYLES = {
    'primary': {
        'bgcolor': COLORS['primary'],
        'color': COLORS['surface'],
        'border_radius': 8,
        'padding': 16
    },
    'secondary': {
        'bgcolor': COLORS['surface'],
        'color': COLORS['primary'],
        'border_radius': 8,
        'padding': 16,
        'border': ft.border.all(1, COLORS['primary'])
    }
}

def create_title(text: str, style: str = 'h1') -> ft.Text:
    """Cria um título com estilo padronizado."""
    return ft.Text(text, **TEXT_STYLES[style])

def create_metric_card(title: str, value: str, unit: str, icon: str, color: str = COLORS['primary']) -> ft.Card:
    """Cria um card de métrica com design moderno."""
    return ft.Card(
        content=ft.Container(
            content=ft.Column([
                # Header do card
                ft.Row([
                    ft.Icon(icon, color=color, size=28),
                    ft.Text(title, **TEXT_STYLES['h4'])
                ], alignment=ft.MainAxisAlignment.START),
                ft.Container(height=16),
                # Valor principal
                ft.Row([
                    ft.Text(value, **TEXT_STYLES['metric_value']),
                    ft.Container(width=8),
                    ft.Text(unit, **TEXT_STYLES['metric_unit'])
                ], alignment=ft.MainAxisAlignment.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            **CONTAINER_CARD_STYLES['metric']
        ),
        elevation=3,
        color=COLORS['surface']
    )

def create_status_badge(status: str, color: str = COLORS['info']) -> ft.Container:
    """Cria um badge de status."""
    return ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.CIRCLE, size=8, color=color),
            ft.Text(status, size=12, color=color, weight=ft.FontWeight.W_500)
        ], spacing=6),
        padding=ft.padding.symmetric(horizontal=12, vertical=6),
        border_radius=12,
        bgcolor=f"{color}20"  # Cor com transparência
    )

def create_progress_indicator(value: float, max_value: float = 100, color: str = COLORS['primary']) -> ft.Container:
    """Cria um indicador de progresso customizado."""
    percentage = (value / max_value) * 100
    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text(f"{value:.1f}", size=14, weight=ft.FontWeight.BOLD),
                ft.Text(f"/ {max_value}", size=12, color=COLORS['text_secondary'])
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(height=4),
            ft.Container(
                content=ft.Container(
                    width=percentage,
                    bgcolor=color,
                    border_radius=2
                ),
                width=100,
                height=4,
                bgcolor=COLORS['border'],
                border_radius=2
            )
        ]),
        padding=8
    )

def create_alert_card(title: str, message: str, alert_type: str = 'info') -> ft.Card:
    """Cria um card de alerta."""
    color_map = {
        'info': COLORS['info'],
        'success': COLORS['success'],
        'warning': COLORS['warning'],
        'danger': COLORS['danger']
    }
    
    icon_map = {
        'info': ft.Icons.INFO,
        'success': ft.Icons.CHECK_CIRCLE,
        'warning': ft.Icons.WARNING,
        'danger': ft.Icons.ERROR
    }
    
    color = color_map.get(alert_type, COLORS['info'])
    icon = icon_map.get(alert_type, ft.Icons.INFO)
    
    return ft.Card(
        content=ft.Container(
            content=ft.Row([
                ft.Icon(icon, color=color, size=24),
                ft.Container(width=12),
                ft.Column([
                    ft.Text(title, **TEXT_STYLES['h4']),
                    ft.Text(message, **TEXT_STYLES['body'])
                ], expand=True)
            ]),
            **CARD_STYLES['default']
        ),
        **CARD_STYLES['default']
    )

def create_data_table(headers: list, data: list) -> ft.DataTable:
    """Cria uma tabela de dados estilizada."""
    return ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text(header, **TEXT_STYLES['h4'])) 
            for header in headers
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(cell), **TEXT_STYLES['body']))
                    for cell in row
                ]
            ) for row in data
        ],
        border=ft.border.all(1, COLORS['border']),
        border_radius=8,
        column_spacing=20,
        heading_row_height=50,
        data_row_min_height=40,
        data_row_max_height=50,
    )

def apply_theme_to_page(page: ft.Page):
    """Aplica o tema personalizado à página."""
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = COLORS['background']
    page.padding = 24
    page.spacing = 24
    
    # Configurar scrollbar customizada
    page.scroll = ft.ScrollMode.AUTO
    
    # Configurar fonte padrão
    page.fonts = {
        "Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap"
    }
    page.theme = ft.Theme(
        font_family="Roboto",
        color_scheme_seed=COLORS['primary']
    )

def create_loading_overlay() -> ft.Container:
    """Cria um overlay de carregamento."""
    return ft.Container(
        content=ft.Column([
            ft.ProgressRing(color=COLORS['primary'], width=32, height=32),
            ft.Container(height=12),
            ft.Text("Carregando...", **TEXT_STYLES['body'])
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        alignment=ft.alignment.center,
        bgcolor=f"{COLORS['surface']}CC",  # Branco com transparência
        border_radius=12,
        padding=24
    )

def create_empty_state(icon: str, title: str, message: str) -> ft.Container:
    """Cria um estado vazio (quando não há dados)."""
    return ft.Container(
        content=ft.Column([
            ft.Icon(icon, size=64, color=COLORS['text_muted']),
            ft.Container(height=16),
            ft.Text(title, **TEXT_STYLES['h3']),
            ft.Container(height=8),
            ft.Text(message, **TEXT_STYLES['body'], text_align=ft.TextAlign.CENTER)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        alignment=ft.alignment.center,
        padding=48
    ) 