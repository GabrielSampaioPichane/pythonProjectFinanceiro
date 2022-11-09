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
v_start_date = "01/01/2012"
v_end_date = "10/29/2022"

# Criação da Janela UI
janela = Tk()
# Adição da biblioteca TKINTER para melhorar a HUD
stylejanela = ttk.Style()

# Style (estilos) Janela
janela.configure(background='#08020D')
stylejanela.configure('TLabel', font=('Arial', 10), fontweight='bold', foreground="#FF5733")
stylejanela.configure('TButton', font=('Arial', 8), background='#08020D', fontweight='bold', borderwidth='10',
                      foreground="#FF5733")
stylejanela.configure('TEntry', font=('Arial', 10), background='#08020D', fontweight='bold', foreground='#35095A')

# Titulo da UI
janela.title('Ações')
janela.geometry("1280x600")
janela.maxsize(1280, 920)

# Criando GUI Graph
V_figure = plt.figure(figsize=(9, 5), dpi=80, facecolor='#08020D')

# Configuração dos eixos do gráfico de vizualização
ax = V_figure.add_subplot(111)
ax.tick_params(axis='x', colors='red')
ax.tick_params(axis='y', colors='red')
ax.patch.set_facecolor('#08020D')


# Função (def) captar dados API yahoo finances
def func_capture_data_yahoo():

    # Lê o input do usuário e converte a escrita para "capslock"
    v_acao_desejada = str.upper(edit_acoes_usuario.get())

    # Verifica se o input do usuário é vazio ou não
    if v_acao_desejada is not None:

        # Captura o dado de input do usuario e envia uma requisição para a API do yahoo finances
        v_cotacoes = webdata.DataReader(f'{v_acao_desejada}', data_source='yahoo', start=v_start_date, end=v_end_date)

        # Apura os dados, selecionando o fechamento ajustado segundo os dados fornecidos pela API
        v_fechamento = v_cotacoes['Adj Close']

        # Apuração dos dados
        v_date = pd.date_range(start=v_start_date, end=v_end_date, freq="B")
        v_fechamento = v_fechamento.reindex(v_date)
        v_fechamento = v_fechamento.fillna(method='ffill')

        # Criação de um gráfico utilizando modelo Canvas para demonstrar ao usuario
        canva = FigureCanvasTkAgg(V_figure, janela)
        canva.get_tk_widget().place(relx=0.2, rely=0.5, anchor='w')

        closegraph = v_fechamento

        ax.plot(closegraph.index, closegraph, color="#FF5733", label=f"{v_acao_desejada}")
        ax.set_xlabel('Date', color="#FF5733", fontweight='bold')
        ax.set_ylabel('Adjusted closing price ($)', color="#FF5733", fontweight='bold')
        ax.legend()


# Função (def) capturar dados de uma tabela do excel
def func_capture_data_excel():
    # Lê os dados da planilha desejada (caso não esteja na mesma pasta que o programa python, adicionar o diretório
    v_ler_plan_dados = pd.read_excel("Dados.xlsx")

    # Lê, nesse caso, a coluna TICKER da planilha acima
    for v_dados in v_ler_plan_dados["TICKER"]:

        # Pesquisa os dados utilizando a API yahoo finances
        v_cotacoes2 = webdata.DataReader(f'{v_dados}', data_source='yahoo', start=v_start_date, end=v_end_date)

        # Apura os dados, selecionando o fechamento ajustado segundo os dados fornecidos pela API
        v_fechamento2 = v_cotacoes2['Adj Close']

        # Apuração dos dados
        v_date = pd.date_range(start=v_start_date, end=v_end_date, freq="B")
        v_fechamento2 = v_fechamento2.reindex(v_date)
        v_fechamento2 = v_fechamento2.fillna(method='ffill')

        # Criação de um gráfico utilizando modelo Canvas para demonstrar ao usuario
        canva = FigureCanvasTkAgg(V_figure, janela)
        canva.get_tk_widget().place(relx=0.2, rely=0.5, anchor='w')

        closegraph2 = v_fechamento2

        ax.plot(closegraph2.index, closegraph2, label=v_dados)
        ax.set_xlabel('Date', color="#FF5733", fontweight='bold')
        ax.set_ylabel('Adjusted closing price ($)', color="#FF5733", fontweight='bold')
        ax.legend()


# Função (def) para salvar dados em uma determinada planilha
def func_save_data_excel():
    # Lê dados de uma planilha/base de dados
    v_tabela_dados_frame = pd.read_excel("Dados.xlsx")

    # Converte em um dataframe
    df1 = {"TICKER": [edit_acoes_usuario.get().upper()]}
    acao_usuario = pd.DataFrame(df1, index={1})

    #  Salva o dataframe concatenando com os dados da planilha em questão
    v_dados_usuario_planframe = pd.concat([v_tabela_dados_frame, acao_usuario], axis=0, ignore_index=False)
    # Limpa células vazias
    v_dados_usuario_planframe.dropna()
    # Salva toda a ação em uma planilha a escolha
    v_dados_usuario_planframe.to_excel("Dados.xlsx", index=False)



# Confi GUI

# Text Input para executar a verificação do dado de acordo com a necessidade
edit_acoes_usuario = ttk.Entry(janela)
edit_acoes_usuario.place(relx=0.35, rely=0.07, anchor='ne')

# Botão TKINTER para executar a função de capturar os dados via API yahoo finances
botao_buscar = ttk.Button(janela, text='YAHOO FINANCES', command=func_capture_data_yahoo)
botao_buscar.place(relx=0.45, rely=0.07, anchor='ne')

# Botão TKINTER para executar a função de capturar os dados via planilha excel
botao_buscar2 = ttk.Button(janela, text='Buscar Tabelinha', command=func_capture_data_excel)
botao_buscar2.place(relx=0.56, rely=0.07, anchor='ne')

# Botão TKINTER para salvar dados na planilha destino
botao_buscar3 = ttk.Button(janela, text='Adicionar Tabelinha', command=func_save_data_excel)
botao_buscar3.place(relx=0.2, rely=0.3, anchor='e')

# Loop para permanecer janela aberta "infinitamente"
janela.mainloop()
