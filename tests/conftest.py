import pytest
import os
import tempfile
from app import create_app, db
from app.models.provider import Provider

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    
    class TestConfig:
        TESTING = True
        SECRET_KEY = 'test-secret-key'
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_path
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    app = create_app(TestConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
    
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def sample_provider(app):
    with app.app_context():
        provider = Provider(
            name='TestProvider',
            intelligence_index=95.5,
            coding_index=92.3,
            agentic_index=94.1,
            price_per_1k_input=0.008,
            price_per_1k_output=0.024,
            latency_ms=120.5,
            throughput_tokens_per_sec=45.2,
            models_count=5
        )
        db.session.add(provider)
        db.session.commit()
        db.session.refresh(provider)
        return provider

@pytest.fixture
def multiple_providers(app):
    with app.app_context():
        providers = [
            Provider(
                name=f'Provider{i}',
                intelligence_index=90 + i,
                coding_index=85 + i,
                agentic_index=88 + i,
                price_per_1k_input=0.005 + i * 0.001,
                price_per_1k_output=0.015 + i * 0.003,
                latency_ms=100 + i * 10,
                throughput_tokens_per_sec=40 + i * 2,
                models_count=3 + i
            )
            for i in range(5)
        ]
        
        for provider in providers:
            db.session.add(provider)
        
        db.session.commit()
        return providers
