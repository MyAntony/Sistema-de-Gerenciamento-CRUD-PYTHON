import os

# Atividade de:

# Antony Rafael - https://github.com/MyAntony
# Débora Magalhães - https://github.com/Debs2Dev
# Brunna Barreto - https://github.com/brunnabarreto
# Luís Felipe - https://github.com/IamLiper


class ClientesCRUD:
    def __init__(self, filename="clientes.txt"):
        self.filename = filename
        self.criar_arquivo_caso_nao_exista()

    def criar_arquivo_caso_nao_exista(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as f:
                pass

    def ler_tudo_clientes(self):
        clientes = []
        with open(self.filename, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    campos = line.strip().split(';')
                    clientes.append({
                        'ID_Cliente': campos[0],
                        'Nome': campos[1],
                        'Contato': campos[2],
                        'Endereco_Rua': campos[3],
                        'Endereco_Bairro': campos[4],
                        'Endereco_Cidade': campos[5],
                        'Endereco_Estado': campos[6],
                        'Telefone': campos[7],
                        'Email': campos[8]
                    })
        return clientes

    def digitar_tudo_clientes(self, clientes):
        with open(self.filename, 'w', encoding='utf-8') as f:
            for cliente in clientes:
                linha = ';'.join([
                    cliente['ID_Cliente'],
                    cliente['Nome'],
                    cliente['Contato'],
                    cliente['Endereco_Rua'],
                    cliente['Endereco_Bairro'],
                    cliente['Endereco_Cidade'],
                    cliente['Endereco_Estado'],
                    cliente['Telefone'],
                    cliente['Email']
                ])
                f.write(linha + '\n')

    def gerar_novo_id(self):
        clientes = self.ler_tudo_clientes()
        if not clientes:
            return "1"
        ultimos_ids = [int(c['ID_Cliente']) for c in clientes if c['ID_Cliente'].isdigit()]
        proximo_num = max(ultimos_ids) + 1 if ultimos_ids else 1
        return str(proximo_num)

    def criar_cliente(self, nome, contato, rua, bairro, cidade, estado, telefone, email):
        id_cliente = self.gerar_novo_id()
        clientes = self.ler_tudo_clientes()
        novo_cliente = {
            'ID_Cliente': id_cliente,
            'Nome': nome,
            'Contato': contato,
            'Endereco_Rua': rua,
            'Endereco_Bairro': bairro,
            'Endereco_Cidade': cidade,
            'Endereco_Estado': estado,
            'Telefone': telefone,
            'Email': email
        }
        clientes.append(novo_cliente)
        self.digitar_tudo_clientes(clientes)
        print(f"Cliente {nome} cadastrado com sucesso com ID {id_cliente}.")
        return id_cliente

    def ler_cliente(self, id_cliente):
        clientes = self.ler_tudo_clientes()
        for cliente in clientes:
            if cliente['ID_Cliente'] == id_cliente:
                return cliente
        print(f"Cliente com ID {id_cliente} não encontrado.")
        return None

    def atualizar_cliente(self, id_cliente, nome=None, contato=None, rua=None, bairro=None, cidade=None, estado=None, telefone=None, email=None):
        clientes = self.ler_tudo_clientes()
        found = False
        for i, cliente in enumerate(clientes):
            if cliente['ID_Cliente'] == id_cliente:
                if nome is not None: clientes[i]['Nome'] = nome
                if contato is not None: clientes[i]['Contato'] = contato
                if rua is not None: clientes[i]['Endereco_Rua'] = rua
                if bairro is not None: clientes[i]['Endereco_Bairro'] = bairro
                if cidade is not None: clientes[i]['Endereco_Cidade'] = cidade
                if estado is not None: clientes[i]['Endereco_Estado'] = estado
                if telefone is not None: clientes[i]['Telefone'] = telefone
                if email is not None: clientes[i]['Email'] = email
                found = True
                break
        if found:
            self.digitar_tudo_clientes(clientes)
            print(f"Cliente com ID {id_cliente} atualizado com sucesso.")
            return True
        else:
            print(f"Cliente com ID {id_cliente} não encontrado para atualização.")
            return False

    def deletar_cliente(self, id_cliente):
        clientes = self.ler_tudo_clientes()
        novos_clientes = [c for c in clientes if c['ID_Cliente'] != id_cliente]
        if len(novos_clientes) == len(clientes):
            print(f"Cliente com ID {id_cliente} não encontrado para exclusão.")
            return False
        self.digitar_tudo_clientes(novos_clientes)
        print(f"Cliente com ID {id_cliente} excluído com sucesso.")
        return True

    def listar_todos_clientes(self):
        return self.ler_tudo_clientes()
class SaidasCaminhoesCRUD:
    def __init__(self, filename="saidas.txt"):
        self.filename = filename
        self.criar_arquivo_caso_nao_exista()

    def criar_arquivo_caso_nao_exista(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as f:
                pass

    def ler_tudo_saidas(self):
        saidas = []
        with open(self.filename, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    campos = line.strip().split(';')
                    saidas.append({
                        'ID_Saida': campos[0],
                        'ID_Caminhao': campos[1],
                        'ID_Cliente': campos[2],
                        'Data_Saida': campos[3],
                        'Destino': campos[4],
                        'Motorista': campos[5]
                    })
        return saidas

    def digitar_tudo_saidas(self, saidas):
        with open(self.filename, 'w', encoding='utf-8') as f:
            for saida in saidas:
                linha = ';'.join([
                    saida['ID_Saida'],
                    saida['ID_Caminhao'],
                    saida['ID_Cliente'],
                    saida['Data_Saida'],
                    saida['Destino'],
                    saida['Motorista']
                ])
                f.write(linha + '\n')

    def criar_saida(self, id_saida, id_caminhao, id_cliente, data_saida, destino, motorista):
        saidas = self.ler_tudo_saidas()
        for saida in saidas:
            if saida['ID_Saida'] == id_saida:
                print(f"Saída com ID {id_saida} já existe.")
                return False
        nova_saida = {
            'ID_Saida': id_saida,
            'ID_Caminhao': id_caminhao,
            'ID_Cliente': id_cliente,
            'Data_Saida': data_saida,
            'Destino': destino,
            'Motorista': motorista
        }
        saidas.append(nova_saida)
        self.digitar_tudo_saidas(saidas)
        print(f"Saída {id_saida} cadastrada com sucesso.")
        return True

    def ler_saida(self, id_saida):
        saidas = self.ler_tudo_saidas()
        for saida in saidas:
            if saida['ID_Saida'] == id_saida:
                return saida
        print(f"Saída com ID {id_saida} não encontrada.")
        return None

    def atualizar_saida(self, id_saida, id_caminhao=None, id_cliente=None, data_saida=None, destino=None, motorista=None):
        saidas = self.ler_tudo_saidas()
        found = False
        for i, saida in enumerate(saidas):
            if saida['ID_Saida'] == id_saida:
                if id_caminhao: saidas[i]['ID_Caminhao'] = id_caminhao
                if id_cliente: saidas[i]['ID_Cliente'] = id_cliente
                if data_saida: saidas[i]['Data_Saida'] = data_saida
                if destino: saidas[i]['Destino'] = destino
                if motorista: saidas[i]['Motorista'] = motorista
                found = True
                break
        if found:
            self.digitar_tudo_saidas(saidas)
            print(f"Saída com ID {id_saida} atualizada com sucesso.")
            return True
        else:
            print(f"Saída com ID {id_saida} não encontrada para atualização.")
            return False

    def deletar_saida(self, id_saida):
        saidas = self.ler_tudo_saidas()
        novas_saidas = [s for s in saidas if s['ID_Saida'] != id_saida]
        if len(novas_saidas) == len(saidas):
            print(f"Saída com ID {id_saida} não encontrada para exclusão.")
            return False
        self.digitar_tudo_saidas(novas_saidas)
        print(f"Saída com ID {id_saida} excluída com sucesso.")
        return True

    def listar_todos_saidas(self):
        return self.ler_tudo_saidas()