from flask import Blueprint, jsonify, request
from app.models.provider import Provider
from app import db

api = Blueprint('api', __name__)

@api.route('/providers', methods=['GET'])
def get_providers():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    sort_by = request.args.get('sort_by', 'intelligence_index')
    sort_order = request.args.get('sort_order', 'desc')
    
    query = Provider.query
    
    if sort_order == 'desc':
        query = query.order_by(getattr(Provider, sort_by).desc())
    else:
        query = query.order_by(getattr(Provider, sort_by).asc())
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    providers = [provider.to_dict() for provider in pagination.items]
    
    return jsonify({
        'providers': providers,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'per_page': per_page
    })

@api.route('/providers/<int:provider_id>', methods=['GET'])
def get_provider(provider_id):
    provider = Provider.query.get_or_404(provider_id)
    return jsonify(provider.to_dict())

@api.route('/providers', methods=['POST'])
def create_provider():
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    existing_provider = Provider.query.filter_by(name=data['name']).first()
    if existing_provider:
        return jsonify({'error': 'Provider with this name already exists'}), 400
    
    provider = Provider(
        name=data['name'],
        intelligence_index=data.get('intelligence_index'),
        coding_index=data.get('coding_index'),
        agentic_index=data.get('agentic_index'),
        price_per_1k_input=data.get('price_per_1k_input'),
        price_per_1k_output=data.get('price_per_1k_output'),
        latency_ms=data.get('latency_ms'),
        throughput_tokens_per_sec=data.get('throughput_tokens_per_sec'),
        models_count=data.get('models_count')
    )
    
    db.session.add(provider)
    db.session.commit()
    
    return jsonify(provider.to_dict()), 201

@api.route('/providers/<int:provider_id>', methods=['PUT'])
def update_provider(provider_id):
    provider = Provider.query.get_or_404(provider_id)
    data = request.get_json()
    
    if 'name' in data:
        provider.name = data['name']
    if 'intelligence_index' in data:
        provider.intelligence_index = data['intelligence_index']
    if 'coding_index' in data:
        provider.coding_index = data['coding_index']
    if 'agentic_index' in data:
        provider.agentic_index = data['agentic_index']
    if 'price_per_1k_input' in data:
        provider.price_per_1k_input = data['price_per_1k_input']
    if 'price_per_1k_output' in data:
        provider.price_per_1k_output = data['price_per_1k_output']
    if 'latency_ms' in data:
        provider.latency_ms = data['latency_ms']
    if 'throughput_tokens_per_sec' in data:
        provider.throughput_tokens_per_sec = data['throughput_tokens_per_sec']
    if 'models_count' in data:
        provider.models_count = data['models_count']
    
    db.session.commit()
    
    return jsonify(provider.to_dict())

@api.route('/providers/<int:provider_id>', methods=['DELETE'])
def delete_provider(provider_id):
    provider = Provider.query.get_or_404(provider_id)
    
    db.session.delete(provider)
    db.session.commit()
    
    return jsonify({'message': 'Provider deleted successfully'}), 200
