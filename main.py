from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Inicialização do app FastAPI
app = FastAPI()

# Passo 1: Criação do modelo Pydantic
class Tarefa(BaseModel):
    nome: str
    descricao: str
    concluida: bool = False

# Passo 3: Lista de tarefas que agora armazena objetos do tipo Tarefa
lista_de_tarefas: list[Tarefa] = []


# Passo 4: Rota de Listar Tarefas (GET)
@app.get("/tarefas", response_model=list[Tarefa])
def listar_tarefas():
    # O FastAPI converte automaticamente os objetos Tarefa em JSON
    return lista_de_tarefas


# Passo 2: Rota de Adicionar Tarefa (POST)
@app.post("/tarefas", status_code=201)
def adicionar_tarefa(tarefa: Tarefa):
    # O FastAPI valida os dados automaticamente antes de entrar aqui
    lista_de_tarefas.append(tarefa)
    return {"mensagem": "Tarefa adicionada com sucesso!", "tarefa": tarefa}


# Passo 5: Rota de Marcar como Concluída (PATCH/PUT)
@app.patch("/tarefas/{nome}/concluir")
def marcar_como_concluida(nome: str):
    # Busca a tarefa na lista usando o campo 'nome' do modelo Pydantic
    for tarefa in lista_de_tarefas:
        if tarefa.nome.lower() == nome.lower():
            tarefa.concluida = True
            return {"mensagem": f"Tarefa '{tarefa.nome}' concluída!", "tarefa": tarefa}
    
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")


# Passo 5: Rota de Remover Tarefa (DELETE)
@app.delete("/tarefas/{nome}")
def remover_tarefa(nome: str):
    # Busca e remove o objeto filtrando pelo campo 'nome'
    for tarefa in lista_de_tarefas:
        if tarefa.nome.lower() == nome.lower():
            lista_de_tarefas.remove(tarefa)
            return {"mensagem": f"Tarefa '{nome}' removida com sucesso!"}
            
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")
