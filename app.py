from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect

from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Curso, Comentario
from logger import logger
from schemas import *
from flask_cors import CORS
from schemas import apresenta_curso
from schemas import CursoViewSchema
from schemas import CursoSchema
from schemas import ListagemCursosSchema
from schemas import apresenta_cursos
from schemas import CursoBuscaSchema
from schemas import CursoDelSchema


info = Info(title="API de Gerenciamento de Cursos", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
curso_tag = Tag(name="Curso", description="Adição, visualização e remoção de cursos à base")
comentario_tag = Tag(name="Comentario", description="Adição de um comentário a um curso cadastrado na base")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect('/openapi')

@app.post('/curso', tags=[curso_tag],
          responses={"200": CursoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_curso(form: CursoSchema):
    """Adiciona um novo Curso à base de dados

    Retorna uma representação dos cursos e comentários associados.
    """
    curso = Curso(
        nome_curso=form.nome_curso,
        nivel_curso=form.nivel_curso,
        instituicao=form.instituicao,
        ano_inicio=form.ano_inicio,
        ano_termino=form.ano_termino,
        situacao=form.situacao,
        valor=form.valor)
    logger.debug(f"Adicionando curso de nome: '{curso.nome_curso}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando curso
        session.add(curso)
        # efetivando o comando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado curso de nome: '{curso.nome_curso}'")
        return apresenta_curso(curso), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Curso de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar curso '{curso.nome_curso}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo Curso :/"
        logger.warning(f"Erro ao adicionar curso '{curso.nome_curso}', {error_msg}")
        return {"message": error_msg}, 400

@app.get('/cursos', tags=[curso_tag],
         responses={"200": ListagemCursosSchema, "404": ErrorSchema})
def get_cursos():
    """Faz a busca por todos os Cursos cadastrados

    Retorna uma representação da listagem de cursos.
    """
    logger.debug(f"Coletando cursos")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    cursos = session.query(Curso).all()

    if not cursos:
        # se não há cursos cadastrados
        return {"cursos": []}, 200
    else:
        logger.debug(f"%d cursos encontrados" % len(cursos))
        # retorna a representação de curso
        return apresenta_cursos(cursos), 200

@app.get('/curso', tags=[curso_tag],
         responses={"200": CursoViewSchema, "404": ErrorSchema})
def get_curso(query: CursoBuscaSchema):
    """Faz a busca por um Curso a partir do id do curso

    Retorna uma representação dos cursos e comentários associados.
    """
    curso_id = query.id
    logger.debug(f"Coletando dados sobre curso #{curso_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    curso = session.query(Curso).filter(Curso.id == curso_id).first()

    if not curso:
        # se o curso não foi encontrado
        error_msg = "Curso não encontrado na base :/"
        logger.warning(f"Erro ao buscar curso '{curso_id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Curso encontrado: '{curso.nome_curso}'")
        # retorna a representação de curso
        return apresenta_curso(curso), 200

@app.delete('/curso', tags=[curso_tag],
            responses={"200": CursoDelSchema, "404": ErrorSchema})
def del_curso(query: CursoBuscaSchema):
    """Deleta um Curso a partir do ID informado

    Retorna uma mensagem de confirmação da remoção.
    """
    curso_id = query.id
    logger.debug(f"Deletando dados sobre curso #{curso_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Curso).filter(Curso.id == curso_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado curso #{curso_id}")
        return {"message": "Curso removido", "id": curso_id}
    else:
        # se o curso não foi encontrado
        error_msg = "Curso não encontrado na base :/"
        logger.warning(f"Erro ao deletar curso #'{curso_id}', {error_msg}")
        return {"message": error_msg}, 404

@app.post('/comentario', tags=[comentario_tag],
          responses={"200": CursoViewSchema, "404": ErrorSchema})
def add_comentario(form: ComentarioSchema):
    """Adiciona de um novo comentário a um curso cadastrado na base identificado pelo id

    Retorna uma representação dos cursos e comentários associados.
    """
    curso_id = form.curso_id
    logger.debug(f"Adicionando comentários ao curso #{curso_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo curso
    curso = session.query(Curso).filter(Curso.id == curso_id).first()

    if not curso:
        # se curso não encontrado
        error_msg = "Curso não encontrado na base :/"
        logger.warning(f"Erro ao adicionar comentário ao curso '{curso_id}', {error_msg}")
        return {"message": error_msg}, 404

    # criando o comentário
    texto = form.texto
    comentario = Comentario(texto=texto, curso_id=curso_id)

    # adicionando o comentário ao curso
    curso.adiciona_comentario(comentario)
    session.commit()

    logger.debug(f"Adicionado comentário ao curso #{curso_id}")

    # retorna a representação de curso
    return apresenta_curso(curso), 200
