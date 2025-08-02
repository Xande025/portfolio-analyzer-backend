from flask import Blueprint, request, jsonify
import yfinance as yf
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from src.models.portfolio import db, Asset, Portfolio, Position, PriceHistory

portfolio_bp = Blueprint('portfolio', __name__)

@portfolio_bp.route('/search-assets', methods=['GET'])
def search_assets():
    """Buscar ativos por símbolo ou nome"""
    query = request.args.get('query', '').strip()
    asset_type = request.args.get('type', 'all')  # 'stock', 'crypto', 'fund', 'all'
    
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    
    results = []
    
    try:
        # Buscar ações usando Yahoo Finance
        if asset_type in ['stock', 'all']:
            try:
                ticker = yf.Ticker(query.upper())
                info = ticker.info
                if info and 'symbol' in info:
                    results.append({
                        'symbol': info.get('symbol', query.upper()),
                        'name': info.get('longName', info.get('shortName', 'N/A')),
                        'type': 'stock',
                        'exchange': info.get('exchange', 'N/A'),
                        'currency': info.get('currency', 'USD')
                    })
            except:
                pass
        
        # Buscar criptomoedas usando CoinGecko API
        if asset_type in ['crypto', 'all']:
            try:
                crypto_url = f"https://api.coingecko.com/api/v3/search?query={query}"
                crypto_response = requests.get(crypto_url, timeout=10)
                if crypto_response.status_code == 200:
                    crypto_data = crypto_response.json()
                    for coin in crypto_data.get('coins', [])[:5]:  # Limitar a 5 resultados
                        results.append({
                            'symbol': coin.get('symbol', '').upper(),
                            'name': coin.get('name', 'N/A'),
                            'type': 'crypto',
                            'exchange': 'CoinGecko',
                            'currency': 'USD',
                            'id': coin.get('id')
                        })
            except:
                pass
        
        return jsonify({'results': results})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@portfolio_bp.route('/asset-data', methods=['GET'])
def get_asset_data():
    """Obter dados históricos de um ativo"""
    symbol = request.args.get('symbol', '').strip().upper()
    asset_type = request.args.get('type', 'stock')
    period = request.args.get('period', '1y')  # 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
    
    if not symbol:
        return jsonify({'error': 'Symbol parameter is required'}), 400
    
    try:
        if asset_type == 'stock':
            # Usar Yahoo Finance para ações
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if hist.empty:
                return jsonify({'error': 'No data found for this symbol'}), 404
            
            # Converter para formato JSON
            data = []
            for date, row in hist.iterrows():
                data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'open': float(row['Open']) if not pd.isna(row['Open']) else None,
                    'high': float(row['High']) if not pd.isna(row['High']) else None,
                    'low': float(row['Low']) if not pd.isna(row['Low']) else None,
                    'close': float(row['Close']) if not pd.isna(row['Close']) else None,
                    'volume': int(row['Volume']) if not pd.isna(row['Volume']) else None
                })
            
            # Obter informações básicas
            info = ticker.info
            asset_info = {
                'symbol': symbol,
                'name': info.get('longName', info.get('shortName', 'N/A')),
                'currency': info.get('currency', 'USD'),
                'exchange': info.get('exchange', 'N/A'),
                'current_price': info.get('regularMarketPrice', data[-1]['close'] if data else None)
            }
            
            return jsonify({
                'asset_info': asset_info,
                'historical_data': data
            })
        
        elif asset_type == 'crypto':
            # Usar CoinGecko para criptomoedas
            # Primeiro, buscar o ID da moeda
            search_url = f"https://api.coingecko.com/api/v3/search?query={symbol}"
            search_response = requests.get(search_url, timeout=10)
            
            if search_response.status_code != 200:
                return jsonify({'error': 'Failed to search cryptocurrency'}), 500
            
            search_data = search_response.json()
            coin_id = None
            
            for coin in search_data.get('coins', []):
                if coin.get('symbol', '').upper() == symbol:
                    coin_id = coin.get('id')
                    break
            
            if not coin_id:
                return jsonify({'error': 'Cryptocurrency not found'}), 404
            
            # Converter período para dias
            days_map = {
                '1d': 1, '5d': 5, '1mo': 30, '3mo': 90, 
                '6mo': 180, '1y': 365, '2y': 730, '5y': 1825
            }
            days = days_map.get(period, 365)
            
            # Obter dados históricos
            history_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
            params = {'vs_currency': 'usd', 'days': days}
            history_response = requests.get(history_url, params=params, timeout=10)
            
            if history_response.status_code != 200:
                return jsonify({'error': 'Failed to fetch cryptocurrency data'}), 500
            
            history_data = history_response.json()
            
            # Processar dados
            prices = history_data.get('prices', [])
            volumes = history_data.get('total_volumes', [])
            
            data = []
            for i, (timestamp, price) in enumerate(prices):
                date = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')
                volume = volumes[i][1] if i < len(volumes) else None
                
                data.append({
                    'date': date,
                    'open': None,  # CoinGecko não fornece OHLC para dados históricos gratuitos
                    'high': None,
                    'low': None,
                    'close': price,
                    'volume': volume
                })
            
            # Obter informações atuais
            current_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
            current_response = requests.get(current_url, timeout=10)
            
            asset_info = {
                'symbol': symbol,
                'name': symbol,
                'currency': 'USD',
                'exchange': 'CoinGecko',
                'current_price': None
            }
            
            if current_response.status_code == 200:
                current_data = current_response.json()
                asset_info.update({
                    'name': current_data.get('name', symbol),
                    'current_price': current_data.get('market_data', {}).get('current_price', {}).get('usd')
                })
            
            return jsonify({
                'asset_info': asset_info,
                'historical_data': data
            })
        
        else:
            return jsonify({'error': 'Unsupported asset type'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@portfolio_bp.route('/calculate-metrics', methods=['POST'])
def calculate_metrics():
    """Calcular métricas de risco e retorno para um portfólio"""
    data = request.get_json()
    
    if not data or 'assets' not in data:
        return jsonify({'error': 'Nenhum portfólio enviado. Envie pelo menos um ativo na lista "assets".'}), 400
    
    assets = data['assets']
    
    try:
        # Coletar dados históricos para todos os ativos
        all_prices = {}
        asset_info = {}
        ativos_invalidos = []
        ativos_sem_dados = []
        
        for asset in assets:
            symbol = asset.get('symbol', '').upper()
            asset_type = asset.get('type', 'stock')
            weight = asset.get('weight', 0)
            
            if not symbol or weight <= 0:
                ativos_invalidos.append(symbol or '(vazio)')
                continue
            
            if asset_type == 'stock':
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period='1y')
                if not hist.empty:
                    prices = hist['Close'].dropna()
                    all_prices[symbol] = prices
                    asset_info[symbol] = {
                        'name': ticker.info.get('longName', symbol),
                        'type': asset_type,
                        'weight': weight
                    }
                else:
                    ativos_sem_dados.append(symbol)
            elif asset_type == 'crypto':
                # Buscar histórico de preços no CoinGecko
                # 1. Buscar o ID da moeda
                search_url = f"https://api.coingecko.com/api/v3/search?query={symbol}"
                search_response = requests.get(search_url, timeout=10)
                if search_response.status_code != 200:
                    ativos_sem_dados.append(symbol + ' (erro CoinGecko)')
                    continue
                search_data = search_response.json()
                coin_id = None
                for coin in search_data.get('coins', []):
                    if coin.get('symbol', '').upper() == symbol:
                        coin_id = coin.get('id')
                        break
                if not coin_id:
                    ativos_sem_dados.append(symbol + ' (não encontrado CoinGecko)')
                    continue
                # 2. Buscar histórico de preços (1 ano)
                history_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
                params = {'vs_currency': 'usd', 'days': 365}
                history_response = requests.get(history_url, params=params, timeout=10)
                if history_response.status_code != 200:
                    ativos_sem_dados.append(symbol + ' (erro histórico CoinGecko)')
                    continue
                history_data = history_response.json()
                prices = history_data.get('prices', [])
                if not prices:
                    ativos_sem_dados.append(symbol + ' (sem preços CoinGecko)')
                    continue
                # Converter para pandas Series
                price_series = pd.Series(
                    [price[1] for price in prices],
                    index=[datetime.fromtimestamp(price[0]/1000) for price in prices]
                )
                price_series = price_series.dropna()
                if price_series.empty:
                    ativos_sem_dados.append(symbol + ' (sem preços CoinGecko)')
                    continue
                all_prices[symbol] = price_series
                asset_info[symbol] = {
                    'name': coin_id,
                    'type': asset_type,
                    'weight': weight
                }
        
        if ativos_invalidos:
            return jsonify({'error': f'Os seguintes ativos são inválidos ou têm peso zero: {", ".join(ativos_invalidos)}. Corrija e tente novamente.'}), 400
        if not all_prices:
            return jsonify({'error': f'Nenhum dado histórico encontrado para os ativos enviados. Ativos sem dados: {", ".join(ativos_sem_dados)}. Verifique os símbolos e tente novamente.'}), 400
        
        # Criar DataFrame com preços alinhados
        price_df = pd.DataFrame(all_prices)
        price_df = price_df.dropna()
        
        if price_df.empty:
            return jsonify({'error': 'Não foi possível alinhar os dados históricos dos ativos (datas em comum insuficientes). Tente outros ativos.'}), 400
        
        # Calcular retornos diários
        returns_df = price_df.pct_change().dropna()
        
        # Calcular métricas
        metrics = {}
        
        # Métricas individuais por ativo
        for symbol in returns_df.columns:
            returns = returns_df[symbol]
            
            # Retorno anualizado
            annual_return = (1 + returns.mean()) ** 252 - 1
            
            # Volatilidade anualizada
            volatility = returns.std() * np.sqrt(252)
            
            # Sharpe ratio (assumindo taxa livre de risco = 0)
            sharpe_ratio = annual_return / volatility if volatility > 0 else 0
            
            # Máximo drawdown
            cumulative_returns = (1 + returns).cumprod()
            rolling_max = cumulative_returns.expanding().max()
            drawdown = (cumulative_returns - rolling_max) / rolling_max
            max_drawdown = drawdown.min()
            
            metrics[symbol] = {
                'annual_return': float(annual_return),
                'volatility': float(volatility),
                'sharpe_ratio': float(sharpe_ratio),
                'max_drawdown': float(max_drawdown),
                'current_price': float(price_df[symbol].iloc[-1])
            }
        
        # Matriz de correlação
        correlation_matrix = returns_df.corr().to_dict()
        
        # Métricas do portfólio (se pesos fornecidos)
        weights = np.array([asset_info[symbol]['weight'] for symbol in returns_df.columns])
        weights = weights / weights.sum()  # Normalizar pesos
        
        # Retorno do portfólio
        portfolio_returns = (returns_df * weights).sum(axis=1)
        portfolio_annual_return = (1 + portfolio_returns.mean()) ** 252 - 1
        portfolio_volatility = portfolio_returns.std() * np.sqrt(252)
        portfolio_sharpe = portfolio_annual_return / portfolio_volatility if portfolio_volatility > 0 else 0
        
        # Máximo drawdown do portfólio
        portfolio_cumulative = (1 + portfolio_returns).cumprod()
        portfolio_rolling_max = portfolio_cumulative.expanding().max()
        portfolio_drawdown = (portfolio_cumulative - portfolio_rolling_max) / portfolio_rolling_max
        portfolio_max_drawdown = portfolio_drawdown.min()
        
        portfolio_metrics = {
            'annual_return': float(portfolio_annual_return),
            'volatility': float(portfolio_volatility),
            'sharpe_ratio': float(portfolio_sharpe),
            'max_drawdown': float(portfolio_max_drawdown)
        }
        
        return jsonify({
            'individual_metrics': metrics,
            'portfolio_metrics': portfolio_metrics,
            'correlation_matrix': correlation_matrix,
            'asset_info': asset_info
        })
    
    except Exception as e:
        import traceback
        print('ERRO AO CALCULAR MÉTRICAS:')
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@portfolio_bp.route('/portfolios', methods=['GET', 'POST'])
def handle_portfolios():
    """Listar ou criar portfólios"""
    if request.method == 'GET':
        portfolios = Portfolio.query.all()
        return jsonify([p.to_dict() for p in portfolios])
    
    elif request.method == 'POST':
        data = request.get_json()
        
        if not data or 'name' not in data:
            return jsonify({'error': 'Portfolio name is required'}), 400
        
        try:
            portfolio = Portfolio(
                name=data['name'],
                description=data.get('description', '')
            )
            
            db.session.add(portfolio)
            db.session.commit()
            
            return jsonify(portfolio.to_dict()), 201
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

@portfolio_bp.route('/portfolios/<int:portfolio_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_portfolio(portfolio_id):
    """Obter, atualizar ou deletar um portfólio específico"""
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    
    if request.method == 'GET':
        return jsonify(portfolio.to_dict())
    
    elif request.method == 'PUT':
        data = request.get_json()
        
        try:
            if 'name' in data:
                portfolio.name = data['name']
            if 'description' in data:
                portfolio.description = data['description']
            
            portfolio.updated_at = datetime.utcnow()
            db.session.commit()
            
            return jsonify(portfolio.to_dict())
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'DELETE':
        try:
            db.session.delete(portfolio)
            db.session.commit()
            return jsonify({'message': 'Portfolio deleted successfully'})
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

