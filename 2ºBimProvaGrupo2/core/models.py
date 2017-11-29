﻿from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import *
from django.core.validators import MaxValueValidator, MinValueValidator

ALUNO = "A"
PROFESSOR = "P"
COORDENADOR = "C"
PERFIS = (
    (ALUNO, 'Aluno'),
    (PROFESSOR, 'Professor'),
    (COORDENADOR, 'Coordenador')
)

class UsuarioManager(BaseUserManager):
    def _criar_usuario(self, ra, password, **campos):
        if not ra: 
            raise ValueError("RA deve ser declarado!")
        user = self.model(ra=ra, **campos)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, ra, password=None, **campos):
        return self._criar_usuario(ra, password, **campos)

    def create_superuser(self, ra, password=None, **campos):
        campos.setdefault('perfil', 'C')
        return self._criar_usuario(ra, password, **campos)

class Usuario(AbstractBaseUser):

    ra = models.IntegerField("RA",unique=True)
    password = models.CharField("Senha", max_length=200)

    nome = models.CharField("Nome", max_length=100)
    email = models.EmailField("E-Mail", max_length=50)

    perfil = models.CharField("Perfil", max_length=1, default="A")
    ativo = models.BooleanField("Ativo", default=True)
    
    USERNAME_FIELD = 'ra'
    REQUIRED_FIELDS = ['nome','email']

    objects = UsuarioManager()

    def get_full_name(self):
        return self.nome

    def get_short_name(self):
        return self.nome

    def __str__(self):
        return self.nome

    @property
    def is_staff(self):
        return self.perfil == "C"

    def has_module_perms(self, package_name):
        return True

    def has_perm(self, perm, obj=None):
        return True

    def has_perms(self, perm_list, obj=None):
        return True
		
class Contato(models.Model):

    assunto = models.CharField("Assunto", max_length=50)
    email = models.EmailField("Email", blank=True)
    nome = models.CharField("Nome", max_length=50)
    mensagem = models.TextField("Mensagem")

    def envia_email(self):
        print("ENVIADO")

class Curso(models.Model):
    sigla = models.CharField(db_column='Sigla', unique=True, max_length=5)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', unique=True, max_length=50)  # Field name made lowercase.

    class Meta:
        db_table = 'Curso'

    def __str__(self):
        return self.nome

class Aluno(Usuario):
    celular = models.CharField(db_column='Celular', max_length=11)  # Field name made lowercase.
    curso = models.ForeignKey(Curso)
    sigla_curso = models.CharField(db_column='Sigla_Curso', max_length=2)  # Field name made lowercase.

    class Meta:
        db_table = 'Aluno'


class Arquivosquestao(models.Model):
    id_questao = models.ForeignKey('Questao', models.DO_NOTHING, db_column='ID_Questao')  # Field name made lowercase.
    arquivo = models.CharField(db_column='Arquivo', max_length=500)  # Field name made lowercase.

    class Meta:
        db_table = 'ArquivosQuestao'
        unique_together = (('id_questao', 'arquivo'),)


class Arquivosresposta(models.Model):
    id_resposta = models.ForeignKey('Resposta', models.DO_NOTHING, db_column='ID_Resposta')  # Field name made lowercase.
    arquivo = models.CharField(db_column='Arquivo', max_length=500)  # Field name made lowercase.

    class Meta:
        db_table = 'ArquivosResposta'
        unique_together = (('id_resposta', 'arquivo'),)

class Cursoturma(models.Model):
    id_curso = models.ForeignKey(Curso, models.DO_NOTHING, db_column='ID_Curso')  # Field name made lowercase.
    id_turma_cursoturma = models.ForeignKey('Turma', models.DO_NOTHING, db_column='ID_Turma')  # Field name made lowercase.

    class Meta:
        db_table = 'CursoTurma'
        unique_together = (('id_curso', 'id_turma_cursoturma'),)


class Disciplina(models.Model):
    nome = models.CharField(db_column='Nome', unique=True, max_length=240)  # Field name made lowercase.
    cargahoraria = models.SmallIntegerField(db_column='CargaHoraria')  # Field name made lowercase.
    teoria = models.DecimalField(db_column='Teoria', max_digits=3, decimal_places=0)  # Field name made lowercase.
    pratica = models.DecimalField(db_column='Pratica', max_digits=3, decimal_places=0)  # Field name made lowercase.
    ementa = models.TextField(db_column='Ementa')  # Field name made lowercase. This field type is a guess.
    competencias = models.TextField(db_column='Competencias')  # Field name made lowercase. This field type is a guess.
    habilidades = models.TextField(db_column='Habilidades')  # Field name made lowercase. This field type is a guess.
    conteudo = models.TextField(db_column='Conteudo')  # Field name made lowercase. This field type is a guess.
    bibliografia_basica = models.TextField(db_column='Bibliografia_Basica')  # Field name made lowercase. This field type is a guess.
    biliografia_complementar = models.TextField(db_column='Biliografia_Complementar')  # Field name made lowercase. This field type is a guess.

    class Meta:
        db_table = 'Disciplina'

    def __str__(self):
        return self.nome

class Disciplinaofertada(models.Model):
    id_disciplina = models.ForeignKey(Disciplina, models.DO_NOTHING, db_column='ID_Disciplina')  # Field name made lowercase.
    ano = models.SmallIntegerField(db_column='Ano')  # Field name made lowercase.
    semestre = models.CharField(db_column='Semestre', max_length=1)  # Field name made lowercase.

    class Meta:
        db_table = 'DisciplinaOfertada'
        unique_together = (('id_disciplina', 'ano', 'semestre'),)

    def __str__(self):
        return self.id_disciplina.nome + ' ' + str(self.ano) + ' semestre ' + str(self.semestre)

class Gradecurricular(models.Model):
    id_curso = models.ForeignKey(Curso, models.DO_NOTHING, db_column='ID_Curso')  # Field name made lowercase.
    ano = models.SmallIntegerField(db_column='Ano')  # Field name made lowercase.
    semestre = models.CharField(db_column='Semestre', max_length=1)  # Field name made lowercase.

    class Meta:
        db_table = 'GradeCurricular'
        unique_together = (('id_curso', 'ano', 'semestre'),)

    def __str__(self):
        return self.id_curso.nome

class Matricula(models.Model):
    id_aluno = models.ForeignKey(Aluno, models.DO_NOTHING, db_column='ID_Aluno')  # Field name made lowercase.
    id_turma_matricula = models.ForeignKey('Turma', models.DO_NOTHING, db_column='ID_Turma')  # Field name made lowercase.

    class Meta:
        db_table = 'Matricula'
        unique_together = (('id_aluno', 'id_turma_matricula'),)


class Periodo(models.Model):
    id_gradecurricular = models.ForeignKey(Gradecurricular, models.DO_NOTHING, db_column='ID_GradeCurricular')  # Field name made lowercase.
    numero = models.SmallIntegerField(db_column='Numero')  # Field name made lowercase.

    class Meta:
        db_table = 'Periodo'
        unique_together = (('id_gradecurricular', 'numero'),)

    def __str__(self):
        return str(self.numero) + ' ' + str(self.id_gradecurricular.ano) + ' ' + str(self.id_gradecurricular.semestre) + ' ' + str(self.id_gradecurricular.id_curso.sigla)

class Periododisciplina(models.Model):
    id_periodo = models.ForeignKey(Periodo, models.DO_NOTHING, db_column='ID_Periodo')  # Field name made lowercase.
    id_disciplina = models.ForeignKey(Disciplina, models.DO_NOTHING, db_column='ID_Disciplina')  # Field name made lowercase.

    class Meta:
        db_table = 'PeriodoDisciplina'
        unique_together = (('id_periodo', 'id_disciplina'),)



class Professor(Usuario):
    apelido = models.CharField(db_column='Apelido', unique=True, max_length=30)  # Field name made lowercase.
    celular = models.CharField(db_column='Celular', max_length=11)  # Field name made lowercase.

    class Meta:
        db_table = 'Professor'

class Turma(models.Model):
    id_disciplinaofertada = models.ForeignKey(Disciplinaofertada, models.DO_NOTHING, db_column='ID_DisciplinaOfertada')  # Field name made lowercase.
    turma = models.CharField(db_column='Identificacao_Turma', max_length=5)  # Field name made lowercase.
    turno = models.CharField(db_column='Turno', max_length=15)  # Field name made lowercase.
    id_professor = models.ForeignKey(Professor, models.DO_NOTHING, db_column='ID_Professor')  # Field name made lowercase.
    max_alunos = models.IntegerField("Maximo_Alunos",validators=[MaxValueValidator(40),MinValueValidator(1)])

    class Meta:
        db_table = 'Turma'
        unique_together = (('id_disciplinaofertada', 'id_professor'),)

    def __str__(self):
        return self.turma

class Questao(models.Model):
    id_professor_questao = models.ForeignKey(Professor, on_delete=models.CASCADE)
    id_turma_questao = models.ForeignKey(Turma, on_delete=models.CASCADE)  # Field name made lowercase.
    numero = models.IntegerField(db_column='Numero')  # Field name made lowercase.
    data_limite_entrega = models.DateField(db_column='Data_Limite_Entrega', max_length=10, help_text="DD/MM/AAAA")  # Field name made lowercase.
    descricao = models.TextField(db_column='Descricao')  # Field name made lowercase. This field type is a guess.
    data = models.DateTimeField(db_column='Data', max_length=10, auto_now_add=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Questao'
        unique_together = (('id_turma_questao', 'numero'),)

    def __str__(self):
        return 'Questao ' + str(self.numero) + ' ' + self.descricao

    def prazo(self, agora):
        return self.data_limite_entrega > agora

class Resposta(models.Model):
    id_questao = models.ForeignKey(Questao, models.DO_NOTHING, db_column='ID_Questao')  # Field name made lowercase.
    id_aluno = models.ForeignKey(Aluno, models.DO_NOTHING, db_column='ID_Aluno')  # Field name made lowercase.
    data_avaliacao = models.DateTimeField(db_column='Data_Avaliacao', max_length=10)  # Field name made lowercase.
    nota = models.DecimalField(db_column='Nota', max_digits=4, decimal_places=2, null=True)  # Field name made lowercase.
    avaliacao = models.TextField(db_column='Avaliacao', null=True)  # Field name made lowercase. This field type is a guess.
    descricao = models.TextField(db_column='Descricao')  # Field name made lowercase. This field type is a guess.
    data_de_envio = models.DateTimeField(db_column='Data_de_Envio', max_length=10)  # Field name made lowercase.

    class Meta:
        db_table = 'Resposta'
        unique_together = (('id_questao', 'id_aluno'),)

class Contato(models.Model):

    assunto = models.CharField("Assunto", max_length=50)
    email = models.EmailField("Email", blank=True)
    nome = models.CharField("Nome", max_length=50)
    mensagem = models.TextField("Mensagem")

    def envia_email(self):
        print("ENVIADO")

class Avisos(models.Model):

    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    titulo = models.CharField("Titulo", max_length=100)
    texto = models.TextField("Texto")
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)

class MensagemAluno(models.Model):

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    assunto = models.CharField("Assunto", max_length=100)
    mensagem = models.TextField("Mensagem")
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)

class Coordenador(Usuario):
    
    apelido = models.CharField("Apelido", unique=True, max_length=30)  # Field name made lowercase.