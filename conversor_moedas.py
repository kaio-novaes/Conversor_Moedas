import requests

def obter_taxa(moeda_base, moeda_destino):
    url = f"https://api.exchangerate-api.com/v4/latest/{moeda_base}"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        taxa_conversao = data['rates'].get(moeda_destino)
        if taxa_conversao:
            return taxa_conversao
        else:
            raise ValueError(f"Moeda '{moeda_destino}' não encontrada.")
    else:
        raise ValueError(f"Falha ao tentar obter as taxas de câmbio: {data['error']}")

def converter_moeda(valor, taxa_conversao):
    return valor * taxa_conversao

def main():
    print("Ex: (BRL) - Real Brasil")
    moeda_base = input("Qual a sua moeda atual: ").upper()
    moeda_destino = input("Para qual moeda você deseja converter: ").upper() 
    valor = float(input("Digite o valor a ser convertido: "))

    try:
        taxa = obter_taxa(moeda_base, moeda_destino)
        valor_convertido = converter_moeda(valor, taxa)
        print(f"{valor} {moeda_base} = {valor_convertido:.2f} {moeda_destino}")
    except Exception as e:
        print(f"Erro ao converter moeda: {e}")

if __name__ == "__main__":
    main()
