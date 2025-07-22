from .user import user_bp
from .cliente import cliente_bp
from .dashboard import dashboard_bp
from .estoque import estoque_bp
from .producao import producao_bp

all_blueprints = [user_bp, cliente_bp, dashboard_bp, estoque_bp, producao_bp]
