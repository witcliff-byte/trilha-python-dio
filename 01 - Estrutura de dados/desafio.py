from abc import ABC, abstractmethod, abstractproperty, abstractclassmethod
from datetime import datetime
import textwrap



class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_contato(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome,data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self.transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            }
        )


class Conta:
    def __init__(self, saldo: float, numero: int, agencia: str, cliente: Cliente, historico: Historico):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            self._saldo -= valor
            print("\n»»» Saque realizado com sucesso! «««")
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n»»» Depósito realizado com sucesso! «««")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite = 500, limite_saques = 3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques diários excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência: \t{self.agencia}
            C\C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def listar_contas(contas):
    for conta in contas:
        print("=" + 100)
        print(textwrap.dedent(str(conta)))

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui contas.")
        return
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Digite o CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return

    valor = float(input("Digite o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    conta.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Digite o CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return

    valor = float(input("Digite o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    conta.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Digite o CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n=========== Extrato ===========")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Nenhuma transação encontrada."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("==================================")

def criar_cliente(clientes):
    cpf = input("Digite o CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("Cliente já cadastrado.")
        return

    nome = input("Digite o nome do cliente: ")
    data_nascimento = input("Digite a data de nascimento (dd/mm/yyyy): ")
    endereco = input("Digite o endereço do cliente (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome = nome, data_nascimento = data_nascimento, cpf = cpf, endereco = endereco)
    clientes.append(cliente)

    print("\nCliente cadastrado com sucesso!")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Digite o CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\nConta criada com sucesso!")

def menu():
    print("\n=========== Menu ===========")
    print("d - Depositar")
    print("s - Sacar")
    print("e - Extrato")
    print("nu - Novo usuário")
    print("nc - Nova conta")
    print("lc - Listar contas")
    print("q - Sair")

    opcao = input("Escolha uma opção: ").lower()

    while opcao not in ["d", "s", "e", "nu", "nc", "lc", "q"]:
        print("Opção inválida. Tente novamente.")
        opcao = input("Escolha uma opção: ").lower()

    return opcao