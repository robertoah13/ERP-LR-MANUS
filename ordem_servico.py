from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class OrdemServico(db.Model):
    __tablename__ = 'ordens_servico'
    
    id = db.Column(db.Integer, primary_key=True)
    numero_os = db.Column(db.String(20), unique=True, nullable=False)
    tipo_protese = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    materiais = db.Column(db.Text, nullable=True)
    cor = db.Column(db.String(50), nullable=True)
    observacoes = db.Column(db.Text, nullable=True)
    
    # Datas
    data_entrada = db.Column(db.DateTime, default=datetime.utcnow)
    data_prazo = db.Column(db.DateTime, nullable=False)
    data_finalizacao = db.Column(db.DateTime, nullable=True)
    data_entrega = db.Column(db.DateTime, nullable=True)
    
    # Status: 'recebido', 'em_producao', 'finalizado', 'entregue'
    status = db.Column(db.String(20), default='recebido')
    
    # Valores
    valor = db.Column(db.Numeric(10, 2), nullable=True)
    valor_pago = db.Column(db.Numeric(10, 2), default=0)
    
    # Chaves estrangeiras
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    usuario_responsavel_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Relacionamentos
    etapas_producao = db.relationship('EtapaProducao', backref='ordem_servico', lazy=True, cascade='all, delete-orphan')
    anexos = db.relationship('AnexoOS', backref='ordem_servico', lazy=True, cascade='all, delete-orphan')
    movimentacoes_estoque = db.relationship('MovimentacaoEstoque', backref='ordem_servico', lazy=True)

    def __repr__(self):
        return f'<OrdemServico {self.numero_os}>'

    def to_dict(self):
        return {
            'id': self.id,
            'numero_os': self.numero_os,
            'tipo_protese': self.tipo_protese,
            'descricao': self.descricao,
            'materiais': self.materiais,
            'cor': self.cor,
            'observacoes': self.observacoes,
            'data_entrada': self.data_entrada.isoformat() if self.data_entrada else None,
            'data_prazo': self.data_prazo.isoformat() if self.data_prazo else None,
            'data_finalizacao': self.data_finalizacao.isoformat() if self.data_finalizacao else None,
            'data_entrega': self.data_entrega.isoformat() if self.data_entrega else None,
            'status': self.status,
            'valor': float(self.valor) if self.valor else None,
            'valor_pago': float(self.valor_pago) if self.valor_pago else 0,
            'cliente_id': self.cliente_id,
            'paciente_id': self.paciente_id,
            'usuario_responsavel_id': self.usuario_responsavel_id,
            'cliente_nome': self.cliente.nome if self.cliente else None,
            'paciente_nome': self.paciente.nome if self.paciente else None
        }

