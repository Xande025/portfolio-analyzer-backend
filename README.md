# 📊 Analisador de Portfólio

Uma ferramenta completa de análise de investimentos que permite construir, otimizar e monitorar portfólios de investimento com métricas avançadas de risco e retorno.

![Analisador de Portfólio](https://img.shields.io/badge/Status-Produção-green) ![Python](https://img.shields.io/badge/Python-3.11-blue) ![React](https://img.shields.io/badge/React-18-blue) ![Flask](https://img.shields.io/badge/Flask-3.0-red)

## 🚀 Funcionalidades

### 📈 Análise de Portfólio
- **Dashboard Interativo**: Visualize métricas essenciais como retorno anual, volatilidade, índice Sharpe e máximo drawdown
- **Gráficos Avançados**: Alocação de ativos, retornos, volatilidade e matriz de correlação
- **Análise Individual**: Histórico de preços, retornos e estatísticas detalhadas de cada ativo

### 🔍 Busca de Ativos
- **Múltiplas Classes**: Ações, criptomoedas e fundos de investimento
- **Busca Inteligente**: Por símbolo ou nome da empresa
- **Dados em Tempo Real**: Preços atualizados via APIs financeiras

### 🎯 Otimização de Portfólio
- **Fronteira Eficiente**: Encontre combinações ótimas de risco e retorno
- **Máximo Sharpe**: Portfólio que maximiza o retorno ajustado ao risco
- **Análise de Eficiência**: Score de eficiência do portfólio atual
- **Sugestões de Rebalanceamento**: Recomendações inteligentes de ajustes

### 🔔 Alertas e Monitoramento
- **Alertas de Preço**: Notificações quando ativos atingem preços-alvo
- **Alertas de Performance**: Monitoramento de métricas do portfólio
- **Monitoramento em Tempo Real**: Acompanhe mudanças de preços instantaneamente
- **Histórico de Alertas**: Visualize alertas acionados recentemente

### 🎨 Interface Moderna
- **Tema Escuro/Claro**: Alternância suave entre temas
- **Design Responsivo**: Otimizado para desktop e mobile
- **Animações Suaves**: Transições e efeitos visuais elegantes
- **Navegação Intuitiva**: Interface limpa e fácil de usar

## 🛠️ Tecnologias

### Backend
- **Python 3.11**: Linguagem principal
- **Flask**: Framework web
- **yfinance**: Dados financeiros em tempo real
- **pandas/numpy**: Análise de dados
- **scipy**: Otimização matemática

### Frontend
- **React 18**: Interface de usuário
- **Vite**: Build tool moderno
- **Tailwind CSS**: Estilização
- **Recharts**: Gráficos interativos
- **Lucide React**: Ícones

### Dados
- **Yahoo Finance**: Preços de ações e criptomoedas
- **APIs Financeiras**: Dados em tempo real
- **Armazenamento Local**: Alertas e configurações

## 📦 Instalação

### Pré-requisitos
- Python 3.11+
- Node.js 18+
- npm ou pnpm

### Backend (Flask)
```bash
cd portfolio-analyzer
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows
pip install -r requirements.txt
python src/main.py
```

### Frontend (React)
```bash
cd portfolio-frontend
npm install  # ou pnpm install
npm run build  # ou pnpm run build
```

### Deploy Completo
```bash
# Construir frontend
cd portfolio-frontend
pnpm run build

# Copiar para Flask
cp -r dist/* ../portfolio-analyzer/src/static/

# Iniciar servidor
cd ../portfolio-analyzer
source venv/bin/activate
python src/main.py
```

## 🚀 Uso Rápido

1. **Adicione Ativos**: Use a busca para encontrar ações ou criptomoedas
2. **Construa Portfólio**: Defina pesos para cada ativo
3. **Analise Métricas**: Visualize retorno, risco e correlações
4. **Otimize**: Use a ferramenta de otimização para encontrar alocação ideal
5. **Configure Alertas**: Monitore preços e performance automaticamente

## 📊 Exemplos de Uso

### Portfólio Diversificado
```
AAPL (Apple): 30%
MSFT (Microsoft): 25%
BTC (Bitcoin): 20%
GOOGL (Google): 15%
TSLA (Tesla): 10%
```

### Métricas Calculadas
- **Retorno Anual**: 18.5%
- **Volatilidade**: 22.3%
- **Índice Sharpe**: 0.83
- **Máximo Drawdown**: -15.2%

## 🔧 Configuração

### Variáveis de Ambiente
```bash
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=sua_chave_secreta
```

### Personalização
- Modifique `src/config.py` para ajustar configurações
- Customize temas em `portfolio-frontend/src/App.css`
- Adicione novos provedores de dados em `src/services/`

## 📚 Documentação

- [Guia do Usuário](docs/USER_GUIDE.md)
- [Documentação da API](docs/API_DOCS.md)
- [Guia de Desenvolvimento](docs/DEVELOPMENT.md)

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- [Yahoo Finance](https://finance.yahoo.com/) pelos dados financeiros
- [React](https://reactjs.org/) pela framework frontend
- [Flask](https://flask.palletsprojects.com/) pela framework backend
- [Tailwind CSS](https://tailwindcss.com/) pelo sistema de design

## 📞 Suporte

Para suporte, abra uma issue no GitHub ou entre em contato através do email: suporte@analisador-portfolio.com

---

**Desenvolvido com ❤️ para investidores inteligentes**

