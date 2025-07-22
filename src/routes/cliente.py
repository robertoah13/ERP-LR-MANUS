from flask import Blueprint, request, jsonify
from src.database import db
from src.models.cliente import Cliente
from datetime import datetime

cliente_bp = Blueprint('cliente', __name__)

@cliente_bp.route('/clientes', methods=['GET'])
def listar_clientes():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        tipo = request.args.get('tipo', '')
        
        query = Cliente.query
        
        if search:
            query = query.filter(Cliente.nome.contains(search))
        
        if tipo:
            query = query.filter(Cliente.tipo == tipo)
        
        query = query.filter(Cliente.ativo == True)
        
        clientes = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'success': True,
            'data': [cliente.to_dict() for cliente in clientes.items],
            'pagination': {
                'page': page,
                'pages': clientes.pages,
                'per_page': per_page,
                'total': clientes.total
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@cliente_bp.route('/clientes', methods=['POST'])
def criar_cliente():
    try:
        data = request.get_json()
        
        # Validações
        if not data.get('nome'):
            return jsonify({'success': False, 'message': 'Nome é obrigatório'}), 400
        
        if not data.get('email'):
            return jsonify({'success': False, 'message': 'Email é obrigatório'}), 400
        
        if not data.get('tipo') or data.get('tipo') not in ['dentista', 'clinica']:
            return jsonify({'success': False, 'message': 'Tipo deve ser "dentista" ou "clinica"'}), 400
        
        # Verificar se email já existe
        cliente_existente = Cliente.query.filter_by(email=data['email']).first()
        if cliente_existente:
            return jsonify({'success': False, 'message': 'Email já cadastrado'}), 400
        
        cliente = Cliente(
            nome=data['nome'],
            tipo=data['tipo'],
            email=data['email'],
            telefone=data.get('telefone'),
            endereco=data.get('endereco'),
            observacoes=data.get('observacoes')
        )
        
        db.session.add(cliente)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cliente criado com sucesso',
            'data': cliente.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@cliente_bp.route('/clientes/<int:cliente_id>', methods=['GET'])
def obter_cliente(cliente_id):
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        return jsonify({
            'success': True,
            'data': cliente.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@cliente_bp.route('/clientes/<int:cliente_id>', methods=['PUT'])
def atualizar_cliente(cliente_id):
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        data = request.get_json()
        
        # Validações
        if 'nome' in data and not data['nome']:
            return jsonify({'success': False, 'message': 'Nome é obrigatório'}), 400
        
        if 'email' in data and not data['email']:
            return jsonify({'success': False, 'message': 'Email é obrigatório'}), 400
        
        if 'tipo' in data and data['tipo'] not in ['dentista', 'clinica']:
            return jsonify({'success': False, 'message': 'Tipo deve ser "dentista" ou "clinica"'}), 400
        
        # Verificar se email já existe (exceto o próprio cliente)
        if 'email' in data:
            cliente_existente = Cliente.query.filter(
                Cliente.email == data['email'],
                Cliente.id != cliente_id
            ).first()
            if cliente_existente:
                return jsonify({'success': False, 'message': 'Email já cadastrado'}), 400
        
        # Atualizar campos
        if 'nome' in data:
            cliente.nome = data['nome']
        if 'tipo' in data:
            cliente.tipo = data['tipo']
        if 'email' in data:
            cliente.email = data['email']
        if 'telefone' in data:
            cliente.telefone = data['telefone']
        if 'endereco' in data:
            cliente.endereco = data['endereco']
        if 'observacoes' in data:
            cliente.observacoes = data['observacoes']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cliente atualizado com sucesso',
            'data': cliente.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@cliente_bp.route('/clientes/<int:cliente_id>', methods=['DELETE'])
def excluir_cliente(cliente_id):
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        
        # Soft delete - apenas marcar como inativo
        cliente.ativo = False
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cliente excluído com sucesso'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@cliente_bp.route('/clientes/<int:cliente_id>/pacientes', methods=['GET'])
def listar_pacientes_cliente(cliente_id):
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        pacientes = [paciente.to_dict() for paciente in cliente.pacientes if paciente.ativo]
        
        return jsonify({
            'success': True,
            'data': pacientes
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@cliente_bp.route('/clientes/<int:cliente_id>/ordens-servico', methods=['GET'])
def listar_ordens_servico_cliente(cliente_id):
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        ordens = [ordem.to_dict() for ordem in cliente.ordens_servico]
        
        return jsonify({
            'success': True,
            'data': ordens
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

