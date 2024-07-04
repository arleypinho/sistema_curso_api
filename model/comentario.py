from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from model import Base

class Comentario(Base):
    __tablename__ = 'comentario'

    id = Column(Integer, primary_key=True)
    texto = Column(String(4000))
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o comentário e um curso.
    # Aqui está sendo definida a coluna 'curso' que vai guardar
    # a referência ao curso, a chave estrangeira que relaciona
    # um curso ao comentário.
    curso_id = Column(Integer, ForeignKey("cursos.pk_curso"), nullable=False)

    def __init__(self, texto: str, curso_id: int, data_insercao: Union[DateTime, None] = None):
        """
        Cria um Comentário

        Arguments:
            texto: o texto de um comentário.
            curso_id: id do curso relacionado ao comentário.
            data_insercao: data de quando o comentário foi feito ou inserido à base.
        """
        self.texto = texto
        self.curso_id = curso_id
        if data_insercao:
            self.data_insercao = data_insercao
