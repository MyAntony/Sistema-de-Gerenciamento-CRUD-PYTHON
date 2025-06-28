import customtkinter as ctk
from tkinter import messagebox, ttk
from models.Clientes import ClientesCRUD
from models.Funcionarios import FuncionariosCRUD
from models.Caminhoes import CaminhoesCRUD
from models.Pecas import PecasCRUD
from models.Fornecedores import FornecedoresCRUD
from Abas.AbaClientes import JanelaClientes
from Abas.AbaFuncionarios import JanelaFuncionarios
from Abas.AbaCaminhoes import JanelaCaminhoes
from Abas.AbaPecas import JanelaPecas
from Abas.AbaFornecedores import JanelaFornecedores

class CRUDView:
    def __init__(self, parent):
        self.parent = parent
        self.create_crud_frame()

    def create_crud_frame(self):
        # Destroi frame antigo se existir
        if hasattr(self, 'crud_frame'):
            self.crud_frame.destroy()

        self.crud_frame = ctk.CTkFrame(self.parent)
        self.crud_frame.grid(row=0, column=1, columnspan=3, rowspan=4, padx=(20, 20), pady=(20, 20), sticky="nsew")

        ctk.CTkLabel(self.crud_frame, text="Menu CRUD", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)

        ctk.CTkButton(
            self.crud_frame, text="Clientes",
            command=lambda: JanelaClientes(self.parent, ClientesCRUD())
        ).pack(pady=10)

        ctk.CTkButton(
            self.crud_frame, text="Funcionários",
            command=lambda: JanelaFuncionarios(self.parent, FuncionariosCRUD())
        ).pack(pady=10)

        ctk.CTkButton(
            self.crud_frame, text="Caminhões",
            command=lambda: JanelaCaminhoes(self.parent, CaminhoesCRUD())
        ).pack(pady=10)

        ctk.CTkButton(
            self.crud_frame, text="Peças",
            command=lambda: JanelaPecas(self.parent, PecasCRUD())
        ).pack(pady=10)

        ctk.CTkButton(
            self.crud_frame, text="Fornecedores",
            command=lambda: JanelaFornecedores(self.parent, FornecedoresCRUD())
        ).pack(pady=10)

# Janelas de CRUD (pode ir implementando cada uma depois)
# class JanelaClientes:
#     def __init__(self, parent, crud_obj):
#         self.crud_obj = crud_obj
#         self.window = ctk.CTkToplevel(parent)
#         self.window.title("LogiTrack - Gerenciar Clientes")
#         self.window.geometry("900x700")
#         self.criar_janelinhas()
#         self.recarregar_lista()

#     def criar_janelinhas(self):
#         labels = ["Nome", "Contato", "Rua", "Bairro", "Cidade", "Estado", "Telefone", "Email"]
#         self.entries = []
#         for i, label in enumerate(labels):
#             ctk.CTkLabel(self.window, text=label + ":").grid(row=1 + i // 2, column=(i % 2) * 2, padx=10, pady=5, sticky="w")
#             entry = ctk.CTkEntry(self.window, width=150)
#             entry.grid(row=1 + i // 2, column=(i % 2) * 2 + 1, padx=10, pady=5)
#             self.entries.append(entry)

#         button_frame = ctk.CTkFrame(self.window)
#         button_frame.grid(row=5, column=0, columnspan=4, padx=20, pady=20)
#         ctk.CTkButton(button_frame, text="Criar", command=self.create_cliente).grid(row=0, column=0, padx=10, pady=5)
#         ctk.CTkButton(button_frame, text="Atualizar", command=self.atualizar_cliente).grid(row=0, column=1, padx=10, pady=5)
#         ctk.CTkButton(button_frame, text="Excluir", command=self.delete_cliente).grid(row=0, column=2, padx=10, pady=5)
#         ctk.CTkButton(button_frame, text="Limpar", command=self.campos_vazios).grid(row=0, column=3, padx=10, pady=5)

#         columns = ("ID", "Nome", "Contato", "Rua", "Bairro", "Cidade", "Estado", "Telefone", "Email")
#         self.tree = ttk.Treeview(self.window, columns=columns, show="headings", height=8)
#         for col in columns:
#             self.tree.heading(col, text=col)
#             self.tree.column(col, width=100)
#         self.tree.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
#         self.tree.bind("<<TreeviewSelect>>", self.on_select)

#     def create_cliente(self):
#         try:
#             values = [e.get() for e in self.entries]
#             if not values[0]:
#                 messagebox.showerror("Erro", "Nome é obrigatório.")
#                 return
#             id_cliente = self.crud_obj.create_cliente(*values)
#             self.recarregar_lista()
#             self.campos_vazios()
#             messagebox.showinfo("Sucesso", f"Cliente cadastrado com sucesso! ID: {id_cliente}")
#         except Exception as e:
#             messagebox.showerror("Erro", f"Verifique os dados: {e}")

#     def atualizar_cliente(self):
#         selected = self.tree.selection()
#         if not selected:
#             messagebox.showerror("Erro", "Selecione um cliente para atualizar.")
#             return
#         item = self.tree.item(selected[0])
#         id_cliente = item['values'][0]
#         try:
#             values = [e.get() for e in self.entries]
#             self.crud_obj.atualizar_cliente(id_cliente, *values)
#             self.recarregar_lista()
#             self.campos_vazios()
#             messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
#         except Exception as e:
#             messagebox.showerror("Erro", f"Verifique os dados: {e}")

#     def delete_cliente(self):
#         selected = self.tree.selection()
#         if not selected:
#             messagebox.showerror("Erro", "Selecione um cliente para excluir.")
#             return
#         item = self.tree.item(selected[0])
#         id_cliente = item['values'][0]
#         self.crud_obj.delete_cliente(id_cliente)
#         self.recarregar_lista()
#         self.campos_vazios()
#         messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")

#     def campos_vazios(self):
#         for e in self.entries:
#             e.delete(0, 'end')

#     def recarregar_lista(self):
#         for row in self.tree.get_children():
#             self.tree.delete(row)
#         clientes = self.crud_obj.list_all_clientes()
#         for cliente in clientes:
#             self.tree.insert('', 'end', values=(
#                 cliente['ID_Cliente'],
#                 cliente['Nome'],
#                 cliente['Telefone'],
#                 cliente['Email'],
#                 cliente['Endereco_Rua'],
#                 cliente['Endereco_Bairro'],
#                 cliente['Endereco_Cidade'],
#                 cliente['Endereco_Estado']
#             ))

#     def on_select(self, event):
#         selected = self.tree.selection()
#         if not selected:
#             return
#         values = self.tree.item(selected[0])['values']
#         for i, e in enumerate(self.entries):
#             e.delete(0, 'end')
#             e.insert(0, values[i+1])

# # ----------------- FUNCIONÁRIOS -----------------
# class JanelaFuncionarios:
#     def __init__(self, parent, crud_obj):
#         self.crud_obj = crud_obj
#         self.window = ctk.CTkToplevel(parent)
#         self.window.title("LogiTrack - Gerenciar Funcionários")
#         self.window.geometry("900x700")
#         self.criar_janelinhas()
#         self.recarregar_lista()

#     def criar_janelinhas(self):
#         labels = ["Nome", "Cargo", "Telefone", "Email", "Rua", "Bairro", "Cidade", "Estado"]
#         self.entries = []
#         for i, label in enumerate(labels):
#             ctk.CTkLabel(self.window, text=label + ":").grid(row=1 + i // 2, column=(i % 2) * 2, padx=10, pady=5, sticky="w")
#             entry = ctk.CTkEntry(self.window, width=150)
#             entry.grid(row=1 + i // 2, column=(i % 2) * 2 + 1, padx=10, pady=5)
#             self.entries.append(entry)

#         button_frame = ctk.CTkFrame(self.window)
#         button_frame.grid(row=6, column=0, columnspan=4, padx=20, pady=20)
#         ctk.CTkButton(button_frame, text="Criar", command=self.create_funcionario).grid(row=0, column=0, padx=10, pady=5)
#         ctk.CTkButton(button_frame, text="Atualizar", command=self.atualizar_funcionario).grid(row=0, column=1, padx=10, pady=5)
#         ctk.CTkButton(button_frame, text="Excluir", command=self.delete_funcionario).grid(row=0, column=2, padx=10, pady=5)
#         ctk.CTkButton(button_frame, text="Limpar", command=self.campos_vazios).grid(row=0, column=3, padx=10, pady=5)

#         columns = ("ID", "Nome", "Cargo", "Telefone", "Email", "Rua", "Bairro", "Cidade", "Estado")
#         self.tree = ttk.Treeview(self.window, columns=columns, show="headings", height=8)
#         for col in columns:
#             self.tree.heading(col, text=col)
#             self.tree.column(col, width=100)
#         self.tree.grid(row=7, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
#         self.tree.bind("<<TreeviewSelect>>", self.on_select)

#     def create_funcionario(self):
#         try:
#             values = [e.get() for e in self.entries]
#             if not values[0] or not values[1]:
#                 messagebox.showerror("Erro", "Nome e Cargo são obrigatórios.")
#                 return
#             id_funcionario = self.crud_obj.create_funcionario(*values)
#             self.recarregar_lista()
#             self.campos_vazios()
#             messagebox.showinfo("Sucesso", f"Funcionário cadastrado com sucesso! ID: {id_funcionario}")
#         except Exception as e:
#             messagebox.showerror("Erro", f"Verifique os dados: {e}")

#     def atualizar_funcionario(self):
#         selected = self.tree.selection()
#         if not selected:
#             messagebox.showerror("Erro", "Selecione um funcionário para atualizar.")
#             return
#         item = self.tree.item(selected[0])
#         id_funcionario = item['values'][0]
#         try:
#             values = [e.get() for e in self.entries]
#             self.crud_obj.atualizar_funcionario(id_funcionario, *values)
#             self.recarregar_lista()
#             self.campos_vazios()
#             messagebox.showinfo("Sucesso", "Funcionário atualizado com sucesso!")
#         except Exception as e:
#             messagebox.showerror("Erro", f"Verifique os dados: {e}")

#     def delete_funcionario(self):
#         selected = self.tree.selection()
#         if not selected:
#             messagebox.showerror("Erro", "Selecione um funcionário para excluir.")
#             return
#         item = self.tree.item(selected[0])
#         id_funcionario = item['values'][0]
#         self.crud_obj.delete_funcionario(id_funcionario)
#         self.recarregar_lista()
#         self.campos_vazios()
#         messagebox.showinfo("Sucesso", "Funcionário excluído com sucesso!")

#     def campos_vazios(self):
#         for e in self.entries:
#             e.delete(0, 'end')

#     def recarregar_lista(self):
#         for row in self.tree.get_children():
#             self.tree.delete(row)
#         funcionarios = self.crud_obj.list_all_funcionarios()
#         for funcionario in funcionarios:
#             self.tree.insert('', 'end', values=(
#                 funcionario['ID_Funcionario'],
#                 funcionario['Nome'],
#                 funcionario['Cargo'],
#                 funcionario['Telefone'],
#                 funcionario['Email'],
#                 funcionario['Endereco_Rua'],
#                 funcionario['Endereco_Bairro'],
#                 funcionario['Endereco_Cidade'],
#                 funcionario['Endereco_Estado']
#             ))

#     def on_select(self, event):
#         selected = self.tree.selection()
#         if not selected:
#             return
#         values = self.tree.item(selected[0])['values']
#         for i, e in enumerate(self.entries):
#             e.delete(0, 'end')
#             e.insert(0, values[i+1])

# # ----------------- CAMINHÕES -----------------
# class JanelaCaminhoes:
#     def __init__(self, parent, crud_obj):
#         self.crud_obj = crud_obj
#         self.window = ctk.CTkToplevel(parent)
#         self.window.title("LogiTrack - Gerenciar Caminhões")
#         self.window.geometry("900x700")
#         self.criar_janelinhas()
#         self.recarregar_lista()

#     def criar_janelinhas(self):
#         labels = ["Marca", "Modelo", "Ano", "Placa", "Quilometragem", "Status"]
#         self.entries = []
#         for i, label in enumerate(labels):
#             ctk.CTkLabel(self.window, text=label + ":").grid(row=1 + i // 2, column=(i % 2) * 2, padx=10, pady=5, sticky="w")
#             entry = ctk.CTkEntry(self.window, width=150)
#             entry.grid(row=1 + i // 2, column=(i % 2) * 2 + 1, padx=10, pady=5)
#             self.entries.append(entry)

#         button_frame = ctk.CTkFrame(self.window)
#         button_frame.grid(row=5, column=0, columnspan=4, padx=20, pady=20)
#         ctk.CTkButton(button_frame, text="Criar", command=self.criar_caminhao).grid(row=0, column=0, padx=10, pady=5)
#         ctk.CTkButton(button_frame, text="Atualizar", command=self.atualizar_caminhao).grid(row=0, column=1, padx=10, pady=5)
#         ctk.CTkButton(button_frame, text="Excluir", command=self.delete_caminhao).grid(row=0, column=2, padx=10, pady=5)
#         ctk.CTkButton(button_frame, text="Limpar", command=self.campos_vazios).grid(row=0, column=3, padx=10, pady=5)

#         columns = ("ID", "Marca", "Modelo", "Ano", "Placa", "Quilometragem", "Status")
#         self.tree = ttk.Treeview(self.window, columns=columns, show="headings", height=8)
#         for col in columns:
#             self.tree.heading(col, text=col)
#             self.tree.column(col, width=100)
#         self.tree.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
#         self.tree.bind("<<TreeviewSelect>>", self.on_select)

#     def criar_caminhao(self):
#         try:
#             values = [e.get() for e in self.entries]
#             if not values[0] or not values[1]:
#                 messagebox.showerror("Erro", "Marca e Modelo são obrigatórios.")
#                 return
#             id_caminhao = self.crud_obj.criar_caminhao(*values)
#             self.recarregar_lista()
#             self.campos_vazios()
#             messagebox.showinfo("Sucesso", f"Caminhão cadastrado com sucesso! ID: {id_caminhao}")
#         except Exception as e:
#             messagebox.showerror("Erro", f"Verifique os dados: {e}")

#     def atualizar_caminhao(self):
#         selected = self.tree.selection()
#         if not selected:
#             messagebox.showerror("Erro", "Selecione um caminhão para atualizar.")
#             return
#         item = self.tree.item(selected[0])
#         id_caminhao = item['values'][0]
#         try:
#             values = [e.get() for e in self.entries]
#             self.crud_obj.atualizar_caminhao(id_caminhao, *values)
#             self.recarregar_lista()
#             self.campos_vazios()
#             messagebox.showinfo("Sucesso", "Caminhão atualizado com sucesso!")
#         except Exception as e:
#             messagebox.showerror("Erro", f"Verifique os dados: {e}")

#     def delete_caminhao(self):
#         selected = self.tree.selection()
#         if not selected:
#             messagebox.showerror("Erro", "Selecione um caminhão para excluir.")
#             return
#         item = self.tree.item(selected[0])
#         id_caminhao = item['values'][0]
#         self.crud_obj.delete_caminhao(id_caminhao)
#         self.recarregar_lista()
#         self.campos_vazios()
#         messagebox.showinfo("Sucesso", "Caminhão excluído com sucesso!")

#     def campos_vazios(self):
#         for e in self.entries:
#             e.delete(0, 'end')

#     def recarregar_lista(self):
#         for row in self.tree.get_children():
#             self.tree.delete(row)
#         caminhoes = self.crud_obj.list_all_caminhoes()
#         for caminhao in caminhoes:
#             self.tree.insert('', 'end', values=(
#                 caminhao['ID_Caminhao'],
#                 caminhao['Marca'],
#                 caminhao['Modelo'],
#                 caminhao['Ano'],
#                 caminhao['Placa'],
#                 caminhao['Quilometragem'],
#                 caminhao['Status']
#             ))

#     def on_select(self, event):
#         selected = self.tree.selection()
#         if not selected:
#             return
#         values = self.tree.item(selected[0])['values']
#         for i, e in enumerate(self.entries):
#             e.delete(0, 'end')
#             e.insert(0, values[i+1])

# # ----------------- PEÇAS -----------------
# class JanelaPecas:
#     def __init__(self, parent, crud_obj):
#         self.crud_obj = crud_obj
#         self.window = ctk.CTkToplevel(parent)
#         self.window.title("LogiTrack - Gerenciar Peças")
#         self.window.geometry("900x700")
#         self.criar_janelinhas()
#         self.recarregar_lista()

#     def criar_janelinhas(self):
#         labels = ["Nome", "Descrição", "Fabricante", "Preço", "Quantidade"]
#         self.entries = []
#         for i, label in enumerate(labels):
#             ctk.CTkLabel(self.window, text=label + ":").grid(row=1 + i // 2, column=(i % 2) * 2, padx=10, pady=5, sticky="w")
#             entry = ctk.CTkEntry(self.window, width=150)
#             entry.grid(row=1 + i // 2, column=(i % 2) * 2 + 1, padx=10, pady=5)
#             self.entries.append(entry)

#         button_frame = ctk.CTkFrame(self.window)
#         button_frame.grid(row=5, column=0, columnspan=4, padx=20, pady=20)
#         ctk.CTkButton(button_frame, text="Criar", command=self.create_peca).grid(row=0, column=0, padx=10, pady=5)
#         ctk.CTkButton(button_frame, text="Atualizar", command=self.atualizar_peca).grid(row=0, column=1, padx=10, pady=5)
#         ctk.CTkButton(button_frame, text="Excluir", command=self.delete_peca).grid(row=0, column=2, padx=10, pady=5)
#         ctk.CTkButton(button_frame, text="Limpar", command=self.campos_vazios).grid(row=0, column=3, padx=10, pady=5)

#         columns = ("ID", "Nome", "Descrição", "Fabricante", "Preço", "Quantidade")
#         self.tree = ttk.Treeview(self.window, columns=columns, show="headings", height=8)
#         for col in columns:
#             self.tree.heading(col, text=col)
#             self.tree.column(col, width=100)
#         self.tree.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
#         self.tree.bind("<<TreeviewSelect>>", self.on_select)

#     def create_peca(self):
#         try:
#             values = [e.get() for e in self.entries]
#             if not values[0] or not values[1]:
#                 messagebox.showerror("Erro", "Nome e Descrição são obrigatórios.")
#                 return
#             id_peca = self.crud_obj.create_peca(*values)
#             self.recarregar_lista()
#             self.campos_vazios()
#             messagebox.showinfo("Sucesso", f"Peça cadastrada com sucesso! ID: {id_peca}")
#         except Exception as e:
#             messagebox.showerror("Erro", f"Verifique os dados: {e}")

#     def atualizar_peca(self):
#         selected = self.tree.selection()
#         if not selected:
#             messagebox.showerror("Erro", "Selecione uma peça para atualizar.")
#             return
#         item = self.tree.item(selected[0])
#         id_peca = item['values'][0]
#         try:
#             values = [e.get() for e in self.entries]
#             self.crud_obj.atualizar_peca(id_peca, *values)
#             self.recarregar_lista()
#             self.campos_vazios()
#             messagebox.showinfo("Sucesso", "Peça atualizada com sucesso!")
#         except Exception as e:
#             messagebox.showerror("Erro", f"Verifique os dados: {e}")

#     def delete_peca(self):
#         selected = self.tree.selection()
#         if not selected:
#             messagebox.showerror("Erro", "Selecione uma peça para excluir.")
#             return
#         item = self.tree.item(selected[0])
#         id_peca = item['values'][0]
#         self.crud_obj.delete_peca(id_peca)
#         self.recarregar_lista()
#         self.campos_vazios()
#         messagebox.showinfo("Sucesso", "Peça excluída com sucesso!")

#     def campos_vazios(self):
#         for e in self.entries:
#             e.delete(0, 'end')

#     def recarregar_lista(self):
#         for row in self.tree.get_children():
#             self.tree.delete(row)
#         pecas = self.crud_obj.list_all_pecas()
#         for peca in pecas:
#             self.tree.insert('', 'end', values=(
#                 peca['ID_Peca'],
#                 peca['Nome'],
#                 peca['Descricao'],
#                 peca['Fabricante'],
#                 peca['Preco'],
#                 peca['Quantidade']
#             ))

#     def on_select(self, event):
#         selected = self.tree.selection()
#         if not selected:
#             return
#         values = self.tree.item(selected[0])['values']
#         for i, e in enumerate(self.entries):
#             e.delete(0, 'end')
#             e.insert(0, values[i+1])

# # ----------------- FORNECEDORES -----------------
# class JanelaFornecedores:
#     def __init__(self, parent, crud_obj):
#         self.crud_obj = crud_obj
#         self.window = ctk.CTkToplevel(parent)
#         self.window.title("LogiTrack - Gerenciar Fornecedores")
#         self.window.geometry("900x700")
#         self.criar_janelinhas()
#         self.recarregar_lista()

#     def criar_janelinhas(self):
#         labels = ["Nome", "Contato", "Rua", "Bairro", "Cidade", "Estado", "Telefone", "Email"]
#         self.entries = []
#         for i, label in enumerate(labels):
#             ctk.CTkLabel(self.window, text=label + ":").grid(row=1 + i // 2, column=(i % 2) * 2, padx=10, pady=5, sticky="w")
#             entry = ctk.CTkEntry(self.window, width=150)
#             entry.grid(row=1 + i // 2, column=(i % 2) * 2 + 1, padx=10, pady=5)
#             self.entries.append(entry)

#         button_frame = ctk.CTkFrame(self.window)
#         button_frame.grid(row=6, column=0, columnspan=4, padx=20, pady=20)
#         ctk.CTkButton(button_frame, text="Criar", command=self.create_fornecedor).grid(row=0, column=0, padx=10, pady=5)
#         ctk.CTkButton(button_frame, text="Atualizar", command=self.atualizar_fornecedor).grid(row=0, column=1, padx=10, pady=5)
#         ctk.CTkButton(button_frame, text="Excluir", command=self.delete_fornecedor).grid(row=0, column=2, padx=10, pady=5)
#         ctk.CTkButton(button_frame, text="Limpar", command=self.campos_vazios).grid(row=0, column=3, padx=10, pady=5)

#         columns = ("ID", "Nome", "Contato", "Rua", "Bairro", "Cidade", "Estado", "Telefone", "Email")
#         self.tree = ttk.Treeview(self.window, columns=columns, show="headings", height=8)
#         for col in columns:
#             self.tree.heading(col, text=col)
#             self.tree.column(col, width=100)
#         self.tree.grid(row=7, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
#         self.tree.bind("<<TreeviewSelect>>", self.on_select)

#     def create_fornecedor(self):
#         try:
#             values = [e.get() for e in self.entries]
#             if not values[0] or not values[1]:
#                 messagebox.showerror("Erro", "Nome e Contato são obrigatórios.")
#                 return
#             id_fornecedor = self.crud_obj.create_fornecedor(*values)
#             self.recarregar_lista()
#             self.campos_vazios()
#             messagebox.showinfo("Sucesso", f"Fornecedor cadastrado com sucesso! ID: {id_fornecedor}")
#         except Exception as e:
#             messagebox.showerror("Erro", f"Verifique os dados: {e}")

#     def atualizar_fornecedor(self):
#         selected = self.tree.selection()
#         if not selected:
#             messagebox.showerror("Erro", "Selecione um fornecedor para atualizar.")
#             return
#         item = self.tree.item(selected[0])
#         id_fornecedor = item['values'][0]
#         try:
#             values = [e.get() for e in self.entries]
#             self.crud_obj.atualizar_fornecedor(id_fornecedor, *values)
#             self.recarregar_lista()
#             self.campos_vazios()
#             messagebox.showinfo("Sucesso", "Fornecedor atualizado com sucesso!")
#         except Exception as e:
#             messagebox.showerror("Erro", f"Verifique os dados: {e}")

#     def delete_fornecedor(self):
#         selected = self.tree.selection()
#         if not selected:
#             messagebox.showerror("Erro", "Selecione um fornecedor para excluir.")
#             return
#         item = self.tree.item(selected[0])
#         id_fornecedor = item['values'][0]
#         self.crud_obj.delete_fornecedor(id_fornecedor)
#         self.recarregar_lista()
#         self.campos_vazios()
#         messagebox.showinfo("Sucesso", "Fornecedor excluído com sucesso!")

#     def campos_vazios(self):
#         for e in self.entries:
#             e.delete(0, 'end')

#     def recarregar_lista(self):
#         for row in self.tree.get_children():
#             self.tree.delete(row)
#         fornecedores = self.crud_obj.list_all_fornecedores()
#         for fornecedor in fornecedores:
#             self.tree.insert('', 'end', values=(
#                 fornecedor['ID_Fornecedor'],
#                 fornecedor['Nome'],
#                 fornecedor['Contato'],
#                 fornecedor['Endereco_Rua'],
#                 fornecedor['Endereco_Bairro'],
#                 fornecedor['Endereco_Cidade'],
#                 fornecedor['Endereco_Estado'],
#                 fornecedor['Telefone'],
#                 fornecedor['Email']
#             ))

#     def on_select(self, event):
#         selected = self.tree.selection()
#         if not selected:
#             return
#         values = self.tree.item(selected[0])['values']
#         for i, e in enumerate(self.entries):
#             e.delete(0, 'end')
#             e.insert(0, values[i+1])