from app import db, create_app
from app.models.provider import Provider

def init_db():
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")

def add_sample_data():
    app = create_app()
    with app.app_context():
        sample_providers = [
            {
                'name': 'Anthropic',
                'intelligence_index': 95.2,
                'coding_index': 92.8,
                'agentic_index': 94.1,
                'price_per_1k_input': 0.008,
                'price_per_1k_output': 0.024,
                'latency_ms': 120.5,
                'throughput_tokens_per_sec': 45.2,
                'models_count': 5
            },
            {
                'name': 'OpenAI',
                'intelligence_index': 94.8,
                'coding_index': 93.5,
                'agentic_index': 92.7,
                'price_per_1k_input': 0.01,
                'price_per_1k_output': 0.03,
                'latency_ms': 115.3,
                'throughput_tokens_per_sec': 48.7,
                'models_count': 8
            },
            {
                'name': 'Google',
                'intelligence_index': 93.5,
                'coding_index': 91.2,
                'agentic_index': 90.8,
                'price_per_1k_input': 0.007,
                'price_per_1k_output': 0.021,
                'latency_ms': 130.2,
                'throughput_tokens_per_sec': 42.5,
                'models_count': 6
            },
            {
                'name': 'Amazon',
                'intelligence_index': 88.7,
                'coding_index': 87.3,
                'agentic_index': 86.5,
                'price_per_1k_input': 0.005,
                'price_per_1k_output': 0.015,
                'latency_ms': 145.8,
                'throughput_tokens_per_sec': 38.2,
                'models_count': 4
            },
            {
                'name': 'DeepSeek',
                'intelligence_index': 90.2,
                'coding_index': 92.1,
                'agentic_index': 88.7,
                'price_per_1k_input': 0.003,
                'price_per_1k_output': 0.009,
                'latency_ms': 125.6,
                'throughput_tokens_per_sec': 41.8,
                'models_count': 3
            }
        ]
        
        for provider_data in sample_providers:
            existing_provider = Provider.query.filter_by(name=provider_data['name']).first()
            if not existing_provider:
                provider = Provider(**provider_data)
                db.session.add(provider)
        
        db.session.commit()
        print("Sample data added successfully!")

if __name__ == '__main__':
    init_db()
    add_sample_data()
