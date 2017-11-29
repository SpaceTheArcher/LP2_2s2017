from django.shortcuts import render, redirect
from django.http import request
from core.forms import ContatoForm, DisciplinaForm, AvisosForm, MensagemAlunoForm, QuestaoForm, RespostaForm, CadastroForm, MatriculaForm
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required, user_passes_test
from core.models import Aluno, Professor, MensagemAluno, Avisos, Questao, Resposta, Matricula
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from datetime import *

# Create your views here.

def checa_aluno(usuario):
    return usuario.perfil == "A" or usuario.perfil == "C"

def checa_professor(usuario):
    return usuario.perfil == "P" or usuario.perfil == "C"

def checa_coordenador(usuario):
    return usuario.perfil == "C"

'''@login_required(login_url="/Login")
@user_passes_test(checa_aluno)
def page_boletim(request):
    aluno = Aluno.objects.get(id=request.user.id)
    print(aluno.curso)
    contexto = {
        "curso":aluno.curso
    }
    return render(request,"aluno.html", contexto)'''

@login_required(login_url="/Login")
@user_passes_test(checa_professor)
def page_cadastro_disciplina(request):
    if request.POST:
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            form.save()
            print("DISCIPLINA CADASTRADA")
    else:
        form = DisciplinaForm()
    context = {
        "form":form
    }
    return render(request,"CadastrarDisciplina.html",context)

def logout(request):
    return render(request, "index.html")
    
def index(request):
    return render(request, "index.html")

def page_lista_cursos(request):
    contexto = {
        "cursos":[
        {"nome":"Segurança Da Informação","link":"/Disciplinas/SegDaInformacao"}, 
        {"nome":"Arquitetura de Software","link":"PADS"}, 
        {"nome":"Jogos Digitais","link":"JD"},
        {"nome":"Redes de Computadores","link":"RC"},
        {"nome":"Sistemas de Informação","link":"SI"}
        ],
        "faculdade":"Faculdade Lorenzinni",
    }
    return render(request, "ListaCursos.html", contexto)

def page_noticias(request):
    return render(request, "noticias.html")

def page_login(request):
    return render(request, "LoginPage.html")
    
'''def page_cadastro_disciplina(request):
	if request.POST:
		form = DisciplinaForm(request.POST)
		if form.is_valid():
			form.save()
	else :
		form = DisciplinaForm()
	context = {
		"form":form
	}
	return render(request,"CadastrarDisciplina.html",context)'''
	
def page_contato(request) :
    if request.POST:
        form = ContatoForm(request.POST)
        if form.is_valid():
            form.save()
            print("MENSAGEM ENVIADA")
    else:
        form = ContatoForm()
    contexto = {
		"form":form
    }
    return render(request, "Contato.html", contexto)

@login_required(login_url="/Login")
@user_passes_test(checa_professor)
def page_avisos(request) :
    if request.POST:
        form = AvisosForm(request.POST)
        aviso = form.save(commit=False)
        aviso.professor = Professor.objects.get(nome=request.user.nome)
        if form.is_valid():
            aviso.save()
            print("AVISO ENVIADO | %s | %s | %s | %s" %(aviso.professor, aviso.titulo, aviso.texto, aviso.turma))
    else:
        form = AvisosForm()
    contexto = {
		"form":form
    }
    return render(request, "AvisoProfessor.html", contexto)

@login_required(login_url="/Login")
@user_passes_test(checa_aluno)
def page_mensagem_aluno(request) :
    if request.POST:
        form = MensagemAlunoForm(request.POST)
        mensagem = form.save(commit=False)
        mensagem.aluno = Aluno.objects.get(nome=request.user.nome)
        if form.is_valid():
            mensagem.save()
            print("MENSAGEM ENVIADA")
    else:
        form = MensagemAlunoForm()
    contexto = {
		"form":form
    }
    return render(request, "MensagemAluno.html", contexto)

def page_cadastro_usuario(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = CadastroForm()
    contexto = {'form': form}
    return render(request, 'CadastroPage.html', contexto)

def page_detalhes_cursos(request):
    return render(request, "DesCurso.html")

def page_detalhes_segdainf(request):
    return render(request, "SegDaInf.html")

def page_disciplinas_segdainf(request):
    return render(request, "dSegDaInfo.html")

def page_disciplina_seginfoatualidade(request):
    return render(request, "SegInfoAtualidade.html")

def page_nova_senha(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.Aluno, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Senha atualizada com sucesso!')
            return redirect('change_password')
        else:
            messages.error(request, 'Por favor arrume os seguintes erros :')
    else:
        form = PasswordChangeForm(request.user)
    contexto = {
        "form":form
    }
    return render(request, 'ForgotPass.html', contexto)

@login_required(login_url="/Login")
@user_passes_test(checa_professor)
def page_perfil_professor(request) :
    return render(request, "PerfilProfessor.html")

@login_required(login_url="/Login")
@user_passes_test(checa_coordenador)
def page_perfil_coordenador(request) :
    return render(request, "PerfilCoordenador.html")

@login_required(login_url="/Login")
@user_passes_test(checa_aluno)
def page_perfil_aluno(request) :
    return render(request, "PerfilAluno.html")

@login_required(login_url="/Login")
@user_passes_test(checa_professor)
def page_mensagens_professor(request):
    mensagens = MensagemAluno.objects.all()
    user = Professor.objects.get(nome=request.user.nome)
    contexto = {
        "mensagens":mensagens,
        "user":user
    }
    return render(request, "MensagensProfessor.html", contexto)

@login_required(login_url="/Login")
@user_passes_test(checa_aluno)
def page_avisos_aluno(request):
    avisos = Avisos.objects.all()
    contexto = {
        "avisos":avisos,
    }
    return render(request, "AvisosAluno.html", contexto)

@login_required(login_url="/Login")
@user_passes_test(checa_professor)
def page_cadastrar_questao(request):
    if request.method == 'POST' :
        form = QuestaoForm(request.POST)
        questao = form.save(commit=False)
        questao.id_professor_questao_id = request.user.id
        if form.is_valid():
            questao.save()
            print("QUESTAO ENVIADA")
    else :
        form = QuestaoForm()
    contexto = {
        "form":form,
    }
    return render(request, "CadastrarQuestao.html", contexto)

@login_required(login_url="/Login")
@user_passes_test(checa_aluno)
def page_responder_questao(request):
    agora = date.today()
    respondidas = []
    exibir = []
    esconder = []
    for questoes in Questao.objects.all():
        for respostas in Resposta.objects.all():
            if respostas.id_questao == questoes:
                if respostas.id_aluno == Aluno.objects.get(id=request.user.id):
                    respondidas.append(questoes)
        else :
            if questoes.prazo(agora):
                exibir.append(questoes)
            else:
                esconder.append(questoes)
    tuple(exibir)
    tuple(esconder)
    tuple(respondidas)
    if request.method == 'POST' :
        form = RespostaForm(request.POST)
        respostas = form.save(commit=False)
        respostas.data_de_envio = agora
        respostas.data_avaliacao = agora
        respostas.id_aluno = Aluno.objects.get(nome=request.user.nome)
        if form.is_valid():
            respostas.save()
            print("RESPOSTA ENVIADA")
            return redirect('/QuestoesRecebidas')
        else:
            print("PRAZO VENCIDO")
    else :
        form = RespostaForm()
        print("GET")
    contexto = {
        "form":form,
        "exibir":exibir,
        "esconder":esconder,
        "respondidas":respondidas
    }
    return render(request, "QuestoesRecebidas.html", contexto)

@login_required(login_url="/Login")
@user_passes_test(checa_professor)
def page_respostas_recebidas(request):
    respostas = Resposta.objects.all()
    contexto = {
        "respostas":respostas,
    }
    return render(request, "RespostasRecebidas.html", contexto)

@login_required(login_url="/Login")
@user_passes_test(checa_professor)
def page_resumo_tarefas(request):
    questoes = []
    questoesr = {}
    alunostotal = []
    questoesnr = {}
    respondido = []
    naorespondido = []
    for questao in Questao.objects.all():
        list(respondido)
        list(naorespondido)
        respondido = []
        naorespondido = []
        if questao.id_professor_questao == Professor.objects.get(id=request.user.id):
            for aluno in Aluno.objects.all():
                naorespondido.append(aluno)
                for resposta in Resposta.objects.all():
                    if resposta.id_aluno == aluno :
                        if resposta.id_questao == questao:
                            respondido.append(aluno)
                            naorespondido.remove(aluno)
            tuple(respondido)
            tuple(naorespondido)                
            questoesr[questao] = {'respondido':respondido}
            questoesnr[questao] = {'naorespondido':naorespondido}
        questoes.append(questao)
    print(questoesr)
    print(questoesnr)
    tuple(questoes)
    contexto = {
        "questoesr":questoesr,
        "questoesnr":questoesnr,
        "respondido":respondido,
        "naorespondido":naorespondido,
        "questoes":questoes
    }
    return render(request, "ResumoTarefaProfessor.html", contexto)

@login_required(login_url="/Login")
@user_passes_test(checa_aluno)
def page_aluno_matricula(request) :
    reg = False
    if request.POST:
        form = MatriculaForm(request.POST)
        matricula = form.save(commit=False)
        matricula.id_aluno = Aluno.objects.get(id=request.user.id)
        for matriculas in Matricula.objects.all():
            if matriculas.id_aluno == Aluno.objects.get(id=request.user.id) :
                if matriculas.id_turma_matricula == matricula.id_turma_matricula:
                    reg = True
                    break
                else : 
                    continue
            else :
                continue  
        if reg == False:    
            if form.is_valid():
                matricula.save()
                print("Matricula Realizada")
                return redirect('/Matricular')
        else :
            print("JA REGISTRADO")
    else:
        form = MatriculaForm()
    contexto = {
		"form":form,
        "reg":reg,
    }
    return render(request, "AlunoMatricula.html", contexto)