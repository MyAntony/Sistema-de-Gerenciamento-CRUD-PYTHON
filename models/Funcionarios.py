import os

class FuncionariosCRUD:
    def __init__(self, filename="funcionarios.txt"):
        self.filename = filename
        self.criar_arquivo_caso_nao_exista()

    def criar_arquivo_caso_nao_exista(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as f:
                pass

    def ler_tudo_funcionarios(self):
        funcionarios = []
        with open(self.filename, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    campos = line.strip().split(';')
                    funcionarios.append({
                        'ID_Funcionario': campos[0],
                        'Nome': campos[1],
                        'Cargo': campos[2],
                        'Telefone': campos[3],
                        'Email': campos[4],
                        'Endereco_Rua': campos[5],
                        'Endereco_Bairro': campos[6],
                        'Endereco_Cidade': campos[7],
                        'Endereco_Estado': campos[8]
                    })
        return funcionarios

    def digitar_tudo_funcionarios(self, funcionarios):
        with open(self.filename, 'w', encoding='utf-8') as f:
            for funcionario in funcionarios:
                linha = ';'.join([
                    funcionario['ID_Funcionario'],
                    funcionario['Nome'],
                    funcionario['Cargo'],
                    funcionario['Telefone'],
                    funcionario['Email'],
                    funcionario['Endereco_Rua'],
                    funcionario['Endereco_Bairro'],
                    funcionario['Endereco_Cidade'],
                    funcionario['Endereco_Estado']
                ])
                f.write(linha + '\n')

    def gerar_novo_id(self):
        funcionarios = self.ler_tudo_funcionarios()
        if not funcionarios:
            return "1"
        ultimos_ids = [int(f['ID_Funcionario']) for f in funcionarios if f['ID_Funcionario'].isdigit()]
        proximo_num = max(ultimos_ids) + 1 if ultimos_ids else 1
        return str(proximo_num)

    def criar_funcionario(self, nome, cargo, telefone, email, rua, bairro, cidade, estado):
        id_funcionario = self.gerar_novo_id()
        funcionarios = self.ler_tudo_funcionarios()
        novo_funcionario = {
            'ID_Funcionario': id_funcionario,
            'Nome': nome,
            'Cargo': cargo,
            'Telefone': telefone,
            'Email': email,
            'Endereco_Rua': rua,
            'Endereco_Bairro': bairro,
            'Endereco_Cidade': cidade,
            'Endereco_Estado': estado
        }
        funcionarios.append(novo_funcionario)
        self.digitar_tudo_funcionarios(funcionarios)
        print(f"Funcionário cadastrado com sucesso com ID {id_funcionario}.")
        return id_funcionario

    def ler_funcionario(self, id_funcionario):
        funcionarios = self.ler_tudo_funcionarios()
        for funcionario in funcionarios:
            if funcionario['ID_Funcionario'] == id_funcionario:
                return funcionario
        print(f"Funcionário com ID {id_funcionario} não encontrado.")
        return None

    def atualizar_funcionario(self, id_funcionario, nome=None, cargo=None, telefone=None, email=None, rua=None, bairro=None, cidade=None, estado=None):
        funcionarios = self.ler_tudo_funcionarios()
        found = False
        for i, funcionario in enumerate(funcionarios):
            if funcionario['ID_Funcionario'] == id_funcionario:
                if nome: funcionarios[i]['Nome'] = nome
                if cargo: funcionarios[i]['Cargo'] = cargo
                if telefone: funcionarios[i]['Telefone'] = telefone
                if email: funcionarios[i]['Email'] = email
                if rua: funcionarios[i]['Endereco_Rua'] = rua
                if bairro: funcionarios[i]['Endereco_Bairro'] = bairro
                if cidade: funcionarios[i]['Endereco_Cidade'] = cidade
                if estado: funcionarios[i]['Endereco_Estado'] = estado
                found = True
                break
        if found:
            self.digitar_tudo_funcionarios(funcionarios)
            print(f"Funcionário com ID {id_funcionario} atualizado com sucesso.")
            return True
        else:
            print(f"Funcionário com ID {id_funcionario} não encontrado para atualização.")
            return False

    def deletar_funcionario(self, id_funcionario):
        funcionarios = self.ler_tudo_funcionarios()
        novos_funcionarios = [f for f in funcionarios if f['ID_Funcionario'] != id_funcionario]
        if len(novos_funcionarios) == len(funcionarios):
            print(f"Funcionário com ID {id_funcionario} não encontrado para exclusão.")
            return False
        self.digitar_tudo_funcionarios(novos_funcionarios)
        print(f"Funcionário com ID {id_funcionario} excluído com sucesso.")
        return True

    def listar_todos_funcionarios(self):
        return self.ler_tudo_funcionarios()
