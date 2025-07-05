import os

# Atividade de:

# Antony Rafael - https://github.com/MyAntony
# Débora Magalhães - https://github.com/Debs2Dev
# Brunna Barreto - https://github.com/brunnabarreto
# Luís Felipe - https://github.com/IamLiper


class CaminhoesCRUD:
    def __init__(self, filename="caminhoes.txt"):
        self.filename = filename
        self.criar_arquivo_caso_nao_exista()

    def criar_arquivo_caso_nao_exista(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as f:
                pass

    def ler_tudo_caminhoes(self):
        caminhoes = []
        with open(self.filename, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    campos = line.strip().split(';')
                    if len(campos) == 7:
                        caminhoes.append({
                            'ID_Caminhao': campos[0],
                            'Marca': campos[1],
                            'Modelo': campos[2],
                            'Ano': campos[3],
                            'Placa': campos[4],
                            'Quilometragem': campos[5],
                            'Status': campos[6]
                        })
        return caminhoes

    def digitar_tudo_caminhoes(self, caminhoes):
        with open(self.filename, 'w', encoding='utf-8') as f:
            for caminhao in caminhoes:
                linha = ';'.join([
                    caminhao['ID_Caminhao'],
                    caminhao['Marca'],
                    caminhao['Modelo'],
                    str(caminhao['Ano']),
                    caminhao['Placa'],
                    str(caminhao['Quilometragem']),
                    caminhao['Status']
                ])
                f.write(linha + '\n')

    def gerar_novo_id(self):
        caminhoes = self.ler_tudo_caminhoes()
        if not caminhoes:
            return "1"
        ultimos_ids = [int(c['ID_Caminhao']) for c in caminhoes if c['ID_Caminhao'].isdigit()]
        proximo_num = max(ultimos_ids) + 1 if ultimos_ids else 1
        return str(proximo_num)

    def criar_caminhao(self, marca, modelo, ano, placa, quilometragem, status):
        id_caminhao = self.gerar_novo_id()
        caminhoes = self.ler_tudo_caminhoes()
        novo_caminhao = {
            'ID_Caminhao': id_caminhao,
            'Marca': marca,
            'Modelo': modelo,
            'Ano': str(ano),
            'Placa': placa,
            'Quilometragem': str(quilometragem),
            'Status': status
        }
        caminhoes.append(novo_caminhao)
        self.digitar_tudo_caminhoes(caminhoes)
        print(f"Caminhão cadastrado com sucesso com ID {id_caminhao}.")
        return id_caminhao

    def ler_caminhao(self, id_caminhao):
        caminhoes = self.ler_tudo_caminhoes()
        for caminhao in caminhoes:
            if caminhao['ID_Caminhao'] == id_caminhao:
                return caminhao
        print(f"Caminhão com ID {id_caminhao} não encontrado.")
        return None

    def atualizar_caminhao(self, id_caminhao, marca=None, modelo=None, ano=None, placa=None, quilometragem=None, status=None):
        caminhoes = self.ler_tudo_caminhoes()
        found = False
        for i, caminhao in enumerate(caminhoes):
            if caminhao['ID_Caminhao'] == id_caminhao:
                if marca: caminhoes[i]['Marca'] = marca
                if modelo: caminhoes[i]['Modelo'] = modelo
                if ano: caminhoes[i]['Ano'] = str(ano)
                if placa: caminhoes[i]['Placa'] = placa
                if quilometragem: caminhoes[i]['Quilometragem'] = str(quilometragem)
                if status: caminhoes[i]['Status'] = status
                found = True
                break
        if found:
            self.digitar_tudo_caminhoes(caminhoes)
            print(f"Caminhão com ID {id_caminhao} atualizado com sucesso.")
            return True
        else:
            print(f"Caminhão com ID {id_caminhao} não encontrado para atualização.")
            return False

    def deletar_caminhao(self, id_caminhao):
        caminhoes = self.ler_tudo_caminhoes()
        novos_caminhoes = [c for c in caminhoes if c['ID_Caminhao'] != id_caminhao]
        if len(novos_caminhoes) == len(caminhoes):
            print(f"Caminhão com ID {id_caminhao} não encontrado para exclusão.")
            return False
        self.digitar_tudo_caminhoes(novos_caminhoes)
        print(f"Caminhão com ID {id_caminhao} excluído com sucesso.")
        return True

    def listar_todos_caminhoes(self):
        return self.ler_tudo_caminhoes()
