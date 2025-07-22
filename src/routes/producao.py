from flask import Blueprint, request, jsonify
from src.database import db
from src.models.etapa_producao import EtapaProducao
from src.models.ordem_servico import OrdemServico
from src.models.user import User
from datetime import datetime

producao_bp = Blueprint('producao', __name__)

@producao_bp.route('/producao/etapas', methods=['GET'])
def listar_etapas_producao():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status', '')
        usuario_id = request.args.get('usuario_id', type=int)
        ordem_servico_id = request.args.get('ordem_servico_id', type=int)
        
        query = EtapaProducao.query.join(OrdemServico)
        
        if status:
            query = query.filter(EtapaProducao.status == status)
        
        if usuario_id:
            query = query.filter(EtapaProducao.usuario_responsavel_id == usuario_id)
        
        if ordem_servico_id:
            query = query.filter(EtapaProducao.ordem_servico_id == ordem_servico_id)
        
        query = query.order_by(EtapaProducao.ordem)
        
        etapas = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'success': True,
            'data': [etapa.to_dict() for etapa in etapas.items],
            'pagination': {
                'page': page,
                'pages': etapas.pages,
                'per_page': per_page,
                'total': etapas.total
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@producao_bp.route('/producao/etapas/<int:etapa_id>/iniciar', methods=['PUT'])
def iniciar_etapa(etapa_id):
    try:
        etapa = EtapaProducao.query.get_or_404(etapa_id)
        data = request.get_json()
        
        if etapa.status != 'pendente':
            return jsonify({'success': False, 'message': 'Etapa já foi iniciada'}), 400
        
        etapa.status = 'em_andamento'
        etapa.data_inicio = datetime.utcnow()
        
        if data.get('usuario_responsavel_id'):
            etapa.usuario_responsavel_id = data['usuario_responsavel_id']
        
        # Atualizar status da OS para "em_producao" se for a primeira etapa
        if etapa.ordem == 1:
            etapa.ordem_servico.status = 'em_producao'
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Etapa iniciada com sucesso',
            'data': etapa.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@producao_bp.route('/producao/etapas/<int:etapa_id>/finalizar', methods=['PUT'])
def finalizar_etapa(etapa_id):
    try:
        etapa = EtapaProducao.query.get_or_404(etapa_id)
        data = request.get_json()
        
        if etapa.status != 'em_andamento':
            return jsonify({'success': False, 'message': 'Etapa não está em andamento'}), 400
        
        etapa.status = 'concluida'
        etapa.data_fim = datetime.utcnow()
        
        # Calcular tempo real
        if etapa.data_inicio:
            tempo_real = (etapa.data_fim - etapa.data_inicio).total_seconds() / 60
            etapa.tempo_real = int(tempo_real)
        
        if data.get('observacoes'):
            etapa.observacoes = data['observacoes']
        
        # Verificar se todas as etapas foram concluídas
        etapas_ordem = EtapaProducao.query.filter_by(
            ordem_servico_id=etapa.ordem_servico_id
        ).all()
        
        todas_concluidas = all(e.status == 'concluida' for e in etapas_ordem)
        
        if todas_concluidas:
            etapa.ordem_servico.status = 'finalizado'
            etapa.ordem_servico.data_finalizacao = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Etapa finalizada com sucesso',
            'data': etapa.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@producao_bp.route('/producao/etapas/<int:etapa_id>', methods=['PUT'])
def atualizar_etapa(etapa_id):
    try:
        etapa = EtapaProducao.query.get_or_404(etapa_id)
        data = request.get_json()
        
        # Atualizar campos permitidos
        if 'nome' in data:
            etapa.nome = data['nome']
        if 'descricao' in data:
            etapa.descricao = data['descricao']
        if 'tempo_estimado' in data:
            etapa.tempo_estimado = data['tempo_estimado']
        if 'observacoes' in data:
            etapa.observacoes = data['observacoes']
        if 'usuario_responsavel_id' in data:
            etapa.usuario_responsavel_id = data['usuario_responsavel_id']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Etapa atualizada com sucesso',
            'data': etapa.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@producao_bp.route('/producao/kanban', methods=['GET'])
def kanban_producao():
    try:
        # Buscar etapas agrupadas por status
        etapas_pendentes = EtapaProducao.query.filter_by(status='pendente').join(OrdemServico).all()
        etapas_andamento = EtapaProducao.query.filter_by(status='em_andamento').join(OrdemServico).all()
        etapas_concluidas = EtapaProducao.query.filter_by(status='concluida').join(OrdemServico).all()
        
        return jsonify({
            'success': True,
            'data': {
                'pendentes': [etapa.to_dict() for etapa in etapas_pendentes],
                'em_andamento': [etapa.to_dict() for etapa in etapas_andamento],
                'concluidas': [etapa.to_dict() for etapa in etapas_concluidas]
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@producao_bp.route('/producao/estatisticas', methods=['GET'])
def estatisticas_producao():
    try:
        # Estatísticas gerais
        total_etapas = EtapaProducao.query.count()
        etapas_pendentes = EtapaProducao.query.filter_by(status='pendente').count()
        etapas_andamento = EtapaProducao.query.filter_by(status='em_andamento').count()
        etapas_concluidas = EtapaProducao.query.filter_by(status='concluida').count()
        
        # Tempo médio por tipo de etapa
        etapas_com_tempo = EtapaProducao.query.filter(
            EtapaProducao.tempo_real.isnot(None)
        ).all()
        
        tempos_por_tipo = {}
        for etapa in etapas_com_tempo:
            if etapa.nome not in tempos_por_tipo:
                tempos_por_tipo[etapa.nome] = []
            tempos_por_tipo[etapa.nome].append(etapa.tempo_real)
        
        tempo_medio_por_tipo = {}
        for tipo, tempos in tempos_por_tipo.items():
            tempo_medio_por_tipo[tipo] = sum(tempos) / len(tempos) if tempos else 0
        
        # Produtividade por usuário (últimos 30 dias)
        from datetime import timedelta
        data_limite = datetime.utcnow() - timedelta(days=30)
        
        etapas_recentes = EtapaProducao.query.filter(
            EtapaProducao.data_fim >= data_limite,
            EtapaProducao.status == 'concluida'
        ).all()
        
        produtividade_usuarios = {}
        for etapa in etapas_recentes:
            if etapa.usuario_responsavel_id:
                if etapa.usuario_responsavel_id not in produtividade_usuarios:
                    produtividade_usuarios[etapa.usuario_responsavel_id] = 0
                produtividade_usuarios[etapa.usuario_responsavel_id] += 1
        
        return jsonify({
            'success': True,
            'data': {
                'total_etapas': total_etapas,
                'etapas_pendentes': etapas_pendentes,
                'etapas_andamento': etapas_andamento,
                'etapas_concluidas': etapas_concluidas,
                'tempo_medio_por_tipo': tempo_medio_por_tipo,
                'produtividade_usuarios': produtividade_usuarios
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@producao_bp.route('/producao/cronograma', methods=['GET'])
def cronograma_producao():
    try:
        usuario_id = request.args.get('usuario_id', type=int)
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        
        query = EtapaProducao.query.join(OrdemServico)
        
        if usuario_id:
            query = query.filter(EtapaProducao.usuario_responsavel_id == usuario_id)
        
        if data_inicio:
            data_inicio_dt = datetime.strptime(data_inicio, '%Y-%m-%d')
            query = query.filter(OrdemServico.data_prazo >= data_inicio_dt)
        
        if data_fim:
            data_fim_dt = datetime.strptime(data_fim, '%Y-%m-%d')
            query = query.filter(OrdemServico.data_prazo <= data_fim_dt)
        
        etapas = query.filter(
            EtapaProducao.status.in_(['pendente', 'em_andamento'])
        ).order_by(OrdemServico.data_prazo).all()
        
        cronograma = []
        for etapa in etapas:
            cronograma.append({
                **etapa.to_dict(),
                'ordem_servico': etapa.ordem_servico.to_dict()
            })
        
        return jsonify({
            'success': True,
            'data': cronograma
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

