from pydantic import BaseModel
from typing import Optional, List
from model.curso import Curso
from model.comentario import Comentario


class CursoSchema(BaseModel):
    """ Define como um novo curso a ser inserido deve ser representado. """
    nome_curso: str
    nivel_curso: str
    instituicao: str
    ano_inicio: int
    ano_termino: Optional[int]
    situacao: str
    valor: float


class CursoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca por um curso. Que será feita apenas com base no ID do curso. """
    id: int


class ListagemCursosSchema(BaseModel):
    """ Define como uma listagem de cursos será retornada. """
    cursos: List[CursoSchema]


def apresenta_cursos(cursos: List[Curso]):
    """ Retorna uma representação dos cursos seguindo o schema definido em CursoViewSchema. """
    result = []
    for curso in cursos:
        result.append({
            "id": curso.id,
            "nome_curso": curso.nome_curso,
            "nivel_curso": curso.nivel_curso,
            "instituicao": curso.instituicao,
            "ano_inicio": curso.ano_inicio,
            "ano_termino": curso.ano_termino,
            "situacao": curso.situacao,
            "valor": curso.valor,
        })
    return {"cursos": result}


class CursoViewSchema(BaseModel):
    """ Define como um curso será retornado: curso + comentários. """
    id: int
    nome_curso: str
    nivel_curso: str
    instituicao: str
    ano_inicio: int
    ano_termino: Optional[int]
    situacao: str
    valor: float
    total_comentarios: int
    comentarios: List["ComentarioSchema"]


class CursoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição de remoção. """
    message: str
    id: int


def apresenta_curso(curso: Curso):
    """ Retorna uma representação do curso seguindo o schema definido em CursoViewSchema. """
    return {
        "id": curso.id,
        "nome_curso": curso.nome_curso,
        "nivel_curso": curso.nivel_curso,
        "instituicao": curso.instituicao,
        "ano_inicio": curso.ano_inicio,
        "ano_termino": curso.ano_termino,
        "situacao": curso.situacao,
        "valor": curso.valor,
        "total_comentarios": len(curso.comentarios),
        "comentarios": [{"texto": c.texto} for c in curso.comentarios]
    }


class ComentarioSchema(BaseModel):
    """ Define como um novo comentário a ser inserido deve ser representado. """
    texto: str
    curso_id: int


class ComentarioViewSchema(BaseModel):
    """ Define como um comentário será retornado. """
    id: int
    texto: str
    data_insercao: Optional[str]


def apresenta_comentario(comentario: Comentario):
    """ Retorna uma representação do comentário seguindo o schema definido em ComentarioViewSchema. """
    return {
        "id": comentario.id,
        "texto": comentario.texto,
        "data_insercao": comentario.data_insercao.strftime("%Y-%m-%d %H:%M:%S") if comentario.data_insercao else None
    }
