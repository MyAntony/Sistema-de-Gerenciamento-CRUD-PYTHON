import customtkinter as ctk
from tkinter import messagebox, ttk

# Atividade de:

# Antony Rafael - https://github.com/MyAntony
# Débora Magalhães - https://github.com/Debs2Dev
# Brunna Barreto - https://github.com/brunnabarreto
# Luís Felipe - https://github.com/IamLiper


class JanelaFuncionarios:
    def __init__(self, parent, crud_obj):
        self.crud_obj = crud_obj
        self.window = ctk.CTkToplevel(parent)
        self.window.title("LogiTrack - Gerenciar Funcionários")
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

        labels = ["Nome", "Cargo", "Telefone", "Email", "Rua", "Bairro", "Cidade", "Estado"]
        self.entries = []
        for i, label in enumerate(labels):
            ctk.CTkLabel(self.window, text=label + ":").grid(row=1 + i // 2, column=(i % 2) * 2, padx=10, pady=5, sticky="w")
            entry = ctk.CTkEntry(self.window, width=150)
            entry.grid(row=1 + i // 2, column=(i % 2) * 2 + 1, padx=10, pady=5)
            self.entries.append(entry)

        button_frame = ctk.CTkFrame(self.window)
        button_frame.grid(row=6, column=0, columnspan=4, padx=20, pady=20)
        ctk.CTkButton(button_frame, text="Criar", command=self.criar_funcionario).grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Atualizar", command=self.atualizar_funcionario).grid(row=0, column=1, padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Excluir", command=self.deletar_funcionario).grid(row=0, column=2, padx=10, pady=5)
        ctk.CTkButton(button_frame, text="Limpar", command=self.campos_vazios).grid(row=0, column=3, padx=10, pady=5)

        columns = ("ID", "Nome", "Cargo", "Telefone", "Email", "Rua", "Bairro", "Cidade", "Estado")
        self.tree = ttk.Treeview(self.window, columns=columns, show="headings", height=8)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.grid(row=7, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def criar_funcionario(self):
        try:
            values = [e.get() for e in self.entries]
            if not values[0] or not values[1]:
                messagebox.showerror("Erro", "Nome e Cargo são obrigatórios.")
                return
            id_funcionario = self.crud_obj.criar_funcionario(*values)
            self.recarregar_lista()
            self.campos_vazios()
            messagebox.showinfo("Sucesso", f"Funcionário cadastrado com sucesso! ID: {id_funcionario}")
        except Exception as e:
            messagebox.showerror("Erro", f"Verifique os dados: {e}")

    def atualizar_funcionario(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um funcionário para atualizar.")
            return
        item = self.tree.item(selected[0])
        id_funcionario = str(item['values'][0])
        try:
            values = [e.get() for e in self.entries]
            self.crud_obj.atualizar_funcionario(
                id_funcionario,
                nome=values[0],
                cargo=values[1],
                telefone=values[2],
                email=values[3],
                rua=values[4],
                bairro=values[5],
                cidade=values[6],
                estado=values[7]
            )
            self.recarregar_lista()
            self.campos_vazios()
            messagebox.showinfo("Sucesso", "Funcionário atualizado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Verifique os dados: {e}")

    def deletar_funcionario(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um funcionário para excluir.")
            return
        item = self.tree.item(selected[0])
        id_funcionario = str(item['values'][0])  # <-- conversão para string
        self.crud_obj.deletar_funcionario(id_funcionario)
        self.recarregar_lista()
        self.campos_vazios()
        messagebox.showinfo("Sucesso", "Funcionário excluído com sucesso!")

    def campos_vazios(self):
        for e in self.entries:
            e.delete(0, 'end')

    def recarregar_lista(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        funcionarios = self.crud_obj.listar_todos_funcionarios()
        for funcionario in funcionarios:
            self.tree.insert('', 'end', values=(
                funcionario['ID_Funcionario'],
                funcionario['Nome'],
                funcionario['Cargo'],
                funcionario['Telefone'],
                funcionario['Email'],
                funcionario['Endereco_Rua'],
                funcionario['Endereco_Bairro'],
                funcionario['Endereco_Cidade'],
                funcionario['Endereco_Estado']
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
        # Busca todos os funcionários cadastrados
        funcionarios = self.crud_obj.listar_todos_funcionarios()
        encontrados = []  # Lista para armazenar os funcionários encontrados
        # Para cada funcionário, verifica se o termo pesquisado aparece em qualquer campo
        for funcionario in funcionarios:
            if any(termo in str(valor).lower() for valor in funcionario.values()):
                # Se encontrar, insere o funcionário na Treeview
                self.tree.insert('', 'end', values=(
                    funcionario['ID_Funcionario'],
                    funcionario['Nome'],
                    funcionario['Cargo'],
                    funcionario['Telefone'],
                    funcionario['Email'],
                    funcionario['Endereco_Rua'],
                    funcionario['Endereco_Bairro'],
                    funcionario['Endereco_Cidade'],
                    funcionario['Endereco_Estado']
                ))
                encontrados.append(funcionario)  # Adiciona à lista de encontrados
        # Se encontrou pelo menos um funcionário, preenche os campos do formulário com o primeiro encontrado
        if len(encontrados) >= 1:
            campos = [
                encontrados[0]['Nome'],
                encontrados[0]['Cargo'],
                encontrados[0]['Telefone'],
                encontrados[0]['Email'],
                encontrados[0]['Endereco_Rua'],
                encontrados[0]['Endereco_Bairro'],
                encontrados[0]['Endereco_Cidade'],
                encontrados[0]['Endereco_Estado']
            ]
            # Preenche cada campo do formulário com os dados do funcionário encontrado
            for entry, valor in zip(self.entries, campos):
                entry.delete(0, 'end')
                entry.insert(0, valor)
