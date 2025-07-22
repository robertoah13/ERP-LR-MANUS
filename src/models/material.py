from src.database import db
from datetime import datetime



class Material(db.Model):
    __tablename__ = 'materiais'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.String(50), unique=True, nullable=True)
    descricao = db.Column(db.Text, nullable=True)
    categoria = db.Column(db.String(50), nullable=True)
    unidade_medida = db.Column(db.String(20), nullable=False)  # 'kg', 'g', 'ml', 'unidade', etc.
    
    # Estoque
    quantidade_atual = db.Column(db.Numeric(10, 3), default=0)
    quantidade_minima = db.Column(db.Numeric(10, 3), default=0)
    
    # Preços
    preco_unitario = db.Column(db.Numeric(10, 2), nullable=True)
    
    # Fornecedor
    fornecedor = db.Column(db.String(100), nullable=True)
    
    # Localização no estoque
    localizacao = db.Column(db.String(100), nullable=True)
    
    # Validade
    data_validade = db.Column(db.Date, nullable=True)
    
    ativo = db.Column(db.Boolean, default=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    movimentacoes = db.relationship('MovimentacaoEstoque', backref='material', lazy=True)

    def __repr__(self):
        return f'<Material {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'codigo': self.codigo,
            'descricao': self.descricao,
            'categoria': self.categoria,
            'unidade_medida': self.unidade_medida,
            'quantidade_atual': float(self.quantidade_atual) if self.quantidade_atual else 0,
            'quantidade_minima': float(self.quantidade_minima) if self.quantidade_minima else 0,
            'preco_unitario': float(self.preco_unitario) if self.preco_unitario else None,
            'fornecedor': self.fornecedor,
            'localizacao': self.localizacao,
            'data_validade': self.data_validade.isoformat() if self.data_validade else None,
            'ativo': self.ativo,
            'data_cadastro': self.data_cadastro.isoformat() if self.data_cadastro else None,
            'estoque_critico': self.quantidade_atual <= self.quantidade_minima if self.quantidade_atual and self.quantidade_minima else False
        }

