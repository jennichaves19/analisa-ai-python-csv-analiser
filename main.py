import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt

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
        total_funcionarios = df['Funcionarios'].nunique() if 'Funcionarios' in df.columns else "N/A"

        resultado_label.config(text=f"Total de Visitantes: {total_visitas}\n"
                                    f"Faturamento Médio: {faturamento_medio}\n"
                                    f"Total de Vendas: {total_vendas}\n"
                                    f"Total de Funcionários: {total_funcionarios}")

        gerar_grafico_btn.config(state=tk.NORMAL)
        gerar_grafico_btn.df = df

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao processar os dados: {e}")

# Função para gerar gráficos
def gerar_grafico():
    df = gerar_grafico_btn.df

    plt.figure()

    if 'Vendas' in df.columns or 'Visitantes' in df.columns or 'Faturamento' in df.columns:
        if 'Vendas' in df.columns:
            df.groupby('Data')['Vendas'].sum().plot(kind='bar', alpha=0.7, label='Vendas')

        if 'Visitantes' in df.columns:
            df.groupby('Data')['Visitantes'].sum().plot(kind='bar', alpha=0.7, label='Visitantes')

        if 'Faturamento' in df.columns:
            df.groupby('Data')['Faturamento'].sum().plot(kind='bar', alpha=0.7, label='Faturamento')

        plt.title("Métricas por Dia")
        plt.xlabel("Data")
        plt.ylabel("Valores")
        plt.legend()
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

# Estilo dos botões
def update_button_style():
    if gerar_grafico_btn['state'] == tk.NORMAL:
        gerar_grafico_btn.config(bg="#008CBA", fg="white")
    else:
        gerar_grafico_btn.config(bg="white", fg="gray")

gerar_grafico_btn.bind("<Configure>", lambda e: update_button_style())

# Executar a interface
root.mainloop()
