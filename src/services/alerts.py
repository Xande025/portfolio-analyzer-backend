import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import yfinance as yf
from dataclasses import dataclass, asdict
import uuid

@dataclass
class PriceAlert:
    id: str
    symbol: str
    target_price: float
    condition: str  # 'above' ou 'below'
    current_price: float
    created_at: str
    triggered: bool = False
    triggered_at: Optional[str] = None

@dataclass
class PerformanceAlert:
    id: str
    portfolio_id: str
    metric: str  # 'return', 'sharpe', 'drawdown'
    threshold: float
    condition: str  # 'above' ou 'below'
    current_value: float
    created_at: str
    triggered: bool = False
    triggered_at: Optional[str] = None

class AlertManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.alerts_file = os.path.join(data_dir, "alerts.json")
        self.performance_alerts_file = os.path.join(data_dir, "performance_alerts.json")
        
        # Criar diretório se não existir
        os.makedirs(data_dir, exist_ok=True)
        
        # Inicializar arquivos se não existirem
        if not os.path.exists(self.alerts_file):
            self._save_alerts([])
        if not os.path.exists(self.performance_alerts_file):
            self._save_performance_alerts([])
    
    def create_price_alert(self, symbol: str, target_price: float, condition: str) -> Dict[str, Any]:
        """
        Cria um alerta de preço para um ativo
        """
        try:
            # Obter preço atual
            ticker = yf.Ticker(symbol)
            current_price = ticker.history(period="1d")['Close'].iloc[-1]
            
            alert = PriceAlert(
                id=str(uuid.uuid4()),
                symbol=symbol.upper(),
                target_price=target_price,
                condition=condition.lower(),
                current_price=float(current_price),
                created_at=datetime.now().isoformat()
            )
            
            # Carregar alertas existentes
            alerts = self._load_alerts()
            alerts.append(alert)
            self._save_alerts(alerts)
            
            return {
                "success": True,
                "alert": asdict(alert),
                "message": f"Alerta criado para {symbol} quando preço estiver {condition} {target_price}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro ao criar alerta: {str(e)}"
            }
    
    def create_performance_alert(self, portfolio_id: str, metric: str, 
                               threshold: float, condition: str) -> Dict[str, Any]:
        """
        Cria um alerta de performance para um portfólio
        """
        try:
            alert = PerformanceAlert(
                id=str(uuid.uuid4()),
                portfolio_id=portfolio_id,
                metric=metric.lower(),
                threshold=threshold,
                condition=condition.lower(),
                current_value=0.0,  # Será atualizado no check
                created_at=datetime.now().isoformat()
            )
            
            # Carregar alertas existentes
            alerts = self._load_performance_alerts()
            alerts.append(alert)
            self._save_performance_alerts(alerts)
            
            return {
                "success": True,
                "alert": asdict(alert),
                "message": f"Alerta de {metric} criado para quando estiver {condition} {threshold}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro ao criar alerta: {str(e)}"
            }
    
    def check_price_alerts(self) -> List[Dict[str, Any]]:
        """
        Verifica todos os alertas de preço e retorna os que foram acionados
        """
        alerts = self._load_alerts()
        triggered_alerts = []
        
        for alert in alerts:
            if alert.triggered:
                continue
                
            try:
                # Obter preço atual
                ticker = yf.Ticker(alert.symbol)
                current_price = ticker.history(period="1d")['Close'].iloc[-1]
                alert.current_price = float(current_price)
                
                # Verificar condição
                triggered = False
                if alert.condition == 'above' and current_price >= alert.target_price:
                    triggered = True
                elif alert.condition == 'below' and current_price <= alert.target_price:
                    triggered = True
                
                if triggered:
                    alert.triggered = True
                    alert.triggered_at = datetime.now().isoformat()
                    triggered_alerts.append(asdict(alert))
                    
            except Exception as e:
                print(f"Erro ao verificar alerta {alert.id}: {str(e)}")
                continue
        
        # Salvar alertas atualizados
        self._save_alerts(alerts)
        
        return triggered_alerts
    
    def get_active_alerts(self) -> Dict[str, Any]:
        """
        Retorna todos os alertas ativos (não acionados)
        """
        price_alerts = [asdict(alert) for alert in self._load_alerts() if not alert.triggered]
        performance_alerts = [asdict(alert) for alert in self._load_performance_alerts() if not alert.triggered]
        
        return {
            "price_alerts": price_alerts,
            "performance_alerts": performance_alerts,
            "total_active": len(price_alerts) + len(performance_alerts)
        }
    
    def get_triggered_alerts(self, days: int = 7) -> Dict[str, Any]:
        """
        Retorna alertas acionados nos últimos N dias
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        
        price_alerts = []
        for alert in self._load_alerts():
            if alert.triggered and alert.triggered_at:
                triggered_date = datetime.fromisoformat(alert.triggered_at)
                if triggered_date >= cutoff_date:
                    price_alerts.append(asdict(alert))
        
        performance_alerts = []
        for alert in self._load_performance_alerts():
            if alert.triggered and alert.triggered_at:
                triggered_date = datetime.fromisoformat(alert.triggered_at)
                if triggered_date >= cutoff_date:
                    performance_alerts.append(asdict(alert))
        
        return {
            "price_alerts": price_alerts,
            "performance_alerts": performance_alerts,
            "total_triggered": len(price_alerts) + len(performance_alerts),
            "period_days": days
        }
    
    def delete_alert(self, alert_id: str, alert_type: str = "price") -> Dict[str, Any]:
        """
        Remove um alerta específico
        """
        try:
            if alert_type == "price":
                alerts = self._load_alerts()
                alerts = [alert for alert in alerts if alert.id != alert_id]
                self._save_alerts(alerts)
            else:
                alerts = self._load_performance_alerts()
                alerts = [alert for alert in alerts if alert.id != alert_id]
                self._save_performance_alerts(alerts)
            
            return {
                "success": True,
                "message": "Alerta removido com sucesso"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Erro ao remover alerta: {str(e)}"
            }
    
    def get_portfolio_monitoring(self, symbols: List[str]) -> Dict[str, Any]:
        """
        Monitora performance atual do portfólio
        """
        try:
            monitoring_data = {
                "timestamp": datetime.now().isoformat(),
                "assets": {},
                "alerts_triggered": 0
            }
            
            # Verificar alertas de preço
            triggered_alerts = self.check_price_alerts()
            monitoring_data["alerts_triggered"] = len(triggered_alerts)
            monitoring_data["recent_alerts"] = triggered_alerts
            
            # Obter dados atuais dos ativos
            for symbol in symbols:
                try:
                    ticker = yf.Ticker(symbol)
                    hist = ticker.history(period="5d")
                    
                    if not hist.empty:
                        current_price = hist['Close'].iloc[-1]
                        prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
                        change_pct = ((current_price - prev_price) / prev_price) * 100
                        
                        monitoring_data["assets"][symbol] = {
                            "current_price": float(current_price),
                            "previous_price": float(prev_price),
                            "change_percent": float(change_pct),
                            "volume": int(hist['Volume'].iloc[-1]) if 'Volume' in hist else 0,
                            "status": "up" if change_pct > 0 else "down" if change_pct < 0 else "stable"
                        }
                        
                except Exception as e:
                    monitoring_data["assets"][symbol] = {
                        "error": f"Erro ao obter dados: {str(e)}"
                    }
            
            return monitoring_data
            
        except Exception as e:
            return {
                "error": f"Erro no monitoramento: {str(e)}"
            }
    
    def _load_alerts(self) -> List[PriceAlert]:
        """Carrega alertas de preço do arquivo"""
        try:
            with open(self.alerts_file, 'r') as f:
                data = json.load(f)
                return [PriceAlert(**alert) for alert in data]
        except:
            return []
    
    def _save_alerts(self, alerts: List[PriceAlert]):
        """Salva alertas de preço no arquivo"""
        with open(self.alerts_file, 'w') as f:
            json.dump([asdict(alert) for alert in alerts], f, indent=2)
    
    def _load_performance_alerts(self) -> List[PerformanceAlert]:
        """Carrega alertas de performance do arquivo"""
        try:
            with open(self.performance_alerts_file, 'r') as f:
                data = json.load(f)
                return [PerformanceAlert(**alert) for alert in data]
        except:
            return []
    
    def _save_performance_alerts(self, alerts: List[PerformanceAlert]):
        """Salva alertas de performance no arquivo"""
        with open(self.performance_alerts_file, 'w') as f:
            json.dump([asdict(alert) for alert in alerts], f, indent=2)

