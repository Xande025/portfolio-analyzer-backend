from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Asset(db.Model):
    """Modelo para representar um ativo financeiro"""
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    asset_type = db.Column(db.String(20), nullable=False)  # 'stock', 'crypto', 'fund'
    exchange = db.Column(db.String(50))
    currency = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'symbol': self.symbol,
            'name': self.name,
            'asset_type': self.asset_type,
            'exchange': self.exchange,
            'currency': self.currency,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Portfolio(db.Model):
    """Modelo para representar um portfólio de investimentos"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento com posições
    positions = db.relationship('Position', backref='portfolio', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'positions': [pos.to_dict() for pos in self.positions]
        }

class Position(db.Model):
    """Modelo para representar uma posição em um portfólio"""
    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), nullable=False)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    average_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    asset = db.relationship('Asset', backref='positions')
    
    def to_dict(self):
        return {
            'id': self.id,
            'portfolio_id': self.portfolio_id,
            'asset_id': self.asset_id,
            'quantity': self.quantity,
            'average_price': self.average_price,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'asset': self.asset.to_dict() if self.asset else None
        }

class PriceHistory(db.Model):
    """Modelo para armazenar histórico de preços"""
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    open_price = db.Column(db.Float)
    high_price = db.Column(db.Float)
    low_price = db.Column(db.Float)
    close_price = db.Column(db.Float, nullable=False)
    volume = db.Column(db.BigInteger)
    adjusted_close = db.Column(db.Float)
    
    # Relacionamento
    asset = db.relationship('Asset', backref='price_history')
    
    # Índice único para evitar duplicatas
    __table_args__ = (db.UniqueConstraint('asset_id', 'date', name='unique_asset_date'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'asset_id': self.asset_id,
            'date': self.date.isoformat() if self.date else None,
            'open_price': self.open_price,
            'high_price': self.high_price,
            'low_price': self.low_price,
            'close_price': self.close_price,
            'volume': self.volume,
            'adjusted_close': self.adjusted_close
        }

