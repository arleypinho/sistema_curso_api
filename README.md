## API de Gerenciamento de Cursos com Flask ##

Este é um aplicativo Flask que fornece uma API para gerenciar cursos, incluindo adição, busca, remoção de cursos e adição de comentários aos cursos existentes como se fosse uma espécia de Cadastro de currículos.

## Funcionalidades
 - Adicionar Curso: Endpoint para adicionar um novo curso à base de dados.
 - Listar Cursos: Endpoint para buscar todos os cursos cadastrados na base.
 - Buscar Curso por ID: Endpoint para buscar um curso específico pelo seu ID.
 - Remover Curso por ID: Endpoint para remover um curso existente pelo seu ID.
 - Adicionar Comentário: Endpoint para adicionar um comentário a um curso existente pelo seu ID.


## Como Executar
Instalação de Dependências:

# Como executar 


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.

Após iniciar o aplicativo, você pode acessar a documentação da API para explorar e testar os endpoints disponíveis.
Documentação disponível em /openapi, escolha entre Swagger, Redoc ou RapiDoc.


## Estrutura do Código
 - app.py: Define os endpoints da API usando Flask e Flask-OpenAPI3 para documentação.
 - model.py: Contém definições de modelos SQLAlchemy para Curso e Comentario.
 - schemas.py: Define os schemas de entrada e saída para os endpoints da API.
 - logger.py: Configuração do logger para registrar eventos e erros do aplicativo.


## Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para abrir questionamentos para reportar bugs ou propor melhorias.


