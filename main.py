from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Inicialização com metadados personalizados da sua API de Tarefas
app = FastAPI(
    title="API de Tarefas",
    description="Essa é uma API de tarefas, onde você pode adicionar, atualizar status, deletar e listar tarefas.",
    version="1.0.0",
    contact={
        "name": "brendo henrique",
        "email": "brendohenriquelopes@gmail.com"
    }
)

# Banco de dados simulado armazenando instâncias do tipo Tarefa
minhas_tarefas = {}

# Modelo de dados Pydantic com a estrutura solicitada
class Tarefa(BaseModel):
    nome: str
    descricao: str
    concluida: bool = False


@app.get("/")
def hello_world():
    return {"Hello": "World!"}


@app.get("/tarefas")
def listar_tarefas():
    if not minhas_tarefas:
        return {"message": "Não existe nenhuma tarefa cadastrada!"}
    # O FastAPI serializa automaticamente os objetos Pydantic para JSON
    return {"tarefas": minhas_tarefas}


@app.post("/adiciona")
def adicionar_tarefa(id_tarefa: int, tarefa: Tarefa):
    if id_tarefa in minhas_tarefas:
        raise HTTPException(status_code=400, detail="Essa tarefa já existe, meu parceiro!")
    
    # Armazena o próprio objeto (instância de Tarefa) diretamente
    minhas_tarefas[id_tarefa] = tarefa
    return {"mensagem": "Tarefa adicionada com sucesso!", "tarefa": minhas_tarefas[id_tarefa]}


@app.patch("/concluir/{id_tarefa}")
def marcar_como_concluida(id_tarefa: int):
    if id_tarefa not in minhas_tarefas:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada!")
    
    # Altera o atributo do objeto usando a notação de ponto (.) em vez de colchetes
    minhas_tarefas[id_tarefa].concluida = True
    return {"mensagem": f"Tarefa {id_tarefa} concluída!", "tarefa": minhas_tarefas[id_tarefa]}


@app.delete("/deletar/{id_tarefa}")
def remover_tarefa(id_tarefa: int):
    if id_tarefa not in minhas_tarefas:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada!")
    
    del minhas_tarefas[id_tarefa]
    return {"mensagem": f"Tarefa {id_tarefa} removida com sucesso!"}
