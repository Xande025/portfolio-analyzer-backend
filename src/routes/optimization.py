from flask import Blueprint, request, jsonify
from services.optimization import PortfolioOptimizer

optimization_bp = Blueprint('optimization', __name__)
optimizer = PortfolioOptimizer()

@optimization_bp.route('/api/optimize-portfolio', methods=['POST'])
def optimize_portfolio():
    """
    Otimiza um portfólio e retorna a fronteira eficiente
    """
    try:
        data = request.get_json()
        symbols = data.get('symbols', [])
        period = data.get('period', '1y')
        
        if not symbols:
            return jsonify({'error': 'Lista de símbolos é obrigatória'}), 400
        
        # Extrair apenas os símbolos dos ativos
        if isinstance(symbols[0], dict):
            symbols = [asset['symbol'] for asset in symbols]
        
        result = optimizer.get_efficient_frontier(symbols, period)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Erro na otimização: {str(e)}'}), 500

@optimization_bp.route('/api/suggest-rebalancing', methods=['POST'])
def suggest_rebalancing():
    """
    Sugere rebalanceamento baseado em pesos ótimos
    """
    try:
        data = request.get_json()
        current_weights = data.get('current_weights', {})
        optimal_weights = data.get('optimal_weights', {})
        threshold = data.get('threshold', 0.05)
        
        if not current_weights or not optimal_weights:
            return jsonify({'error': 'Pesos atuais e ótimos são obrigatórios'}), 400
        
        suggestions = optimizer.suggest_rebalancing(
            current_weights, optimal_weights, threshold
        )
        
        return jsonify(suggestions)
        
    except Exception as e:
        return jsonify({'error': f'Erro nas sugestões: {str(e)}'}), 500

@optimization_bp.route('/api/portfolio-efficiency', methods=['POST'])
def analyze_portfolio_efficiency():
    """
    Analisa a eficiência do portfólio atual
    """
    try:
        data = request.get_json()
        assets = data.get('assets', [])
        
        if not assets:
            return jsonify({'error': 'Lista de ativos é obrigatória'}), 400
        
        symbols = [asset['symbol'] for asset in assets]
        current_weights = {asset['symbol']: asset['weight']/100 for asset in assets}
        
        # Obter fronteira eficiente
        optimization_result = optimizer.get_efficient_frontier(symbols)
        
        if 'error' in optimization_result:
            return jsonify(optimization_result), 400
        
        # Calcular métricas do portfólio atual
        mean_returns = optimization_result['mean_returns']
        current_return = sum(current_weights[symbol] * mean_returns[symbol] 
                           for symbol in symbols)
        
        # Comparar com portfólio ótimo
        max_sharpe = optimization_result.get('max_sharpe_portfolio')
        efficiency_score = 0
        
        if max_sharpe:
            optimal_sharpe = max_sharpe['sharpe']
            current_risk = sum(current_weights[symbol] * mean_returns[symbol] 
                             for symbol in symbols)  # Simplificado
            current_sharpe = (current_return - optimizer.risk_free_rate) / max(current_risk, 0.01)
            efficiency_score = min(current_sharpe / optimal_sharpe, 1.0) if optimal_sharpe > 0 else 0
        
        return jsonify({
            'current_portfolio': {
                'return': current_return,
                'weights': current_weights,
                'efficiency_score': efficiency_score
            },
            'optimization_data': optimization_result,
            'recommendations': {
                'efficiency_rating': 'Excelente' if efficiency_score > 0.9 
                                   else 'Boa' if efficiency_score > 0.7 
                                   else 'Regular' if efficiency_score > 0.5 
                                   else 'Precisa melhorar',
                'should_rebalance': efficiency_score < 0.8
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro na análise: {str(e)}'}), 500

