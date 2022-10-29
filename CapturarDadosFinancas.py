from tkinter import ttk, Tk
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas_datareader import data as webdata

'''
Author: Gabriel Sampaio Pichane

City: Hortolândia, SP

Country: Brasil

Version: 1.0B

'''
# tempo de amostra
start_date = "01/01/2012"
end_date = "10/01/2022"

# Janela config
janela = Tk()
stylejanela = ttk.Style()

# Style janela configuration
janela.configure(background='#08020D')
stylejanela.configure('TLabel', font=('Arial', 10), fontweight='bold', foreground="#FF5733")
stylejanela.configure('TButton', font=('Arial', 8), background='#08020D', fontweight='bold', borderwidth='10',
                      foreground="#FF5733")
stylejanela.configure('TEntry', font=('Arial', 10), background='#08020D', fontweight='bold', foreground='#35095A')

# Titulo
janela.title('Ações')
janela.geometry("1280x600")
janela.maxsize(1280, 920)

# Criando GUI Graph

figure = plt.figure(figsize=(9, 5), dpi=80, facecolor='#08020D')

ax = figure.add_subplot(111)
ax.tick_params(axis='x', colors='red')
ax.tick_params(axis='y', colors='red')
ax.patch.set_facecolor('#08020D')


# Função (def) captar dados API yahoo finances
def pegar_acoes_web_yahoo():
    acao_desejada = str.upper(edit_acoes_usuario.get())
    if acao_desejada is not None:
        cotacoes = webdata.DataReader(f'{acao_desejada}', data_source='yahoo', start=start_date, end=end_date)
        print(cotacoes)
        fechamento = cotacoes['Adj Close']

        date = pd.date_range(start=start_date, end=end_date, freq="B")
        fechamento = fechamento.reindex(date)
        fechamento = fechamento.fillna(method='ffill')

        canva = FigureCanvasTkAgg(figure, janela)
        canva.get_tk_widget().place(relx=0.2, rely=0.5, anchor='w')

        closegraph = fechamento

        ax.plot(closegraph.index, closegraph, color="#FF5733", label=f"{acao_desejada}")
        ax.set_xlabel('Date', color="#FF5733", fontweight='bold')
        ax.set_ylabel('Adjusted closing price ($)', color="#FF5733", fontweight='bold')
        ax.legend()


# Função (def) captar dados de uma tabela do excell
def capturar_dados_tabelinha():
    ler_plan_dados = pd.read_excel("Dados.xlsx")

    for dados in ler_plan_dados["TICKER"]:
        cotacoes2 = webdata.DataReader(f'{dados}', data_source='yahoo', start=start_date, end=end_date)

        fechamento2 = cotacoes2['Adj Close']

        date = pd.date_range(start=start_date, end=end_date, freq="B")
        fechamento2 = fechamento2.reindex(date)
        fechamento2 = fechamento2.fillna(method='ffill')

        canva = FigureCanvasTkAgg(figure, janela)
        canva.get_tk_widget().place(relx=0.2, rely=0.5, anchor='w')

        closegraph2 = fechamento2

        ax.plot(closegraph2.index, closegraph2, label=dados)
        ax.set_xlabel('Date', color="#FF5733", fontweight='bold')
        ax.set_ylabel('Adjusted closing price ($)', color="#FF5733", fontweight='bold')
        ax.legend()


def adicionar_dados_tabelinha():
    tabela_dados_frame = pd.read_excel("Dados.xlsx")
    df1 = {"TICKER": [edit_acoes_usuario.get().upper()]}
    acao_usuario = pd.DataFrame(df1, index={1})
    print(acao_usuario)
    dados_usuario_planframe = pd.concat([tabela_dados_frame, acao_usuario], axis=0, ignore_index=False)
    dados_usuario_planframe.dropna()
    dados_usuario_planframe.to_excel("Dados.xlsx", index=False)
    print(dados_usuario_planframe)


# Confi GUI

edit_acoes_usuario = ttk.Entry(janela)
edit_acoes_usuario.place(relx=0.35, rely=0.07, anchor='ne')

botao_buscar = ttk.Button(janela, text='YAHOO FINANCES', command=pegar_acoes_web_yahoo)
botao_buscar.place(relx=0.45, rely=0.07, anchor='ne')

botao_buscar2 = ttk.Button(janela, text='Buscar Tabelinha', command=capturar_dados_tabelinha)
botao_buscar2.place(relx=0.56, rely=0.07, anchor='ne')

botao_buscar3 = ttk.Button(janela, text='Adicionar Tabelinha', command=adicionar_dados_tabelinha)
botao_buscar3.place(relx=0.2, rely=0.3, anchor='e')

# Loop para permanecer janela aberta "infinitamente"
janela.mainloop()
