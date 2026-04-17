import pytest
from app import db
from app.models.provider import Provider
from app.utils.database import init_db, add_sample_data

class TestDatabaseOperations:
    def test_init_db_creates_tables(self, app):
        with app.app_context():
            db.drop_all()
            assert Provider.query.count() == 0
            
            init_db()
            
            assert Provider.query.count() == 0

    def test_add_sample_data(self, app):
        with app.app_context():
            db.drop_all()
            db.create_all()
            
            assert Provider.query.count() == 0
            
            add_sample_data()
            
            assert Provider.query.count() > 0
            
            providers = Provider.query.all()
            for provider in providers:
                assert provider.name is not None
                assert provider.intelligence_index is not None

    def test_sample_data_structure(self, app):
        with app.app_context():
            db.drop_all()
            db.create_all()
            add_sample_data()
            
            provider = Provider.query.first()
            
            assert hasattr(provider, 'id')
            assert hasattr(provider, 'name')
            assert hasattr(provider, 'intelligence_index')
            assert hasattr(provider, 'coding_index')
            assert hasattr(provider, 'agentic_index')
            assert hasattr(provider, 'price_per_1k_input')
            assert hasattr(provider, 'price_per_1k_output')
            assert hasattr(provider, 'latency_ms')
            assert hasattr(provider, 'throughput_tokens_per_sec')
            assert hasattr(provider, 'models_count')
            assert hasattr(provider, 'last_updated')

    def test_provider_query_operations(self, app, multiple_providers):
        with app.app_context():
            all_providers = Provider.query.all()
            assert len(all_providers) == 5
            
            sorted_by_intelligence = Provider.query.order_by(
                Provider.intelligence_index.desc()
            ).all()
            
            assert sorted_by_intelligence[0].intelligence_index >= sorted_by_intelligence[1].intelligence_index
            
            filtered = Provider.query.filter(
                Provider.intelligence_index > 92
            ).all()
            
            assert len(filtered) > 0

    def test_provider_pagination(self, app, multiple_providers):
        with app.app_context():
            pagination = Provider.query.paginate(page=1, per_page=2, error_out=False)
            
            assert pagination.total == 5
            assert pagination.pages == 3
            assert pagination.page == 1
            assert len(pagination.items) == 2
            
            pagination2 = Provider.query.paginate(page=2, per_page=2, error_out=False)
            assert pagination2.page == 2
            assert len(pagination2.items) == 2

    def test_provider_bulk_operations(self, app):
        with app.app_context():
            providers = [
                Provider(name=f'BulkProvider{i}', intelligence_index=80 + i)
                for i in range(10)
            ]
            
            db.session.bulk_save_objects(providers)
            db.session.commit()
            
            assert Provider.query.count() == 10
            
            Provider.query.delete()
            db.session.commit()
            
            assert Provider.query.count() == 0

    def test_provider_transaction_rollback(self, app):
        with app.app_context():
            try:
                provider1 = Provider(name='TransactionTest1', intelligence_index=90.0)
                db.session.add(provider1)
                db.session.flush()
                
                provider2 = Provider(name='TransactionTest1', intelligence_index=85.0)
                db.session.add(provider2)
                db.session.commit()
                
                assert False, "Should have raised an exception"
            except Exception:
                db.session.rollback()
                
                count = Provider.query.filter_by(name='TransactionTest1').count()
                assert count == 0
