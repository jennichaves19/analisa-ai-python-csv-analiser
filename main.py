import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt

# Função para abrir o arquivo
def abrir_arquivo():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            # Ler o CSV considerando a primeira linha como cabeçalho
            df = pd.read_csv(file_path, encoding='utf-8', delimiter=';', header=0)
            print(df.head())  # Para verificar se os dados foram lidos corretamente

            # Converter a coluna 'Data' para o formato correto (DD/MM/YYYY)
            if 'Data' in df.columns:
                df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')

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

        gerar_grafico_btn.config(state=tk.NORMAL)  # Habilita o botão após processar os dados
        update_button_style()  # Atualiza o estilo do botão
        gerar_grafico_btn.df = df  # Armazena o dataframe para o botão de gerar gráfico

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao processar os dados: {e}")

# Função para atualizar o estilo do botão
def update_button_style():
    if gerar_grafico_btn['state'] == tk.NORMAL:
        gerar_grafico_btn.config(bg="#008CBA", fg="white")
    else:
        gerar_grafico_btn.config(bg="white", fg="gray")

# Função para gerar gráficos
def gerar_grafico():
    df = gerar_grafico_btn.df

    plt.figure(figsize=(10, 6))  # Aumenta o tamanho da figura

    # Definindo cores para cada métrica
    cores = {
        'Vendas': 'blue',
        'Visitantes': 'orange',
        'Faturamento': 'green'
    }

    # Verifica se as colunas existem e plota cada uma
    if 'Data' in df.columns:
        # Agrupar os dados por data
        grouped_data = df.groupby('Data').sum()

        # Tamanho da barra
        bar_width = 0.2  # Largura da barra reduzida

        # Posições das barras
        indices = range(len(grouped_data))

        # Plota cada métrica com largura de barra reduzida
        if 'Vendas' in grouped_data.columns:
            plt.bar([i - bar_width for i in indices], grouped_data['Vendas'], width=bar_width, color=cores['Vendas'], alpha=0.7, label='Vendas')

        if 'Visitantes' in grouped_data.columns:
            plt.bar(indices, grouped_data['Visitantes'], width=bar_width, color=cores['Visitantes'], alpha=0.7, label='Visitantes')

        if 'Faturamento' in grouped_data.columns:
            plt.bar([i + bar_width for i in indices], grouped_data['Faturamento'], width=bar_width, color=cores['Faturamento'], alpha=0.7, label='Faturamento')

        plt.title("Métricas por Dia")
        plt.xlabel("Data")
        plt.ylabel("Valores")
        plt.xticks(indices, grouped_data.index.strftime('%d/%m/%Y'), rotation=45)  # Rotaciona as labels do eixo X
        plt.legend()
        plt.tight_layout()  # Ajusta o layout para melhor visualização
        plt.show()
    else:
        messagebox.showerror("Erro", "Não foi possível gerar o gráfico. Colunas 'Vendas', 'Visitantes' ou 'Faturamento' não encontradas.")

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

# Label para exibir resultados
resultado_label = tk.Label(frame, text="Nenhum dado carregado. Insira uma planilha CSV (UTF-8 delimitado por vírgulas.)", justify="center", bg="#f0f0f0")
resultado_label.pack(pady=10)

# Botão para gerar gráfico (inicialmente desativado)
gerar_grafico_btn = tk.Button(frame, text="Gerar Gráfico", command=gerar_grafico, state=tk.DISABLED, bg="white", fg="gray", borderwidth=0, padx=10, pady=5)
gerar_grafico_btn.pack(pady=10)

# Executar a interface
root.mainloop()
