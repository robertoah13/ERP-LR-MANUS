from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class AnexoOS(db.Model):
    __tablename__ = 'anexos_os'
    
    id = db.Column(db.Integer, primary_key=True)
    nome_arquivo = db.Column(db.String(255), nullable=False)
    nome_original = db.Column(db.String(255), nullable=False)
    tipo_arquivo = db.Column(db.String(50), nullable=True)  # 'imagem', 'documento', 'radiografia', etc.
    tamanho = db.Column(db.Integer, nullable=True)  # em bytes
    caminho = db.Column(db.String(500), nullable=False)
    
    descricao = db.Column(db.Text, nullable=True)
    data_upload = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Chaves estrangeiras
    ordem_servico_id = db.Column(db.Integer, db.ForeignKey('ordens_servico.id'), nullable=False)
    usuario_upload_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<AnexoOS {self.nome_original}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome_arquivo': self.nome_arquivo,
            'nome_original': self.nome_original,
            'tipo_arquivo': self.tipo_arquivo,
            'tamanho': self.tamanho,
            'caminho': self.caminho,
            'descricao': self.descricao,
            'data_upload': self.data_upload.isoformat() if self.data_upload else None,
            'ordem_servico_id': self.ordem_servico_id,
            'usuario_upload_id': self.usuario_upload_id
        }

