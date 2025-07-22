from flask import Blueprint, request, jsonify
from src.database import db
from src.models.ordem_servico import OrdemServico
from src.models.cliente import Cliente
from src.models.paciente import Paciente
from src.models.material import Material
from src.models.financeiro import ContaReceber, ContaPagar
from src.models.etapa_producao import EtapaProducao
from src.models.agenda import EventoAgenda
from datetime import datetime, date, timedelta

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard/resumo', methods=['GET'])
def resumo_dashboard():
    try:
        hoje = date.today()
        inicio_mes = hoje.replace(day=1)
        
        # Estatísticas gerais
        total_clientes = Cliente.query.filter_by(ativo=True).count()
        total_pacientes = Paciente.query.filter_by(ativo=True).count()
        total_ordens = OrdemServico.query.count()
        
        # Ordens por status
        ordens_recebidas = OrdemServico.query.filter_by(status='recebido').count()
        ordens_producao = OrdemServico.query.filter_by(status='em_producao').count()
        ordens_finalizadas = OrdemServico.query.filter_by(status='finalizado').count()
        ordens_entregues = OrdemServico.query.filter_by(status='entregue').count()
        
        # Ordens atrasadas
        ordens_atrasadas = OrdemServico.query.filter(
            OrdemServico.data_prazo < datetime.now(),
            OrdemServico.status.in_(['recebido', 'em_producao'])
        ).count()
        
        # Financeiro
        total_a_receber = db.session.query(
            db.func.sum(ContaReceber.valor - ContaReceber.valor_pago)
        ).filter(ContaReceber.status == 'pendente').scalar() or 0
        
        total_a_pagar = db.session.query(
            db.func.sum(ContaPagar.valor - ContaPagar.valor_pago)
        ).filter(ContaPagar.status == 'pendente').scalar() or 0
        
        faturamento_mes = db.session.query(
            db.func.sum(ContaReceber.valor_pago)
        ).filter(
            ContaReceber.data_pagamento >= inicio_mes,
            ContaReceber.status == 'pago'
        ).scalar() or 0
        
        # Estoque crítico
        materiais_criticos = Material.query.filter(
            Material.quantidade_atual <= Material.quantidade_minima,
            Material.ativo == True
        ).count()
        
        # Eventos de hoje
        eventos_hoje = EventoAgenda.query.filter(
            db.func.date(EventoAgenda.data_inicio) == hoje,
            EventoAgenda.status == 'agendado'
        ).count()
        
        return jsonify({
            'success': True,
            'data': {
                'clientes': {
                    'total': total_clientes
                },
                'pacientes': {
                    'total': total_pacientes
                },
                'ordens_servico': {
                    'total': total_ordens,
                    'recebidas': ordens_recebidas,
                    'em_producao': ordens_producao,
                    'finalizadas': ordens_finalizadas,
                    'entregues': ordens_entregues,
                    'atrasadas': ordens_atrasadas
                },
                'financeiro': {
                    'total_a_receber': float(total_a_receber),
                    'total_a_pagar': float(total_a_pagar),
                    'faturamento_mes': float(faturamento_mes)
                },
                'estoque': {
                    'materiais_criticos': materiais_criticos
                },
                'agenda': {
                    'eventos_hoje': eventos_hoje
                }
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@dashboard_bp.route('/dashboard/graficos', methods=['GET'])
def graficos_dashboard():
    try:
        # Últimos 6 meses
        hoje = date.today()
        meses = []
        for i in range(6):
            mes_data = hoje.replace(day=1) - timedelta(days=30*i)
            meses.append(mes_data)
        meses.reverse()
        
        # Faturamento por mês
        faturamento_mensal = []
        for mes in meses:
            proximo_mes = (mes.replace(day=28) + timedelta(days=4)).replace(day=1)
            
            faturamento = db.session.query(
                db.func.sum(ContaReceber.valor_pago)
            ).filter(
                ContaReceber.data_pagamento >= mes,
                ContaReceber.data_pagamento < proximo_mes,
                ContaReceber.status == 'pago'
            ).scalar() or 0
            
            faturamento_mensal.append({
                'mes': mes.strftime('%Y-%m'),
                'valor': float(faturamento)
            })
        
        # Ordens por mês
        ordens_mensais = []
        for mes in meses:
            proximo_mes = (mes.replace(day=28) + timedelta(days=4)).replace(day=1)
            
            ordens = OrdemServico.query.filter(
                OrdemServico.data_entrada >= datetime.combine(mes, datetime.min.time()),
                OrdemServico.data_entrada < datetime.combine(proximo_mes, datetime.min.time())
            ).count()
            
            ordens_mensais.append({
                'mes': mes.strftime('%Y-%m'),
                'quantidade': ordens
            })
        
        # Tipos de prótese mais solicitados
        tipos_protese = db.session.query(
            OrdemServico.tipo_protese,
            db.func.count(OrdemServico.id).label('quantidade')
        ).group_by(OrdemServico.tipo_protese).order_by(
            db.func.count(OrdemServico.id).desc()
        ).limit(10).all()
        
        tipos_protese_data = [
            {'tipo': tipo, 'quantidade': quantidade}
            for tipo, quantidade in tipos_protese
        ]
        
        # Status das ordens
        status_ordens = db.session.query(
            OrdemServico.status,
            db.func.count(OrdemServico.id).label('quantidade')
        ).group_by(OrdemServico.status).all()
        
        status_ordens_data = [
            {'status': status, 'quantidade': quantidade}
            for status, quantidade in status_ordens
        ]
        
        return jsonify({
            'success': True,
            'data': {
                'faturamento_mensal': faturamento_mensal,
                'ordens_mensais': ordens_mensais,
                'tipos_protese': tipos_protese_data,
                'status_ordens': status_ordens_data
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@dashboard_bp.route('/dashboard/alertas', methods=['GET'])
def alertas_dashboard():
    try:
        alertas = []
        
        # Ordens atrasadas
        ordens_atrasadas = OrdemServico.query.filter(
            OrdemServico.data_prazo < datetime.now(),
            OrdemServico.status.in_(['recebido', 'em_producao'])
        ).count()
        
        if ordens_atrasadas > 0:
            alertas.append({
                'tipo': 'warning',
                'titulo': 'Ordens Atrasadas',
                'mensagem': f'{ordens_atrasadas} ordem(ns) de serviço em atraso',
                'link': '/ordens-servico?status=atrasadas'
            })
        
        # Materiais com estoque crítico
        materiais_criticos = Material.query.filter(
            Material.quantidade_atual <= Material.quantidade_minima,
            Material.ativo == True
        ).count()
        
        if materiais_criticos > 0:
            alertas.append({
                'tipo': 'danger',
                'titulo': 'Estoque Crítico',
                'mensagem': f'{materiais_criticos} material(is) com estoque baixo',
                'link': '/estoque/materiais?critico=true'
            })
        
        # Contas vencidas
        contas_vencidas = ContaReceber.query.filter(
            ContaReceber.data_vencimento < date.today(),
            ContaReceber.status == 'pendente'
        ).count()
        
        if contas_vencidas > 0:
            alertas.append({
                'tipo': 'warning',
                'titulo': 'Contas Vencidas',
                'mensagem': f'{contas_vencidas} conta(s) a receber vencida(s)',
                'link': '/financeiro/contas-receber?vencidas=true'
            })
        
        # Eventos de hoje
        hoje = date.today()
        eventos_hoje = EventoAgenda.query.filter(
            db.func.date(EventoAgenda.data_inicio) == hoje,
            EventoAgenda.status == 'agendado'
        ).count()
        
        if eventos_hoje > 0:
            alertas.append({
                'tipo': 'info',
                'titulo': 'Eventos Hoje',
                'mensagem': f'{eventos_hoje} evento(s) agendado(s) para hoje',
                'link': '/agenda/hoje'
            })
        
        return jsonify({
            'success': True,
            'data': alertas
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@dashboard_bp.route('/dashboard/atividades-recentes', methods=['GET'])
def atividades_recentes():
    try:
        limite = request.args.get('limite', 10, type=int)
        
        # Últimas ordens criadas
        ordens_recentes = OrdemServico.query.order_by(
            OrdemServico.data_entrada.desc()
        ).limit(limite).all()
        
        atividades = []
        
        for ordem in ordens_recentes:
            atividades.append({
                'tipo': 'ordem_criada',
                'titulo': f'Nova OS: {ordem.numero_os}',
                'descricao': f'Ordem de serviço criada para {ordem.paciente.nome}',
                'data': ordem.data_entrada.isoformat(),
                'link': f'/ordens-servico/{ordem.id}'
            })
        
        # Ordenar por data
        atividades.sort(key=lambda x: x['data'], reverse=True)
        
        return jsonify({
            'success': True,
            'data': atividades[:limite]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@dashboard_bp.route('/dashboard/producao', methods=['GET'])
def dashboard_producao():
    try:
        # Etapas por status
        etapas_pendentes = EtapaProducao.query.filter_by(status='pendente').count()
        etapas_andamento = EtapaProducao.query.filter_by(status='em_andamento').count()
        etapas_concluidas = EtapaProducao.query.filter_by(status='concluida').count()
        
        # Próximas etapas a vencer (próximos 3 dias)
        data_limite = datetime.now() + timedelta(days=3)
        
        etapas_proximas = EtapaProducao.query.join(OrdemServico).filter(
            EtapaProducao.status.in_(['pendente', 'em_andamento']),
            OrdemServico.data_prazo <= data_limite
        ).order_by(OrdemServico.data_prazo).limit(10).all()
        
        etapas_proximas_data = []
        for etapa in etapas_proximas:
            etapas_proximas_data.append({
                **etapa.to_dict(),
                'ordem_servico': etapa.ordem_servico.to_dict()
            })
        
        return jsonify({
            'success': True,
            'data': {
                'etapas_pendentes': etapas_pendentes,
                'etapas_andamento': etapas_andamento,
                'etapas_concluidas': etapas_concluidas,
                'proximas_etapas': etapas_proximas_data
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

