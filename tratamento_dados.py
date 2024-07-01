import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Função para obter o caminho do diretório onde o script está localizado
def get_script_dir():
    return os.path.dirname(os.path.abspath(__file__))

def classificar_iri(iri_medio):
    if iri_medio < 1.9:
        return 1
    elif 1.9 <= iri_medio < 2.7:
        return 2
    elif 2.7 <= iri_medio < 3.5:
        return 3
    elif 3.5 <= iri_medio < 4.6:
        return 4
    else:  # iri_medio >= 4.6
        return 5

def pegar_dados_agrupados(dados_ano):
    #variáveis auxiliares para identificar os segmentos
    km_0 = dados[:, 1][0]
    km_1 = km_0

    soma_iri = 0
    soma_flecha = 0
    soma_igg = 0
    soma_panela = 0
    soma_trinca = 0
    soma_remendo = 0

    segmentos_iri = []
    segmentos_flecha = []
    segmentos_igg = []
    segmentos_panela = []
    segmentos_trinca = []
    segmentos_remendo = []
    classificacao_iri = []
    km_referencia = []

    iri_exc = []
    iri_bom = []
    iri_reg = []
    iri_rui = []
    iri_pes = []

    contar_posicao_iri_exc = 0
    contar_posicao_iri_bom = 0
    contar_posicao_iri_reg = 0
    contar_posicao_iri_rui = 0
    contar_posicao_iri_pes = 0

    contar_loop = 0

    #loop para rodar cada linha dos dados
    for i, km in enumerate(dados_ano[:, 1]):
        #iterando todos os km's para agrupar os segmentos
        km_1 = km
        #tamanho mínimo do segmento
        segmento_min = 10
        #Colunas: IRI - 4 / flecha - 5 / IGG - 6 / panelas/buracos - 7 / trincamento - 8
        soma_iri += dados_ano[i][4]
        soma_flecha += dados_ano[i][5]
        soma_igg += dados_ano[i][6]
        soma_panela += dados_ano[i][7]
        soma_trinca += dados_ano[i][8]
        soma_remendo += dados_ano[i][15]

        if km_1 - km_0 >= segmento_min:

            km_referencia.append(km)

            iri_segmento = soma_iri/contar_loop         #é uma média
            flexa_segmento = soma_flecha/contar_loop    #é uma média
            igg_segmento = soma_igg/contar_loop         #é uma média
            panela_segmento = soma_panela               #é a soma
            trinca_segmento = soma_trinca/contar_loop   #é uma média
            remendo_segmento = soma_remendo/contar_loop   #é uma média
            
            #salvar todos os valores dos segmentos em uma lista
            segmentos_iri.append(iri_segmento)
            segmentos_flecha.append(flexa_segmento)
            segmentos_igg.append(igg_segmento)
            segmentos_panela.append(panela_segmento)
            segmentos_trinca.append(trinca_segmento)
            segmentos_remendo.append(remendo_segmento)

            #classificando o iri de todos os segmentos e salvando todos em uma lista
            classe_iri = classificar_iri(iri_segmento)
            classificacao_iri.append(classe_iri)

            #agrupando todos os defeitos de acordo com a classificação do IRI
            if classe_iri == 1:
                iri_exc.append((contar_posicao_iri_exc, iri_segmento, flexa_segmento, igg_segmento, panela_segmento, trinca_segmento, remendo_segmento))
                contar_posicao_iri_exc += 1
            elif classe_iri == 2:
                iri_bom.append((contar_posicao_iri_bom, iri_segmento, flexa_segmento, igg_segmento, panela_segmento, trinca_segmento, remendo_segmento))
                contar_posicao_iri_bom += 1
            elif classe_iri == 3:
                iri_reg.append((contar_posicao_iri_reg, iri_segmento, flexa_segmento, igg_segmento, panela_segmento, trinca_segmento, remendo_segmento))
                contar_posicao_iri_reg += 1
            elif classe_iri == 4:
                iri_rui.append((contar_posicao_iri_rui, iri_segmento, flexa_segmento, igg_segmento, panela_segmento, trinca_segmento, remendo_segmento))
                contar_posicao_iri_rui += 1
            else:
                iri_pes.append((contar_posicao_iri_pes, iri_segmento, flexa_segmento, igg_segmento, panela_segmento, trinca_segmento, remendo_segmento))
                contar_posicao_iri_pes += 1

            #Caso não coloquemos o agrupamento, mas sim por km, decomentaros if's
            # if classe_iri == 1:
            #     iri_exc.append((km, contar_panelas/contar_loop))
            #     km += 1
            # elif classe_iri == 2:
            #     iri_bom.append((km, contar_panelas/contar_loop))
            #     km += 1
            # elif classe_iri == 3:
            #     iri_reg.append((km, contar_panelas/contar_loop))
            #     km += 1
            # elif classe_iri == 4:
            #     iri_rui.append((km, contar_panelas/contar_loop))
            #     km += 1
            # else:
            #     iri_pes.append((km, contar_panelas/contar_loop))
            #     km += 1

            #zerando as variáveis para contar tudo de novo para o novo segmento
            soma_iri = 0
            soma_flecha = 0
            soma_igg = 0
            soma_panela = 0
            soma_trinca = 0
            soma_remendo = 0

            contar_loop = 0
            km_0 = km_1

        if i == (len(dados_ano[:, 1]) - 1):
            km_referencia.append(km)

            iri_segmento = soma_iri/contar_loop         #é uma média
            flexa_segmento = soma_flecha/contar_loop    #é uma média
            igg_segmento = soma_igg/contar_loop         #é uma média
            panela_segmento = soma_panela               #é a soma
            trinca_segmento = soma_trinca/contar_loop   #é uma média
            remendo_segmento = soma_remendo/contar_loop   #é uma média
            
            #salvar todos os valores dos segmentos em uma lista
            segmentos_iri.append(iri_segmento)
            segmentos_flecha.append(flexa_segmento)
            segmentos_igg.append(igg_segmento)
            segmentos_panela.append(panela_segmento)
            segmentos_trinca.append(trinca_segmento)
            segmentos_remendo.append(remendo_segmento)

            #classificando o iri de todos os segmentos e salvando todos em uma lista
            classe_iri = classificar_iri(iri_segmento)
            classificacao_iri.append(classe_iri)

            #agrupando todos os defeitos de acordo com a classificação do IRI
            if classe_iri == 1:
                iri_exc.append((contar_posicao_iri_exc, iri_segmento, flexa_segmento, igg_segmento, panela_segmento, trinca_segmento, remendo_segmento))
                contar_posicao_iri_exc += 1
            elif classe_iri == 2:
                iri_bom.append((contar_posicao_iri_bom, iri_segmento, flexa_segmento, igg_segmento, panela_segmento, trinca_segmento, remendo_segmento))
                contar_posicao_iri_bom += 1
            elif classe_iri == 3:
                iri_reg.append((contar_posicao_iri_reg, iri_segmento, flexa_segmento, igg_segmento, panela_segmento, trinca_segmento, remendo_segmento))
                contar_posicao_iri_reg += 1
            elif classe_iri == 4:
                iri_rui.append((contar_posicao_iri_rui, iri_segmento, flexa_segmento, igg_segmento, panela_segmento, trinca_segmento, remendo_segmento))
                contar_posicao_iri_rui += 1
            else:
                iri_pes.append((contar_posicao_iri_pes, iri_segmento, flexa_segmento, igg_segmento, panela_segmento, trinca_segmento, remendo_segmento))
                contar_posicao_iri_pes += 1

            #zerando as variáveis para contar tudo de novo para o novo segmento
            soma_iri = 0
            soma_flecha = 0
            soma_igg = 0
            soma_panela = 0
            soma_trinca = 0
            soma_remendo = 0

            contar_loop = 0
            km_0 = km_1
        
        contar_loop += 1

    array_kms = np.array(km_referencia)
    array_iri = np.array(segmentos_iri)
    array_flechas = np.array(segmentos_flecha)
    array_iggs = np.array(segmentos_igg)
    array_panelas = np.array(segmentos_panela)
    array_trincas = np.array(segmentos_trinca)
    array_remendo = np.array(segmentos_remendo)
    array_classificacao_iri = np.array(classificacao_iri)

    array_iri_exc = np.array(iri_exc)
    array_iri_bom = np.array(iri_bom)
    array_iri_reg = np.array(iri_reg)
    array_iri_rui = np.array(iri_rui)
    array_iri_pes = np.array(iri_pes)

    for row in array_iri_bom:
        row[0] = row[0] + contar_posicao_iri_exc

    for row in array_iri_reg:
        row[0] = row[0] + contar_posicao_iri_exc + contar_posicao_iri_bom

    for row in array_iri_rui:
        row[0] = row[0] + contar_posicao_iri_exc + contar_posicao_iri_bom + contar_posicao_iri_reg

    for row in array_iri_pes:
        row[0] = row[0] + contar_posicao_iri_exc + contar_posicao_iri_bom + contar_posicao_iri_reg + contar_posicao_iri_rui

    return array_iri_exc, array_iri_bom, array_iri_reg, array_iri_rui, array_iri_pes

def plotar(exc, bom, reg, rui, pes, defeito, escala):
    #Defeitos = Índice Segmento - 0, IRI - 1, Flexa - 2, IGG - 3, Panela - 4, Trincamento - 5

    legenda_ano = ['2014', '2015', '2017', '2018', '2020', '2021', '2022']
    legenda_defeito = ['Índice Segmento', 'IRI', 'Flecha', 'IGG', 'Panela', 'Trincamento', 'Remendo']
    legenda_unidade = ['(un)', '', '(mm)', '', '(un)', '(%)', '(%)']
    escala_eixo_y = [40, 7, 10, 250, 400, 100, 12]

    # Configurar o tamanho da figura
    plt.figure(figsize=(12, 6))

    for i in range(len(legenda_ano)):
        # Gráfico de colunas 2014
        plt.subplot(2, 4, i+1)  # 2 linha, 4 colunas, 1º gráfico
        if len(exc[i]) > 0:
            plt.bar(exc[i][:, 0], exc[i][:, defeito], color='blue', label="Excelente",width=0.8)
        if len(bom[i]) > 0:
            plt.bar(bom[i][:, 0], bom[i][:, defeito], color='green', label="Boa",width=0.8)
        if len(reg[i]) > 0:
            plt.bar(reg[i][:, 0], reg[i][:, defeito], color='orange', label="Regular",width=0.8)
        if len(rui[i]) > 0:
            plt.bar(rui[i][:, 0], rui[i][:, defeito], color='brown', label="Ruim",width=0.8)
        if len(pes[i]) > 0:
            plt.bar(pes[i][:, 0], pes[i][:, defeito], color='red', label="Péssima",width=0.8)

        plt.title(f'{legenda_ano[i]}', fontsize=16, fontweight='bold')
        plt.xlabel('Agrupamento dos segmentos', fontsize=15)
        plt.ylabel(f'{legenda_defeito[defeito]} {legenda_unidade[defeito]}', fontsize=16)
        plt.gca().set_xticklabels([])
        if escala == 'sim':
            plt.ylim(0, escala_eixo_y[defeito])

        # Adicionar uma legenda consolidada fora do loop na posição (2, 4, 8)
        ax = plt.subplot(2, 4, 8)  # Posiciona a legenda no subplot 8
        # Criar uma legenda combinada
        labels = ['Excelente', 'Boa', 'Regular', 'Ruim', 'Péssima']
        colors = ['blue', 'green', 'orange', 'brown', 'red']
        handles = [plt.Line2D([0], [0], color=color, lw=5) for color in colors]
        ax.legend(handles, labels, fontsize=16)
        ax.axis('off')  # Desativar o eixo para o subplot da legenda

    #Não haver sobreposição
    plt.tight_layout()
    # Exibição do gráfico
    plt.show()

anos = ['2014', '2015', '2017', '2018', '2020', '2021', '2022']
classe_exc = []
classe_bom = []
classe_reg = []
classe_rui = []
classe_pes = []

for a, ano in enumerate(anos):
    pasta = os.path.join(get_script_dir(), f'dados_txt/{ano}.txt')
    #lendo dados e transformando em np.array
    df = pd.read_csv(pasta, delimiter='\t')
    dados = np.array(df)

    agrupamento_iri_exc, agrupamento_iri_bom, agrupamento_iri_reg, agrupamento_iri_rui, agrupamento_iri_pes = pegar_dados_agrupados(dados_ano=dados)

    classe_exc.append(agrupamento_iri_exc)
    classe_bom.append(agrupamento_iri_bom)
    classe_reg.append(agrupamento_iri_reg)
    classe_rui.append(agrupamento_iri_rui)
    classe_pes.append(agrupamento_iri_pes)






#====================DEFINA QUAL É O DEFEITO A SER ANALISADO AQUI========================
#Defeitos = Índice Segmento - 0, IRI - 1, Flexa - 2, IGG - 3, Panela - 4, Trincamento - 5, Remendo - 6
plotar(classe_exc, classe_bom, classe_reg, classe_rui, classe_pes, defeito=3, escala="sim")