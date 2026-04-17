from flask import Blueprint, jsonify, request
from app.models.provider import Provider
from app.models.model import Model
from app import db

api = Blueprint('api', __name__)

@api.route('/providers', methods=['GET'])
def get_providers():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    sort_by = request.args.get('sort_by', 'intelligence_index')
    sort_order = request.args.get('sort_order', 'desc')
    search = request.args.get('search', '')
    
    query = Provider.query
    
    if search:
        query = query.filter(Provider.name.ilike(f'%{search}%'))
    
    valid_sort_fields = ['name', 'intelligence_index', 'coding_index', 'agentic_index', 
                         'price_per_1k_input', 'price_per_1k_output', 'latency_ms', 
                         'throughput_tokens_per_sec', 'models_count']
    
    if sort_by not in valid_sort_fields:
        sort_by = 'intelligence_index'
    
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
    include_models = request.args.get('include_models', 'false').lower() == 'true'
    provider = Provider.query.get_or_404(provider_id)
    return jsonify(provider.to_dict(include_models=include_models))

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
        logo_url=data.get('logo_url'),
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
    if 'logo_url' in data:
        provider.logo_url = data['logo_url']
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

@api.route('/models', methods=['GET'])
def get_models():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    sort_by = request.args.get('sort_by', 'intelligence_index')
    sort_order = request.args.get('sort_order', 'desc')
    search = request.args.get('search', '')
    provider_id = request.args.get('provider_id', type=int)
    provider_name = request.args.get('provider_name', '')
    license_type = request.args.get('license_type', '')
    is_open_source = request.args.get('is_open_source', None)
    min_context_window = request.args.get('min_context_window', type=int)
    max_context_window = request.args.get('max_context_window', type=int)
    
    query = Model.query.join(Provider)
    
    if search:
        query = query.filter(
            db.or_(
                Model.name.ilike(f'%{search}%'),
                Provider.name.ilike(f'%{search}%')
            )
        )
    
    if provider_id:
        query = query.filter(Model.provider_id == provider_id)
    
    if provider_name:
        query = query.filter(Provider.name.ilike(f'%{provider_name}%'))
    
    if license_type:
        query = query.filter(Model.license_type.ilike(f'%{license_type}%'))
    
    if is_open_source is not None:
        query = query.filter(Model.is_open_source == (is_open_source.lower() == 'true'))
    
    if min_context_window:
        query = query.filter(Model.context_window >= min_context_window)
    
    if max_context_window:
        query = query.filter(Model.context_window <= max_context_window)
    
    valid_sort_fields = ['name', 'intelligence_index', 'coding_index', 'agentic_index',
                         'context_window', 'price_per_1k_input', 'price_per_1k_output',
                         'latency_ms', 'throughput_tokens_per_sec', 'openness_index',
                         'model_size']
    
    if sort_by not in valid_sort_fields:
        sort_by = 'intelligence_index'
    
    if sort_order == 'desc':
        query = query.order_by(getattr(Model, sort_by).desc())
    else:
        query = query.order_by(getattr(Model, sort_by).asc())
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    models = [model.to_dict() for model in pagination.items]
    
    return jsonify({
        'models': models,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'per_page': per_page
    })

@api.route('/models/<int:model_id>', methods=['GET'])
def get_model(model_id):
    include_provider = request.args.get('include_provider', 'false').lower() == 'true'
    model = Model.query.get_or_404(model_id)
    return jsonify(model.to_dict(include_provider=include_provider))

@api.route('/models', methods=['POST'])
def create_model():
    data = request.get_json()
    
    if not data or 'name' not in data or 'provider_id' not in data:
        return jsonify({'error': 'Name and provider_id are required'}), 400
    
    provider = Provider.query.get(data['provider_id'])
    if not provider:
        return jsonify({'error': 'Provider not found'}), 404
    
    existing_model = Model.query.filter_by(
        name=data['name'],
        provider_id=data['provider_id']
    ).first()
    
    if existing_model:
        return jsonify({'error': 'Model with this name already exists for this provider'}), 400
    
    model = Model(
        name=data['name'],
        provider_id=data['provider_id'],
        context_window=data.get('context_window'),
        license_type=data.get('license_type'),
        openness_index=data.get('openness_index'),
        intelligence_index=data.get('intelligence_index'),
        coding_index=data.get('coding_index'),
        agentic_index=data.get('agentic_index'),
        price_per_1k_input=data.get('price_per_1k_input'),
        price_per_1k_output=data.get('price_per_1k_output'),
        latency_ms=data.get('latency_ms'),
        throughput_tokens_per_sec=data.get('throughput_tokens_per_sec'),
        model_size=data.get('model_size'),
        is_open_source=data.get('is_open_source', False)
    )
    
    db.session.add(model)
    db.session.commit()
    
    return jsonify(model.to_dict()), 201

@api.route('/models/<int:model_id>', methods=['PUT'])
def update_model(model_id):
    model = Model.query.get_or_404(model_id)
    data = request.get_json()
    
    if 'name' in data:
        model.name = data['name']
    if 'provider_id' in data:
        provider = Provider.query.get(data['provider_id'])
        if not provider:
            return jsonify({'error': 'Provider not found'}), 404
        model.provider_id = data['provider_id']
    if 'context_window' in data:
        model.context_window = data['context_window']
    if 'license_type' in data:
        model.license_type = data['license_type']
    if 'openness_index' in data:
        model.openness_index = data['openness_index']
    if 'intelligence_index' in data:
        model.intelligence_index = data['intelligence_index']
    if 'coding_index' in data:
        model.coding_index = data['coding_index']
    if 'agentic_index' in data:
        model.agentic_index = data['agentic_index']
    if 'price_per_1k_input' in data:
        model.price_per_1k_input = data['price_per_1k_input']
    if 'price_per_1k_output' in data:
        model.price_per_1k_output = data['price_per_1k_output']
    if 'latency_ms' in data:
        model.latency_ms = data['latency_ms']
    if 'throughput_tokens_per_sec' in data:
        model.throughput_tokens_per_sec = data['throughput_tokens_per_sec']
    if 'model_size' in data:
        model.model_size = data['model_size']
    if 'is_open_source' in data:
        model.is_open_source = data['is_open_source']
    
    db.session.commit()
    
    return jsonify(model.to_dict())

@api.route('/models/<int:model_id>', methods=['DELETE'])
def delete_model(model_id):
    model = Model.query.get_or_404(model_id)
    
    db.session.delete(model)
    db.session.commit()
    
    return jsonify({'message': 'Model deleted successfully'}), 200

@api.route('/filters/options', methods=['GET'])
def get_filter_options():
    providers = Provider.query.order_by(Provider.name).all()
    provider_names = [p.name for p in providers]
    
    license_types = db.session.query(Model.license_type).distinct().filter(
        Model.license_type.isnot(None)
    ).all()
    license_types = [lt[0] for lt in license_types if lt[0]]
    
    model_sizes = db.session.query(Model.model_size).distinct().filter(
        Model.model_size.isnot(None),
        Model.model_size != 'N/A'
    ).all()
    model_sizes = [ms[0] for ms in model_sizes if ms[0]]
    
    context_windows = db.session.query(Model.context_window).distinct().filter(
        Model.context_window.isnot(None)
    ).all()
    context_windows = sorted([cw[0] for cw in context_windows if cw[0]])
    
    return jsonify({
        'providers': provider_names,
        'license_types': license_types,
        'model_sizes': model_sizes,
        'context_windows': context_windows,
        'is_open_source_options': [True, False]
    })
