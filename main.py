from objetos import ObjetoAcessoDados, ControladorSistema

banco = ObjetoAcessoDados()
sistema = ControladorSistema(banco)

# cadastro inicial de animais
if sistema.listarAnimais() == []:
    sistema.cadastrarAnimal("Rex", "Cachorro", 3, "Macho")
    sistema.cadastrarAnimal("Luna", "Gato", 2, "Fêmea")
    sistema.cadastrarAnimal("Thor", "Cachorro", 4, "Macho")
    sistema.cadastrarAnimal("Margarida", "Cachorro", 4, "Fêmea")
    sistema.cadastrarAnimal("Florzinha", "Cachorro", 2, "Fêmea")
    sistema.cadastrarAnimal("Pepa", "Cachorro", 3, "Fêmea")
    sistema.cadastrarAnimal("Pipoca", "Cachorro", 4, "Macho")
    sistema.cadastrarAnimal("Mel", "Cachorro", 1, "Fêmea")


print("\n     Iniciar/Cadastrar    ")
if input("Deseja cadastrar um novo usuário? (s/n): ").lower() == "s":
    print("\n     Cadastrar seu Usuário     ")

    sistema.cadastrarUsuario(
        input("Nome de usuário: "),
        input("Email: "),
        input("Senha: ")
    )
    print("\n     Usuário Cadastrado!    ")
print("\n---- INICIAR SESSAO ----")
email = input("Email: ")
inicio = sistema.iniciarSessao(email, input("Senha: "))

while True:
    if  inicio is False:
        if input("\nUsuario não encontrado. Deseja tentar novamente?(s/n)").lower() == "n":
            break
        else:
            email = input("Email: ")
            inicio = sistema.iniciarSessao(email, input("Senha: "))
    else:
        usuario: dict = [
            usuario for usuario in banco.consultar("Usuario")
            if usuario["email"] == email
        ][0]
    
        print(f"\nBem-vindo(a), {usuario['nome']}!")
    
        if [
            endereco for endereco in banco.consultar("Endereco")
            if endereco["id_usuario"] == usuario["id_usuario"]
        ] == []:
    
            print("\n     Cadastrar seu Endereço     ")
    
            sistema.cadastrarEndereco(
                usuario["id_usuario"],
                input("Rua: "),
                input("Número: "),
                input("Bairro: "),
                input("Cidade: "),
                input("Estado: "),
                input("CEP: ")
            )

        print("\n===== MENU =====")
        print("1 - Listar animais disponíveis")
        print("2 - Realizar doação monetária")
        print("3 - Requisitar adoção")
        print("4 - Minhas adoções e doações")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")


        if opcao == "1":

            animais = [
                f'\n{animal["id_animal"]}  '
                f'{animal["nome"]}  '
                f'{animal["especie"]}  '
                f'{animal["idade"]}  '
                f'{animal["sexo"]}'
                for animal in sistema.listarAnimais()
            ]

            print("\nID Nome Espécie Idade Sexo Status")
            print(*animais)

        elif opcao == "2":

            print("\n......Realizar Doação Monetária......")

            animais = [
                f'\n{animal["id_animal"]}  '
                f'{animal["nome"]}  '
                f'{animal["especie"]}  '
                f'{animal["idade"]}  '
                f'{animal["sexo"]}'
                for animal in sistema.listarAnimais()
            ]

            print("ID Nome Espécie Idade Sexo")
            print(*animais)

            sistema.realizarDoacao(
                usuario["id_usuario"],
                input("ID do animal: "),
                float(input("Valor da doação: R$"))
            )

            print("\nDoação realizada com sucesso!")
        elif opcao == "3":

            print("\n......Requisitar Adoção......")
            print("\n     Pets Disponíveis     ")

            lista_animais = [
                f'\n{animal["id_animal"]}  '
                f'{animal["nome"]}  '
                f'{animal["especie"]}  '
                f'{animal["idade"]}  '
                f'{animal["sexo"]}'
                for animal in sistema.listarAnimais()
                if animal["status"] == "Disponível"
            ]

            print("ID Nome Espécie Idade Sexo")
            print(*lista_animais)

            sistema.requisitarAdocao(
                usuario["id_usuario"],
                int(input("Identificador do animal: "))
            )

            print("\nRequisição de adoção realizada com sucesso!")
            print("\nAguarde a análise do seu pedido. Você será notificado(a) por e-mail.")
        elif opcao == "4":

            print("\n===== MINHAS REQUISIÇÕES DE ADOÇÃO =====")

            adocoes = [
                adocao
                for adocao in banco.consultar("Adocao")
                if adocao["id_usuario"] == usuario["id_usuario"]
            ]

            if adocoes == []:
                print("\nNenhuma requisição de adoção encontrada.")

            else:
                for adocao in adocoes:

                    animal = [
                        animal
                        for animal in sistema.listarAnimais()
                        if animal["id_animal"] == adocao["id_animal"]
                    ][0]

                    print(
                        f'\nAnimal: {animal["nome"]}'
                        f'\nEspécie: {animal["especie"]}'
                        f'\nData da requisição: {adocao["data_adocao"]}'
                    )


            print("\n===== MINHAS DOAÇÕES =====")

            doacoes = [
                doacao
                for doacao in banco.consultar("Doacao")
                if doacao["id_usuario"] == usuario["id_usuario"]
            ]

            if doacoes == []:
                print("\nNenhuma doação encontrada.")

            else:
                for doacao in doacoes:

                    animal = [
                        animal
                        for animal in sistema.listarAnimais()
                        if animal["id_animal"] == doacao["id_animal"]
                    ][0]

                    print(
                        f'\nPet beneficiado: {animal["nome"]}'
                        f'\nEspécie: {animal["especie"]}'
                        f'\nValor: R$ {doacao["valor"]}'
                        f'\nData da doação: {doacao["data_doacao"]}'
                    )
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")
        input("\n<")

banco.desconectar()