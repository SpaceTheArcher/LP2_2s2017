"""impacta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from core.views import index
from core.views import page_lista_cursos
from core.views import page_noticias
from core.views import page_login
from core.views import page_nova_senha
from core.views import page_cadastro_disciplina
from core.views import page_contato
from core.views import page_cadastro_usuario
from core.views import page_detalhes_cursos
from core.views import page_detalhes_segdainf
from core.views import page_disciplinas_segdainf
from core.views import page_disciplina_seginfoatualidade
from core.views import page_avisos
from core.views import page_mensagem_aluno
from core.views import page_perfil_professor
from core.views import page_perfil_aluno
from core.views import page_perfil_coordenador
from core.views import page_mensagens_professor
from core.views import page_avisos_aluno
from core.views import page_cadastrar_questao
from core.views import page_responder_questao
from core.views import page_respostas_recebidas
from core.views import page_resumo_tarefas
from core.views import page_aluno_matricula
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name="home"), #index
    url(r'^home/', index), #index
    url(r'^Lista_Cursos/', page_lista_cursos), #Lista De Cursos
    url(r'^Noticias/', page_noticias), #Noticias
    url(r"^Login/", login, {"template_name":"LoginPage.html"}, name="login"), #Pag de Login
    url(r'^Logout/', logout, {'next_page':'home'}, name="logout"),
    url(r'^Nova_Senha/', page_nova_senha, name='change_password'), #Esqueci Minha Senha
    url(r'^Disciplinas/Nova_Disciplina', page_cadastro_disciplina), #Cadastrar Disciplina
    url(r'^Contato/', page_contato), #Contato
    url(r'^Cadastre-se/', page_cadastro_usuario), #Cadastre-se
    url(r'^Detalhes/Cursos/$', page_detalhes_cursos), #Detalhes Cursos
    url(r'^Detalhes/Cursos/SegDaInformacao/', page_detalhes_segdainf), #Detalhes Seg. Da Informação
    url(r'^Disciplinas/SegDaInformacao/', page_disciplinas_segdainf), #Disciplinas Seg. Da Informação
    url(r'^Disciplinas/SegInfoAtualidade/', page_disciplina_seginfoatualidade), #Disciplina Seg. Da Informação na Atualidade
    url(r'^Professor/CriarAviso/', page_avisos),
    url(r'^EnviarMensagem/', page_mensagem_aluno),
    url(r'^PerfilProfessor/', page_perfil_professor),
    url(r'^PerfilAluno/', page_perfil_aluno),
    url(r'^PerfilCoordenador/', page_perfil_coordenador),
    url(r'^Professor/MensagensRecebidas/', page_mensagens_professor),
    url(r'^AvisosRecebidos/', page_avisos_aluno),
    url(r'^Professor/CadastrarQuestao/', page_cadastrar_questao),
    url(r'^QuestoesRecebidas/', page_responder_questao),
    url(r'^Professor/Respostas', page_respostas_recebidas),
    url(r'^Professor/ResumoTarefas', page_resumo_tarefas),
    url(r'^Matricular/', page_aluno_matricula)
]
