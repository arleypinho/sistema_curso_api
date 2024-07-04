from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship

from model import Base, Comentario

class Curso(Base):
    __tablename__ = 'cursos'

    id = Column("pk_curso", Integer, primary_key=True)
    nome_curso = Column(String(140), unique=True)
    nivel_curso = Column(String(20), nullable=False)
    instituicao = Column(String(140))
    ano_inicio = Column(Integer, nullable=False)
    ano_termino = Column(Integer)
    situacao = Column(String, nullable=False)
    valor = Column(Float)

    # Definição do relacionamento entre o curso e o comentário.
    comentarios = relationship("Comentario")

    def __init__(self, nome_curso, nivel_curso, instituicao, ano_inicio, ano_termino, situacao, valor):
        self.nome_curso = nome_curso
        self.nivel_curso = nivel_curso
        self.instituicao = instituicao
        self.ano_inicio = ano_inicio
        self.ano_termino = ano_termino
        self.situacao = situacao
        self.valor = valor

    def adiciona_comentario(self, comentario: Comentario):
        """ Adiciona um novo comentário ao Curso """
        self.comentarios.append(comentario)
