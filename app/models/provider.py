from app import db
from datetime import datetime

class Provider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    logo_url = db.Column(db.String(500))
    intelligence_index = db.Column(db.Float)
    coding_index = db.Column(db.Float)
    agentic_index = db.Column(db.Float)
    price_per_1k_input = db.Column(db.Float)
    price_per_1k_output = db.Column(db.Float)
    latency_ms = db.Column(db.Float)
    throughput_tokens_per_sec = db.Column(db.Float)
    models_count = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    models = db.relationship('Model', backref='provider', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self, include_models=False):
        result = {
            'id': self.id,
            'name': self.name,
            'logo_url': self.logo_url,
            'intelligence_index': self.intelligence_index,
            'coding_index': self.coding_index,
            'agentic_index': self.agentic_index,
            'price_per_1k_input': self.price_per_1k_input,
            'price_per_1k_output': self.price_per_1k_output,
            'latency_ms': self.latency_ms,
            'throughput_tokens_per_sec': self.throughput_tokens_per_sec,
            'models_count': self.models_count,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }
        
        if include_models:
            result['models'] = [model.to_dict() for model in self.models.all()]
        
        return result
