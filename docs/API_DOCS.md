# 🔌 Documentação da API - Analisador de Portfólio

Esta documentação descreve todas as APIs REST disponíveis no backend do Analisador de Portfólio.

## 📋 Visão Geral

- **Base URL**: `http://localhost:5000/api`
- **Formato**: JSON
- **Autenticação**: Não requerida (versão atual)
- **CORS**: Habilitado para desenvolvimento

## 📊 APIs de Portfólio

### Buscar Ativos
Busca ativos financeiros por símbolo ou nome.

```http
GET /api/search?query={query}&type={type}
```

#### Parâmetros
- `query` (string, obrigatório): Símbolo ou nome do ativo
- `type` (string, opcional): Tipo do ativo (`stock`, `crypto`, `fund`)

#### Resposta
```json
{
  "results": [
    {
      "symbol": "AAPL",
      "name": "Apple Inc.",
      "type": "stock",
      "exchange": "NASDAQ",
      "currency": "USD"
    }
  ],
  "count": 1
}
```

### Calcular Métricas do Portfólio
Calcula métricas de risco e retorno para um portfólio.

```http
POST /api/calculate-metrics
```

#### Body
```json
{
  "assets": [
    {
      "symbol": "AAPL",
      "weight": 50,
      "name": "Apple Inc.",
      "type": "stock"
    },
    {
      "symbol": "BTC-USD",
      "weight": 50,
      "name": "Bitcoin",
      "type": "crypto"
    }
  ],
  "period": "1y"
}
```

#### Resposta
```json
{
  "portfolio_return": 0.1845,
  "portfolio_volatility": 0.2234,
  "sharpe_ratio": 0.8267,
  "max_drawdown": -0.1523,
  "individual_returns": {
    "AAPL": 0.2283,
    "BTC-USD": 0.1407
  },
  "individual_volatilities": {
    "AAPL": 0.2156,
    "BTC-USD": 0.4512
  },
  "correlation_matrix": {
    "AAPL": {"AAPL": 1.0, "BTC-USD": 0.1234},
    "BTC-USD": {"AAPL": 0.1234, "BTC-USD": 1.0}
  }
}
```

### Obter Dados Históricos
Retorna dados históricos de preços para um ativo.

```http
GET /api/asset-data/{symbol}?period={period}&interval={interval}
```

#### Parâmetros
- `symbol` (string): Símbolo do ativo
- `period` (string, opcional): Período (`1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max`)
- `interval` (string, opcional): Intervalo (`1m`, `2m`, `5m`, `15m`, `30m`, `60m`, `90m`, `1h`, `1d`, `5d`, `1wk`, `1mo`, `3mo`)

#### Resposta
```json
{
  "symbol": "AAPL",
  "data": [
    {
      "date": "2024-01-01",
      "open": 185.64,
      "high": 186.95,
      "low": 185.01,
      "close": 186.38,
      "volume": 54686900,
      "returns": 0.0234
    }
  ],
  "info": {
    "name": "Apple Inc.",
    "sector": "Technology",
    "market_cap": 2876543210000
  }
}
```

## 🎯 APIs de Otimização

### Otimizar Portfólio
Calcula a fronteira eficiente e portfólio ótimo.

```http
POST /api/optimize-portfolio
```

#### Body
```json
{
  "symbols": ["AAPL", "MSFT", "BTC-USD"],
  "period": "1y"
}
```

#### Resposta
```json
{
  "efficient_frontier": [
    {
      "return": 0.15,
      "risk": 0.18,
      "sharpe": 0.72,
      "weights": [0.4, 0.3, 0.3]
    }
  ],
  "max_sharpe_portfolio": {
    "weights": [0.35, 0.45, 0.20],
    "return": 0.1845,
    "risk": 0.1923,
    "sharpe": 0.8567
  },
  "min_variance_portfolio": {
    "weights": [0.6, 0.4, 0.0],
    "risk": 0.1456
  },
  "symbols": ["AAPL", "MSFT", "BTC-USD"],
  "mean_returns": {
    "AAPL": 0.2283,
    "MSFT": 0.1967,
    "BTC-USD": 0.1407
  },
  "risk_free_rate": 0.02
}
```

### Sugerir Rebalanceamento
Sugere ajustes no portfólio baseado em pesos ótimos.

```http
POST /api/suggest-rebalancing
```

#### Body
```json
{
  "current_weights": {
    "AAPL": 0.5,
    "MSFT": 0.3,
    "BTC-USD": 0.2
  },
  "optimal_weights": {
    "AAPL": 0.35,
    "MSFT": 0.45,
    "BTC-USD": 0.20
  },
  "threshold": 0.05
}
```

#### Resposta
```json
{
  "needs_rebalancing": true,
  "total_deviation": 0.30,
  "suggestions": [
    {
      "symbol": "AAPL",
      "current_weight": 0.5,
      "optimal_weight": 0.35,
      "deviation": 0.15,
      "action": "diminuir",
      "change_needed": -0.15
    },
    {
      "symbol": "MSFT",
      "current_weight": 0.3,
      "optimal_weight": 0.45,
      "deviation": 0.15,
      "action": "aumentar",
      "change_needed": 0.15
    }
  ],
  "threshold": 0.05
}
```

### Analisar Eficiência do Portfólio
Analisa a eficiência do portfólio atual comparado ao ótimo.

```http
POST /api/portfolio-efficiency
```

#### Body
```json
{
  "assets": [
    {
      "symbol": "AAPL",
      "weight": 50,
      "name": "Apple Inc.",
      "type": "stock"
    }
  ]
}
```

#### Resposta
```json
{
  "current_portfolio": {
    "return": 0.1845,
    "weights": {"AAPL": 0.5, "MSFT": 0.5},
    "efficiency_score": 0.85
  },
  "optimization_data": {
    "max_sharpe_portfolio": {...},
    "efficient_frontier": [...]
  },
  "recommendations": {
    "efficiency_rating": "Boa",
    "should_rebalance": false
  }
}
```

## 🔔 APIs de Alertas

### Criar Alerta de Preço
Cria um alerta para quando um ativo atingir determinado preço.

```http
POST /api/alerts/price
```

#### Body
```json
{
  "symbol": "AAPL",
  "target_price": 200.00,
  "condition": "above"
}
```

#### Resposta
```json
{
  "success": true,
  "alert": {
    "id": "uuid-string",
    "symbol": "AAPL",
    "target_price": 200.00,
    "condition": "above",
    "current_price": 186.38,
    "created_at": "2024-01-15T10:30:00Z",
    "triggered": false
  },
  "message": "Alerta criado para AAPL quando preço estiver above 200.0"
}
```

### Criar Alerta de Performance
Cria um alerta para métricas do portfólio.

```http
POST /api/alerts/performance
```

#### Body
```json
{
  "portfolio_id": "default",
  "metric": "return",
  "threshold": 15.0,
  "condition": "below"
}
```

#### Resposta
```json
{
  "success": true,
  "alert": {
    "id": "uuid-string",
    "portfolio_id": "default",
    "metric": "return",
    "threshold": 15.0,
    "condition": "below",
    "current_value": 0.0,
    "created_at": "2024-01-15T10:30:00Z",
    "triggered": false
  },
  "message": "Alerta de return criado para quando estiver below 15.0"
}
```

### Listar Alertas Ativos
Retorna todos os alertas que ainda não foram acionados.

```http
GET /api/alerts/active
```

#### Resposta
```json
{
  "price_alerts": [
    {
      "id": "uuid-string",
      "symbol": "AAPL",
      "target_price": 200.00,
      "condition": "above",
      "current_price": 186.38,
      "created_at": "2024-01-15T10:30:00Z",
      "triggered": false
    }
  ],
  "performance_alerts": [],
  "total_active": 1
}
```

### Listar Alertas Acionados
Retorna alertas acionados nos últimos N dias.

```http
GET /api/alerts/triggered?days=7
```

#### Resposta
```json
{
  "price_alerts": [
    {
      "id": "uuid-string",
      "symbol": "TSLA",
      "target_price": 250.00,
      "condition": "above",
      "current_price": 251.45,
      "created_at": "2024-01-10T10:30:00Z",
      "triggered": true,
      "triggered_at": "2024-01-14T15:45:00Z"
    }
  ],
  "performance_alerts": [],
  "total_triggered": 1,
  "period_days": 7
}
```

### Verificar Alertas
Verifica manualmente todos os alertas de preço.

```http
POST /api/alerts/check
```

#### Resposta
```json
{
  "triggered_alerts": [
    {
      "id": "uuid-string",
      "symbol": "AAPL",
      "target_price": 200.00,
      "current_price": 201.50,
      "triggered_at": "2024-01-15T16:20:00Z"
    }
  ],
  "count": 1
}
```

### Remover Alerta
Remove um alerta específico.

```http
DELETE /api/alerts/{alert_id}?type=price
```

#### Resposta
```json
{
  "success": true,
  "message": "Alerta removido com sucesso"
}
```

### Monitorar Portfólio
Monitora performance atual dos ativos do portfólio.

```http
POST /api/monitoring/portfolio
```

#### Body
```json
{
  "assets": [
    {"symbol": "AAPL"},
    {"symbol": "MSFT"}
  ]
}
```

#### Resposta
```json
{
  "timestamp": "2024-01-15T16:30:00Z",
  "assets": {
    "AAPL": {
      "current_price": 186.38,
      "previous_price": 185.64,
      "change_percent": 0.40,
      "volume": 54686900,
      "status": "up"
    },
    "MSFT": {
      "current_price": 384.52,
      "previous_price": 382.15,
      "change_percent": 0.62,
      "volume": 23456789,
      "status": "up"
    }
  },
  "alerts_triggered": 0,
  "recent_alerts": []
}
```

### Resumo de Alertas
Retorna estatísticas gerais dos alertas.

```http
GET /api/alerts/summary
```

#### Resposta
```json
{
  "active_count": 5,
  "triggered_count": 2,
  "active_price_alerts": 4,
  "active_performance_alerts": 1,
  "recent_triggered": 2,
  "status": "healthy"
}
```

## 🔧 Códigos de Status

### Sucesso
- `200 OK`: Requisição bem-sucedida
- `201 Created`: Recurso criado com sucesso

### Erro do Cliente
- `400 Bad Request`: Parâmetros inválidos
- `404 Not Found`: Recurso não encontrado
- `422 Unprocessable Entity`: Dados inválidos

### Erro do Servidor
- `500 Internal Server Error`: Erro interno do servidor

## 📝 Exemplos de Uso

### Python
```python
import requests

# Buscar ativo
response = requests.get('http://localhost:5000/api/search?query=AAPL')
data = response.json()

# Calcular métricas
portfolio = {
    "assets": [
        {"symbol": "AAPL", "weight": 60, "name": "Apple", "type": "stock"},
        {"symbol": "BTC-USD", "weight": 40, "name": "Bitcoin", "type": "crypto"}
    ]
}
response = requests.post('http://localhost:5000/api/calculate-metrics', json=portfolio)
metrics = response.json()

# Criar alerta
alert = {
    "symbol": "AAPL",
    "target_price": 200.0,
    "condition": "above"
}
response = requests.post('http://localhost:5000/api/alerts/price', json=alert)
```

### JavaScript
```javascript
// Buscar ativo
const searchResponse = await fetch('http://localhost:5000/api/search?query=AAPL');
const searchData = await searchResponse.json();

// Calcular métricas
const portfolio = {
  assets: [
    {symbol: "AAPL", weight: 60, name: "Apple", type: "stock"},
    {symbol: "BTC-USD", weight: 40, name: "Bitcoin", type: "crypto"}
  ]
};

const metricsResponse = await fetch('http://localhost:5000/api/calculate-metrics', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify(portfolio)
});
const metrics = await metricsResponse.json();

// Criar alerta
const alert = {
  symbol: "AAPL",
  target_price: 200.0,
  condition: "above"
};

const alertResponse = await fetch('http://localhost:5000/api/alerts/price', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify(alert)
});
```

## 🚀 Rate Limiting

Atualmente não há rate limiting implementado, mas recomenda-se:
- Máximo 100 requisições por minuto por IP
- Cache de dados quando possível
- Uso responsável das APIs de dados em tempo real

## 🔒 Segurança

### Versão Atual
- Sem autenticação requerida
- CORS habilitado para desenvolvimento
- Validação básica de entrada

### Produção (Recomendado)
- Implementar autenticação JWT
- Rate limiting por usuário
- Validação rigorosa de entrada
- HTTPS obrigatório

---

**Para mais informações, consulte o [Guia do Usuário](USER_GUIDE.md) ou abra uma issue no GitHub.**

