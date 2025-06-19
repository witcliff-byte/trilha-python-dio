contas = []
AGENCIA = "0001"
numero_conta = 1
usuarios = []
menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[nu] Novo usuário
[nc] Nova conta
[lu] Listar usuários
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

def depositar(saldo, extrato, /):
    valor = float(input("Informe o valor do depósito: "))
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato

def sacar(*, saldo, extrato, limite, numero_saques, limite_saques):
    valor = float(input("Informe o valor do saque: "))
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= LIMITE_SAQUES

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")

    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")

    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1

    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato, numero_saques

def exibir_extrato(saldo, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ").strip()
    cpf = "".join(filter(str.isdigit, cpf))
    usuario_existente = any(u["cpf"] == cpf for u in usuarios)
    if usuario_existente:
        print("Já existe usuário com esse CPF!")
        return
    nome = input("Informe o nome completo: ").strip()
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ").strip()
    endereco = input("Informe o endereço (logradouro, nº - bairro - cidade/UF): ").strip()
    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })
    print("Usuário criado com sucesso!")
def criar_conta(agencia, numero_conta, usuarios, contas):
    cpf = input("Informe o CPF do usuário: ").strip()
    usuario = next((u for u in usuarios if u["cpf"] == cpf), None)
    if not usuario:
        print("Usuário não encontrado! Cadastro não realizado.")
        return
    conta = {
        "agencia": agencia,
        "numero_conta": numero_conta,
        "usuario": usuario
    }
    contas.append(conta)
    print(f"Conta criada com sucesso! Agência: {agencia} | Número da conta: {numero_conta}")

def listar_usuarios(usuarios):
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return
    print("\n===== LISTA DE USUÁRIOS =====")
    for usuario in usuarios:
        print(f"Nome: {usuario['nome']}")
        print(f"CPF: {usuario['cpf']}")
        print(f"Data de Nascimento: {usuario['data_nascimento']}")
        print(f"Endereço: {usuario['endereco']}")
        print("-----------------------------")


while True:
    opcao = input(menu)

    if opcao == "d":
        saldo, extrato = depositar(saldo, extrato)

    elif opcao == "s":
        saldo, extrato, numero_saques = sacar(
            saldo=saldo,
            extrato=extrato,
            limite=limite,
            numero_saques=numero_saques,
            limite_saques=LIMITE_SAQUES
        )

    elif opcao == "e":
        exibir_extrato(saldo, extrato)

    elif opcao == "nu":
        criar_usuario(usuarios)

    elif opcao == "nc":
        criar_conta(AGENCIA, numero_conta, usuarios, contas)
        numero_conta += 1  # Incrementa após criar conta

    elif opcao == "lu":
        listar_usuarios(usuarios)

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
