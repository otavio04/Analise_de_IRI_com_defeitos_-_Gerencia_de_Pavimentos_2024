import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.optimize import curve_fit



#====================DEFINA QUAL É O DEFEITO A SER ANALISADO AQUI========================
#Defeitos = Índice Segmento - 0, IRI - 1, Flexa - 2, IGG - 3, Panela - 4, Trincamento - 5, Remendo - 6
defeito_ = 3

#====================DEFINA QUAL É A PARTIÇÃO MÍNIMA DO TRECHO AQUI========================
tamanho_minimo_segmento = 10 #km



def model(x, a, b):
    return a * x + b

def selecionar_defeito(a, b, c, d, e, f, opcao):
    if opcao == 1:
        return a
    elif opcao == 2:
        return b
    elif opcao == 3:
        return c
    elif opcao == 4:
        return d
    elif opcao == 5:
        return e
    elif opcao == 6:
        return f
    elif opcao == 0:
        return 0

def analise_classes_iri(exc, bom, reg, rui, pes, defeito):

    legenda_ano = ['2014', '2015', '2017', '2018', '2020', '2021', '2022']
    legenda_defeito = ['Índice Segmento', 'IRI', 'Flecha', 'IGG', 'Panela', 'Trincamento', 'Remendo']
    legenda_unidade = ['(un)', '', '(mm)', '', '(un)', '(%)', '(%)']

    # Configurar o tamanho da figura
    plt.figure(figsize=(12, 6))

    for i in range (len(legenda_ano)):

        n_exc = 0
        n_bom = 0
        n_reg = 0
        n_rui = 0
        n_pes = 0

        media_exc = 0
        media_bom = 0
        media_reg = 0
        media_rui = 0
        media_pes = 0

        if len(exc[i]) > 0:
            n_exc = len(exc[i][:, defeito])
            media_exc = np.average(exc[i][:, defeito])

        if len(bom[i]) > 0:
            n_bom = len(bom[i][:, defeito])
            media_bom = np.average(bom[i][:, defeito])

        if len(reg[i]) > 0:
            n_reg = len(reg[i][:, defeito])
            media_reg = np.average(reg[i][:, defeito])

        if len(rui[i]) > 0:
            n_rui = len(rui[i][:, defeito])
            media_rui = np.average(rui[i][:, defeito])

        if len(pes[i]) > 0:
            n_pes = len(pes[i][:, defeito])
            media_pes = np.average(pes[i][:, defeito])
        
        n = np.array([n_exc, n_bom, n_reg, n_rui, n_pes])
        media = np.array([media_exc, media_bom, media_reg, media_rui, media_pes])
        
        # Gráfico de colunas 2014
        plt.subplot(2, 4, i+1)  # 2 linha, 4 colunas, 1º gráfico
        barras = plt.bar(['Excelente', 'Bom', 'Regular', 'Ruim', 'Péssimo'], media, 
                         color=['blue', 'green', 'orange', 'brown', 'red'])

        plt.title(f'{legenda_ano[i]}', fontsize=15, fontweight='bold')
        plt.xlabel('Classe IRI', fontsize=15)
        plt.ylabel(f'{legenda_defeito[defeito]} médio{legenda_unidade[defeito]}', fontsize=15)
        plt.ylim(0, max(media)*1.15)
        # plt.legend()

        # Inclinação do eixo x e alinhamento a direita
        plt.xticks(rotation=45, ha='right')  # rotação e alinhamento à direita dos ticks
        # Aumentar a fonte das escalas dos dois eixos
        plt.tick_params(axis='both', labelsize=12)

        # Adicionando rótulos nas barras com os valores de IGG
        for j, barra in enumerate(barras):
            height = barra.get_height()
            plt.annotate(f'{media[j]:.2f}',
                         xy=(barra.get_x() + barra.get_width() / 2, height),
                         xytext=(0, 3),  # offset vertical
                         textcoords="offset points",
                         ha='center', va='bottom', fontsize=9)
        
        if defeito == 3:
            # Limites IGG 20, 40, 80 e 160
            y_lines = [20, 40, 80, 160]
            x_max = (4.7)  # Ajustar a posição para ficar dentro dos limites do gráfico
            for y_line in y_lines:
                plt.axhline(y=y_line, color='purple', alpha=0.8, linestyle='--', linewidth=0.5)
                plt.text(x_max, y_line, f'{y_line}', color='purple', alpha=0.8, verticalalignment='center', horizontalalignment='left')
            
            # Ajustando escala aos dados
            plt.ylim(0, max(max(media), 160)*1.15)

        elif defeito == 1:
            # Limites IRI 1.9, 2.7, 3.5 e 4.6
            y_lines = [1.9, 2.7, 3.5, 4.6]
            x_max = (4.7)  # Ajustar a posição para ficar dentro dos limites do gráfico
            for y_line in y_lines:
                plt.axhline(y=y_line, color='purple', alpha=0.8, linestyle='--', linewidth=0.5)
                plt.text(x_max, y_line, f'{y_line}', color='purple', alpha=0.8, verticalalignment='center', horizontalalignment='left')
            
            # Ajustando escala aos dados
            plt.ylim(0, max(max(media), 4.6)*1.15)
        
        
    #Não haver sobreposição
    plt.tight_layout()
    # Exibição do gráfico
    plt.show()

def estatistica(dados_y, dados_x, defeito):

    # Configurar o tamanho da figura
    plt.figure(figsize=(12, 6))
    legenda_ano = ['2014', '2015', '2017', '2018', '2020', '2021', '2022']
    legenda_defeito = ['Índice Segmento', 'IRI', 'Flecha', 'IGG', 'Panela', 'Trincamento', 'Remendo']
    legenda_unidade = ['(un)', '', '(mm)', '', '(un)', '(%)', '(%)']

    for i in range(len(dados_y)):

        chute_inicial = [1, 1]
        # Ajuste dos parâmetros usando curve_fit com os chutes iniciais
        params, covariance = curve_fit(model, dados_x[i], dados_y[i], p0=chute_inicial)
        a, b = params

        # y previstos
        y_pred = [model(x_dados, a, b) for x_dados in dados_x[i]]

        # Média dos valores observados
        y_mean = np.mean(dados_y[i])
        # Soma dos quadrados dos resíduos
        ss_res = np.sum((dados_y[i] - y_pred) ** 2)

        # Soma dos quadrados totais
        ss_tot = np.sum((dados_y[i] - y_mean) ** 2)

        # Calcular o coeficiente de determinação (R²)
        r2 = 1 - (ss_res / ss_tot)

        # Gráfico de colunas 2014
        plt.subplot(2, 4, i+1)  # 2 linha, 4 colunas, 1º gráfico
        plt.scatter(dados_x[i], dados_y[i], color='blue', alpha=0.2, label=f'R² = {round(r2, 2)}')

        # Gere pontos x para plotar a reta
        x_line = np.linspace(min(dados_x[i]), max(dados_x[i]), 100)
        y_line = a * x_line + b

        # Plote a reta
        plt.plot(x_line, y_line, color='blue', label=f'y = {round(a, 2)}x + {round(b, 2)}')

        plt.title(f'{legenda_ano[i]}', fontsize=16, fontweight='bold')
        plt.xlabel(f'{legenda_defeito[defeito]} {legenda_unidade[defeito]}', fontsize=16)
        plt.ylabel('IRI', fontsize=16)
        plt.legend()

    #Não haver sobreposição
    plt.tight_layout()
    # Exibição do gráfico
    plt.show()

def plotar_histogramas(exc, bom, reg, rui, pes, defeito, escala):
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

        if defeito == 3:
            # Limites IGG 20, 40, 80 e 160
            y_lines = [20, 40, 80, 160]
            x_max = (len(exc[i]) + len(bom[i]) + len(reg[i]) + len(rui[i]) + len(pes[i])) * 1.05  # Ajustar a posição para ficar dentro dos limites do gráfico
            for y_line in y_lines:
                plt.axhline(y=y_line, color='purple', alpha=0.8, linestyle='--', linewidth=0.5)
                plt.text(x_max, y_line, f'{y_line}', color='purple', alpha=0.8, verticalalignment='center', horizontalalignment='left')
        elif defeito == 1:
            # Limites IRI 1.9, 2.7, 3.5 e 4.6
            y_lines = [1.9, 2.7, 3.5, 4.6]
            x_max = (len(exc[i]) + len(bom[i]) + len(reg[i]) + len(rui[i]) + len(pes[i])) * 1.05  # Ajustar a posição para ficar dentro dos limites do gráfico
            for y_line in y_lines:
                plt.axhline(y=y_line, color='purple', alpha=0.8, linestyle='--', linewidth=0.5)
                plt.text(x_max, y_line, f'{y_line}', color='purple', alpha=0.8, verticalalignment='center', horizontalalignment='left')

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

def pegar_dados_agrupados(dados_ano, segmento_min):
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

    return array_iri_exc, array_iri_bom, array_iri_reg, array_iri_rui, array_iri_pes, array_iri, array_flechas, array_iggs, array_panelas, array_trincas, array_remendo

def get_script_dir():
    return os.path.dirname(os.path.abspath(__file__))

anos = ['2014', '2015', '2017', '2018', '2020', '2021', '2022']
classe_exc = []
classe_bom = []
classe_reg = []
classe_rui = []
classe_pes = []

segmentos_iri = []
segmentos_flecha = []
segmentos_igg = []
segmentos_panela = []
segmentos_trincamento = []
segmentos_remendo = []

for a, ano in enumerate(anos):
    pasta = os.path.join(get_script_dir(), f'dados_txt/{ano}.txt')
    #lendo dados e transformando em np.array
    df = pd.read_csv(pasta, delimiter='\t')
    dados = np.array(df)

    i_exc, i_bom, i_reg, i_rui, i_pes, seg_iri, seg_flecha, seg_igg, seg_panela, seg_trinca, seg_remendo = pegar_dados_agrupados(dados_ano=dados, segmento_min=tamanho_minimo_segmento)

    classe_exc.append(i_exc)
    classe_bom.append(i_bom)
    classe_reg.append(i_reg)
    classe_rui.append(i_rui)
    classe_pes.append(i_pes)

    segmentos_iri.append(seg_iri)
    segmentos_flecha.append(seg_flecha)
    segmentos_igg.append(seg_igg)
    segmentos_panela.append(seg_panela)
    segmentos_trincamento.append(seg_trinca)
    segmentos_remendo.append(seg_remendo)


#====================HISTOGRAMAS========================
plotar_histogramas(classe_exc, classe_bom, classe_reg, classe_rui, classe_pes, defeito=defeito_, escala="sim")

#====================ESTATÍSTICA COM IRI========================
if defeito_ != 0:
    defeito_escolhido = selecionar_defeito(a=segmentos_iri, b=segmentos_flecha, c=segmentos_igg, d=segmentos_panela, e=segmentos_trincamento, f=segmentos_remendo, opcao=defeito_)
    estatistica(segmentos_iri, defeito_escolhido, defeito=defeito_)

#====================ANÁLISE POR CLASSE DE IRI========================
analise_classes_iri(classe_exc, classe_bom, classe_reg, classe_rui, classe_pes, defeito=defeito_)