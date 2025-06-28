import customtkinter as ctk
from tkinter import messagebox, ttk

class JanelaCaminhoes:
    def __init__(self, parent, crud_obj):
        self.crud_obj = crud_obj
        self.window = ctk.CTkToplevel(parent)
        self.window.title("LogiTrack - Gerenciar Caminhões")
        self.window.geometry("900x700")
        self.criar_janelinhas()
        self.recarregar_lista()

    def criar_janelinhas(self):
        # Barra de pesquisa
        barrinha_de_pesquisa = ctk.CTkFrame(self.window)
        barrinha_de_pesquisa.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
        ctk.CTkLabel(barrinha_de_pesquisa, text="Pesquisar:").pack(side="left", padx=5)
        self.search_entry = ctk.CTkEntry(barrinha_de_pesquisa, width=200)
        self.search_entry.pack(side="left", padx=5)
        ctk.CTkButton(barrinha_de_pesquisa, text="Buscar", command=self.pesquisar).pack(side="left", padx=5)
        ctk.CTkButton(barrinha_de_pesquisa, text="Limpar", command=self.recarregar_lista).pack(side="left", padx=5)

        labels = ["Marca", "Modelo", "Ano", "Placa", "Quilometragem", "Status"]
        self.entries = []
        for i, label in enumerate(labels):
            ctk.CTkLabel(self.window, text=label + ":").grid(row=1 + i // 2, column=(i % 2) * 2, padx=10, pady=5, sticky="w")
            entry = ctk.CTkEntry(self.window, width=150)
            entry.grid(row=1 + i // 2, column=(i % 2) * 2 + 1, padx=10, pady=5)
            self.entries.append(entry)

        button_frame = ctk.CTkFrame(self.window)
        button_frame.grid(row=5, column=0, columnspan=4, padx=20, pady=20)
        ctk.CTkButton(button_frame, text="Criar", command=self.criar_caminhao).grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Atualizar", command=self.atualizar_caminhao).grid(row=0, column=1, padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Excluir", command=self.deletar_caminhao).grid(row=0, column=2, padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Limpar", command=self.campos_vazios).grid(row=0, column=3, padx=10, pady=5)

        columns = ("ID", "Marca", "Modelo", "Ano", "Placa", "Quilometragem", "Status")
        self.tree = ttk.Treeview(self.window, columns=columns, show="headings", height=8)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def criar_caminhao(self):
        try:
            values = [e.get() for e in self.entries]
            if not values[0] or not values[1]:
                messagebox.showerror("Erro", "Marca e Modelo são obrigatórios.")
                return
            id_caminhao = self.crud_obj.criar_caminhao(*values)
            self.recarregar_lista()
            self.campos_vazios()
            messagebox.showinfo("Sucesso", f"Caminhão cadastrado com sucesso! ID: {id_caminhao}")
        except Exception as e:
            messagebox.showerror("Erro", f"Verifique os dados: {e}")

    def atualizar_caminhao(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um caminhão para atualizar.")
            return
        item = self.tree.item(selected[0])
        id_caminhao = str(item['values'][0])
        try:
            values = [e.get() for e in self.entries]
            self.crud_obj.atualizar_caminhao(
                id_caminhao,
                marca=values[0],
                modelo=values[1],
                ano=values[2],
                placa=values[3],
                quilometragem=values[4],
                status=values[5]
            )
            self.recarregar_lista()
            self.campos_vazios()
            messagebox.showinfo("Sucesso", "Caminhão atualizado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Verifique os dados: {e}")

    def deletar_caminhao(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um caminhão para excluir.")
            return
        item = self.tree.item(selected[0])
        id_caminhao = str(item['values'][0])
        self.crud_obj.deletar_caminhao(id_caminhao)
        self.recarregar_lista()
        self.campos_vazios()
        messagebox.showinfo("Sucesso", "Caminhão excluído com sucesso!")

    def campos_vazios(self):
        for e in self.entries:
            e.delete(0, 'end')

    def recarregar_lista(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        caminhoes = self.crud_obj.listar_todos_caminhoes()
        for caminhao in caminhoes:
            self.tree.insert('', 'end', values=(
                caminhao['ID_Caminhao'],
                caminhao['Marca'],
                caminhao['Modelo'],
                caminhao['Ano'],
                caminhao['Placa'],
                caminhao['Quilometragem'],
                caminhao['Status']
            ))

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0])['values']
        for i, e in enumerate(self.entries):
            e.delete(0, 'end')
            e.insert(0, values[i+1])

    def pesquisar(self):
        # Obtém o termo digitado na barra de pesquisa e converte para minúsculo
        termo = self.search_entry.get().lower()
        
        # Limpa todos os itens atuais da Treeview para mostrar apenas os resultados filtrados
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Busca todos os caminhões cadastrados
        caminhoes = self.crud_obj.listar_todos_caminhoes()
        encontrados = []  # Lista para armazenar os caminhões que correspondem à pesquisa
        
        # Para cada caminhão, verifica se o termo pesquisado aparece em qualquer campo
        for caminhao in caminhoes:
            if any(termo in str(valor).lower() for valor in caminhao.values()):
                # Se encontrar, insere o caminhão na Treeview
                self.tree.insert('', 'end', values=(
                    caminhao['ID_Caminhao'],
                    caminhao['Marca'],
                    caminhao['Modelo'],
                    caminhao['Ano'],
                    caminhao['Placa'],
                    caminhao['Quilometragem'],
                    caminhao['Status']
                ))
                encontrados.append(caminhao)  # Adiciona à lista de encontrados
        
        # Se encontrou pelo menos um caminhão, preenche os campos do formulário com o primeiro encontrado
        if len(encontrados) >= 1:
            campos = [
                encontrados[0]['Marca'],
                encontrados[0]['Modelo'],
                encontrados[0]['Ano'],
                encontrados[0]['Placa'],
                encontrados[0]['Quilometragem'],
                encontrados[0]['Status']
            ]
            # Preenche cada campo do formulário com os dados do caminhão encontrado
            for entry, valor in zip(self.entries, campos):
                entry.delete(0, 'end')
                entry.insert(0, valor)
