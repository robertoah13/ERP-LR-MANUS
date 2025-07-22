from flask import Blueprint, request, jsonify
from src.database import db
from src.models.material import Material
from src.models.movimentacao_estoque import MovimentacaoEstoque
from datetime import datetime

estoque_bp = Blueprint('estoque', __name__)

@estoque_bp.route('/estoque/materiais', methods=['GET'])
def listar_materiais():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        categoria = request.args.get('categoria', '')
        critico = request.args.get('critico', type=bool)
        
        query = Material.query
        
        if search:
            query = query.filter(
                db.or_(
                    Material.nome.contains(search),
                    Material.codigo.contains(search)
                )
            )
        
        if categoria:
            query = query.filter(Material.categoria == categoria)
        
        if critico:
            query = query.filter(Material.quantidade_atual <= Material.quantidade_minima)
        
        query = query.filter(Material.ativo == True)
        
        materiais = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'success': True,
            'data': [material.to_dict() for material in materiais.items],
            'pagination': {
                'page': page,
                'pages': materiais.pages,
                'per_page': per_page,
                'total': materiais.total
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@estoque_bp.route('/estoque/materiais', methods=['POST'])
def criar_material():
    try:
        data = request.get_json()
        
        # Validações
        if not data.get('nome'):
            return jsonify({'success': False, 'message': 'Nome é obrigatório'}), 400
        
        if not data.get('unidade_medida'):
            return jsonify({'success': False, 'message': 'Unidade de medida é obrigatória'}), 400
        
        # Verificar se código já existe (se fornecido)
        if data.get('codigo'):
            material_existente = Material.query.filter_by(codigo=data['codigo']).first()
            if material_existente:
                return jsonify({'success': False, 'message': 'Código já cadastrado'}), 400
        
        material = Material(
            nome=data['nome'],
            codigo=data.get('codigo'),
            descricao=data.get('descricao'),
            categoria=data.get('categoria'),
            unidade_medida=data['unidade_medida'],
            quantidade_atual=data.get('quantidade_atual', 0),
            quantidade_minima=data.get('quantidade_minima', 0),
            preco_unitario=data.get('preco_unitario'),
            fornecedor=data.get('fornecedor'),
            localizacao=data.get('localizacao'),
            data_validade=datetime.strptime(data['data_validade'], '%Y-%m-%d').date() if data.get('data_validade') else None
        )
        
        db.session.add(material)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Material criado com sucesso',
            'data': material.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@estoque_bp.route('/estoque/materiais/<int:material_id>', methods=['GET'])
def obter_material(material_id):
    try:
        material = Material.query.get_or_404(material_id)
        return jsonify({
            'success': True,
            'data': material.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@estoque_bp.route('/estoque/materiais/<int:material_id>', methods=['PUT'])
def atualizar_material(material_id):
    try:
        material = Material.query.get_or_404(material_id)
        data = request.get_json()
        
        # Validações
        if 'nome' in data and not data['nome']:
            return jsonify({'success': False, 'message': 'Nome é obrigatório'}), 400
        
        if 'unidade_medida' in data and not data['unidade_medida']:
            return jsonify({'success': False, 'message': 'Unidade de medida é obrigatória'}), 400
        
        # Verificar se código já existe (exceto o próprio material)
        if 'codigo' in data and data['codigo']:
            material_existente = Material.query.filter(
                Material.codigo == data['codigo'],
                Material.id != material_id
            ).first()
            if material_existente:
                return jsonify({'success': False, 'message': 'Código já cadastrado'}), 400
        
        # Atualizar campos
        if 'nome' in data:
            material.nome = data['nome']
        if 'codigo' in data:
            material.codigo = data['codigo']
        if 'descricao' in data:
            material.descricao = data['descricao']
        if 'categoria' in data:
            material.categoria = data['categoria']
        if 'unidade_medida' in data:
            material.unidade_medida = data['unidade_medida']
        if 'quantidade_minima' in data:
            material.quantidade_minima = data['quantidade_minima']
        if 'preco_unitario' in data:
            material.preco_unitario = data['preco_unitario']
        if 'fornecedor' in data:
            material.fornecedor = data['fornecedor']
        if 'localizacao' in data:
            material.localizacao = data['localizacao']
        if 'data_validade' in data:
            material.data_validade = datetime.strptime(data['data_validade'], '%Y-%m-%d').date() if data['data_validade'] else None
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Material atualizado com sucesso',
            'data': material.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@estoque_bp.route('/estoque/materiais/<int:material_id>/movimentacao', methods=['POST'])
def criar_movimentacao(material_id):
    try:
        material = Material.query.get_or_404(material_id)
        data = request.get_json()
        
        # Validações
        if not data.get('tipo') or data['tipo'] not in ['entrada', 'saida']:
            return jsonify({'success': False, 'message': 'Tipo deve ser "entrada" ou "saida"'}), 400
        
        if not data.get('quantidade') or data['quantidade'] <= 0:
            return jsonify({'success': False, 'message': 'Quantidade deve ser maior que zero'}), 400
        
        if not data.get('usuario_id'):
            return jsonify({'success': False, 'message': 'Usuário é obrigatório'}), 400
        
        # Verificar se há estoque suficiente para saída
        if data['tipo'] == 'saida' and material.quantidade_atual < data['quantidade']:
            return jsonify({'success': False, 'message': 'Estoque insuficiente'}), 400
        
        movimentacao = MovimentacaoEstoque(
            tipo=data['tipo'],
            quantidade=data['quantidade'],
            preco_unitario=data.get('preco_unitario'),
            valor_total=data.get('valor_total'),
            motivo=data.get('motivo'),
            observacoes=data.get('observacoes'),
            material_id=material_id,
            usuario_id=data['usuario_id'],
            ordem_servico_id=data.get('ordem_servico_id')
        )
        
        # Atualizar quantidade do material
        if data['tipo'] == 'entrada':
            material.quantidade_atual += data['quantidade']
        else:  # saida
            material.quantidade_atual -= data['quantidade']
        
        db.session.add(movimentacao)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Movimentação registrada com sucesso',
            'data': movimentacao.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@estoque_bp.route('/estoque/movimentacoes', methods=['GET'])
def listar_movimentacoes():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        material_id = request.args.get('material_id', type=int)
        tipo = request.args.get('tipo', '')
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        
        query = MovimentacaoEstoque.query
        
        if material_id:
            query = query.filter(MovimentacaoEstoque.material_id == material_id)
        
        if tipo:
            query = query.filter(MovimentacaoEstoque.tipo == tipo)
        
        if data_inicio:
            data_inicio_dt = datetime.strptime(data_inicio, '%Y-%m-%d')
            query = query.filter(MovimentacaoEstoque.data_movimentacao >= data_inicio_dt)
        
        if data_fim:
            data_fim_dt = datetime.strptime(data_fim, '%Y-%m-%d')
            query = query.filter(MovimentacaoEstoque.data_movimentacao <= data_fim_dt)
        
        query = query.order_by(MovimentacaoEstoque.data_movimentacao.desc())
        
        movimentacoes = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'success': True,
            'data': [mov.to_dict() for mov in movimentacoes.items],
            'pagination': {
                'page': page,
                'pages': movimentacoes.pages,
                'per_page': per_page,
                'total': movimentacoes.total
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@estoque_bp.route('/estoque/alertas', methods=['GET'])
def alertas_estoque():
    try:
        # Materiais com estoque crítico
        materiais_criticos = Material.query.filter(
            Material.quantidade_atual <= Material.quantidade_minima,
            Material.ativo == True
        ).all()
        
        # Materiais próximos ao vencimento (30 dias)
        from datetime import timedelta
        data_limite = datetime.now().date() + timedelta(days=30)
        
        materiais_vencimento = Material.query.filter(
            Material.data_validade <= data_limite,
            Material.data_validade.isnot(None),
            Material.ativo == True
        ).all()
        
        return jsonify({
            'success': True,
            'data': {
                'materiais_criticos': [material.to_dict() for material in materiais_criticos],
                'materiais_vencimento': [material.to_dict() for material in materiais_vencimento]
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@estoque_bp.route('/estoque/relatorio', methods=['GET'])
def relatorio_estoque():
    try:
        # Valor total do estoque
        materiais = Material.query.filter(Material.ativo == True).all()
        valor_total = sum(
            (material.quantidade_atual * material.preco_unitario) 
            for material in materiais 
            if material.quantidade_atual and material.preco_unitario
        )
        
        # Materiais mais utilizados (últimos 30 dias)
        from datetime import timedelta
        data_limite = datetime.utcnow() - timedelta(days=30)
        
        movimentacoes_saida = MovimentacaoEstoque.query.filter(
            MovimentacaoEstoque.tipo == 'saida',
            MovimentacaoEstoque.data_movimentacao >= data_limite
        ).all()
        
        uso_por_material = {}
        for mov in movimentacoes_saida:
            if mov.material_id not in uso_por_material:
                uso_por_material[mov.material_id] = {
                    'material_nome': mov.material.nome,
                    'quantidade_total': 0
                }
            uso_por_material[mov.material_id]['quantidade_total'] += mov.quantidade
        
        # Ordenar por quantidade utilizada
        materiais_mais_usados = sorted(
            uso_por_material.values(),
            key=lambda x: x['quantidade_total'],
            reverse=True
        )[:10]
        
        return jsonify({
            'success': True,
            'data': {
                'valor_total_estoque': float(valor_total),
                'total_materiais': len(materiais),
                'materiais_criticos': len([m for m in materiais if m.quantidade_atual <= m.quantidade_minima]),
                'materiais_mais_usados': materiais_mais_usados
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

