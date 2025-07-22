from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class EventoAgenda(db.Model):
    __tablename__ = 'eventos_agenda'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    
    # Tipo: 'entrega', 'coleta', 'visita', 'manutencao', 'outro'
    tipo = db.Column(db.String(20), nullable=False)
    
    data_inicio = db.Column(db.DateTime, nullable=False)
    data_fim = db.Column(db.DateTime, nullable=True)
    
    # Status: 'agendado', 'realizado', 'cancelado'
    status = db.Column(db.String(20), default='agendado')
    
    observacoes = db.Column(db.Text, nullable=True)
    
    # Chaves estrangeiras
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=True)
    ordem_servico_id = db.Column(db.Integer, db.ForeignKey('ordens_servico.id'), nullable=True)
    usuario_responsavel_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    def __repr__(self):
        return f'<EventoAgenda {self.titulo}>'

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'tipo': self.tipo,
            'data_inicio': self.data_inicio.isoformat() if self.data_inicio else None,
            'data_fim': self.data_fim.isoformat() if self.data_fim else None,
            'status': self.status,
            'observacoes': self.observacoes,
            'cliente_id': self.cliente_id,
            'ordem_servico_id': self.ordem_servico_id,
            'usuario_responsavel_id': self.usuario_responsavel_id,
            'cliente_nome': self.cliente.nome if self.cliente else None,
            'ordem_servico_numero': self.ordem_servico.numero_os if self.ordem_servico else None
        }

