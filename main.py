
from src.objetos import ObjetoAcessoDados, ControladorSistema

banco = ObjetoAcessoDados()
sistema = ControladorSistema(banco)


print("\n===== TESTE 1: CADASTRAR USUARIO =====")

sistema.cadastrarUsuario(
    "Maria Silva",
    "maria@email.com",
    "123456"
)

usuarios = banco.consultar("Usuario")
id_usuario = usuarios[0]["id_usuario"]

print("Usuário cadastrado:", usuarios)


print("\n===== INICIAR SESSAO =====")

print("Login correto:",
      sistema.iniciarSessao("maria@email.com", "123456"))

print("Login incorreto:",
      sistema.iniciarSessao("maria@email.com", "senha_errada"))


print("\n===== CADASTRAR ENDERECO =====")

sistema.cadastrarEndereco(
    id_usuario,
    "Rua das Flores",
    "100",
    "Centro",
    "Suzano",
    "SP",
    "08600-000"
)

print("Endereços:", banco.consultar("Endereco"))


print("\n===== CADASTRAR ANIMAL =====")

sistema.cadastrarAnimal(
    "Rex",
    "Cachorro",
    3,
    "Macho"
)

animais = sistema.listarAnimais()
id_animal = animais[0]["id_animal"]

print("Animais:", animais)


print("\n===== REALIZAR DOACAO =====")

resultado = sistema.realizarDoacao(
    id_usuario,
    id_animal,
    50.00
)

print("Doação registrada:", resultado)
print("Doações:", sistema.listarDoacoes())


print("\n===== REQUISITAR ADOCAO =====")

resultado = sistema.requisitarAdocao(
    id_usuario,
    id_animal
)

print("Adoção solicitada:", resultado)
print("Animal após adoção:", sistema.listarAnimais())


print("\n===== TENTAR ADOTAR NOVAMENTE =====")

resultado = sistema.requisitarAdocao(
    id_usuario,
    id_animal
)

print("Segunda adoção aceita:", resultado)


banco.desconectar()

print("\n===== TESTES FINALIZADOS =====")
