import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import shutil
import os

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

    # Gráfico de barras
    if 'Vendas' in df.columns or 'Visitantes' in df.columns or 'Faturamento' in df.columns:
        if 'Vendas' in df.columns:
            df.groupby('Data')['Vendas'].sum().plot(kind='bar', alpha=0.7, label='Total de Vendas', color='blue', width=0.3)

        if 'Visitantes' in df.columns:
            df.groupby('Data')['Visitantes'].sum().plot(kind='bar', alpha=0.7, label='Total de Visitantes', color='orange', width=0.3)

        if 'Faturamento' in df.columns:
            df.groupby('Data')['Faturamento'].mean().plot(kind='bar', alpha=0.7, label='Faturamento Médio', color='green', width=0.3)

        plt.title("Métricas por Dia")
        plt.xlabel("Data")
        plt.ylabel("Valores")
        plt.legend()
        plt.tight_layout()
        plt.show()
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
