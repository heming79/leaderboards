from app import db, create_app
from app.models.provider import Provider
from app.models.model import Model

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
                'logo_url': 'https://pbs.twimg.com/profile_images/1815749859648188416/ntF2fXaL_400x400.jpg',
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
                'logo_url': 'https://pbs.twimg.com/profile_images/1845481318018711552/3U1HfF3__400x400.jpg',
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
                'logo_url': 'https://pbs.twimg.com/profile_images/1787631458989670400/7f4F2Xb__400x400.jpg',
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
                'name': 'Amazon Bedrock',
                'logo_url': 'https://pbs.twimg.com/profile_images/1776498567831375872/8Z7X9Y1__400x400.jpg',
                'intelligence_index': 88.7,
                'coding_index': 87.3,
                'agentic_index': 86.5,
                'price_per_1k_input': 0.005,
                'price_per_1k_output': 0.015,
                'latency_ms': 145.8,
                'throughput_tokens_per_sec': 38.2,
                'models_count': 12
            },
            {
                'name': 'DeepSeek',
                'logo_url': 'https://pbs.twimg.com/profile_images/1823456789012345678/abc123xyz_400x400.jpg',
                'intelligence_index': 90.2,
                'coding_index': 92.1,
                'agentic_index': 88.7,
                'price_per_1k_input': 0.003,
                'price_per_1k_output': 0.009,
                'latency_ms': 125.6,
                'throughput_tokens_per_sec': 41.8,
                'models_count': 4
            },
            {
                'name': 'Mistral',
                'logo_url': 'https://pbs.twimg.com/profile_images/1798765432109876543/mistral_400x400.jpg',
                'intelligence_index': 89.5,
                'coding_index': 88.2,
                'agentic_index': 87.6,
                'price_per_1k_input': 0.002,
                'price_per_1k_output': 0.006,
                'latency_ms': 95.3,
                'throughput_tokens_per_sec': 55.2,
                'models_count': 6
            },
            {
                'name': 'Groq',
                'logo_url': 'https://pbs.twimg.com/profile_images/1801234567890123456/groq_400x400.jpg',
                'intelligence_index': 87.8,
                'coding_index': 86.5,
                'agentic_index': 85.3,
                'price_per_1k_input': 0.001,
                'price_per_1k_output': 0.003,
                'latency_ms': 45.2,
                'throughput_tokens_per_sec': 120.5,
                'models_count': 5
            },
            {
                'name': 'Together.ai',
                'logo_url': 'https://pbs.twimg.com/profile_images/1789012345678901234/together_400x400.jpg',
                'intelligence_index': 88.2,
                'coding_index': 87.1,
                'agentic_index': 86.4,
                'price_per_1k_input': 0.0015,
                'price_per_1k_output': 0.0045,
                'latency_ms': 85.6,
                'throughput_tokens_per_sec': 65.3,
                'models_count': 20
            },
            {
                'name': 'Microsoft Azure',
                'logo_url': 'https://pbs.twimg.com/profile_images/1776543210987654321/azure_400x400.jpg',
                'intelligence_index': 92.5,
                'coding_index': 91.8,
                'agentic_index': 90.5,
                'price_per_1k_input': 0.009,
                'price_per_1k_output': 0.027,
                'latency_ms': 135.4,
                'throughput_tokens_per_sec': 40.8,
                'models_count': 10
            },
            {
                'name': 'Alibaba',
                'logo_url': 'https://pbs.twimg.com/profile_images/1812345678901234567/alibaba_400x400.jpg',
                'intelligence_index': 86.5,
                'coding_index': 88.3,
                'agentic_index': 84.2,
                'price_per_1k_input': 0.002,
                'price_per_1k_output': 0.006,
                'latency_ms': 150.2,
                'throughput_tokens_per_sec': 35.6,
                'models_count': 8
            },
            {
                'name': 'Qwen',
                'logo_url': 'https://pbs.twimg.com/profile_images/1823456789012345678/qwen_400x400.jpg',
                'intelligence_index': 87.2,
                'coding_index': 89.1,
                'agentic_index': 85.8,
                'price_per_1k_input': 0.0015,
                'price_per_1k_output': 0.0045,
                'latency_ms': 110.5,
                'throughput_tokens_per_sec': 48.3,
                'models_count': 7
            },
            {
                'name': 'Meta',
                'logo_url': 'https://pbs.twimg.com/profile_images/1834567890123456789/meta_400x400.jpg',
                'intelligence_index': 85.8,
                'coding_index': 84.5,
                'agentic_index': 83.2,
                'price_per_1k_input': 0.0005,
                'price_per_1k_output': 0.0015,
                'latency_ms': 105.3,
                'throughput_tokens_per_sec': 52.1,
                'models_count': 15
            }
        ]
        
        provider_objects = {}
        
        for provider_data in sample_providers:
            existing_provider = Provider.query.filter_by(name=provider_data['name']).first()
            if not existing_provider:
                provider = Provider(**provider_data)
                db.session.add(provider)
                db.session.flush()
                provider_objects[provider_data['name']] = provider
            else:
                provider_objects[provider_data['name']] = existing_provider
        
        db.session.commit()
        
        sample_models = [
            {
                'name': 'Claude 3.5 Sonnet',
                'provider_name': 'Anthropic',
                'context_window': 200000,
                'license_type': 'Proprietary',
                'openness_index': 10.0,
                'intelligence_index': 95.2,
                'coding_index': 92.8,
                'agentic_index': 94.1,
                'price_per_1k_input': 0.003,
                'price_per_1k_output': 0.015,
                'latency_ms': 120.5,
                'throughput_tokens_per_sec': 45.2,
                'model_size': 'N/A',
                'is_open_source': False
            },
            {
                'name': 'Claude 3 Opus',
                'provider_name': 'Anthropic',
                'context_window': 200000,
                'license_type': 'Proprietary',
                'openness_index': 10.0,
                'intelligence_index': 96.5,
                'coding_index': 94.2,
                'agentic_index': 95.8,
                'price_per_1k_input': 0.015,
                'price_per_1k_output': 0.075,
                'latency_ms': 180.3,
                'throughput_tokens_per_sec': 32.5,
                'model_size': 'N/A',
                'is_open_source': False
            },
            {
                'name': 'GPT-4o',
                'provider_name': 'OpenAI',
                'context_window': 128000,
                'license_type': 'Proprietary',
                'openness_index': 10.0,
                'intelligence_index': 94.8,
                'coding_index': 93.5,
                'agentic_index': 92.7,
                'price_per_1k_input': 0.005,
                'price_per_1k_output': 0.015,
                'latency_ms': 115.3,
                'throughput_tokens_per_sec': 48.7,
                'model_size': 'N/A',
                'is_open_source': False
            },
            {
                'name': 'GPT-4o mini',
                'provider_name': 'OpenAI',
                'context_window': 128000,
                'license_type': 'Proprietary',
                'openness_index': 10.0,
                'intelligence_index': 88.5,
                'coding_index': 87.2,
                'agentic_index': 86.5,
                'price_per_1k_input': 0.00015,
                'price_per_1k_output': 0.0006,
                'latency_ms': 85.2,
                'throughput_tokens_per_sec': 65.3,
                'model_size': 'N/A',
                'is_open_source': False
            },
            {
                'name': 'o3-mini',
                'provider_name': 'OpenAI',
                'context_window': 200000,
                'license_type': 'Proprietary',
                'openness_index': 10.0,
                'intelligence_index': 93.2,
                'coding_index': 92.8,
                'agentic_index': 91.5,
                'price_per_1k_input': 0.0011,
                'price_per_1k_output': 0.0044,
                'latency_ms': 150.5,
                'throughput_tokens_per_sec': 38.2,
                'model_size': 'N/A',
                'is_open_source': False
            },
            {
                'name': 'Gemini 1.5 Pro',
                'provider_name': 'Google',
                'context_window': 2000000,
                'license_type': 'Proprietary',
                'openness_index': 10.0,
                'intelligence_index': 93.5,
                'coding_index': 91.2,
                'agentic_index': 90.8,
                'price_per_1k_input': 0.0035,
                'price_per_1k_output': 0.0105,
                'latency_ms': 130.2,
                'throughput_tokens_per_sec': 42.5,
                'model_size': 'N/A',
                'is_open_source': False
            },
            {
                'name': 'Gemini 1.5 Flash',
                'provider_name': 'Google',
                'context_window': 1000000,
                'license_type': 'Proprietary',
                'openness_index': 10.0,
                'intelligence_index': 86.8,
                'coding_index': 85.5,
                'agentic_index': 84.2,
                'price_per_1k_input': 0.000075,
                'price_per_1k_output': 0.0003,
                'latency_ms': 95.6,
                'throughput_tokens_per_sec': 58.3,
                'model_size': 'N/A',
                'is_open_source': False
            },
            {
                'name': 'DeepSeek V3',
                'provider_name': 'DeepSeek',
                'context_window': 128000,
                'license_type': 'Proprietary',
                'openness_index': 10.0,
                'intelligence_index': 90.2,
                'coding_index': 92.1,
                'agentic_index': 88.7,
                'price_per_1k_input': 0.00027,
                'price_per_1k_output': 0.0011,
                'latency_ms': 125.6,
                'throughput_tokens_per_sec': 41.8,
                'model_size': 'N/A',
                'is_open_source': False
            },
            {
                'name': 'DeepSeek R1',
                'provider_name': 'DeepSeek',
                'context_window': 64000,
                'license_type': 'DeepSeek Open R1 License',
                'openness_index': 75.0,
                'intelligence_index': 91.5,
                'coding_index': 93.8,
                'agentic_index': 90.2,
                'price_per_1k_input': 0.00055,
                'price_per_1k_output': 0.00219,
                'latency_ms': 145.3,
                'throughput_tokens_per_sec': 35.6,
                'model_size': '671B',
                'is_open_source': True
            },
            {
                'name': 'Mistral Large 2',
                'provider_name': 'Mistral',
                'context_window': 128000,
                'license_type': 'Proprietary',
                'openness_index': 10.0,
                'intelligence_index': 89.5,
                'coding_index': 88.2,
                'agentic_index': 87.6,
                'price_per_1k_input': 0.002,
                'price_per_1k_output': 0.006,
                'latency_ms': 95.3,
                'throughput_tokens_per_sec': 55.2,
                'model_size': 'N/A',
                'is_open_source': False
            },
            {
                'name': 'Mistral 7B',
                'provider_name': 'Mistral',
                'context_window': 32000,
                'license_type': 'Apache 2.0',
                'openness_index': 100.0,
                'intelligence_index': 72.5,
                'coding_index': 70.2,
                'agentic_index': 68.5,
                'price_per_1k_input': 0.00005,
                'price_per_1k_output': 0.00015,
                'latency_ms': 55.2,
                'throughput_tokens_per_sec': 85.3,
                'model_size': '7B',
                'is_open_source': True
            },
            {
                'name': 'Llama 3.1 405B',
                'provider_name': 'Meta',
                'context_window': 128000,
                'license_type': 'Llama 3.1',
                'openness_index': 90.0,
                'intelligence_index': 85.8,
                'coding_index': 84.5,
                'agentic_index': 83.2,
                'price_per_1k_input': 0.0005,
                'price_per_1k_output': 0.0015,
                'latency_ms': 105.3,
                'throughput_tokens_per_sec': 52.1,
                'model_size': '405B',
                'is_open_source': True
            },
            {
                'name': 'Llama 3.1 70B',
                'provider_name': 'Meta',
                'context_window': 128000,
                'license_type': 'Llama 3.1',
                'openness_index': 90.0,
                'intelligence_index': 82.5,
                'coding_index': 81.2,
                'agentic_index': 80.5,
                'price_per_1k_input': 0.0003,
                'price_per_1k_output': 0.0009,
                'latency_ms': 85.6,
                'throughput_tokens_per_sec': 62.3,
                'model_size': '70B',
                'is_open_source': True
            },
            {
                'name': 'Qwen 2.5 72B',
                'provider_name': 'Qwen',
                'context_window': 128000,
                'license_type': 'Qwen',
                'openness_index': 85.0,
                'intelligence_index': 87.2,
                'coding_index': 89.1,
                'agentic_index': 85.8,
                'price_per_1k_input': 0.0003,
                'price_per_1k_output': 0.0009,
                'latency_ms': 110.5,
                'throughput_tokens_per_sec': 48.3,
                'model_size': '72B',
                'is_open_source': True
            },
            {
                'name': 'Qwen 2.5 VL 30B',
                'provider_name': 'Qwen',
                'context_window': 32000,
                'license_type': 'Qwen',
                'openness_index': 85.0,
                'intelligence_index': 82.5,
                'coding_index': 80.2,
                'agentic_index': 78.5,
                'price_per_1k_input': 0.0002,
                'price_per_1k_output': 0.0006,
                'latency_ms': 95.3,
                'throughput_tokens_per_sec': 55.2,
                'model_size': '30B',
                'is_open_source': True
            },
            {
                'name': 'Claude 3.5 Haiku',
                'provider_name': 'Anthropic',
                'context_window': 200000,
                'license_type': 'Proprietary',
                'openness_index': 10.0,
                'intelligence_index': 86.5,
                'coding_index': 85.2,
                'agentic_index': 84.8,
                'price_per_1k_input': 0.0008,
                'price_per_1k_output': 0.004,
                'latency_ms': 85.2,
                'throughput_tokens_per_sec': 58.5,
                'model_size': 'N/A',
                'is_open_source': False
            },
            {
                'name': 'GPT-4 Turbo',
                'provider_name': 'OpenAI',
                'context_window': 128000,
                'license_type': 'Proprietary',
                'openness_index': 10.0,
                'intelligence_index': 92.5,
                'coding_index': 91.8,
                'agentic_index': 90.5,
                'price_per_1k_input': 0.01,
                'price_per_1k_output': 0.03,
                'latency_ms': 145.2,
                'throughput_tokens_per_sec': 35.8,
                'model_size': 'N/A',
                'is_open_source': False
            },
            {
                'name': 'Gemini 2.0 Flash',
                'provider_name': 'Google',
                'context_window': 1000000,
                'license_type': 'Proprietary',
                'openness_index': 10.0,
                'intelligence_index': 88.2,
                'coding_index': 87.5,
                'agentic_index': 86.2,
                'price_per_1k_input': 0.0001,
                'price_per_1k_output': 0.0004,
                'latency_ms': 88.5,
                'throughput_tokens_per_sec': 62.3,
                'model_size': 'N/A',
                'is_open_source': False
            },
            {
                'name': 'Mistral Small 3',
                'provider_name': 'Mistral',
                'context_window': 32000,
                'license_type': 'Proprietary',
                'openness_index': 10.0,
                'intelligence_index': 78.5,
                'coding_index': 77.2,
                'agentic_index': 76.5,
                'price_per_1k_input': 0.0001,
                'price_per_1k_output': 0.0003,
                'latency_ms': 65.2,
                'throughput_tokens_per_sec': 75.3,
                'model_size': 'N/A',
                'is_open_source': False
            },
            {
                'name': 'Llama 3.2 3B',
                'provider_name': 'Meta',
                'context_window': 128000,
                'license_type': 'Llama 3.2',
                'openness_index': 90.0,
                'intelligence_index': 65.5,
                'coding_index': 63.2,
                'agentic_index': 61.5,
                'price_per_1k_input': 0.00005,
                'price_per_1k_output': 0.0001,
                'latency_ms': 45.2,
                'throughput_tokens_per_sec': 95.3,
                'model_size': '3B',
                'is_open_source': True
            }
        ]
        
        for model_data in sample_models:
            provider_name = model_data.pop('provider_name')
            provider = provider_objects.get(provider_name)
            
            if provider:
                existing_model = Model.query.filter_by(
                    name=model_data['name'],
                    provider_id=provider.id
                ).first()
                
                if not existing_model:
                    model = Model(provider_id=provider.id, **model_data)
                    db.session.add(model)
        
        db.session.commit()
        print("Sample data added successfully!")
        print(f"Added {len(sample_providers)} providers and {len(sample_models)} models")

if __name__ == '__main__':
    init_db()
    add_sample_data()
