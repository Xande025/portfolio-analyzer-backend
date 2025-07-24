import numpy as np
import pandas as pd
from scipy.optimize import minimize
from typing import Dict, List, Tuple, Any
import yfinance as yf
from datetime import datetime, timedelta

class PortfolioOptimizer:
    def __init__(self):
        self.risk_free_rate = 0.02  # 2% taxa livre de risco
    
    def get_efficient_frontier(self, symbols: List[str], period: str = "1y") -> Dict[str, Any]:
        """
        Calcula a fronteira eficiente para um conjunto de ativos
        """
        try:
            # Baixar dados históricos
            data = {}
            for symbol in symbols:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period=period)
                if not hist.empty:
                    data[symbol] = hist['Close'].pct_change().dropna()
            
            if not data:
                return {"error": "Não foi possível obter dados para os ativos"}
            
            # Criar DataFrame com retornos
            returns_df = pd.DataFrame(data)
            returns_df = returns_df.dropna()
            
            if returns_df.empty:
                return {"error": "Dados insuficientes para otimização"}
            
            # Calcular estatísticas
            mean_returns = returns_df.mean() * 252  # Anualizar
            cov_matrix = returns_df.cov() * 252  # Anualizar
            
            # Gerar fronteira eficiente
            num_portfolios = 50
            target_returns = np.linspace(mean_returns.min(), mean_returns.max(), num_portfolios)
            
            efficient_portfolios = []
            for target_return in target_returns:
                try:
                    weights = self._optimize_portfolio(mean_returns, cov_matrix, target_return)
                    if weights is not None:
                        portfolio_return = np.sum(weights * mean_returns)
                        portfolio_risk = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
                        sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_risk
                        
                        efficient_portfolios.append({
                            'return': portfolio_return,
                            'risk': portfolio_risk,
                            'sharpe': sharpe_ratio,
                            'weights': weights.tolist()
                        })
                except:
                    continue
            
            # Encontrar portfólio de máximo Sharpe
            max_sharpe_portfolio = self._get_max_sharpe_portfolio(mean_returns, cov_matrix)
            
            # Encontrar portfólio de mínima variância
            min_variance_portfolio = self._get_min_variance_portfolio(cov_matrix)
            
            return {
                "efficient_frontier": efficient_portfolios,
                "max_sharpe_portfolio": max_sharpe_portfolio,
                "min_variance_portfolio": min_variance_portfolio,
                "symbols": symbols,
                "mean_returns": mean_returns.to_dict(),
                "risk_free_rate": self.risk_free_rate
            }
            
        except Exception as e:
            return {"error": f"Erro na otimização: {str(e)}"}
    
    def _optimize_portfolio(self, mean_returns, cov_matrix, target_return):
        """
        Otimiza portfólio para um retorno alvo específico
        """
        num_assets = len(mean_returns)
        
        # Função objetivo: minimizar variância
        def objective(weights):
            return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        
        # Restrições
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},  # Soma dos pesos = 1
            {'type': 'eq', 'fun': lambda x: np.sum(x * mean_returns) - target_return}  # Retorno alvo
        ]
        
        # Limites (0 <= peso <= 1)
        bounds = tuple((0, 1) for _ in range(num_assets))
        
        # Pesos iniciais iguais
        initial_weights = np.array([1/num_assets] * num_assets)
        
        try:
            result = minimize(objective, initial_weights, method='SLSQP', 
                            bounds=bounds, constraints=constraints)
            
            if result.success:
                return result.x
            else:
                return None
        except:
            return None
    
    def _get_max_sharpe_portfolio(self, mean_returns, cov_matrix):
        """
        Encontra o portfólio com máximo índice Sharpe
        """
        num_assets = len(mean_returns)
        
        def objective(weights):
            portfolio_return = np.sum(weights * mean_returns)
            portfolio_risk = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
            return -(portfolio_return - self.risk_free_rate) / portfolio_risk  # Negativo para maximizar
        
        constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]
        bounds = tuple((0, 1) for _ in range(num_assets))
        initial_weights = np.array([1/num_assets] * num_assets)
        
        try:
            result = minimize(objective, initial_weights, method='SLSQP', 
                            bounds=bounds, constraints=constraints)
            
            if result.success:
                weights = result.x
                portfolio_return = np.sum(weights * mean_returns)
                portfolio_risk = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
                sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_risk
                
                return {
                    'weights': weights.tolist(),
                    'return': portfolio_return,
                    'risk': portfolio_risk,
                    'sharpe': sharpe_ratio
                }
        except:
            pass
        
        return None
    
    def _get_min_variance_portfolio(self, cov_matrix):
        """
        Encontra o portfólio de mínima variância
        """
        num_assets = len(cov_matrix)
        
        def objective(weights):
            return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        
        constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]
        bounds = tuple((0, 1) for _ in range(num_assets))
        initial_weights = np.array([1/num_assets] * num_assets)
        
        try:
            result = minimize(objective, initial_weights, method='SLSQP', 
                            bounds=bounds, constraints=constraints)
            
            if result.success:
                weights = result.x
                portfolio_risk = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
                
                return {
                    'weights': weights.tolist(),
                    'risk': portfolio_risk
                }
        except:
            pass
        
        return None
    
    def suggest_rebalancing(self, current_weights: Dict[str, float], 
                          optimal_weights: Dict[str, float], 
                          threshold: float = 0.05) -> Dict[str, Any]:
        """
        Sugere rebalanceamento baseado na diferença entre pesos atuais e ótimos
        """
        suggestions = []
        total_deviation = 0
        
        for symbol in current_weights:
            current = current_weights.get(symbol, 0)
            optimal = optimal_weights.get(symbol, 0)
            deviation = abs(current - optimal)
            total_deviation += deviation
            
            if deviation > threshold:
                action = "aumentar" if optimal > current else "diminuir"
                suggestions.append({
                    'symbol': symbol,
                    'current_weight': current,
                    'optimal_weight': optimal,
                    'deviation': deviation,
                    'action': action,
                    'change_needed': optimal - current
                })
        
        needs_rebalancing = total_deviation > threshold
        
        return {
            'needs_rebalancing': needs_rebalancing,
            'total_deviation': total_deviation,
            'suggestions': suggestions,
            'threshold': threshold
        }

