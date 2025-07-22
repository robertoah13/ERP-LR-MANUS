from src.database import db
from datetime import datetime



class MovimentacaoEstoque(db.Model):
    __tablename__ = 'movimentacoes_estoque'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Tipo: 'entrada' ou 'saida'
    tipo = db.Column(db.String(10), nullable=False)
    
    quantidade = db.Column(db.Numeric(10, 3), nullable=False)
    preco_unitario = db.Column(db.Numeric(10, 2), nullable=True)
    valor_total = db.Column(db.Numeric(10, 2), nullable=True)
    
    motivo = db.Column(db.String(100), nullable=True)  # 'compra', 'uso_producao', 'ajuste', 'perda', etc.
    observacoes = db.Column(db.Text, nullable=True)
    
    data_movimentacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Chaves estrangeiras
    material_id = db.Column(db.Integer, db.ForeignKey('materiais.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ordem_servico_id = db.Column(db.Integer, db.ForeignKey('ordens_servico.id'), nullable=True)  # Para saídas vinculadas a OS

    def __repr__(self):
        return f'<MovimentacaoEstoque {self.tipo} - {self.quantidade}>'

    def to_dict(self):
        return {
            'id': self.id,
            'tipo': self.tipo,
            'quantidade': float(self.quantidade) if self.quantidade else 0,
            'preco_unitario': float(self.preco_unitario) if self.preco_unitario else None,
            'valor_total': float(self.valor_total) if self.valor_total else None,
            'motivo': self.motivo,
            'observacoes': self.observacoes,
            'data_movimentacao': self.data_movimentacao.isoformat() if self.data_movimentacao else None,
            'material_id': self.material_id,
            'usuario_id': self.usuario_id,
            'ordem_servico_id': self.ordem_servico_id,
            'material_nome': self.material.nome if self.material else None
        }

