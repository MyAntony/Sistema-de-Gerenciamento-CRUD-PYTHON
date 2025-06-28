import customtkinter as ctk
from tkinter import messagebox, ttk

class JanelaPecas:
    def __init__(self, parent, crud_obj):
        self.crud_obj = crud_obj
        self.window = ctk.CTkToplevel(parent)
        self.window.title("LogiTrack - Gerenciar Peças")
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

        labels = ["Nome", "Descrição", "Fabricante", "Preço", "Quantidade"]
        self.entries = []
        for i, label in enumerate(labels):
            ctk.CTkLabel(self.window, text=label + ":").grid(row=1 + i // 2, column=(i % 2) * 2, padx=10, pady=5, sticky="w")
            entry = ctk.CTkEntry(self.window, width=150)
            entry.grid(row=1 + i // 2, column=(i % 2) * 2 + 1, padx=10, pady=5)
            self.entries.append(entry)

        button_frame = ctk.CTkFrame(self.window)
        button_frame.grid(row=5, column=0, columnspan=4, padx=20, pady=20)
        ctk.CTkButton(button_frame, text="Criar", command=self.create_peca).grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Atualizar", command=self.atualizar_peca).grid(row=0, column=1, padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Excluir", command=self.delete_peca).grid(row=0, column=2, padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Limpar", command=self.campos_vazios).grid(row=0, column=3, padx=10, pady=5)

        columns = ("ID", "Nome", "Descrição", "Fabricante", "Preço", "Quantidade")
        self.tree = ttk.Treeview(self.window, columns=columns, show="headings", height=8)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def create_peca(self):
        try:
            values = [e.get() for e in self.entries]
            if not values[0] or not values[1]:
                messagebox.showerror("Erro", "Nome e Descrição são obrigatórios.")
                return
            id_peca = self.crud_obj.create_peca(*values)
            self.recarregar_lista()
            self.campos_vazios()
            messagebox.showinfo("Sucesso", f"Peça cadastrada com sucesso! ID: {id_peca}")
        except Exception as e:
            messagebox.showerror("Erro", f"Verifique os dados: {e}")

    def atualizar_peca(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione uma peça para atualizar.")
            return
        item = self.tree.item(selected[0])
        id_peca = str(item['values'][0])
        try:
            values = [e.get() for e in self.entries]
            self.crud_obj.atualizar_peca(
                id_peca,
                nome=values[0],
                descricao=values[1],
                fabricante=values[2],
                preco=values[3],
                quantidade=values[4]
            )
            self.recarregar_lista()
            self.campos_vazios()
            messagebox.showinfo("Sucesso", "Peça atualizada com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Verifique os dados: {e}")

    def delete_peca(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione uma peça para excluir.")
            return
        item = self.tree.item(selected[0])
        id_peca = str(item['values'][0])
        self.crud_obj.delete_peca(id_peca)
        self.recarregar_lista()
        self.campos_vazios()
        messagebox.showinfo("Sucesso", "Peça excluída com sucesso!")

    def campos_vazios(self):
        for e in self.entries:
            e.delete(0, 'end')

    def recarregar_lista(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        pecas = self.crud_obj.list_all_pecas()
        for peca in pecas:
            self.tree.insert('', 'end', values=(
                peca['ID_Peca'],
                peca['Nome'],
                peca['Descricao'],
                peca['Fabricante'],
                peca['Preco'],
                peca['Quantidade']
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
        # Pega o termo digitado na barra de pesquisa e converte para minúsculo
        termo = self.search_entry.get().lower()
        # Limpa a Treeview para mostrar apenas os resultados filtrados
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Busca todas as peças cadastradas
        pecas = self.crud_obj.list_all_pecas()
        encontrados = []  # Lista para armazenar as peças encontradas
        # Para cada peça, verifica se o termo pesquisado aparece em qualquer campo
        for peca in pecas:
            if any(termo in str(valor).lower() for valor in peca.values()):
                # Se encontrar, insere a peça na Treeview
                self.tree.insert('', 'end', values=(
                    peca['ID_Peca'],
                    peca['Nome'],
                    peca['Descricao'],
                    peca['Fabricante'],
                    peca['Preco'],
                    peca['Quantidade']
                ))
                encontrados.append(peca)  # Adiciona à lista de encontrados
        # Se encontrou pelo menos uma peça, preenche os campos do formulário com a primeira encontrada
        if len(encontrados) >= 1:
            campos = [
                encontrados[0]['Nome'],
                encontrados[0]['Descricao'],
                encontrados[0]['Fabricante'],
                encontrados[0]['Preco'],
                encontrados[0]['Quantidade']
            ]
            # Preenche cada campo do formulário com os dados da peça encontrada
            for entry, valor in zip(self.entries, campos):
                entry.delete(0, 'end')
                entry.insert(0, valor)
