import pytest
from app.models.provider import Provider
from datetime import datetime

class TestProviderModel:
    def test_create_provider(self, app):
        with app.app_context():
            provider = Provider(
                name='TestModel',
                intelligence_index=95.5,
                coding_index=92.3,
                agentic_index=94.1,
                price_per_1k_input=0.008,
                price_per_1k_output=0.024,
                latency_ms=120.5,
                throughput_tokens_per_sec=45.2,
                models_count=5
            )
            
            assert provider.name == 'TestModel'
            assert provider.intelligence_index == 95.5
            assert provider.coding_index == 92.3
            assert provider.agentic_index == 94.1
            assert provider.price_per_1k_input == 0.008
            assert provider.price_per_1k_output == 0.024
            assert provider.latency_ms == 120.5
            assert provider.throughput_tokens_per_sec == 45.2
            assert provider.models_count == 5

    def test_provider_to_dict(self, app):
        with app.app_context():
            provider = Provider(
                name='DictTest',
                intelligence_index=90.0,
                coding_index=85.0,
                agentic_index=88.0
            )
            
            provider_dict = provider.to_dict()
            
            assert isinstance(provider_dict, dict)
            assert provider_dict['name'] == 'DictTest'
            assert provider_dict['intelligence_index'] == 90.0
            assert provider_dict['coding_index'] == 85.0
            assert provider_dict['agentic_index'] == 88.0
            assert 'id' in provider_dict
            assert 'last_updated' in provider_dict

    def test_provider_default_values(self, app):
        with app.app_context():
            provider = Provider(name='DefaultTest')
            
            assert provider.name == 'DefaultTest'
            assert provider.intelligence_index is None
            assert provider.coding_index is None
            assert provider.agentic_index is None
            assert provider.price_per_1k_input is None
            assert provider.price_per_1k_output is None
            assert provider.latency_ms is None
            assert provider.throughput_tokens_per_sec is None
            assert provider.models_count is None

    def test_provider_save_to_db(self, app, db):
        with app.app_context():
            provider = Provider(
                name='SaveTest',
                intelligence_index=95.0
            )
            
            db.session.add(provider)
            db.session.commit()
            
            saved_provider = Provider.query.filter_by(name='SaveTest').first()
            assert saved_provider is not None
            assert saved_provider.id is not None
            assert saved_provider.name == 'SaveTest'
            assert saved_provider.intelligence_index == 95.0

    def test_provider_update(self, app, db):
        with app.app_context():
            provider = Provider(
                name='UpdateTest',
                intelligence_index=90.0
            )
            
            db.session.add(provider)
            db.session.commit()
            
            provider.intelligence_index = 95.0
            db.session.commit()
            
            updated_provider = Provider.query.filter_by(name='UpdateTest').first()
            assert updated_provider.intelligence_index == 95.0

    def test_provider_delete(self, app, db):
        with app.app_context():
            provider = Provider(
                name='DeleteTest',
                intelligence_index=90.0
            )
            
            db.session.add(provider)
            db.session.commit()
            
            provider_id = provider.id
            
            db.session.delete(provider)
            db.session.commit()
            
            deleted_provider = Provider.query.get(provider_id)
            assert deleted_provider is None

    def test_provider_unique_name(self, app, db):
        with app.app_context():
            provider1 = Provider(name='UniqueTest', intelligence_index=90.0)
            db.session.add(provider1)
            db.session.commit()
            
            provider2 = Provider(name='UniqueTest', intelligence_index=85.0)
            db.session.add(provider2)
            
            with pytest.raises(Exception):
                db.session.commit()

    def test_provider_last_updated(self, app, db):
        with app.app_context():
            provider = Provider(
                name='TimestampTest',
                intelligence_index=90.0
            )
            
            db.session.add(provider)
            db.session.commit()
            
            assert provider.last_updated is not None
            assert isinstance(provider.last_updated, datetime)
            
            original_timestamp = provider.last_updated
            
            provider.intelligence_index = 95.0
            db.session.commit()
            
            assert provider.last_updated >= original_timestamp
