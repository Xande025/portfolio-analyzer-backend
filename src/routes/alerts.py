from flask import Blueprint, request, jsonify
from services.alerts import AlertManager

alerts_bp = Blueprint('alerts', __name__)
alert_manager = AlertManager()

@alerts_bp.route('/api/alerts/price', methods=['POST'])
def create_price_alert():
    """
    Cria um alerta de preço para um ativo
    """
    try:
        data = request.get_json()
        symbol = data.get('symbol', '').upper()
        target_price = data.get('target_price')
        condition = data.get('condition', 'above')  # 'above' ou 'below'
        
        if not symbol or target_price is None:
            return jsonify({'error': 'Símbolo e preço alvo são obrigatórios'}), 400
        
        if condition not in ['above', 'below']:
            return jsonify({'error': 'Condição deve ser "above" ou "below"'}), 400
        
        result = alert_manager.create_price_alert(symbol, float(target_price), condition)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'error': f'Erro ao criar alerta: {str(e)}'}), 500

@alerts_bp.route('/api/alerts/performance', methods=['POST'])
def create_performance_alert():
    """
    Cria um alerta de performance para um portfólio
    """
    try:
        data = request.get_json()
        portfolio_id = data.get('portfolio_id', 'default')
        metric = data.get('metric')  # 'return', 'sharpe', 'drawdown'
        threshold = data.get('threshold')
        condition = data.get('condition', 'below')  # 'above' ou 'below'
        
        if not metric or threshold is None:
            return jsonify({'error': 'Métrica e limite são obrigatórios'}), 400
        
        if metric not in ['return', 'sharpe', 'drawdown', 'volatility']:
            return jsonify({'error': 'Métrica inválida'}), 400
        
        if condition not in ['above', 'below']:
            return jsonify({'error': 'Condição deve ser "above" ou "below"'}), 400
        
        result = alert_manager.create_performance_alert(
            portfolio_id, metric, float(threshold), condition
        )
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'error': f'Erro ao criar alerta: {str(e)}'}), 500

@alerts_bp.route('/api/alerts/active', methods=['GET'])
def get_active_alerts():
    """
    Retorna todos os alertas ativos
    """
    try:
        alerts = alert_manager.get_active_alerts()
        return jsonify(alerts)
        
    except Exception as e:
        return jsonify({'error': f'Erro ao obter alertas: {str(e)}'}), 500

@alerts_bp.route('/api/alerts/triggered', methods=['GET'])
def get_triggered_alerts():
    """
    Retorna alertas acionados recentemente
    """
    try:
        days = request.args.get('days', 7, type=int)
        alerts = alert_manager.get_triggered_alerts(days)
        return jsonify(alerts)
        
    except Exception as e:
        return jsonify({'error': f'Erro ao obter alertas: {str(e)}'}), 500

@alerts_bp.route('/api/alerts/<alert_id>', methods=['DELETE'])
def delete_alert(alert_id):
    """
    Remove um alerta específico
    """
    try:
        alert_type = request.args.get('type', 'price')
        result = alert_manager.delete_alert(alert_id, alert_type)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'error': f'Erro ao remover alerta: {str(e)}'}), 500

@alerts_bp.route('/api/alerts/check', methods=['POST'])
def check_alerts():
    """
    Verifica manualmente todos os alertas
    """
    try:
        triggered_alerts = alert_manager.check_price_alerts()
        return jsonify({
            'triggered_alerts': triggered_alerts,
            'count': len(triggered_alerts)
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro ao verificar alertas: {str(e)}'}), 500

@alerts_bp.route('/api/monitoring/portfolio', methods=['POST'])
def monitor_portfolio():
    """
    Monitora performance atual do portfólio
    """
    try:
        data = request.get_json()
        assets = data.get('assets', [])
        
        if not assets:
            return jsonify({'error': 'Lista de ativos é obrigatória'}), 400
        
        symbols = [asset['symbol'] for asset in assets]
        monitoring_data = alert_manager.get_portfolio_monitoring(symbols)
        
        return jsonify(monitoring_data)
        
    except Exception as e:
        return jsonify({'error': f'Erro no monitoramento: {str(e)}'}), 500

@alerts_bp.route('/api/alerts/summary', methods=['GET'])
def get_alerts_summary():
    """
    Retorna resumo de todos os alertas
    """
    try:
        active_alerts = alert_manager.get_active_alerts()
        triggered_alerts = alert_manager.get_triggered_alerts(7)
        
        summary = {
            'active_count': active_alerts['total_active'],
            'triggered_count': triggered_alerts['total_triggered'],
            'active_price_alerts': len(active_alerts['price_alerts']),
            'active_performance_alerts': len(active_alerts['performance_alerts']),
            'recent_triggered': triggered_alerts['total_triggered'],
            'status': 'healthy' if active_alerts['total_active'] > 0 else 'no_alerts'
        }
        
        return jsonify(summary)
        
    except Exception as e:
        return jsonify({'error': f'Erro ao obter resumo: {str(e)}'}), 500

