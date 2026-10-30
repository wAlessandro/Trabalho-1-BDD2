import sqlite3
from datetime import date

class ObjetoAcessoDados:
    """Implementa os métodos definidos no diagrama usando sqlite3."""

    def __init__(self, nome_banco="ong_animais.db"):
        self.nome_banco = nome_banco
        self.conexao = None
        self.conectar()
        self._criarTabelas()

    def conectar(self):
        """Retorna a conexão SQLite."""
        if self.conexao is None:
            self.conexao = sqlite3.connect(self.nome_banco)
            self.conexao.row_factory = sqlite3.Row
            self.conexao.execute("PRAGMA foreign_keys = ON")
        return self.conexao

    def desconectar(self):
        """Encerra a conexão."""
        if self.conexao is not None:
            self.conexao.close()
            self.conexao = None

    def executarTransacao(self, comando: str) -> bool:
        """Executa um comando SQL e informa se foi executado com sucesso."""
        try:
            self.conectar().execute(comando)
            self.conexao.commit()
            return True
        except sqlite3.Error:
            self.conexao.rollback()
            return False

    def inserir(self, entidade: object) -> bool:
        """Insere um registro. entidade deve ser um dicionário com 'tabela' e 'dados'."""
        try:
            tabela = entidade["tabela"]
            dados = entidade["dados"]
            self._validarTabela(tabela)
            colunas = list(dados.keys())
            sql_colunas = ", ".join(colunas)
            marcadores = ", ".join("?" for _ in colunas)
            sql = f"INSERT INTO {tabela} ({sql_colunas}) VALUES ({marcadores})"
            self.conectar().execute(sql, tuple(dados.values()))
            self.conexao.commit()
            return True
        except (sqlite3.Error, KeyError, TypeError, ValueError):
            if self.conexao:
                self.conexao.rollback()
            return False

    def atualizar(self, entidade: object) -> bool:
        """Atualiza um registro. entidade contém tabela, id_coluna, id e dados."""
        try:
            tabela = entidade["tabela"]
            id_coluna = entidade["id_coluna"]
            id_valor = entidade["id"]
            dados = entidade["dados"]
            self._validarTabela(tabela)
            atribuicoes = ", ".join(f"{coluna} = ?" for coluna in dados)
            valores = list(dados.values()) + [id_valor]
            sql = f"UPDATE {tabela} SET {atribuicoes} WHERE {id_coluna} = ?"
            cursor = self.conectar().execute(sql, valores)
            self.conexao.commit()
            return cursor.rowcount > 0
        except (sqlite3.Error, KeyError, TypeError, ValueError):
            if self.conexao:
                self.conexao.rollback()
            return False

    def excluir(self, entidade: object) -> bool:
        """Exclui um registro. entidade contém tabela, id_coluna e id."""
        try:
            tabela = entidade["tabela"]
            id_coluna = entidade["id_coluna"]
            id_valor = entidade["id"]
            self._validarTabela(tabela)
            sql = f"DELETE FROM {tabela} WHERE {id_coluna} = ?"
            cursor = self.conectar().execute(sql, (id_valor,))
            self.conexao.commit()
            return cursor.rowcount > 0
        except (sqlite3.Error, KeyError, TypeError, ValueError):
            if self.conexao:
                self.conexao.rollback()
            return False

    def consultar(self, tipo: str) -> list:
        """Consulta todos os registros do tipo/tabela informado."""
        try:
            self._validarTabela(tipo)
            cursor = self.conectar().execute(f"SELECT * FROM {tipo}")
            return [dict(registro) for registro in cursor.fetchall()]
        except (sqlite3.Error, TypeError, ValueError):
            return []

    def _validarTabela(self, tabela):
        tabelas_permitidas = {"Usuario", "Endereco", "Animal", "Doacao", "Adocao"}
        if tabela not in tabelas_permitidas:
            raise ValueError("Tabela inválida.")

    def _criarTabelas(self):
        self.conectar().executescript("""
            CREATE TABLE IF NOT EXISTS Usuario (
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS Endereco (
                id_endereco INTEGER PRIMARY KEY AUTOINCREMENT,
                id_usuario INTEGER NOT NULL UNIQUE,
                rua TEXT,
                numero TEXT,
                bairro TEXT,
                cidade TEXT,
                estado TEXT,
                cep TEXT,
                FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
            );

            CREATE TABLE IF NOT EXISTS Animal (
                id_animal INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                especie TEXT NOT NULL,
                idade INTEGER NOT NULL,
                sexo TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Disponível'
            );

            CREATE TABLE IF NOT EXISTS Doacao (
                id_doacao INTEGER PRIMARY KEY AUTOINCREMENT,
                id_usuario INTEGER NOT NULL,
                id_animal INTEGER NOT NULL,
                valor REAL NOT NULL,
                data_doacao TEXT NOT NULL,
                FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
                FOREIGN KEY (id_animal) REFERENCES Animal(id_animal)
            );

            CREATE TABLE IF NOT EXISTS Adocao (
                id_adocao INTEGER PRIMARY KEY AUTOINCREMENT,
                id_usuario INTEGER NOT NULL,
                id_animal INTEGER NOT NULL,
                data_adocao TEXT NOT NULL,
                FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
                FOREIGN KEY (id_animal) REFERENCES Animal(id_animal)
            );
        """)
        self.conexao.commit()


class Usuario:
    def __init__(self, id_usuario: int, nome: str, email: str, senha: str):
        self.id_usuario: int = id_usuario
        self.nome: str = nome
        self.email: str = email
        self.senha: str = senha


class Endereco:
    def __init__(self, id_endereco: int, id_usuario: int, rua: str, numero: str, bairro: str, cidade: str, estado: str, cep: str):
        self.id_endereco: int = id_endereco
        self.id_usuario: int = id_usuario
        self.rua: str = rua
        self.numero: str = numero
        self.bairro: str = bairro
        self.cidade: str = cidade
        self.estado: str = estado
        self.cep: str = cep


class Animal:
    def __init__(self, id_animal: int, nome: str, especie: str, idade: int, sexo: str, status: str ="Disponível"):
        self.id_animal: int = id_animal
        self.nome: str = nome
        self.especie: str = especie
        self.idade: int = idade
        self.sexo: str = sexo
        self.status: str = status


class Doacao:
    def __init__(self, id_doacao: int, id_usuario: int, id_animal: int, valor: float, data_doacao=None):
        self.id_doacao: int = id_doacao
        self.id_usuario: int = id_usuario
        self.id_animal: int = id_animal
        self.valor: float = valor
        self.data_doacao = data_doacao or date.today().isoformat()


class Adocao:
    def __init__(self, id_adocao, id_usuario, id_animal, data_adocao=None):
        self.id_adocao = id_adocao
        self.id_usuario = id_usuario
        self.id_animal = id_animal
        self.data_adocao: str = data_adocao or date.today().isoformat()


class ControladorSistema:
    def __init__(self, banco_dados):
        self.banco_dados = banco_dados

    def iniciarSessao(self, email: str, senha: str) -> bool:
        usuarios = self.banco_dados.consultar("Usuario")
        return any(u["email"] == email and u["senha"] == senha for u in usuarios)

    def cadastrarUsuario(self, nome: str, email: str, senha: str):
        return self.banco_dados.inserir({
            "tabela": "Usuario",
            "dados": {"nome": nome, "email": email, "senha": senha}
        })

    def cadastrarEndereco(self, idUsuario: int, rua: str, numero: str,
                          bairro: str, cidade: str, estado: str, cep: str):
        return self.banco_dados.inserir({
            "tabela": "Endereco",
            "dados": {
                "id_usuario": idUsuario, "rua": rua, "numero": numero,
                "bairro": bairro, "cidade": cidade, "estado": estado, "cep": cep
            }
        })

    def cadastrarAnimal(self, nome: str, especie: str, idade: int, sexo: str):
        return self.banco_dados.inserir({
            "tabela": "Animal",
            "dados": {
                "nome": nome, "especie": especie, "idade": idade,
                "sexo": sexo, "status": "Disponível"
            }
        })

    def realizarDoacao(self, idUsuario: int, idAnimal: int, valor: float):
        return self.banco_dados.inserir({
            "tabela": "Doacao",
            "dados": {
                "id_usuario": idUsuario, "id_animal": idAnimal,
                "valor": valor, "data_doacao": date.today().isoformat()
            }
        })

    def requisitarAdocao(self, idUsuario: int, idAnimal: int):
        animais = self.banco_dados.consultar("Animal")
        animal_disponivel = any(
            a["id_animal"] == idAnimal and a["status"] == "Disponível"
            for a in animais
        )
        if not animal_disponivel:
            return False

        sucesso = self.banco_dados.inserir({
            "tabela": "Adocao",
            "dados": {
                "id_usuario": idUsuario,
                "id_animal": idAnimal,
                "data_adocao": date.today().isoformat()
            }
        })
        if sucesso:
            self.banco_dados.atualizar({
                "tabela": "Animal",
                "id_coluna": "id_animal",
                "id": idAnimal,
                "dados": {"status": "Adotado"}
            })
        return sucesso

    def listarAnimais(self) -> list:
        return self.banco_dados.consultar("Animal")

    def listarDoacoes(self) -> list:
        return self.banco_dados.consultar("Doacao")


if __name__ == "__main__":
    banco = ObjetoAcessoDados()
    sistema = ControladorSistema(banco)

    print("Sistema iniciado. Banco SQLite: ong_animais.db")

    banco.desconectar()
