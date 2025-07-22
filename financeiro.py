from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ContaReceber(db.Model):
    __tablename__ = 'contas_receber'
    
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    valor_pago = db.Column(db.Numeric(10, 2), default=0)
    
    data_vencimento = db.Column(db.Date, nullable=False)
    data_pagamento = db.Column(db.Date, nullable=True)
    
    # Status: 'pendente', 'pago', 'vencido'
    status = db.Column(db.String(20), default='pendente')
    
    observacoes = db.Column(db.Text, nullable=True)
    
    # Chaves estrangeiras
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    ordem_servico_id = db.Column(db.Integer, db.ForeignKey('ordens_servico.id'), nullable=True)

    def __repr__(self):
        return f'<ContaReceber {self.descricao}>'

    def to_dict(self):
        return {
            'id': self.id,
            'descricao': self.descricao,
            'valor': float(self.valor) if self.valor else 0,
            'valor_pago': float(self.valor_pago) if self.valor_pago else 0,
            'valor_pendente': float(self.valor - self.valor_pago) if self.valor and self.valor_pago else float(self.valor) if self.valor else 0,
            'data_vencimento': self.data_vencimento.isoformat() if self.data_vencimento else None,
            'data_pagamento': self.data_pagamento.isoformat() if self.data_pagamento else None,
            'status': self.status,
            'observacoes': self.observacoes,
            'cliente_id': self.cliente_id,
            'ordem_servico_id': self.ordem_servico_id,
            'cliente_nome': self.cliente.nome if self.cliente else None
        }

class ContaPagar(db.Model):
    __tablename__ = 'contas_pagar'
    
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    valor_pago = db.Column(db.Numeric(10, 2), default=0)
    
    data_vencimento = db.Column(db.Date, nullable=False)
    data_pagamento = db.Column(db.Date, nullable=True)
    
    # Status: 'pendente', 'pago', 'vencido'
    status = db.Column(db.String(20), default='pendente')
    
    categoria = db.Column(db.String(50), nullable=True)  # 'material', 'equipamento', 'servico', etc.
    fornecedor = db.Column(db.String(100), nullable=True)
    observacoes = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<ContaPagar {self.descricao}>'

    def to_dict(self):
        return {
            'id': self.id,
            'descricao': self.descricao,
            'valor': float(self.valor) if self.valor else 0,
            'valor_pago': float(self.valor_pago) if self.valor_pago else 0,
            'valor_pendente': float(self.valor - self.valor_pago) if self.valor and self.valor_pago else float(self.valor) if self.valor else 0,
            'data_vencimento': self.data_vencimento.isoformat() if self.data_vencimento else None,
            'data_pagamento': self.data_pagamento.isoformat() if self.data_pagamento else None,
            'status': self.status,
            'categoria': self.categoria,
            'fornecedor': self.fornecedor,
            'observacoes': self.observacoes
        }

