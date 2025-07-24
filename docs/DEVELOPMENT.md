# 🛠️ Guia de Desenvolvimento - Analisador de Portfólio

Este guia é destinado a desenvolvedores que desejam contribuir, modificar ou estender o Analisador de Portfólio.

## 🏗️ Arquitetura do Sistema

### Visão Geral
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Dados         │
│   (React)       │◄──►│   (Flask)       │◄──►│   (APIs)        │
│                 │    │                 │    │                 │
│ • Dashboard     │    │ • REST APIs     │    │ • Yahoo Finance │
│ • Otimização    │    │ • Cálculos      │    │ • Dados Reais   │
│ • Alertas       │    │ • Persistência  │    │ • Cache Local   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Estrutura de Diretórios
```
portfolio-analyzer/
├── src/                    # Backend Flask
│   ├── main.py            # Aplicação principal
│   ├── models/            # Modelos de dados
│   ├── routes/            # Endpoints da API
│   ├── services/          # Lógica de negócio
│   └── static/            # Frontend buildado
├── docs/                  # Documentação
├── data/                  # Dados persistidos
├── requirements.txt       # Dependências Python
└── README.md

portfolio-frontend/
├── src/
│   ├── components/        # Componentes React
│   ├── contexts/          # Context providers
│   ├── hooks/             # Custom hooks
│   └── App.jsx           # Aplicação principal
├── public/               # Arquivos estáticos
├── package.json          # Dependências Node.js
└── vite.config.js        # Configuração Vite
```

## 🔧 Configuração do Ambiente

### Pré-requisitos
- Python 3.11+
- Node.js 18+
- Git
- Editor de código (VS Code recomendado)

### Setup Inicial
```bash
# Clonar repositório
git clone <repository-url>
cd portfolio-analyzer

# Backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# Frontend
cd ../portfolio-frontend
npm install
```

### Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto:
```bash
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=dev-secret-key
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

## 🏃‍♂️ Executando em Desenvolvimento

### Backend (Flask)
```bash
cd portfolio-analyzer
source venv/bin/activate
python src/main.py
# Servidor rodando em http://localhost:5000
```

### Frontend (React)
```bash
cd portfolio-frontend
npm run dev
# Servidor rodando em http://localhost:5173
```

### Build de Produção
```bash
# Frontend
cd portfolio-frontend
npm run build

# Copiar para Flask
cp -r dist/* ../portfolio-analyzer/src/static/

# Executar Flask
cd ../portfolio-analyzer
python src/main.py
```

## 📁 Estrutura do Código

### Backend (Flask)

#### main.py
Ponto de entrada da aplicação Flask.
```python
from flask import Flask
from flask_cors import CORS
from routes.portfolio import portfolio_bp
from routes.optimization import optimization_bp
from routes.alerts import alerts_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(portfolio_bp)
app.register_blueprint(optimization_bp)
app.register_blueprint(alerts_bp)
```

#### Models (models/)
Estruturas de dados e classes de domínio.
```python
# models/portfolio.py
@dataclass
class Asset:
    symbol: str
    name: str
    type: str
    weight: float = 0.0

@dataclass
class Portfolio:
    assets: List[Asset]
    metrics: Optional[Dict] = None
```

#### Routes (routes/)
Endpoints da API REST.
```python
# routes/portfolio.py
@portfolio_bp.route('/api/search', methods=['GET'])
def search_assets():
    query = request.args.get('query')
    # Lógica de busca
    return jsonify(results)
```

#### Services (services/)
Lógica de negócio e cálculos.
```python
# services/portfolio_calculator.py
class PortfolioCalculator:
    def calculate_metrics(self, assets, period='1y'):
        # Cálculos de métricas
        return metrics
```

### Frontend (React)

#### Componentes (components/)
Componentes reutilizáveis da interface.
```jsx
// components/Dashboard.jsx
const Dashboard = ({ selectedAssets, setSelectedAssets }) => {
  const [metrics, setMetrics] = useState(null)
  
  useEffect(() => {
    if (selectedAssets.length > 0) {
      calculateMetrics()
    }
  }, [selectedAssets])
  
  return (
    <div className="dashboard">
      {/* Interface do dashboard */}
    </div>
  )
}
```

#### Contexts (contexts/)
Gerenciamento de estado global.
```jsx
// contexts/ThemeContext.jsx
export const ThemeProvider = ({ children }) => {
  const [isDark, setIsDark] = useState(false)
  
  const toggleTheme = () => setIsDark(!isDark)
  
  return (
    <ThemeContext.Provider value={{ isDark, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}
```

## 🧪 Testes

### Backend
```bash
# Instalar dependências de teste
pip install pytest pytest-flask

# Executar testes
pytest tests/
```

### Frontend
```bash
# Instalar dependências de teste
npm install --save-dev @testing-library/react vitest

# Executar testes
npm run test
```

### Estrutura de Testes
```
tests/
├── backend/
│   ├── test_portfolio.py
│   ├── test_optimization.py
│   └── test_alerts.py
└── frontend/
    ├── Dashboard.test.jsx
    ├── OptimizationPanel.test.jsx
    └── AlertsPanel.test.jsx
```

## 📊 Adicionando Novas Funcionalidades

### Nova Métrica de Portfólio

1. **Backend**: Adicionar cálculo em `services/portfolio_calculator.py`
```python
def calculate_new_metric(self, returns_data):
    # Implementar cálculo
    return new_metric_value
```

2. **API**: Incluir na resposta de `/api/calculate-metrics`
```python
metrics['new_metric'] = calculator.calculate_new_metric(returns_data)
```

3. **Frontend**: Exibir no Dashboard
```jsx
<div className="metric-card">
  <h3>Nova Métrica</h3>
  <span>{metrics.new_metric}</span>
</div>
```

### Novo Tipo de Alerta

1. **Backend**: Estender `services/alerts.py`
```python
@dataclass
class NewAlertType:
    id: str
    condition: str
    threshold: float
    # Novos campos específicos
```

2. **API**: Adicionar endpoint em `routes/alerts.py`
```python
@alerts_bp.route('/api/alerts/new-type', methods=['POST'])
def create_new_alert():
    # Implementar criação
    return jsonify(result)
```

3. **Frontend**: Adicionar interface em `AlertsPanel.jsx`
```jsx
const NewAlertForm = () => {
  // Formulário para novo tipo de alerta
}
```

### Nova Fonte de Dados

1. **Backend**: Criar serviço em `services/data_providers/`
```python
class NewDataProvider:
    def get_asset_data(self, symbol, period):
        # Implementar integração
        return data
```

2. **Integração**: Adicionar em `services/portfolio_calculator.py`
```python
def get_data_from_multiple_sources(self, symbol):
    # Tentar múltiplas fontes
    return consolidated_data
```

## 🎨 Estilização e UI

### Tailwind CSS
O projeto usa Tailwind CSS para estilização. Classes principais:

```css
/* Tema escuro/claro */
.dark:bg-gray-800
.bg-white

/* Animações */
.transition-all
.duration-300
.hover:scale-105

/* Layout responsivo */
.grid
.md:grid-cols-2
.lg:grid-cols-3
```

### Componentes UI
Baseados em shadcn/ui:
- `Card`, `CardHeader`, `CardContent`
- `Button`, `Input`, `Select`
- `Badge`, `Progress`

### Adicionando Novos Estilos
```css
/* App.css */
.custom-animation {
  @apply transition-all duration-500 ease-in-out;
}

.custom-gradient {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

## 📈 Performance e Otimização

### Backend
- **Cache**: Implementar cache Redis para dados frequentes
- **Async**: Usar async/await para operações I/O
- **Database**: Migrar para PostgreSQL em produção

### Frontend
- **Code Splitting**: Usar React.lazy() para componentes grandes
- **Memoization**: React.memo() e useMemo() para cálculos pesados
- **Bundle Size**: Analisar com `npm run build -- --analyze`

### Exemplo de Otimização
```jsx
// Memoização de cálculos pesados
const expensiveCalculation = useMemo(() => {
  return calculateComplexMetrics(selectedAssets)
}, [selectedAssets])

// Lazy loading de componentes
const OptimizationPanel = lazy(() => import('./OptimizationPanel'))
```

## 🚀 Deploy e Produção

### Preparação para Produção
1. **Configurações**: Usar variáveis de ambiente
2. **Segurança**: Implementar autenticação
3. **Monitoring**: Adicionar logs e métricas
4. **HTTPS**: Configurar certificados SSL

### Docker (Opcional)
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "src/main.py"]
```

### CI/CD Pipeline
```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest
      - name: Deploy
        run: # Deploy script
```

## 🐛 Debugging

### Backend
```python
# Adicionar logs
import logging
logging.basicConfig(level=logging.DEBUG)

# Debug específico
@portfolio_bp.route('/api/debug')
def debug_endpoint():
    return jsonify({
        'assets': session.get('assets', []),
        'metrics': session.get('metrics', {})
    })
```

### Frontend
```jsx
// React Developer Tools
// Console logs para debugging
console.log('Selected assets:', selectedAssets)

// Error boundaries
class ErrorBoundary extends React.Component {
  componentDidCatch(error, errorInfo) {
    console.error('Error caught:', error, errorInfo)
  }
}
```

## 📝 Convenções de Código

### Python (Backend)
- PEP 8 para formatação
- Type hints obrigatórios
- Docstrings para funções públicas
- Nomes descritivos para variáveis

```python
def calculate_portfolio_metrics(
    assets: List[Asset], 
    period: str = "1y"
) -> Dict[str, float]:
    """
    Calcula métricas de risco e retorno para um portfólio.
    
    Args:
        assets: Lista de ativos do portfólio
        period: Período para análise histórica
        
    Returns:
        Dicionário com métricas calculadas
    """
    # Implementação
```

### JavaScript (Frontend)
- ESLint + Prettier para formatação
- Componentes funcionais com hooks
- Props tipadas com PropTypes
- Nomes descritivos para funções

```jsx
const PortfolioMetrics = ({ assets, onMetricsChange }) => {
  const [loading, setLoading] = useState(false)
  
  const calculateMetrics = useCallback(async () => {
    setLoading(true)
    try {
      const metrics = await fetchMetrics(assets)
      onMetricsChange(metrics)
    } catch (error) {
      console.error('Error calculating metrics:', error)
    } finally {
      setLoading(false)
    }
  }, [assets, onMetricsChange])
  
  return (
    // JSX
  )
}
```

## 🤝 Contribuindo

### Processo de Contribuição
1. Fork o repositório
2. Crie uma branch para sua feature
3. Implemente as mudanças
4. Adicione testes
5. Execute todos os testes
6. Faça commit com mensagem descritiva
7. Abra um Pull Request

### Mensagens de Commit
```bash
feat: adicionar otimização de portfólio
fix: corrigir cálculo de correlação
docs: atualizar documentação da API
style: formatar código com prettier
refactor: reorganizar estrutura de componentes
test: adicionar testes para alertas
```

## 📞 Suporte para Desenvolvedores

- **Issues**: Use GitHub Issues para bugs e features
- **Discussões**: GitHub Discussions para dúvidas
- **Email**: dev@analisador-portfolio.com
- **Discord**: [Link do servidor] (se disponível)

---

**Happy coding! 🚀**

