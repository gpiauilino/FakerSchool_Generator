# %%
# initialize a generator


#Dataset escolar com dados randomicos projetado para amostra do Microsoft Customer Insights
#Padrão escola particular, com estrutura financeira básica.

#-------------------------------
from calendar import month
import os
import re
from typing import Concatenate
import uuid
from collections import defaultdict
from secrets import choice
import random
import numpy as np
import pandas as pd
from faker import Faker
from tqdm import tqdm
import unicodedata
from string import ascii_letters

from random import randrange
from datetime import timedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta

#Definição de conteudo da lib para dados Brasileiros
fake = Faker(['pt_BR'])

def tirar_acentos(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

remove_letra = lambda x, unwanted : ''.join([ c for i, c in enumerate(x) if i != unwanted])

def gerar_polos():
    for polo in polos:
        id_Polo = uuid.uuid1().int
        lista_ids_polos.append(id_Polo)

        fake_polos["idPolo"].append(id_Polo)
        fake_polos["Nome"].append(polo)
        fake_polos["UF"].append(np.random.choice(uf_endereco))
        fake_polos["QTSalas"].append(qtSalas)
        fake_polos["Endereco"].append(fake.street_name())

def gerar_professores():
    # Professores
    for _ in tqdm(range(qtProfessores), desc = "Escolhendo professores"):
        id_professor = uuid.uuid1().int
        lista_ids_professores.append(id_professor)
        fake_professores['idProfessor'].append(id_professor)
        fake_professores['nivelEscolar'].append(np.random.choice(professores_nivelescolar))
        fake_professores['nome'].append(fake.name())
        fake_professores['classeProfessor'].append(np.random.choice(classeprofessores))
        fake_professores['nomePolo'].append(np.random.choice(polos))

def gerar_alunos():
    ra_matriculas = 0
    # Alunos
    for _ in tqdm(range(qtAtlunos), desc= "Gerando Alunos"):
        
        id_aluno = uuid.uuid1().int
        lista_ids_alunos.append(id_aluno)

        fake_alunos["IdAluno"].append(id_aluno)
        fake_alunos["idPolo"].append(np.random.choice(lista_ids_polos))

        nome_completo = fake.name()
        ultimo_nome = nome_completo.rsplit(' ', 1)[-1]
        
        # nickname = ''.join(e for e in nome_completo if e.isalnum()) # ficou acentos
        nickname = s = re.sub(r"[^a-z0-9]","", tirar_acentos(nome_completo.lower()))

        fake_alunos["Nome"].append(nome_completo) 
        fake_alunos["Sobrenome"].append(ultimo_nome)
        fake_alunos["Idade"].append(fake.random_int(14, 27))
        fake_alunos["Etnia"].append(np.random.choice(etnia_tipo))
        fake_alunos["Genero"].append(np.random.choice(genero_tipo))
        fake_alunos["UF"].append(np.random.choice(uf_endereco))
        fake_alunos['contactPhoto'].append(np.random.choice(urlImage))
        # fake_alunos["email"].append(f"{nickname}@{fake.email().rsplit('@', 1)[-1]}")
        
        s = f"{nickname}@{np.random.choice(dominios)}"
        lista_emails.append(s)
        fake_alunos["email"].append(s)
        fake_alunos['endereco'].append(fake.street_name())
        fake_alunos['cidade'].append(fake.city())


        # Base matricula está no mesmo loop que alunos, relação de 1:1 não sendo necessário novo loop/cada aluno
        ra_matriculas = ra_matriculas + 1
        id_matricula = ra_matriculas

        fake_baseMatricula['id_matricula'].append(id_matricula)
        fake_baseMatricula['idAluno'].append(id_aluno)
        
        # if np.random.choice(status_matricula) == "Inativa":
        #     status_real = np.random.choice(motivo_cancelamento)
        # else:
        #     status_real = ""
        m=np.random.choice(status_matricula)
        status_real = np.random.choice(motivo_cancelamento) if m == "Inativa" else "" 
        fake_baseMatricula['status'].append(m)
        fake_baseMatricula['motivoCancelamento'].append(status_real)

        # Atividades / aluno
        # #print("Atividades / aluno")
        quantidade_de_atividades = np.random.randint(2,7)
        for _ in tqdm(range(quantidade_de_atividades), desc = "Corrigindo provas e atividades"):

            id_atividade = uuid.uuid1().int
            fake_atividades['idAtividade'].append(id_atividade)
            fake_atividades['idAluno'].append(id_aluno)
            fake_atividades['Tipo'].append(np.random.choice(atividades_tipo))
            fake_atividades['Data'].append(fake.date_between(start_date='-5M', end_date='today'))
            fake_atividades['Nota'].append(np.random.choice(perfil_notas))


        #Ocorrencias
        quantidade_de_ocorrencias = np.random.randint(1,3)
        for _ in tqdm(range(quantidade_de_ocorrencias), desc= "Anotando ocorrências"):
            id_ocorrencia = uuid.uuid1().int
            
            fake_ocorrencias['idOcorrencia'].append(id_ocorrencia)      
            fake_ocorrencias['idAluno'].append(id_aluno)
            fake_ocorrencias['Area'].append(np.random.choice(ocorrencias_areas))
            fake_ocorrencias['Tipo'].append(np.random.choice(ocorrencias_tipo))
            fake_ocorrencias['Aula'].append(np.random.choice(disciplinas))
            fake_ocorrencias['Data'].append(fake.date_between(start_date='-5M', end_date='today'))

        #Responsáveis
        for _ in tqdm(range(quantidade_de_responsaveis), desc = "Contatando os pais"):
            
            id_responsavel = uuid.uuid1().int
            lista_ids_responsaveis.append(id_responsavel)
            
            fake_responsaveis['idReponsvel'].append(id_responsavel)
            fake_responsaveis['idAluno'].append(id_aluno)
            fake_responsaveis['grauParentestco'].append(np.random.choice(grau_parentesco))
            fake_responsaveis['telefone'].append(fake.phone_number())
            fake_responsaveis['nome'].append(fake.name())

            # Chamados abertos pelos responsaveis	
            quantidade_de_chamados = np.random.randint(2,4)
            dias_corridos = np.random.randint(3,6)
            for _ in tqdm(range(quantidade_de_chamados), desc = "Registrando chamados"):
                
                id_chamado = uuid.uuid1().int
                lista_ids_chamados.append(id_chamado)
                fake_chamados['idChamado'].append(id_chamado)
                fake_chamados['id_responsavel'].append(id_responsavel)
                fake_chamados['motivo'].append(np.random.choice(chamado_motivo))
                fake_chamados['prioridade'].append(np.random.choice(prioridades_tipo))
                fake_chamados['createdDate'].append(fake.date_between(start_date='-6M', end_date='today'))
                fake_chamados['closeDate'].append(fake.date_between(start_date='-6M', end_date='today'))
                fake_chamados['SLA'].append(np.random.choice(sla))

            # Analytics de NPS do responsavel
            quantidade_de_surveys = np.random.randint(2,4)
            for _ in tqdm(range(quantidade_de_surveys), desc= "NPS Responsável"):
                
                id_RespostaResp = uuid.uuid1().int
                lista_ids_surveys.append(id_RespostaResp)
                fake_analyticsResponsavelNPS['idSurvey'].append(id_RespostaResp)
                fake_analyticsResponsavelNPS['id_responsavel'].append(id_responsavel)
                fake_analyticsResponsavelNPS['data'].append(fake.date_between(start_date='-6M', end_date='today'))
                fake_analyticsResponsavelNPS['nota'].append(np.random.choice(perfil_nps))
                fake_analyticsResponsavelNPS['textDescricao'].append(surveys_textDescricao)

            # Pagamentos
            dias_de_atraso = np.random.randint(0,5)
            data_cobranca = datetime.strptime('2/28/2022', '%m/%d/%Y')
                        
            for _ in tqdm(range (numero_de_pagamentos), desc = "Pagando contas"):

                if np.random.randint(1,101) <= 97:
                    dias_de_atraso = np.random.randint(0,5) 
                    # dt_pagamento = start_date = (dt_cobranca '-3d'), end_date = (dt_cobranca'+3d')     
                    start_dt = data_cobranca - timedelta(days=dias_de_atraso)
                    end_dt = data_cobranca + timedelta(days=dias_de_atraso)
                    dt_pagamento = fake.date_between(start_date=start_dt, end_date=end_dt)
                else:
                    dt_pagamento = ""
                id_pagamento = uuid.uuid1().int
                
                fake_pagamentos['idPagamento'].append(id_pagamento)
                fake_pagamentos['idAluno'].append(id_aluno)
                fake_pagamentos['DataPag'].append(dt_pagamento)
                fake_pagamentos['DataCobranca'].append(data_cobranca)

                if dt_pagamento == "":
                    status_pagamento = "Inadimplente"
                elif dt_pagamento > data_cobranca.date(): 
                    status_pagamento = "Pago com atraso"
                elif dt_pagamento <= data_cobranca.date():
                    status_pagamento = "Quitado"
                else: 
                    status_pagamento = "indef."
                fake_pagamentos['status'].append(status_pagamento)
            
                # PagamentosExtra            
                for _ in tqdm(range(numero_de_pagExtra), "Vendendo extra $$"):
                    
                    id_pagamentoExtra = uuid.uuid1().int
                    
                    fake_pagamentosExtra['idExtra'].append(id_pagamentoExtra)
                    fake_pagamentosExtra['idPagamento'].append(id_pagamento)
                    fake_pagamentosExtra['DataPag'].append(fake.date_between(start_date= '-6M', end_date='today'))
                    fake_pagamentosExtra['tipo'].append(np.random.choice(pagExtra_tipo))
                    fake_pagamentosExtra['valor'].append(np.random.uniform(15.3,51.4))
                
                data_cobranca = data_cobranca + relativedelta(months=1)

        ################################################################
        # Aulas
        for _ in tqdm(range(quantidade_de_aulas), desc = "Criando aulas"):
            
            id_aula = uuid.uuid1().int
            lista_ids_aulas.append(id_aula)
            fake_aulas['idAula'].append(id_aula)
            fake_aulas['data'].append(fake.date_between(start_date='-5M', end_date='today'))
            fake_aulas['disciplina'].append(np.random.choice(disciplinas))
            fake_aulas['cargaHoraria'].append(np.random.choice(carga_horariaAula))

            # Presenca dos alunos
            for _ in tqdm(range(quantidade_de_aulasPordia), desc = "Anotando quem faltou"):
                
                id_presenca_discente = uuid.uuid1().int
                lista_ids_presenca_discente.append(id_presenca_discente)
                fake_PresencaDiscente['idPresencaDiscente'].append(id_presenca_discente)
                fake_PresencaDiscente['idAluno'].append(id_aluno)
                fake_PresencaDiscente['idAula'].append(id_aula)
                fake_PresencaDiscente['nps_Professor'].append(np.random.choice(perfil_nps_Professor))
                fake_PresencaDiscente['nps_Conteudo'].append(np.random.choice(perfil_nps_Conteudo))
                fake_PresencaDiscente['status'].append(np.random.choice(status_presenca))


            # Presenca dos professores        
            for _ in tqdm(range(quantidade_de_aulasPordia), desc = "Validando professores"):
                
                id_presenca_docente = uuid.uuid1().int
                fake_PresencaDocente['idPresencaDocente'].append(id_presenca_docente)
                fake_PresencaDocente['idProfessor'].append(np.random.choice(lista_ids_professores))
                fake_PresencaDocente['idAula'].append(id_aula)
                fake_PresencaDocente['status'].append(np.random.choice(status_presenca))




        ################################################################
        #Web Analytics para análise de acessos e interação com plataforma de conteudos da escola, considerando email do aluno
        quantidade_de_acessos = np.random.randint(10,400)
        for _ in tqdm(range(quantidade_de_acessos), "Web Analytics"):
            #print('Gerando dados de Web Analytics')
            id_Web = uuid.uuid1().int
            lista_de_ids_acessos.append(id_Web)
                    
            fake_analytics_webAccess['idWeb'].append(id_Web)
            #fake_analytics_webAccess['idAluno'].append(id_aluno)
            e = np.random.choice(lista_emails)
            fake_analytics_webAccess['email'].append(e)
            
            e = remove_letra(e,np.random.randint(5))
            fake_analytics_webAccess['email_rem'].append(e)
            
            inds = [i for i,_ in enumerate(e) if not e.isspace()]
            sam = random.sample(inds, 3)
            letts =  iter(random.sample(ascii_letters, 3))
            lst = list(e)
            for ind in sam:
                lst[ind] = next(letts)

            fake_analytics_webAccess['email_rem2'].append("".join(lst))            
                
            fake_analytics_webAccess['idAluno'].append(id_aluno)

            ##############################################################
            #File Contents        
            quantidade_actions = np.random.randint(1,3)
            for _ in tqdm(range(quantidade_actions), "Analisando ações na web"):
                #print('Gerando dados de Web Analytics')
                idContent = np.random.choice(ids_contents)
                lista_ids_fileContents.append(idContent)
                        
                fake_fileContents['idWeb'].append(id_Web)
                fake_fileContents['idContent'].append(idContent)
                #fake_fileContents['data'].append(fake.date_between(start_date='-5M', end_date='today'))
                


    # %%

if __name__ == '__main__':

    n=0
    for _ in range(10):
        n = n + 1
        print(f'RA{n:05}')

    
    #Parametros da Escola
    nps = np.random.randint(1,5)
    #Quantidade de alunos por escola
    qtAtlunos = 1500
    #quantidade de professores no total
    qtProfessores = 35
    #quantiade média de salas por escola
    qtSalas = np.random.randint(3,6)
    quantidade_de_responsaveis = np.random.randint(1,2)
    numero_de_pagamentos = 5
    numero_de_pagExtra = 6
    quantidade_de_aulas = 100
    quantidade_de_aulasPordia = 5


    # %%

    #class faker.providers.person.pt_BR.Provider(generator: Any)

    #Tabelas
    fake_alunos = defaultdict(list)
    fake_responsaveis = defaultdict(list)
    fake_ocorrencias = defaultdict(list)
    fake_atividades = defaultdict(list)
    fake_aulas = defaultdict(list)
    fake_PresencaDiscente= defaultdict(list)
    fake_PresencaDocente = defaultdict(list)
    fake_professores = defaultdict(list)
    fake_pagamentos = defaultdict(list)
    fake_pagamentosExtra = defaultdict(list)
    fake_chamados = defaultdict(list)
    fake_analyticsResponsavelNPS = defaultdict(list)


    fake_baseMatricula = defaultdict(list)
    fake_polos = defaultdict(list)
    fake_analytics_webAccess = defaultdict(list)
    fake_fileContents = defaultdict(list)

    ocorrencias_areas = ['Pátio', 'Cantina', 'Sala de aula', 'Quadra de Esportes', 'Banheiros','Laboratório','Biblioteca','Pátio','Sala de aula','Pátio','Sala de aula','Pátio','Sala de aula']
    ocorrencias_tipo = ['Grave', 'Notificação', 'Moderada', 'Leve','Moderada', 'Leve','Moderada', 'Leve','Moderada', 'Leve']
    atividades_tipo = ['Prova', 'Esportiva', 'Trabalho de casa','Trabalho em grupo','Laboratorial', 'Trabalho de casa','Trabalho em grupo','Trabalho de casa','Trabalho em grupo','Prova', 'Prova', 'Prova']
    atividade_extra = ['Curso Extra','Compra de Livros', 'Atividade Cultura']
    genero_tipo = ['Masculino','Feminino','Não-binário','Masculino','Feminino']
    etnia_tipo = ['Indígena','Negro','Branco','Pardo','Mulato','Caboclo','Cafuzo','Negro','Branco','Pardo','Negro','Branco','Pardo','Negro','Branco','Pardo']

    classe_matricula = ['A','B','C']
    serie_matricula = ['1º','2º','3º']
    status_matricula = ['Ativa','Ativa','Ativa','Ativa','Ativa','Ativa','Ativa','Ativa','Ativa','Ativa','Ativa','Inativa']
    motivo_cancelamento = ['Desistência','Motivos financeiros','Insatisfação','Motivos financeiros','Insatisfação','Motivos financeiros','Insatisfação','Insatisfação','Insatisfação','Insatisfação']

    uf_endereco = ['SP','SP','SP','SP','SP','RJ','RJ','RJ','RJ','MG','MG','MG','BA','CE','PE','PI','PR','SC','MA','AM']
    status_aula =['Presente','Falta']

    disciplinas = ['Matemática','Português','Biologia','Química','Geografia','Informática','Física','Astronomia']
    grau_parentesco = ['1º','2º','3º']
    professores_nivelescolar = ['Superior Completo','Mestrado','Doutorado','Mestrado','Mestrado','Mestrado','Mestrado']
    prioridades_tipo = ['Baixa','Média','Alta','Média','Alta','Média','Alta','Média','Alta']
    chamado_motivo = ['Problemas com acesso na escola','Problemas com acesso na escola','Problemas com acesso na escola','Problemas com acesso ao portal','Boleto sem baixa','Atualização cadastral','Financiamento escolar','Atualização cadastral','Financiamento escolar','Atualização cadastral','Financiamento escolar','Atualização cadastral','Financiamento escolar','Programa de inclusão','Isenção de taxas','Outros']
    aula_nome = ['Normal','Conjunta','Aula de campo','Laboratorial']
    polos = ['Smart A', 'Smart B', 'Smart C']
    dominios = ['gmail.com', 'hotmail.com', 'instituicao.com.br','live.com.br','hotmail.com.br','outlook.com.br','bol.com.br','yahoo.com.br','yahoo.com.br']
    surveys_textDescricao = ["Como você responsável avalia o nosso sistema de ensino?"]

    perfil_notas = [0,1,2,3,4,4,5,5,6,6,7,7,7,8,8,8,8,9,9,9,9,9,9,9,9,10,10,10,10,10]
    perfil_nps = [1,2,3,4,4,4,4,4,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5]
    perfil_nps_Professor = [1,2,3,4,4,4,4,4,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5]
    perfil_nps_Conteudo = [1,2,3,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5]
    status_presenca = ['Presente', 'Presente','Presente','Presente','Presente','Presente','Presente','Presente','Presente','Presente','Presente','Presente','Faltou']
    sla = [0,0,0,0,0,0,0,0,0,0,0,1]
    ids_contents = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]

    #status_pagamento = ['Quitado','Quitado','Quitado','Quitado','Quitado','Quitado','Quitado','Quitado','Quitado','Quitado','Quitado','Inadimplente']
    pagExtra_tipo = ['Unidade Extra Curricular', 'Livro', 'Teatro', 'Museu', 'Evento', 'Livro', 'Livro', 'Livro', 'Livro', 'Livro', 'Livro','Unidade Extra Curricular','Unidade Extra Curricular','Unidade Extra Curricular','Unidade Extra Curricular','Unidade Extra Curricular']
    classeprofessores = ['Dedicado','Dedicado','Dedicado','Dedicado','Dedicado','Dedicado','Dedicado','Dedicado','Dedicado','Dedicado','Dedicado', 'Part-time', 'Convidado', 'Convidado', 'Convidado']
    letras = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x,','y','z']


    carga_horariaAula = [1,1,1,1,1,1,2,2]

    urlImage = ['https://i2.wp.com/gatinhobranco.com/wp-content/uploads/2018/02/pounce-livro-gatinhos-pulando-fotografia.jpg?fit=932%2C500&ssl=1',
    'https://super.abril.com.br/wp-content/uploads/2016/11/gatinhos-filhotes-reconhecem-a-voz-da-prc3b3pria-mc3a3e.jpg?resize=630,420',
    'https://static7.depositphotos.com/1029178/785/i/950/depositphotos_7859857-stock-photo-little-cat-read-a-book.jpg',
    'https://i.pinimg.com/736x/57/c1/fb/57c1fb34f435bb21c86cfd3ab4d46d7a.jpg',
    'https://i.pinimg.com/736x/a9/ad/77/a9ad77698ef583b4bd0f972aa20a0519.jpg',
    'https://i0.wp.com/www.portaldodog.com.br/cachorros/wp-content/uploads/2019/12/dogue-de-bordeaux-1047521_1280.jpg?fit=1000%2C666&ssl=1&resize=1280%2C720',
    'http://sc04.alicdn.com/kf/H506e860dada5440c8a29672e84a15a66q.jpg']





    # %%

    #Unidades estudantis (Polos)


    lista_ids_alunos = []
    lista_ids_polos = []    
    lista_ids_professores = []
    lista_ids_surveys = []
    lista_ids_chamados = []
    lista_ids_responsaveis = []
    lista_emails = []
    lista_ids_pagamentos = []
    lista_ids_pagamentosExtra = []
    lista_ids_aulas = []
    lista_ids_presenca_discente = []
    lista_de_ids_acessos = []
    lista_de_ids_matricula = []
    lista_ids_fileContents = []

    gerar_polos()
    gerar_professores()
    gerar_alunos()
    
    #Inicio de exportacao para csv

    print("Salvando tudim em CSV")

    os.chdir('C:\\Projetos\\DummySchool\\FakerSchool_Generator\\Dataset')

    pd.DataFrame(fake_alunos).to_csv("alunos.csv", index=False)
    pd.DataFrame(fake_ocorrencias).to_csv("ocorrencias.csv", index=False)
    pd.DataFrame(fake_atividades).to_csv("atividades.csv", index=False)
    pd.DataFrame(fake_aulas).to_csv("aulas.csv", index=False)
    pd.DataFrame(fake_PresencaDiscente).to_csv("presencaDiscente.csv", index=False)
    pd.DataFrame(fake_PresencaDocente).to_csv("presencaDocente.csv", index=False)
    pd.DataFrame(fake_professores).to_csv("professores.csv", index=False)
    pd.DataFrame(fake_pagamentos).to_csv("pagamentos.csv", index=False)
    pd.DataFrame(fake_pagamentosExtra).to_csv("pagamentosExtra.csv", index=False)
    pd.DataFrame(fake_chamados).to_csv("chamados.csv", index=False)
    pd.DataFrame(fake_analyticsResponsavelNPS).to_csv("analyticsResponsavelNPS.csv", index=False)
    pd.DataFrame(fake_baseMatricula).to_csv("baseMatricula.csv", index=False)
    pd.DataFrame(fake_polos).to_csv("polos.csv", index=False)
    pd.DataFrame(fake_analytics_webAccess).to_csv("analytics_WebAccess.csv",index=False)
    pd.DataFrame(fake_fileContents).to_csv("fileContents.csv", index=False)
    pd.DataFrame(fake_responsaveis).to_csv("responsaveis.csv", index=False)

    print("Concluído")
