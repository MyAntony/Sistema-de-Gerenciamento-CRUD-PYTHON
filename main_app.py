import customtkinter as ctk
from views.crud_view import CRUDView
from sensor_view import SensorView
from light_view import LightView
from models.Caminhoes import CaminhoesCRUD
from models.Clientes import ClientesCRUD

# Atividade de:

# Antony Rafael - https://github.com/MyAntony
# Débora Magalhães - https://github.com/Debs2Dev
# Brunna Barreto - https://github.com/brunnabarreto
# Luís Felipe - https://github.com/IamLiper


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("LogiTrack: Gestão de Transportes")
        self.geometry("1200x700")

        # Configurar o layout do grid (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Criar o frame da barra lateral com widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="LogiTrack", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)

        self.sidebar_button_1 = ctk.CTkButton(self.sidebar_frame, text="Home", command=self.show_home)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = ctk.CTkButton(self.sidebar_frame, text="CRUD", command=self.mostrar_crud)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = ctk.CTkButton(self.sidebar_frame, text="Sensores IoT", command=self.mostrar_sensors)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_4 = ctk.CTkButton(self.sidebar_frame, text="Controle de Luzes", command=self.mostrar_luzes)
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)
        # self.sidebar_button_5 = ctk.CTkButton(self.sidebar_frame, text="Caminhões", command=self.mostrar_caminhoes)
        # self.sidebar_button_5.grid(row=5, column=0, padx=20, pady=10)
        # self.sidebar_button_6 = ctk.CTkButton(self.sidebar_frame, text="Funcionários", command=self.mostrar_funcionarios)
        # self.sidebar_button_6.grid(row=6, column=0, padx=20, pady=10)

        
        # inicializar views
        # self.crud_view = CRUDView(self)
        self.crud_view = CRUDView(self)
        self.sensor_view = SensorView(self)
        self.light_view = LightView(self)
        
        # Mostrar a tela inicial
        self.show_home()

    def limpar_main(self):
        # Limpar a área principal
        for widget in self.winfo_children():
            if widget != self.sidebar_frame:
                widget.destroy()

    def show_home(self):
        self.limpar_main()
        
        # Criar o frame principal
        home_frame = ctk.CTkFrame(self)
        home_frame.grid(row=0, column=1, columnspan=3, rowspan=4, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
        # Adicionar boas-vindas
        welcome_label = ctk.CTkLabel(home_frame, text="Bem-vindo ao LogiTrack", 
                                    font=ctk.CTkFont(size=32, weight="bold"))
        welcome_label.grid(row=0, column=0, padx=20, pady=40)
        
        subtitle_label = ctk.CTkLabel(home_frame, text="Sistema de Gestão de Transportes", 
                                     font=ctk.CTkFont(size=18))
        subtitle_label.grid(row=1, column=0, padx=20, pady=10)
        
        description_label = ctk.CTkLabel(home_frame, 
                                       text="Gerencie sua transportadora de forma eficiente:\n\n" +
                                            "• Controle de peças, fornecedores e caminhões\n" +
                                            "• Gestão de funcionários e clientes\n" +
                                            "• Monitoramento de saídas de caminhões\n" +
                                            "• Sistema de sensores IoT\n" +
                                            "• Controle inteligente de luzes",
                                       font=ctk.CTkFont(size=14),
                                       justify="left")
        description_label.grid(row=2, column=0, padx=20, pady=30)

    def mostrar_crud(self):
        self.limpar_main()
        self.crud_view = CRUDView(self)

    def mostrar_sensors(self):
        self.limpar_main()
        self.sensor_view.criar_sensor_frame()

    def mostrar_luzes(self):
        self.limpar_main()
        self.light_view.criar_light_frame()

    # def mostrar_caminhoes(self):
    #     self.limpar_main()
    #     self.caminhoes_view = JanelaCaminhoes(self, CaminhoesCRUD())

    # def mostrar_funcionarios(self):
    #     self.limpar_main()
    #     self.funcionarios_view = JanelaFuncionarios(self)


# class ClientesCRUD:
#     def __init__(self, filename="clientes.txt"):
#         self.filename = filename
#         self.criar_arquivo_caso_nao_exista()

#     def criar_arquivo_caso_nao_exista(self):
#         import os
#         if not os.path.exists(self.filename):
#             with open(self.filename, 'w', encoding='utf-8') as f:
#                 pass

#     def ler_tudo_clientes(self):
#         clientes = []
#         with open(self.filename, 'r', encoding='utf-8') as f:
#             for line in f:
#                 if line.strip():
#                     campos = line.strip().split(';')
#                     clientes.append({
#                         'ID_Cliente': campos[0],
#                         'Nome': campos[1],
#                         'Contato': campos[2],
#                         'Endereco_Rua': campos[3],
#                         'Endereco_Bairro': campos[4],
#                         'Endereco_Cidade': campos[5],
#                         'Endereco_Estado': campos[6],
#                         'Telefone': campos[7],
#                         'Email': campos[8]
#                     })
#         return clientes

#     def digitar_tudo_clientes(self, clientes):
#         with open(self.filename, 'w', encoding='utf-8') as f:
#             for cliente in clientes:
#                 linha = ';'.join([
#                     cliente['ID_Cliente'],
#                     cliente['Nome'],
#                     cliente['Contato'],
#                     cliente['Endereco_Rua'],
#                     cliente['Endereco_Bairro'],
#                     cliente['Endereco_Cidade'],
#                     cliente['Endereco_Estado'],
#                     cliente['Telefone'],
#                     cliente['Email']
#                 ])
#                 f.write(linha + '\n')

#     def criar_cliente(self, id_cliente, nome, contato, rua, bairro, cidade, estado, telefone, email):
#         clientes = self.ler_tudo_clientes()
#         for cliente in clientes:
#             if cliente['ID_Cliente'] == id_cliente:
#                 print(f"Cliente com ID {id_cliente} já existe.")
#                 return False
#         novo_cliente = {
#             'ID_Cliente': id_cliente,
#             'Nome': nome,
#             'Contato': contato,
#             'Endereco_Rua': rua,
#             'Endereco_Bairro': bairro,
#             'Endereco_Cidade': cidade,
#             'Endereco_Estado': estado,
#             'Telefone': telefone,
#             'Email': email
#         }
#         clientes.append(novo_cliente)
#         self.digitar_tudo_clientes(clientes)
#         print(f"Cliente {nome} cadastrado com sucesso.")
#         return True

#     def ler_cliente(self, id_cliente):
#         clientes = self.ler_tudo_clientes()
#         for cliente in clientes:
#             if cliente['ID_Cliente'] == id_cliente:
#                 return cliente
#         print(f"Cliente com ID {id_cliente} não encontrado.")
#         return None

#     def atualizar_cliente(self, id_cliente, nome=None, contato=None, rua=None, bairro=None, cidade=None, estado=None, telefone=None, email=None):
#         clientes = self.ler_tudo_clientes()
#         found = False
#         for i, cliente in enumerate(clientes):
#             if cliente['ID_Cliente'] == id_cliente:
#                 if nome: clientes[i]['Nome'] = nome
#                 if contato: clientes[i]['Contato'] = contato
#                 if rua: clientes[i]['Endereco_Rua'] = rua
#                 if bairro: clientes[i]['Endereco_Bairro'] = bairro
#                 if cidade: clientes[i]['Endereco_Cidade'] = cidade
#                 if estado: clientes[i]['Endereco_Estado'] = estado
#                 if telefone: clientes[i]['Telefone'] = telefone
#                 if email: clientes[i]['Email'] = email
#                 found = True
#                 break
#         if found:
#             self.digitar_tudo_clientes(clientes)
#             print(f"Cliente com ID {id_cliente} atualizado com sucesso.")
#             return True
#         else:
#             print(f"Cliente com ID {id_cliente} não encontrado para atualização.")
#             return False

#     def deletar_cliente(self, id_cliente):
#         clientes = self.ler_tudo_clientes()
#         novos_clientes = [c for c in clientes if c['ID_Cliente'] != id_cliente]
#         if len(novos_clientes) == len(clientes):
#             print(f"Cliente com ID {id_cliente} não encontrado para exclusão.")
#             return False
#         self.digitar_tudo_clientes(novos_clientes)
#         print(f"Cliente com ID {id_cliente} excluído com sucesso.")
#         return True

#     def listar_todos_clientes(self):
#         return self.ler_tudo_clientes()

# class JanelaCaminhoes:
#     def __init__(self, parent, crud_obj):
#         self.crud_obj = crud_obj
#         self.window = ctk.CTkToplevel(parent)
#         self.window.title("LogiTrack - Gerenciar Caminhões")
#         self.window.geometry("900x700")
#         ctk.CTkLabel(self.window, text="Em breve: CRUD de Caminhões", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=50)

# class JanelaFuncionarios:
#     def __init__(self, parent, crud_obj):
#         self.crud_obj = crud_obj
#         self.window = ctk.CTkToplevel(parent)
#         self.window.title("LogiTrack - Gerenciar Funcionários")
#         self.window.geometry("900x700")
#         ctk.CTkLabel(self.window, text="Em breve: CRUD de Funcionários", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=50)

if __name__ == "__main__":
    app = App()
    app.mainloop()


