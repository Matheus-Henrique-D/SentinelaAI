# 🌳 Sentinela Verde - Monitoramento Inteligente da Qualidade do Ar

## 🎯 **Visão Geral**

O **Sentinela Verde** é um sistema completo de monitoramento preditivo da qualidade do ar que combina sensores IoT, inteligência artificial e uma interface moderna para fornecer análises em tempo real e previsões futuras.

---

## ✨ **Principais Funcionalidades**

### 🔍 **Monitoramento em Tempo Real**
- **Concentração de Gases**: Monitoramento de CO₂, amônia, benzeno e álcool
- **Material Particulado**: Medição de PM2.5 e PM10
- **Condições Ambientais**: Temperatura e umidade relativa
- **Atualização Automática**: Dados atualizados a cada 2 segundos

### 🤖 **Inteligência Artificial**
- **Classificação Híbrida**: Combina regras tradicionais com IA
- **Árvore de Decisão**: Modelo de machine learning para classificação
- **Previsão Temporal**: Modelos de séries temporais (Holt-Winters)
- **Horizonte de 24h**: Previsões das próximas 24 horas

### 📊 **Interface Moderna e Interativa**
- **Design Responsivo**: Adapta-se a diferentes tamanhos de tela
- **Paleta de Cores Verde**: Tema ambiental profissional
- **Cards Informativos**: Métricas organizadas e visuais
- **Gráficos Dinâmicos**: Previsões com cores temáticas
- **Botão Interativo**: Gera valores aleatórios para testes

---

## 🎨 **Interface Melhorada - Funcionalidades**

### 🖥️ **Layout Organizado**

#### **Header Informativo**
- 🌳 **Título Principal**: "Sentinela Verde"
- 📝 **Subtítulo**: "Monitoramento Inteligente da Qualidade do Ar"
- 🟢 **Status Badge**: Indicador de conexão (Conectado/Conectando)
- 🔄 **Botão Interativo**: "Gerar Novos Dados" para testes

#### **Seção de Métricas**
- 📊 **5 Cards Principais**:
  - **Concentração Geral** (ppm) - Ícone: 🌬️
  - **PM2.5** (µg/m³) - Ícone: ☁️
  - **PM10** (µg/m³) - Ícone: 🌫️
  - **Temperatura** (°C) - Ícone: 🌡️
  - **Umidade** (%) - Ícone: 💧

#### **Análise Preditiva**
- 📈 **Gráfico de Previsão**: 24 horas com 3 métricas
- 🎯 **Card de Qualidade**: Status da IA com descrição
- 📊 **Barras de Progresso**: Visualização das métricas

### 🔄 **Funcionalidade Interativa**

#### **Botão "Gerar Novos Dados"**
- **Localização**: Canto superior direito
- **Design**: Botão verde com ícone de refresh
- **Funcionalidade**: Gera valores aleatórios realistas

#### **Valores Gerados**
```python
# Faixas de valores aleatórios
Concentração: 50-800 ppm
PM2.5: 5-60 µg/m³
PM10: 10-120 µg/m³
Temperatura: 15-35°C
Umidade: 30-90%
```

#### **Qualidade do Ar Dinâmica**
- **🟢 Excelente**: Concentração < 200, PM2.5 < 12, PM10 < 25
- **🟡 Bom**: Concentração < 400, PM2.5 < 25, PM10 < 50
- **🟠 Moderado**: Concentração < 600, PM2.5 < 35, PM10 < 75
- **🔴 Ruim**: Valores acima dos limites

---

## 🛠️ **Tecnologias Utilizadas**

### **Backend**
- **Python 3.9+**: Linguagem principal
- **Pandas & NumPy**: Análise de dados
- **Scikit-learn**: Machine Learning (Árvore de Decisão)
- **Statsmodels**: Previsão de séries temporais
- **Paho-MQTT**: Comunicação IoT

### **Frontend**
- **Flet**: Framework de interface gráfica
- **Matplotlib**: Geração de gráficos
- **PyYAML**: Configuração do sistema

### **Hardware**
- **ESP32**: Microcontrolador principal
- **MQ-135**: Sensor de qualidade do ar
- **DHT11/22**: Sensor de temperatura e umidade

---

## 🚀 **Como Executar**

### **1. Instalação das Dependências**
```bash
cd SentinelaAI
pip install -r requirements.txt
```

### **2. Opções de Execução**

#### **A) Demonstração Interativa (Recomendado)**
```bash
python demo_simple.py
```
**Características:**
- ✅ Funciona imediatamente
- 🔄 Botão para gerar valores aleatórios
- 📊 Interface completa e responsiva
- 🎨 Design moderno

#### **B) Demonstração Avançada**
```bash
python demo_interface.py
```
**Características:**
- ⚠️ Pode ter problemas de compatibilidade
- 🎨 Interface mais avançada
- 📊 Dados simulados complexos

#### **C) Interface Real (Com Sensor)**
```bash
python main_app.py
```
**Características:**
- 🔌 Requer sensor Arduino conectado
- 📡 Comunicação MQTT ativa
- 🤖 IA treinada com dados reais

---

## 📱 **Características da Interface**

### **✅ Funcionalidades Implementadas**
- 🎨 **Design System Moderno**: Paleta de cores verde temática
- 📊 **Cards de Métricas**: Ícones, valores grandes, unidades separadas
- 📈 **Gráficos Dinâmicos**: Previsões coloridas e informativas
- 🎯 **Indicadores de Qualidade**: Cores semânticas e ícones
- 📊 **Barras de Progresso**: Visualização das métricas
- 🟢 **Status Badges**: Indicadores visuais de conexão
- 📱 **Layout Responsivo**: Adapta-se ao tamanho da tela
- 🔄 **Atualização em Tempo Real**: Interface dinâmica

### **🎨 Melhorias Visuais**
- 🌈 **Paleta de Cores**: Verde ambiental (#2E7D32, #4CAF50, #81C784)
- 📝 **Tipografia Hierárquica**: Títulos, subtítulos, corpo de texto
- 🎯 **Ícones Intuitivos**: Cada métrica tem seu ícone específico
- 📊 **Visualização Clara**: Dados organizados e fáceis de ler
- 🎨 **Elevação e Sombras**: Cards com profundidade visual

---

## 🔧 **Configuração**

### **Arquivo config.yaml**
```yaml
# Limites de qualidade do ar
air_quality_limits:
  Concentracao_Geral_PPM: 300.0
  PM2.5_ug_m3: 25.0
  PM10_ug_m3: 50.0

# Configurações MQTT
mqtt:
  broker_address: "test.mosquitto.org"
  topic: "sentinela/dados_csv"

# API externa
api:
  token: "sua_chave_aqui"
  city: "rio claro"
```

---

## 📊 **Estrutura do Projeto**

```
SentinelaAI/
├── main_app.py              # Aplicação principal
├── demo_simple.py           # Demonstração interativa
├── demo_interface.py        # Demonstração avançada
├── frontend.py              # Interface principal
├── backend.py               # Lógica e IA
├── styles.py                # Sistema de design
├── config.yaml              # Configurações
├── requirements.txt         # Dependências
├── arduino_sentinela_verde.ino/  # Código Arduino
├── README_ATUALIZADO.md     # Este arquivo
└── COMO_USAR.md            # Instruções de uso
```

---

## 🎯 **Casos de Uso**

### **1. Monitoramento Ambiental**
- **Indústrias**: Controle de emissões
- **Escolas**: Monitoramento da qualidade do ar
- **Hospitais**: Ambiente controlado
- **Escritórios**: Conforto dos funcionários

### **2. Pesquisa e Desenvolvimento**
- **Universidades**: Estudos ambientais
- **Laboratórios**: Análise de poluentes
- **Startups**: Produtos IoT ambientais

### **3. Cidades Inteligentes**
- **Sensores Urbanos**: Monitoramento da cidade
- **Alertas Públicos**: Qualidade do ar em tempo real
- **Políticas Públicas**: Base de dados para decisões

---

## 🔮 **Funcionalidades Futuras**

### **Próximas Melhorias Planejadas**
- 🌙 **Tema Escuro**: Modo noturno
- 🎬 **Animações**: Transições suaves
- 🔔 **Notificações**: Alertas visuais
- 📤 **Exportação**: Relatórios em PDF/Excel
- ⚙️ **Configuração**: Painel de personalização
- 📱 **App Mobile**: Versão para smartphones
- 🌐 **Dashboard Web**: Interface web responsiva

---

## 🎉 **Demonstração Interativa**

### **Como Testar a Interface**

1. **Execute a demonstração**:
   ```bash
   python demo_simple.py
   ```

2. **Explore a interface**:
   - Observe os cards de métricas
   - Veja o gráfico de previsão
   - Verifique a qualidade do ar

3. **Teste a interatividade**:
   - Clique no botão "Gerar Novos Dados"
   - Observe como os valores mudam
   - Veja a qualidade do ar mudar
   - Acompanhe o gráfico sendo atualizado

4. **Teste a responsividade**:
   - Redimensione a janela
   - Veja como o layout se adapta

---

## 💡 **Dicas de Uso**

### **Para Desenvolvedores**
- Use `demo_simple.py` para testar a interface
- Modifique `styles.py` para personalizar cores
- Ajuste `config.yaml` para suas necessidades
- Conecte sensores reais para dados autênticos

### **Para Usuários Finais**
- A interface se adapta automaticamente
- Os dados são atualizados em tempo real
- Use o botão para simular diferentes cenários
- Monitore a qualidade do ar continuamente

---

## 🏆 **Conquistas do Projeto**

### **✅ Implementado com Sucesso**
- 🎨 Interface moderna e profissional
- 🤖 Sistema de IA funcional
- 📊 Visualização de dados avançada
- 🔄 Interatividade completa
- 📱 Design responsivo
- 🎯 Usabilidade intuitiva

### **🌟 Diferenciais**
- **Classificação Híbrida**: IA + regras tradicionais
- **Previsão Preditiva**: 24 horas à frente
- **Interface Interativa**: Testes em tempo real
- **Design Ambiental**: Tema verde profissional
- **Arquitetura Modular**: Fácil manutenção

---

## 📞 **Suporte e Contribuição**

### **Problemas Comuns**
- **Interface não abre**: Verifique se o Python está instalado
- **Erro de módulo**: Execute `pip install -r requirements.txt`
- **Dados não atualizam**: Verifique a conexão MQTT

### **Como Contribuir**
1. Teste a interface e reporte bugs
2. Sugira melhorias visuais
3. Adicione novas funcionalidades
4. Melhore a documentação

---

## 🎊 **Conclusão**

O **Sentinela Verde** representa uma solução completa e moderna para monitoramento ambiental, combinando:

- 🔬 **Tecnologia Avançada**: IA e IoT
- 🎨 **Design Profissional**: Interface moderna
- 🔄 **Interatividade**: Testes em tempo real
- 📊 **Visualização Clara**: Dados organizados
- 🌍 **Impacto Ambiental**: Monitoramento sustentável

**O futuro do monitoramento ambiental está aqui! 🌳✨**

---

*Desenvolvido com ❤️ para um mundo mais limpo e inteligente.* 