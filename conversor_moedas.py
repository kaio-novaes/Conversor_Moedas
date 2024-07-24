import requests
from datetime import date, datetime


class Moeda:
    """
    Representa uma moeda com seu título e valor.
    """
    def __init__(self, titulo: str, valor_moeda: str):
        self.titulo = titulo
        self.valor_moeda = valor_moeda


class ConversaoMoeda:
    """
    Representa o histórico de uma moeda com valor, base, data de início, data de fim e taxas.

    Atributos:
        valor (float): O valor a ser convertido.
        base (str): A moeda base da conversão.
        data (date): A data da conversão.
        taxas (dict): Um dicionário de taxas de conversão.
    """
    def __init__(self, valor: float, base: str, data: date, taxas: dict):
        self.valor = valor
        self.base = base
        self.data = data
        self.taxas = taxas


class HistoricoMoeda:
    """
    Representa o histórico de uma moeda com valor, base, data de início, data de fim e taxas.

    Atributos:
        valor (float): O valor da moeda.
        base (str): A moeda base do histórico.
        data_inicio (date): A data de início do histórico.
        data_fim (date): A data de fim do histórico.
        taxas (list): Uma lista de taxas históricas.
    """
    def __init__(self, valor: float, base: str, data_inicio: date, data_fim: date, taxas: list):
        self.valor = valor
        self.base = base
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.taxas = taxas


class DadosMoeda:
    """
    Gerencia o armazenamento de dados relacionados a moedas e conversões.

    Atributos:
        valor (float): O valor padrão para conversão.
        moedas (list): Uma lista de objetos Moeda disponíveis.
        origem (Moeda): A moeda de origem selecionada.
        destino (Moeda): A moeda de destino selecionada.
        conversao (ConversaoMoeda): Os dados da última conversão realizada.
        taxa_conversao (float): A taxa de conversão atual.
        dados_historicos (dict): Os dados históricos de conversão entre moedas.
        serie_temporal_moeda (list): Uma série temporal de moedas e valores.
    """
    def __init__(self):
        self.valor = 1000
        self.moedas = []
        self.origem = None
        self.destino = None
        self.conversao = None
        self.taxa_conversao = 0.0
        self.dados_historicos = None
        self.serie_temporal_moeda = None

    def inicializar_dados(self):
        """
        Inicia o armazenamento carregando moedas, interagindo com o usuário e obtendo os dados.
        """
        self.obter_moedas()
        self.interacao_usuario()
        self.obter_dados_historicos()

    def inverter_moedas(self):
        """
        Inverte as moedas de origem e destino.
        """
        self.origem, self.destino = self.destino, self.origem

    def analisar_dados_historicos(self):
        """
        Analisa os dados históricos obtidos e cria uma série temporal de moedas e valores.
        """
        if not self.dados_historicos or 'rates' not in self.dados_historicos:
            return
        
        self.serie_temporal_moeda = []
        for chave, valor in self.dados_historicos['rates'].items():
            self.serie_temporal_moeda.append({
                'nome': chave,
                'valor': valor[self.destino.valor]
            })

    def definir_taxa_conversao(self, dados: ConversaoMoeda):
        """
        Define a taxa de conversão com base nos dados fornecidos.
        """
        self.taxa_conversao = list(dados.taxas.values())[0]

    def obter_moedas(self):
        """
        Obtém a lista de moedas disponíveis da API Frankfurter.
        """
        try:
            response = requests.get('https://api.frankfurter.app/currencies')
            if response.status_code == 200:
                dados = response.json()
                self.moedas = [
                    Moeda(titulo=titulo, valor_moeda=valor)
                    for valor, titulo in dados.items()
                ]
                self.moedas.sort(key=lambda x: x.titulo)
            else:
                print(f"Erro ao tentar obter moedas: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição HTTP: {e}")

    def interacao_usuario(self):
        """
        Interage com o usuário para obter o valor a ser convertido e as moedas de origem e destino.
        """
        try:
            print("Conversor de moedas:".center(30))
            print("=" * 30)
            self.valor = float(input("\nQual valor deseja converter: "))
            print("Lista de moedas disponíveis:")
            for i, moeda in enumerate(self.moedas, start=1):
                print(f"{i} - {moeda.titulo}")

            moeda_origem = int(input("Qual a moeda de origem: (número correspondente): ")) - 1
            moeda_destino = int(input("Qual a moeda de destino: (número correspondente): ")) - 1

            self.origem = self.moedas[moeda_origem]
            self.destino = self.moedas[moeda_destino]

            print(f"Convertendo {self.valor:.2f} {self.origem.titulo} para {self.destino.titulo}...")
            self.obter_conversao()

            print(f"Taxa de conversão de {self.origem.titulo} para {self.destino.titulo}: {self.taxa_conversao:.2f}")

        except ValueError:
            print(f"Valor inválido. Digite um número válido.")
        except IndexError:
            print(f"Escolha inválida para a moeda. Digite um número correspondente à lista.")

    def obter_conversao(self):
        """
        Obtém a taxa de conversão atual da moeda de origem para a moeda de destino.
        """
        if not self.valor or not self.origem or not self.destino or self.origem.valor_moeda == self.destino.valor_moeda:
            return
        
        try:
            response = requests.get("https://api.frankfurter.app/latest", params={
                'amount': self.valor,
                'from': self.origem.valor_moeda,
                'to': self.destino.valor_moeda
            })
            if response.status_code == 200:
                dados = response.json()
                self.definir_taxa_conversao(ConversaoMoeda(
                    valor=self.valor,
                    base=dados['base'],
                    data=datetime.strptime(dados['date'], '%Y-%m-%d').date(),
                    taxas=dados['rates']
                ))
            else:
                print(f"Erro ao tentar obter conversão {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição HTTP: {e}")

    def obter_dados_historicos(self):
        """
        Obtém os dados históricos de conversão entre moedas da API Frankfurter.
        """
        try:
            data_inicio = date.today()
            data_fim = date.today()  
            response = requests.get("https://api.frankfurter.app", params={
                'from': self.origem.valor_moeda,
                'to': self.destino.valor_moeda,
                'amount': self.valor,
                'start_date': data_inicio,
                'end_date': data_fim
            })
            if response.status_code == 200:
                dados = response.json()
                self.dados_historicos = dados
                self.analisar_dados_historicos()
            else:
                print(f"Erro ao obter histórico: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição HTTP: {e}")

if __name__ == "__main__":
    armazenamento_moeda = DadosMoeda()
    armazenamento_moeda.inicializar_dados()
