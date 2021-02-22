import psycopg2


class User:


    def __init__(self):
        self.reset()

    def reset(self):
        self.id = None
        self.cliente = ''
        self.email = ''
        self.password = ''
        self.nif = ''
        self.nome = ''
        self.morada = ''

    def herokudb(self):
        Host = 'ec2-54-75-235-28.eu-west-1.compute.amazonaws.com'
        Database = 'd2i8vmdqr6hqck'
        User = 'dlopinbemujdnz'
        Password = 'c2f51674e9042bcd8985d5040cfe270542eec1ed42625e1e7fde56274000d210'
        return psycopg2.connect(host=Host, database=Database, user=User, password=Password, sslmode='require')

    def gravar(self, login, email, password):
        ficheiro = self.herokudb()
        db = ficheiro.cursor()
        #db.execute("drop table usr")
        db.execute("CREATE TABLE IF NOT EXISTS usr (id serial primary key,login text,email text, passe text, nif text, nome text, morada char(60))")
        db.execute("INSERT INTO usr VALUES (DEFAULT ,%s, %s, %s)", (login, email, self.code(password),))
        ficheiro.commit()
        ficheiro.close()

    def existe(self, login):
        try:
            ficheiro = self.herokudb()
            db = ficheiro.cursor()
            db.execute("SELECT * FROM usr WHERE login = %s", (login,))
            valor = db.fetchone()
            ficheiro.close()
        except:
            valor = None
        return valor

    def log(self, login, password):
        ficheiro = self.herokudb()
        db = ficheiro.cursor()
        db.execute("SELECT * FROM usr WHERE login = %s and password = %s", (login, self.code(password),))
        valor = db.fetchone()
        ficheiro.close()
        return valor

    def alterar(self, login, password):
        ficheiro = self.herokudb()
        db = ficheiro.cursor()
        db.execute("UPDATE usr SET password = %s WHERE login = %s", (self.code(password), login))
        ficheiro.commit()
        ficheiro.close()

    def apaga(self, login):
        ficheiro = self.herokudb()
        db = ficheiro.cursor()
        db.execute("DELETE FROM usr WHERE login = %s", (login,))
        ficheiro.commit()
        ficheiro.close()

    def lista(self):
        try:
            ficheiro = self.herokudb()
            db = ficheiro.cursor()
            db.execute("select * from usr")
            valor = db.fetchall()
            ficheiro.close()
        except:
            valor = None
        return valor

    @staticmethod
    def code(passe):
        import hashlib
        return hashlib.sha3_256(passe.encode()).hexdigest()