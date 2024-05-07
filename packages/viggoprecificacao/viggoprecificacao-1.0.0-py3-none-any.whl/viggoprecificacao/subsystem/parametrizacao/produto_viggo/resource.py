from enum import Enum
from viggocore.database import db
from viggocore.common.subsystem import entity


class PRODUTO_VIGGO_TIPO_LOCACAO(Enum):
    PROPRIO = 'PROPRIO'
    DIRETO_FABRICANTE = 'DIRETO_FABRICANTE'


class PRODUTO_VIGGO_TIPO(Enum):
    VENDA = 'VENDA'
    LOCACAO = 'LOCACAO'


class ProdutoViggo(entity.Entity, db.Model):

    attributes = ['nome', 'descricao', 'valor', 'modelo', 'identificador_prod',
                  'config_acessorios', 'fabricante', 'qtd',
                  'qtd_dias_p_entrega', 'tem_garantia', 'tipo', 'tipo_locacao',
                  'taxa_locacao_fabricante']
    read_only_attributes = ['qtd_disponivel', 'qtd_uso']
    attributes += entity.Entity.attributes

    nome = db.Column(db.String(60), nullable=False)
    descricao = db.Column(db.String(250), nullable=False)
    valor = db.Column(db.Numeric(17, 4), nullable=True)
    modelo = db.Column(db.String(60), nullable=True)
    identificador_prod = db.Column(db.String(50), nullable=True)
    config_acessorios = db.Column(db.String(1000), nullable=True)
    fabricante = db.Column(db.String(250), nullable=True)
    qtd = db.Column(db.Numeric(17, 4), nullable=True)
    qtd_dias_p_entrega = db.Column(db.Numeric(4), nullable=True)
    tem_garantia = db.Column(db.Boolean(), nullable=True)
    tipo = db.Column(db.Enum(PRODUTO_VIGGO_TIPO), nullable=False)
    tipo_locacao = db.Column(db.Enum(PRODUTO_VIGGO_TIPO_LOCACAO),
                             nullable=True)
    taxa_locacao_fabricante = db.Column(db.Numeric(17, 4),
                                        nullable=True)

    def __init__(self, id, nome, descricao, valor, modelo, identificador_prod,
                 config_acessorios, fabricante, qtd, qtd_dias_p_entrega,
                 tem_garantia, tipo, tipo_locacao, taxa_locacao_fabricante,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.nome = nome
        self.descricao = descricao
        self.valor = valor
        self.modelo = modelo
        self.identificador_prod = identificador_prod
        self.config_acessorios = config_acessorios
        self.fabricante = fabricante
        self.qtd = qtd
        self.qtd_dias_p_entrega = qtd_dias_p_entrega
        self.tem_garantia = tem_garantia
        self.tipo = tipo
        self.tipo_locacao = tipo_locacao
        self.taxa_locacao_fabricante = taxa_locacao_fabricante

    @classmethod
    def individual(cls):
        return 'produto_viggo'

    @classmethod
    def collection(cls):
        return 'produto_viggos'
