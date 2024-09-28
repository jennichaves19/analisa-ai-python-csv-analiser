import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Função para abrir o arquivo
def abrir_arquivo():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path, encoding='utf-8', delimiter=';')
                print(df.head())
            else:
                df = pd.read_excel(file_path)

            # Converter a coluna 'Data' para o formato correto (DD/MM/YYYY)
            if 'Data' in df.columns:
                df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')

            gerar_grafico_btn.df = df  # Armazenar o DataFrame no botão para uso posterior
            processar_dados(df)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar o arquivo: {e}")

# Função para processar dados e gerar informações
def processar_dados(df):
    try:
        total_visitas = df['Visitantes'].sum() if 'Visitantes' in df.columns else "N/A"
        faturamento_medio = df['Faturamento'].mean() if 'Faturamento' in df.columns else "N/A"
        total_vendas = df['Vendas'].sum() if 'Vendas' in df.columns else "N/A"

        resultado_label.config(text=f"Total de Visitantes: {total_visitas}\n"
                                    f"Faturamento Médio: {faturamento_medio}\n"
                                    f"Total de Vendas: {total_vendas}")

        gerar_grafico_btn.config(state=tk.NORMAL)
        update_button_style()  # Atualizar estilo do botão ao habilitar

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao processar os dados: {e}")

# Função para gerar gráficos
def gerar_grafico():
    df = gerar_grafico_btn.df

    plt.figure(figsize=(10, 6))

    # Gráfico de barras agrupadas
    if 'Vendas' in df.columns or 'Visitantes' in df.columns or 'Faturamento' in df.columns:
        df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')  # Assegura que a data esteja no formato correto
        df['Data'] = df['Data'].dt.strftime('%d/%m/%Y')  # Formatar data no formato DD/MM/YYYY

        # Agrupar por data e somar/média as colunas
        grouped = df.groupby('Data').sum()

        # Certifique-se de que todos os dados têm o mesmo número de linhas
        n_groups = len(grouped.index)
        bar_width = 0.25
        index = np.arange(n_groups)

        # Verificar se as colunas existem e criar barras somente se os dados forem consistentes
        if 'Vendas' in grouped.columns:
            vendas_data = grouped['Vendas']
        else:
            vendas_data = [0] * n_groups  # Dados vazios se a coluna não existir

        if 'Visitantes' in grouped.columns:
            visitantes_data = grouped['Visitantes']
        else:
            visitantes_data = [0] * n_groups

        if 'Faturamento' in grouped.columns:
            faturamento_data = grouped['Faturamento']
        else:
            faturamento_data = [0] * n_groups

        # Garantir que todas as colunas têm o mesmo tamanho
        if len(vendas_data) == len(visitantes_data) == len(faturamento_data):
            # Criar barras para cada métrica
            plt.bar(index, vendas_data, bar_width, label='Total de Vendas', color='blue')
            plt.bar(index + bar_width, visitantes_data, bar_width, label='Total de Visitantes', color='orange')
            plt.bar(index + 2 * bar_width, faturamento_data, bar_width, label='Faturamento Médio', color='green')

            plt.title("Métricas por Dia")
            plt.xlabel("Data")
            plt.ylabel("Valores")
            plt.xticks(index + bar_width, grouped.index, rotation=45)  # Rotaciona as datas no eixo x para melhor visualização
            plt.legend()
            plt.tight_layout()
            plt.show()
        else:
            messagebox.showerror("Erro", "Os dados têm tamanhos inconsistentes e não podem ser plotados.")
    else:
        messagebox.showerror("Erro", "Não foi possível gerar o gráfico. Colunas 'Vendas', 'Visitantes' ou 'Faturamento' não encontradas.")

# Função para baixar o CSV de exemplo
def baixar_csv_exemplo():
    try:
        # Caminho do arquivo de exemplo
        caminho_exemplo = 'resources/exemplo_dados.csv'  # Ajuste o caminho aqui
        destino = filedialog.asksaveasfilename(defaultextension=".csv",
                                               filetypes=[("CSV files", "*.csv")])
        if destino:
            shutil.copy(caminho_exemplo, destino)
            messagebox.showinfo("Sucesso", "CSV de exemplo baixado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao baixar o arquivo: {e}")

# Interface gráfica
root = tk.Tk()
root.title("Análise de Dados de Clientes")
root.geometry("600x400")
root.configure(bg="#f0f0f0")

# Centralizar conteúdo
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(expand=True)

# Botão para carregar planilha (azul)
abrir_btn = tk.Button(frame, text="Carregar Planilha", command=abrir_arquivo, bg="#008CBA", fg="white", borderwidth=0, padx=10, pady=5)
abrir_btn.pack(pady=10)

# Botão para baixar CSV de exemplo
baixar_btn = tk.Button(frame, text="Baixar CSV de Exemplo", command=baixar_csv_exemplo, bg="#28a745", fg="white", borderwidth=0, padx=10, pady=5)
baixar_btn.pack(pady=10)

# Label para exibir resultados
resultado_label = tk.Label(frame, text="Nenhum dado carregado. Insira uma planilha CSV (UTF-8 delimitado por vírgulas.)", justify="center", bg="#f0f0f0")
resultado_label.pack(pady=10)

# Botão para gerar gráfico (inicialmente desativado)
gerar_grafico_btn = tk.Button(frame, text="Gerar Gráfico", command=gerar_grafico, state=tk.DISABLED, bg="white", fg="gray", borderwidth=0, padx=10, pady=5)
gerar_grafico_btn.pack(pady=10)

# Estilo dos botões
def update_button_style():
    if gerar_grafico_btn['state'] == tk.NORMAL:
        gerar_grafico_btn.config(bg="#008CBA", fg="white")
    else:
        gerar_grafico_btn.config(bg="white", fg="gray")

# Executar a interface
root.mainloop()
