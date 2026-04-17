import pytest
import json

class TestProviderAPI:
    def test_get_providers_empty(self, client):
        response = client.get('/api/providers')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'providers' in data
        assert 'total' in data
        assert 'pages' in data
        assert 'current_page' in data
        assert 'per_page' in data
        assert data['total'] == 0
        assert len(data['providers']) == 0

    def test_get_providers_with_data(self, client, multiple_providers):
        response = client.get('/api/providers')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['total'] == 5
        assert len(data['providers']) == 5

    def test_get_providers_pagination(self, client, multiple_providers):
        response = client.get('/api/providers?page=1&per_page=2')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['total'] == 5
        assert data['pages'] == 3
        assert data['current_page'] == 1
        assert len(data['providers']) == 2

    def test_get_providers_sorting(self, client, multiple_providers):
        response = client.get('/api/providers?sort_by=intelligence_index&sort_order=desc')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['providers']) == 5
        assert data['providers'][0]['intelligence_index'] >= data['providers'][1]['intelligence_index']

    def test_get_provider_by_id(self, client, sample_provider):
        response = client.get(f'/api/providers/{sample_provider.id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == 'TestProvider'
        assert data['intelligence_index'] == 95.5

    def test_get_provider_not_found(self, client):
        response = client.get('/api/providers/999')
        assert response.status_code == 404

    def test_create_provider(self, client):
        provider_data = {
            'name': 'NewProvider',
            'intelligence_index': 90.0,
            'coding_index': 85.0,
            'agentic_index': 88.0,
            'price_per_1k_input': 0.005,
            'price_per_1k_output': 0.015,
            'latency_ms': 100.0,
            'throughput_tokens_per_sec': 40.0,
            'models_count': 3
        }
        
        response = client.post(
            '/api/providers',
            data=json.dumps(provider_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['name'] == 'NewProvider'
        assert data['intelligence_index'] == 90.0

    def test_create_provider_missing_name(self, client):
        provider_data = {
            'intelligence_index': 90.0
        }
        
        response = client.post(
            '/api/providers',
            data=json.dumps(provider_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_create_provider_duplicate_name(self, client, sample_provider):
        provider_data = {
            'name': 'TestProvider',
            'intelligence_index': 90.0
        }
        
        response = client.post(
            '/api/providers',
            data=json.dumps(provider_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_update_provider(self, client, sample_provider):
        update_data = {
            'intelligence_index': 99.9,
            'coding_index': 98.8
        }
        
        response = client.put(
            f'/api/providers/{sample_provider.id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['intelligence_index'] == 99.9
        assert data['coding_index'] == 98.8
        assert data['name'] == 'TestProvider'

    def test_update_provider_not_found(self, client):
        update_data = {
            'intelligence_index': 99.9
        }
        
        response = client.put(
            '/api/providers/999',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 404

    def test_delete_provider(self, client, sample_provider):
        response = client.delete(f'/api/providers/{sample_provider.id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data
        
        get_response = client.get(f'/api/providers/{sample_provider.id}')
        assert get_response.status_code == 404

    def test_delete_provider_not_found(self, client):
        response = client.delete('/api/providers/999')
        assert response.status_code == 404
