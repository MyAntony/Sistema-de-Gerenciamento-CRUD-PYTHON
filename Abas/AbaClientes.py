import customtkinter as ctk
from tkinter import messagebox, ttk
from models.Clientes import ClientesCRUD

# Atividade de:

# Antony Rafael - https://github.com/MyAntony
# Débora Magalhães - https://github.com/Debs2Dev
# Brunna Barreto - https://github.com/brunnabarreto
# Luís Felipe - https://github.com/IamLiper


class JanelaClientes:
    def __init__(self, parent, crud_obj=None):
        self.crud_obj = crud_obj or ClientesCRUD()
        self.window = ctk.CTkToplevel(parent)
        self.window.title("LogiTrack - Gerenciar Clientes")
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

        # Campos de cadastro
        labels = ["Nome", "Contato", "Rua", "Bairro", "Cidade", "Estado", "Telefone", "Email"]
        self.entries = []
        for i, label in enumerate(labels):
            ctk.CTkLabel(self.window, text=label + ":").grid(row=1 + i // 2, column=(i % 2) * 2, padx=10, pady=5, sticky="w")
            entry = ctk.CTkEntry(self.window, width=150)
            entry.grid(row=1 + i // 2, column=(i % 2) * 2 + 1, padx=10, pady=5)
            self.entries.append(entry)

        button_frame = ctk.CTkFrame(self.window)
        button_frame.grid(row=5, column=0, columnspan=4, padx=20, pady=20)
        ctk.CTkButton(button_frame, text="Criar", command=self.criar_cliente).grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Atualizar", command=self.atualizar_cliente).grid(row=0, column=1, padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Excluir", command=self.deletar_cliente).grid(row=0, column=2, padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Limpar", command=self.campos_vazios).grid(row=0, column=3, padx=10, pady=5)

        columns = ("ID", "Nome", "Contato", "Rua", "Bairro", "Cidade", "Estado", "Telefone", "Email")
        self.tree = ttk.Treeview(self.window, columns=columns, show="headings", height=8)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def criar_cliente(self):
        try:
            values = [e.get() for e in self.entries]
            if not values[0]:
                messagebox.showerror("Erro", "Nome é obrigatório.")
                return
            id_cliente = self.crud_obj.criar_cliente(*values)
            self.recarregar_lista()
            self.campos_vazios()
            messagebox.showinfo("Sucesso", f"Cliente cadastrado com sucesso! ID: {id_cliente}")
        except Exception as e:
            messagebox.showerror("Erro", f"Verifique os dados: {e}")

    def atualizar_cliente(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um cliente para atualizar.")
            return
        item = self.tree.item(selected[0])
        id_cliente = str(item['values'][0])
        try:
            values = [e.get() for e in self.entries]
            self.crud_obj.atualizar_cliente(
                id_cliente,
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
            messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Verifique os dados: {e}")

    def deletar_cliente(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um cliente para excluir.")
            return
        item = self.tree.item(selected[0])
        id_cliente = str(item['values'][0])  # <-- conversão para string
        self.crud_obj.deletar_cliente(id_cliente)
        self.recarregar_lista()
        self.campos_vazios()
        messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")

    def campos_vazios(self):
        for e in self.entries:
            e.delete(0, 'end')

    def recarregar_lista(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        clientes = self.crud_obj.listar_todos_clientes()
        for cliente in clientes:
            self.tree.insert('', 'end', values=(
                cliente['ID_Cliente'],
                cliente['Nome'],
                cliente['Contato'],
                cliente['Endereco_Rua'],
                cliente['Endereco_Bairro'],
                cliente['Endereco_Cidade'],
                cliente['Endereco_Estado'],
                cliente['Telefone'],
                cliente['Email']
            ))

    def pesquisar(self):
        termo = self.search_entry.get().lower()
        print(f"Termo pesquisado: '{termo}'")
        for row in self.tree.get_children():
            self.tree.delete(row)
        clientes = self.crud_obj.listar_todos_clientes()
        encontrados = []
        for cliente in clientes:
            print(cliente)  # Veja o que está sendo lido
            if any(termo in str(valor).lower() for valor in cliente.values()):
                self.tree.insert('', 'end', values=(
                    cliente['ID_Cliente'],
                    cliente['Nome'],
                    cliente['Contato'],
                    cliente['Endereco_Rua'],
                    cliente['Endereco_Bairro'],
                    cliente['Endereco_Cidade'],
                    cliente['Endereco_Estado'],
                    cliente['Telefone'],
                    cliente['Email']
                ))
                encontrados.append(cliente)
        # Se encontrou pelo menos um cliente, preenche os campos com o primeiro encontrado
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

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0])['values']
        # Preenche os campos do formulário a partir do índice 1 (pulando o ID)
        for i, e in enumerate(self.entries):
            e.delete(0, 'end')
            e.insert(0, values[i+1])
