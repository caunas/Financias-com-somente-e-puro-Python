from models import Conta, engine, Bancos, Status, Tipos, Historico
from sqlmodel import Session, select
from datetime import date
import matplotlib.pyplot as plt
from models import Historico
#função parar criar uma conta, e evitar que essa conta seja recriada
def criar_conta(conta: Conta):
 with Session(engine) as session:
    statement = select(Conta).where(Conta.banco==conta.banco)
    results = session.exec(statement).all()
    
    if results:
        print("Já existe uma conta nesse banco!")
        return
    
    session.add(conta)
    session.commit()
    return conta

#função para colocar a lista das contas criadas
def listar_contas():
    with Session(engine) as session:
        statement = select(Conta)
        results = session.exec(statement).all()
        return results
#função para desativar uma conta
def desativar_conta(id):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id==id)
        conta = session.exec(statement).first()
        if conta.valor > 0:
            raise ValueError('Essa conta possui saldo, não é possivel ser desativada!')
        conta.status= Status.INATIVO
        session.commit()
        
#função de transferir saldos entre as contas
def transferir_saldo(id_conta_saida, id_conta_entrada, valor):
 with Session(engine) as session:
    statement = select(Conta).where(Conta.id==id_conta_saida)
    conta_saida = session.exec(statement).first()
    if conta_saida.valor < valor:
        raise ValueError('Saldo insuficiente')
    statement = select(Conta).where(Conta.id==id_conta_entrada)
    conta_entrada = session.exec(statement).first()
    conta_saida.valor -= valor
    conta_entrada.valor += valor
    session.commit()
 
 #função para movimentar o dinheiro entre as contas
def movimentar_dinheiro(historico: Historico):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id==historico.conta_id)
        conta = session.exec(statement).first()
        
        if conta.Status == Status.ATIVO:
            if historico.tipo == Tipos.ENTRADA:
                conta.valor +=historico.valor
            else:
                if conta.valor < historico.valor:
                    raise ValueError("Saldo Insuficiente")
                conta.valor -= historico.valor
        else:
            raise ValueError("Essa conta foi Desativada.") 
            
            
        session.add(historico)
        session.commit()
        return historico

#função para ver o total somado das contas
def total_contas():
    with Session(engine) as session:
        statement = select(Conta)
        contas = session.exec(statement).all()
        
    total = 0
    for conta in contas:
        total += conta.valor
    return float(total)

#mostra historico entre certas datas
def buscar_historicos_entre_datas(data_inicio: date, data_fim: date):
    with Session(engine) as session:
        statement = select(Historico).where(
            Historico.data >= data_inicio,
            Historico.data <= data_fim
        )
        resultados = session.exec(statement).all()
        return resultados
    
#para melhor visualização, aqui serve para ver um grafico
def criar_grafico():
    with Session(engine) as session:
        statement = select(Conta).where(Conta.Status==Status.ATIVO)
        contas = session.exec(statement).all()
        bancos = []
        for i in contas:
           bancos.append(i.banco.value)
           
        print(bancos)