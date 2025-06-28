import customtkinter as ctk
from tkinter import messagebox, ttk

class JanelaFornecedores:
    def __init__(self, parent, crud_obj):
        self.crud_obj = crud_obj
        self.window = ctk.CTkToplevel(parent)
        self.window.title("LogiTrack - Gerenciar Fornecedores")
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

        labels = ["Nome", "Contato", "Rua", "Bairro", "Cidade", "Estado", "Telefone", "Email"]
        self.entries = []
        for i, label in enumerate(labels):
            ctk.CTkLabel(self.window, text=label + ":").grid(row=1 + i // 2, column=(i % 2) * 2, padx=10, pady=5, sticky="w")
            entry = ctk.CTkEntry(self.window, width=150)
            entry.grid(row=1 + i // 2, column=(i % 2) * 2 + 1, padx=10, pady=5)
            self.entries.append(entry)

        button_frame = ctk.CTkFrame(self.window)
        button_frame.grid(row=6, column=0, columnspan=4, padx=20, pady=20)
        ctk.CTkButton(button_frame, text="Criar", command=self.create_fornecedor).grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Atualizar", command=self.atualizar_fornecedor).grid(row=0, column=1, padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Excluir", command=self.delete_fornecedor).grid(row=0, column=2, padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Limpar", command=self.campos_vazios).grid(row=0, column=3, padx=10, pady=5)

        columns = ("ID", "Nome", "Contato", "Rua", "Bairro", "Cidade", "Estado", "Telefone", "Email")
        self.tree = ttk.Treeview(self.window, columns=columns, show="headings", height=8)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.grid(row=7, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def create_fornecedor(self):
        try:
            values = [e.get() for e in self.entries]
            if not values[0] or not values[1]:
                messagebox.showerror("Erro", "Nome e Contato são obrigatórios.")
                return
            id_fornecedor = self.crud_obj.create_fornecedor(*values)
            self.recarregar_lista()
            self.campos_vazios()
            messagebox.showinfo("Sucesso", f"Fornecedor cadastrado com sucesso! ID: {id_fornecedor}")
        except Exception as e:
            messagebox.showerror("Erro", f"Verifique os dados: {e}")

    def atualizar_fornecedor(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um fornecedor para atualizar.")
            return
        item = self.tree.item(selected[0])
        id_fornecedor = str(item['values'][0])
        try:
            values = [e.get() for e in self.entries]
            self.crud_obj.atualizar_fornecedor(
                id_fornecedor,
                nome=values[0],
                contato=values[1],
                rua=values[2],
                bairro=values[3],
                cidade=values[4],
                estado=values[5],
                telefone=values[6],
                email=values[7]
            )
            self.recarregar_lista()
            self.campos_vazios()
            messagebox.showinfo("Sucesso", "Fornecedor atualizado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Verifique os dados: {e}")

    def delete_fornecedor(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um fornecedor para excluir.")
            return
        item = self.tree.item(selected[0])
        id_fornecedor = str(item['values'][0])
        self.crud_obj.delete_fornecedor(id_fornecedor)
        self.recarregar_lista()
        self.campos_vazios()
        messagebox.showinfo("Sucesso", "Fornecedor excluído com sucesso!")

    def campos_vazios(self):
        for e in self.entries:
            e.delete(0, 'end')

    def recarregar_lista(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        fornecedores = self.crud_obj.list_all_fornecedores()
        for fornecedor in fornecedores:
            self.tree.insert('', 'end', values=(
                fornecedor['ID_Fornecedor'],
                fornecedor['Nome'],
                fornecedor['Contato'],
                fornecedor['Endereco_Rua'],
                fornecedor['Endereco_Bairro'],
                fornecedor['Endereco_Cidade'],
                fornecedor['Endereco_Estado'],
                fornecedor['Telefone'],
                fornecedor['Email']
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
        termo = self.search_entry.get().lower()
        for row in self.tree.get_children():
            self.tree.delete(row)
        fornecedores = self.crud_obj.list_all_fornecedores()
        encontrados = []
        for fornecedor in fornecedores:
            if any(termo in str(valor).lower() for valor in fornecedor.values()):
                self.tree.insert('', 'end', values=(
                    fornecedor['ID_Fornecedor'],
                    fornecedor['Nome'],
                    fornecedor['Contato'],
                    fornecedor['Endereco_Rua'],
                    fornecedor['Endereco_Bairro'],
                    fornecedor['Endereco_Cidade'],
                    fornecedor['Endereco_Estado'],
                    fornecedor['Telefone'],
                    fornecedor['Email']
                ))
                encontrados.append(fornecedor)
        # Preenche os campos com o primeiro encontrado, se houver algum
        if len(encontrados) >= 1:
            campos = [
                encontrados[0]['Nome'],
                encontrados[0]['Contato'],
                encontrados[0]['Endereco_Rua'],
                encontrados[0]['Endereco_Bairro'],
                encontrados[0]['Endereco_Cidade'],
                encontrados[0]['Endereco_Estado'],
                encontrados[0]['Telefone'],
                encontrados[0]['Email']
            ]
            for entry, valor in zip(self.entries, campos):
                entry.delete(0, 'end')
                entry.insert(0, valor)