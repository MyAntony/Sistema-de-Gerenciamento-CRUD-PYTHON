import os

class PecasCRUD:
    def __init__(self, filename="pecas.txt"):
        self.filename = filename
        self.criar_arquivo_caso_nao_exista()

    def criar_arquivo_caso_nao_exista(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as f:
                pass

    def ler_tudo_pecas(self):
        pecas = []
        with open(self.filename, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    campos = line.strip().split(';')
                    pecas.append({
                        'ID_Peca': campos[0],
                        'Nome': campos[1],
                        'Descricao': campos[2],
                        'Fabricante': campos[3],
                        'Preco': campos[4],
                        'Quantidade': campos[5]
                    })
        return pecas

    def digitar_tudo_pecas(self, pecas):
        with open(self.filename, 'w', encoding='utf-8') as f:
            for peca in pecas:
                linha = ';'.join([
                    peca['ID_Peca'],
                    peca['Nome'],
                    peca['Descricao'],
                    peca['Fabricante'],
                    str(peca['Preco']),
                    str(peca['Quantidade'])
                ])
                f.write(linha + '\n')

    def gerar_novo_id(self):
        pecas = self.ler_tudo_pecas()
        if not pecas:
            return "1"
        ultimos_ids = [int(p['ID_Peca']) for p in pecas if p['ID_Peca'].isdigit()]
        proximo_num = max(ultimos_ids) + 1 if ultimos_ids else 1
        return str(proximo_num)

    def criar_peca(self, nome, descricao, fabricante, preco, quantidade):
        id_peca = self.gerar_novo_id()
        pecas = self.ler_tudo_pecas()
        nova_peca = {
            'ID_Peca': id_peca,
            'Nome': nome,
            'Descricao': descricao,
            'Fabricante': fabricante,
            'Preco': str(preco),
            'Quantidade': str(quantidade)
        }
        pecas.append(nova_peca)
        self.digitar_tudo_pecas(pecas)
        print(f"Peça cadastrada com sucesso com ID {id_peca}.")
        return id_peca

    def ler_peca(self, id_peca):
        pecas = self.ler_tudo_pecas()
        for peca in pecas:
            if peca['ID_Peca'] == id_peca:
                return peca
        print(f"Peça com ID {id_peca} não encontrada.")
        return None

    def atualizar_peca(self, id_peca, nome=None, descricao=None, fabricante=None, preco=None, quantidade=None):
        pecas = self.ler_tudo_pecas()
        found = False
        for i, peca in enumerate(pecas):
            if peca['ID_Peca'] == id_peca:
                if nome: pecas[i]['Nome'] = nome
                if descricao: pecas[i]['Descricao'] = descricao
                if fabricante: pecas[i]['Fabricante'] = fabricante
                if preco: pecas[i]['Preco'] = str(preco)
                if quantidade: pecas[i]['Quantidade'] = str(quantidade)
                found = True
                break
        if found:
            self.digitar_tudo_pecas(pecas)
            print(f"Peça com ID {id_peca} atualizada com sucesso.")
            return True
        else:
            print(f"Peça com ID {id_peca} não encontrada para atualização.")
            return False

    def deletar_peca(self, id_peca):
        pecas = self.ler_tudo_pecas()
        novas_pecas = [p for p in pecas if p['ID_Peca'] != id_peca]
        if len(novas_pecas) == len(pecas):
            print(f"Peça com ID {id_peca} não encontrada para exclusão.")
            return False
        self.digitar_tudo_pecas(novas_pecas)
        print(f"Peça com ID {id_peca} excluída com sucesso.")
        return True

    def listar_todos_pecas(self):
        return self.ler_tudo_pecas()
