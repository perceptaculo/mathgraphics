import math
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import interp1d
import numpy as np
import PySimpleGUI as sg

fig = plt.figure(figsize=(10, 6))
pointsy = []
pointsx = []
pointsx2= []
pointsy2= []
tabela_pontos = pd.read_csv("real_dados.csv", sep=';')
ti=0
tf=0

def janela_intervalo():
    sg.theme('Reddit')
    layout = [
        [sg.Text("Mês Inicial (1 a 35): ", size=(15, 1)), sg.Input(key= 'ti', size=(4, 1))],
        [sg.Text("Mês final (2 a 36): ", size=(15, 1)), sg.Input(key= 'tf', size=(4, 1))],
        [sg.Button("Continuar", button_color='red', size=(10, 1)),
         sg.Button("Finalizar", button_color='red', size=(10,1))]
    ]
    return sg.Window('Gerador de Gráfico', layout=layout, icon='logo.ico', finalize=True)

def janela_final():
    sg.theme('Reddit')
    layout = [
          [sg.Text("Cor para a temperatura real"),
           sg.Radio('azul', "RADIO1", default=True), sg.Radio('preto', "RADIO1"), sg.Radio('amarelo', "RADIO1")],
          [sg.Text("Cor para a temperatura teórica"),
           sg.Radio('vermelho', "RADIO2"), sg.Radio('verde', "RADIO2"), sg.Radio('ciano', "RADIO2", default=True)],
          [sg.Listbox(values=('Real', 'Teorico', 'Comparativo'), size=(30, 3))],
          [sg.Button('Gerar Gráfico', button_color='green', size=(15,1)), sg.Button("Voltar", button_color='orange', size=(15,1)),
           sg.Button("Finalizar", button_color='red', size=(15,1))]
    ]
    return sg.Window('Gerador de Gráfico', layout=layout, icon='logo.ico', finalize=True)

janela1, janela2 = janela_intervalo(), None
while True:
    window, event, values = sg.read_all_windows()
    if window == janela1 and event == sg.WIN_CLOSED:
        break
    if window == janela1 and event == 'Finalizar':
        break
    if window == janela1 and event == 'Continuar':
        janela2 = janela_final()
        janela1.hide()
        tinicial = int(values['ti'])
        tfinal = int(values['tf'])

    if window == janela2 and event == 'Gerar Gráfico':
        janela2.hide()
        cores1 = ['blue', 'black', 'yellow', 'red', 'green', 'cyan']
        for i in range(0, 3):
            if values[i] == True:
                color_1 = cores1[i]
        for i in range(3, 6):
            if values[i] == True:
                color_2 = cores1[i]

        # grafico real
        for n in range(tinicial, tfinal + 1):
            a = str(n)
            y2 = tabela_pontos[a].mean()
            pointsy2.append(y2.round(2))
            pointsx2.append(n)
        # grafico teorico
        for x in range(tinicial, tfinal + 1):
            x = x
            y = 5 * math.sin(math.pi / 6 * (x + 3)) + (0.2 * math.pi / 6 * (x + 3)) + 20
            pointsx.append(x)
            pointsy.append(y)

        if values[6] == ['Comparativo']:
            plt.bar(pointsx2, pointsy2, color=color_1, width=-0.4, align='edge')
            plt.bar(pointsx, pointsy, color=color_2, alpha=1, align='edge', width=0.4)
            plt.xlabel("Mês", fontsize=13)
            plt.ylabel("Temperatura Média(Graus Celsius)", fontsize=13)
            plt.title('Comparativo entre temperatura real e teórica')
            plt.legend(['Temperatura Real', "Temperatura Teorica"])
            plt.show()

        if values[6] == ['Teorico']:
            cubic_interploation_model = interp1d(pointsx, pointsy, kind="cubic")
            xs = np.linspace(tinicial, tfinal, 500)
            ys = cubic_interploation_model(xs)
            plt.plot(xs, ys, lw=2, color=color_2)
            plt.grid(color='gray', linestyle='-', linewidth=1)
            plt.xlabel("Mês", fontsize=13)
            plt.ylabel("Temperatura Média(Graus Celsius)", fontsize=13)
            plt.title('Temperatura teórica de janeiro de 2018 a dezembro de 2020')
            plt.show()

        if values[6] == ['Real']:
            plt.bar(pointsx2, pointsy2, lw=2, color=color_1, width=0.5)
            plt.xlabel("Mês", fontsize=13)
            plt.ylabel("Temperatura Média(Graus Celsius)", fontsize=13)
            plt.title('Temperatura real de janeiro de 2018 a dezembro de 2020')
            plt.show()
        if plt.close: #fechando o pyplot fecha-se o programa
            break
    if window == janela2 and event == "Voltar":
        janela2.hide()
        janela1.un_hide()
    if window == janela2 and event == 'Finalizar':
        break