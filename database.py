import sqlite3
from pathlib import Path
from datetime import date, timedelta

DB_PATH = Path(__file__).resolve().parent / "data" / "academia.db"

DURACOES = {
    "Teste 1 Dia":   1,
    "Teste 1 Semana": 7,
    "Mensal":        30,
    "Bimestral":     60,
    "Semestral":    180,
    "Anual":        365,
}

VALORES = {
    "Teste 1 Dia":    0.00,
    "Teste 1 Semana": 0.00,
    "Mensal":        89.90,
    "Bimestral":    159.90,
    "Semestral":    399.90,
    "Anual":        699.90,
}


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def inicializar_banco():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS aluno (
            id_aluno        INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_completo   TEXT NOT NULL,
            cpf             TEXT NOT NULL UNIQUE,
            email           TEXT,
            telefone        TEXT,
            data_nascimento TEXT,
            genero          TEXT,
            status          TEXT DEFAULT 'Ativo',
            ativo           INTEGER DEFAULT 1
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS plano (
            id_plano    INTEGER PRIMARY KEY AUTOINCREMENT,
            id_aluno    INTEGER NOT NULL REFERENCES aluno(id_aluno),
            tipo_plano  TEXT NOT NULL,
            data_inicio TEXT NOT NULL,
            data_fim    TEXT NOT NULL,
            valor       REAL NOT NULL,
            status_plano TEXT DEFAULT 'Ativo'
        )
    """)

    # Migração: adiciona coluna status_plano se não existir
    cols = [r[1] for r in cur.execute("PRAGMA table_info(plano)").fetchall()]
    if "status_plano" not in cols:
        cur.execute("ALTER TABLE plano ADD COLUMN status_plano TEXT DEFAULT 'Ativo'")

    conn.commit()

    total = cur.execute("SELECT COUNT(*) FROM aluno").fetchone()[0]
    if total == 0:
        _seed(conn)
    conn.close()


def _seed(conn):
    hoje = date.today()
    demo = [
        ("João Silva",      "12345678901", "joao@email.com",  "11999990001", "1990-05-10", "Masculino", hoje-timedelta(30),  hoje+timedelta(335), "Anual",        699.90),
        ("Maria Souza",     "98765432100", "maria@email.com", "11999990002", "1995-08-22", "Feminino",  hoje-timedelta(10),  hoje+timedelta(20),  "Mensal",        89.90),
        ("Sama Dungo",      "11122233300", "sama@email.com",  "11999990003", "1988-03-15", "Feminino",  hoje-timedelta(60),  hoje-timedelta(30),  "Mensal",        89.90),
        ("Doria Glarania",  "44455566600", "doria@email.com", "11999990004", "2000-11-02", "Feminino",  hoje-timedelta(90),  hoje-timedelta(60),  "Bimestral",    159.90),
        ("Ferno Utingawe",  "77788899900", "ferno@email.com", "11999990005", "1985-07-30", "Masculino", hoje-timedelta(5),   hoje+timedelta(360), "Anual",        699.90),
        ("Lucas Mendes",    "33344455511", "lucas@email.com", "11999990006", "1998-01-20", "Masculino", hoje-timedelta(20),  hoje+timedelta(40),  "Bimestral",    159.90),
        ("Ana Paula Costa", "66677788822", "ana@email.com",   "11999990007", "1993-06-14", "Feminino",  hoje-timedelta(3),   hoje+timedelta(27),  "Mensal",        89.90),
        ("Pedro Alves",     "55566677733", "pedro@email.com", "11999990008", "1987-09-09", "Masculino", hoje-timedelta(120), hoje-timedelta(30),  "Semestral",    399.90),
        ("Carlos Teste",    "22233344455", "carlos@email.com","11999990009", "2001-03-21", "Masculino", hoje,                hoje+timedelta(1),   "Teste 1 Dia",    0.00),
        ("Julia Semana",    "99988877766", "julia@email.com", "11999990010", "1999-07-11", "Feminino",  hoje,                hoje+timedelta(7),   "Teste 1 Semana", 0.00),
    ]
    cur = conn.cursor()
    for nome, cpf, email, tel, nasc, gen, ini, fim, tipo, val in demo:
        status = "Ativo" if fim >= hoje else "Inativo"
        cur.execute(
            "INSERT INTO aluno (nome_completo,cpf,email,telefone,data_nascimento,genero,status) VALUES (?,?,?,?,?,?,?)",
            (nome, cpf, email, tel, nasc, gen, status)
        )
        id_aluno = cur.lastrowid
        cur.execute(
            "INSERT INTO plano (id_aluno,tipo_plano,data_inicio,data_fim,valor,status_plano) VALUES (?,?,?,?,?,?)",
            (id_aluno, tipo, ini.isoformat(), fim.isoformat(), val, "Ativo" if fim >= hoje else "Inativo")
        )
    conn.commit()
