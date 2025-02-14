#import de modelos, SQL, Fields para criar campos de escolha, e engine para importar e exportar banco
from sqlmodel import SQLModel, Field, create_engine, Relationship
from enum import Enum
from datetime import date

#Classe para que seja escolhida o banco da conta do usuario
class Bancos(Enum):
 NUBANK = 'Nubank'
 SANTANDER = 'Santander'
 INTER = 'Inter'
 WILL = 'Will'
 BANCODOBRASIL = 'Banco do Brasil'

#Classe para esepecificar os status da conta
class Status(Enum):
    ATIVO = 'Ativo'
    INATIVO = 'Inativo'
    ANALISE = 'Em Aprovação'
 
#Classe conta do usuario para que ele altere
class Conta(SQLModel, table=True):
    id: int = Field(primary_key=True)
    valor: float 
    banco: Bancos = Field(default=Bancos.BANCODOBRASIL)
    status: Status = Field(default=Status.ATIVO)
    
class Tipos(Enum):
    ENTRADA = 'Entrada'
    SAIDA = 'Saída'

#Historico de contas de dada conta especifica
class Historico(SQLModel, table=True):
    id: int = Field(primary_key=True)
    conta_id: int = Field(foreign_key="conta.id")
    conta: Conta = Relationship()
    tipo: Tipos = Field(default=Tipos.ENTRADA)
    valor: float
    data: date

#tudo abaixo é para a criação do banco de dados   
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

#abaixo é que não importe desse arquivo, proxima vez que for chamaado Models
if __name__ == "__main__": 
    SQLModel.metadata.create_all(engine)