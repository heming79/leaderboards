from app import db
from datetime import datetime

class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=False)
    context_window = db.Column(db.Integer)
    license_type = db.Column(db.String(100))
    openness_index = db.Column(db.Float)
    intelligence_index = db.Column(db.Float)
    coding_index = db.Column(db.Float)
    agentic_index = db.Column(db.Float)
    price_per_1k_input = db.Column(db.Float)
    price_per_1k_output = db.Column(db.Float)
    latency_ms = db.Column(db.Float)
    throughput_tokens_per_sec = db.Column(db.Float)
    model_size = db.Column(db.String(50))
    is_open_source = db.Column(db.Boolean, default=False)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self, include_provider=False):
        result = {
            'id': self.id,
            'name': self.name,
            'provider_id': self.provider_id,
            'provider_name': self.provider.name if self.provider else None,
            'context_window': self.context_window,
            'license_type': self.license_type,
            'openness_index': self.openness_index,
            'intelligence_index': self.intelligence_index,
            'coding_index': self.coding_index,
            'agentic_index': self.agentic_index,
            'price_per_1k_input': self.price_per_1k_input,
            'price_per_1k_output': self.price_per_1k_output,
            'latency_ms': self.latency_ms,
            'throughput_tokens_per_sec': self.throughput_tokens_per_sec,
            'model_size': self.model_size,
            'is_open_source': self.is_open_source,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }
        
        if include_provider and self.provider:
            result['provider'] = self.provider.to_dict()
        
        return result
