import os

# Atividade de:

# Antony Rafael - https://github.com/MyAntony
# Débora Magalhães - https://github.com/Debs2Dev
# Brunna Barreto - https://github.com/brunnabarreto
# Luís Felipe - https://github.com/IamLiper


class FornecedoresCRUD:
    def __init__(self, filename="fornecedores.txt"):
        self.filename = filename
        self.criar_arquivo_caso_nao_exista()

    def criar_arquivo_caso_nao_exista(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as f:
                pass

    def ler_tudo_fornecedores(self):
        fornecedores = []
        with open(self.filename, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    campos = line.strip().split(';')
                    fornecedores.append({
                        'ID_Fornecedor': campos[0],
                        'Nome': campos[1],
                        'Contato': campos[2],
                        'Endereco_Rua': campos[3],
                        'Endereco_Bairro': campos[4],
                        'Endereco_Cidade': campos[5],
                        'Endereco_Estado': campos[6],
                        'Telefone': campos[7],
                        'Email': campos[8]
                    })
        return fornecedores

    def digitar_tudo_fornecedores(self, fornecedores):
        with open(self.filename, 'w', encoding='utf-8') as f:
            for fornecedor in fornecedores:
                linha = ';'.join([
                    fornecedor['ID_Fornecedor'],
                    fornecedor['Nome'],
                    fornecedor['Contato'],
                    fornecedor['Endereco_Rua'],
                    fornecedor['Endereco_Bairro'],
                    fornecedor['Endereco_Cidade'],
                    fornecedor['Endereco_Estado'],
                    fornecedor['Telefone'],
                    fornecedor['Email']
                ])
                f.write(linha + '\n')

    def gerar_novo_id(self):
        fornecedores = self.ler_tudo_fornecedores()
        if not fornecedores:
            return "1"
        ultimos_ids = [int(f['ID_Fornecedor']) for f in fornecedores if f['ID_Fornecedor'].isdigit()]
        proximo_num = max(ultimos_ids) + 1 if ultimos_ids else 1
        return str(proximo_num)

    def criar_fornecedor(self, nome, contato, rua, bairro, cidade, estado, telefone, email):
        id_fornecedor = self.gerar_novo_id()
        fornecedores = self.ler_tudo_fornecedores()
        novo_fornecedor = {
            'ID_Fornecedor': id_fornecedor,
            'Nome': nome,
            'Contato': contato,
            'Endereco_Rua': rua,
            'Endereco_Bairro': bairro,
            'Endereco_Cidade': cidade,
            'Endereco_Estado': estado,
            'Telefone': telefone,
            'Email': email
        }
        fornecedores.append(novo_fornecedor)
        self.digitar_tudo_fornecedores(fornecedores)
        print(f"Fornecedor cadastrado com sucesso com ID {id_fornecedor}.")
        return id_fornecedor

    def ler_fornecedor(self, id_fornecedor):
        fornecedores = self.ler_tudo_fornecedores()
        for fornecedor in fornecedores:
            if fornecedor['ID_Fornecedor'] == id_fornecedor:
                return fornecedor
        print(f"Fornecedor com ID {id_fornecedor} não encontrado.")
        return None

    def atualizar_fornecedor(self, id_fornecedor, new_nome=None, new_contato=None, new_endereco_rua=None, new_endereco_bairro=None, new_endereco_cidade=None, new_endereco_estado=None, new_telefone=None, new_email=None):
        fornecedores = self.ler_tudo_fornecedores()
        found = False
        for i, fornecedor in enumerate(fornecedores):
            if fornecedor['ID_Fornecedor'] == id_fornecedor:
                if new_nome: fornecedores[i]['Nome'] = new_nome
                if new_contato: fornecedores[i]['Contato'] = new_contato
                if new_endereco_rua: fornecedores[i]['Endereco_Rua'] = new_endereco_rua
                if new_endereco_bairro: fornecedores[i]['Endereco_Bairro'] = new_endereco_bairro
                if new_endereco_cidade: fornecedores[i]['Endereco_Cidade'] = new_endereco_cidade
                if new_endereco_estado: fornecedores[i]['Endereco_Estado'] = new_endereco_estado
                if new_telefone: fornecedores[i]['Telefone'] = new_telefone
                if new_email: fornecedores[i]['Email'] = new_email
                found = True
                break
        if found:
            self.digitar_tudo_fornecedores(fornecedores)
            print(f"Fornecedor com ID {id_fornecedor} atualizado com sucesso.")
            return True
        else:
            print(f"Fornecedor com ID {id_fornecedor} não encontrado para atualização.")
            return False

    def deletar_fornecedor(self, id_fornecedor):
        fornecedores = self.ler_tudo_fornecedores()
        initial_len = len(fornecedores)
        fornecedores = [fornecedor for fornecedor in fornecedores if fornecedor['ID_Fornecedor'] != id_fornecedor]
        if len(fornecedores) < initial_len:
            self.digitar_tudo_fornecedores(fornecedores)
            print(f"Fornecedor com ID {id_fornecedor} excluído com sucesso.")
            return True
        else:
            print(f"Fornecedor com ID {id_fornecedor} não encontrado para exclusão.")
            return False

    def listar_todos_fornecedores(self):
        return self.ler_tudo_fornecedores()
