import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


def carregar_dados(caminho_arquivo):
    data = pd.read_csv(caminho_arquivo)
    return data


def preparar_dados(data):
    data = pd.get_dummies(data, drop_first=True)
    X = data.drop('Preco', axis=1)
    y = data['Preco']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X, X_scaled, y, scaler


def treinar_modelo(X, X_scaled, y):
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model


def prever_voo():
    try:
        duracao = float(duracao_entry.get())
        distancia = float(distancia_entry.get())
        companhia = companhia_combo.get()
        destino = destino_combo.get()
        classe = classe_combo.get()
        tipo_aeronave = tipo_aeronave_combo.get()


        input_data = {
            'Duracao_Voo': [duracao],
            'Distancia': [distancia],
            'Companhia_Aerea_' + companhia: [1] if companhia in companhias else [0],
            'Destino_' + destino: [1] if destino in destinos else [0],
            'Classe_' + classe: [1] if classe in classes else [0],
            'Tipo_Aeronave_' + tipo_aeronave: [1] if tipo_aeronave in tipos_aeronave else [0]
        }

        input_df = pd.DataFrame(input_data)
        input_df = input_df.reindex(columns=X.columns, fill_value=0)
        input_scaled = scaler.transform(input_df)

        preco_previsto = model.predict(input_scaled)[0]
        resultado_label.config(text=f"Preço Previsto: R${preco_previsto:.2f}")

    except Exception as e:
        resultado_label.config(text=f"Erro: {e}")

# Função para visualizar dados
def visualizar_dados():
    if dados is not None:
        top = tk.Toplevel(root)
        top.title("Visualizar Dados")
        tabela = ttk.Treeview(top, columns=list(dados.columns), show="headings")

        for col in dados.columns:
            tabela.heading(col, text=col)
            tabela.column(col, width=100)

        for _, row in dados.iterrows():
            tabela.insert("", "end", values=row.tolist())

        tabela.pack(expand=True, fill="both")
    else:
        resultado_label.config(text="Dados não carregados.")


def prever_disponibilidade():
    try:
        duracao = float(duracao_entry.get())
        tempo_chegada_estimado = pd.to_datetime('now') + pd.to_timedelta(duracao, unit='h')
        disponibilidade_label.config(text=f"Disponível em: {tempo_chegada_estimado}")

    except Exception as e:
        disponibilidade_label.config(text=f"Erro: {e}")

def configurar_interface(root, companhias, destinos, classes, tipos_aeronave):

    tk.Label(root, text="Duração do Voo (horas):").grid(row=0, column=0)
    global duracao_entry
    duracao_entry = tk.Entry(root)
    duracao_entry.grid(row=0, column=1)

    tk.Label(root, text="Distância (km):").grid(row=1, column=0)
    global distancia_entry
    distancia_entry = tk.Entry(root)
    distancia_entry.grid(row=1, column=1)

    tk.Label(root, text="Companhia Aérea:").grid(row=2, column=0)
    global companhia_combo
    companhia_combo = ttk.Combobox(root, values=companhias)
    companhia_combo.grid(row=2, column=1)

    tk.Label(root, text="Destino:").grid(row=3, column=0)
    global destino_combo
    destino_combo = ttk.Combobox(root, values=destinos)
    destino_combo.grid(row=3, column=1)

    tk.Label(root, text="Classe:").grid(row=4, column=0)
    global classe_combo
    classe_combo = ttk.Combobox(root, values=classes)
    classe_combo.grid(row=4, column=1)

    tk.Label(root, text="Tipo de Aeronave:").grid(row=5, column=0)
    global tipo_aeronave_combo
    tipo_aeronave_combo = ttk.Combobox(root, values=tipos_aeronave)
    tipo_aeronave_combo.grid(row=5, column=1)


    prever_button = tk.Button(root, text="Prever Preço", command=prever_voo)
    prever_button.grid(row=6, column=0, columnspan=2)


    global resultado_label
    resultado_label = tk.Label(root, text="")
    resultado_label.grid(row=7, column=0, columnspan=2)


    visualizar_button = tk.Button(root, text="Visualizar Dados", command=visualizar_dados)
    visualizar_button.grid(row=8, column=0, columnspan=2)


    prever_disponibilidade_button = tk.Button(root, text="Prever Disponibilidade", command=prever_disponibilidade)
    prever_disponibilidade_button.grid(row=9, column=0, columnspan=2)


    global disponibilidade_label
    disponibilidade_label = tk.Label(root, text="")
    disponibilidade_label.grid(row=10, column=0, columnspan=2)



dados = carregar_dados('dados_voo.csv')
X, X_scaled, y, scaler = preparar_dados(dados)
model = treinar_modelo(X, X_scaled, y)


companhias = [col.replace('Companhia_Aerea_', '') for col in X.columns if 'Companhia_Aerea_' in col]
destinos = [col.replace('Destino_', '') for col in X.columns if 'Destino_' in col]
classes = [col.replace('Classe_', '') for col in X.columns if 'Classe_' in col]
tipos_aeronave = [col.replace('Tipo_Aeronave_', '') for col in X.columns if 'Tipo_Aeronave_' in col]


root = tk.Tk()
root.title("Previsão de Preço de Voo")
configurar_interface(root, companhias, destinos, classes, tipos_aeronave)
root.mainloop()
