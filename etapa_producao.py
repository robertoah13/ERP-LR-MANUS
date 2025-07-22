from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class EtapaProducao(db.Model):
    __tablename__ = 'etapas_producao'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    ordem = db.Column(db.Integer, nullable=False)  # Ordem da etapa no processo
    
    # Status: 'pendente', 'em_andamento', 'concluida'
    status = db.Column(db.String(20), default='pendente')
    
    # Datas e tempos
    data_inicio = db.Column(db.DateTime, nullable=True)
    data_fim = db.Column(db.DateTime, nullable=True)
    tempo_estimado = db.Column(db.Integer, nullable=True)  # em minutos
    tempo_real = db.Column(db.Integer, nullable=True)  # em minutos
    
    observacoes = db.Column(db.Text, nullable=True)
    
    # Chaves estrangeiras
    ordem_servico_id = db.Column(db.Integer, db.ForeignKey('ordens_servico.id'), nullable=False)
    usuario_responsavel_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    def __repr__(self):
        return f'<EtapaProducao {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'ordem': self.ordem,
            'status': self.status,
            'data_inicio': self.data_inicio.isoformat() if self.data_inicio else None,
            'data_fim': self.data_fim.isoformat() if self.data_fim else None,
            'tempo_estimado': self.tempo_estimado,
            'tempo_real': self.tempo_real,
            'observacoes': self.observacoes,
            'ordem_servico_id': self.ordem_servico_id,
            'usuario_responsavel_id': self.usuario_responsavel_id
        }

