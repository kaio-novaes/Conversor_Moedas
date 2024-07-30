# Conversor Moedas

Este script Python facilita a conversão de valores entre diferentes moedas utilizando dados atualizados da API Frankfurter. Ele oferece funcionalidades para consultar taxas de conversão atuais, acessar dados históricos e interagir com o usuário para realizar conversões.

### Funcionalidades:

* Listagem de Moedas: Obtém e exibe uma lista de todas as moedas disponíveis para conversão a partir da API Frankfurter.
* Conversão de Moeda: Converte um valor especificado de uma moeda de origem para uma moeda de destino, utilizando a taxa de câmbio atual fornecida pela API Frankfurter.
* Dados Históricos de Conversão: Recupera e analisa dados históricos de conversão entre duas moedas, oferecendo uma visão das taxas passadas.

### Componentes Principais:

* Moeda: Representa uma moeda com seu título e código.
* ConversaoMoeda: Armazena informações sobre uma conversão específica, incluindo valor, moeda base e taxas de câmbio.
* HistoricoMoeda: Armazena dados históricos de conversão, incluindo o valor, base, intervalo de datas e taxas históricas.
* DadosMoeda: Gerencia dados de moedas e conversões, interage com o usuário e armazena dados históricos.

#### Bibliotecas:

* **requests:** Para requisições HTTP,
* **datetime:** Para manipulação de datas.
  
#### Versão do Python:

* Python 3.12.

#### Como Usar:

* Insira o valor a ser convertido e selecione as moedas de origem e destino a partir da lista fornecida.
* O script exibirá a taxa de conversão atual, o valor convertido e dados históricos se disponíveis.

### Notas Adicionais:

As conversões são baseadas nas taxas atuais obtidas via API Frankfurter.
O histórico de conversão é analisado para fornecer uma visão das taxas passadas.
