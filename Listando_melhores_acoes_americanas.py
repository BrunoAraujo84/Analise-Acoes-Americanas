import yfinance as yf
import pandas as pd
import requests
import warnings
from bs4 import BeautifulSoup
from datetime import datetime
import requests_cache

# Suprimindo avisos
warnings.filterwarnings('ignore')

# Otimização na criação da sessão request.
session = requests_cache.CachedSession('yfinance_cache', expire_after=300) 

# Resgatar o ano atual
ano = datetime.now().year

# User-Agent para evitar eventuais bloqueios ou redirecionamentos
headers = {"User-Agent": "Mozilla/5.0"}

# Função para obter lista de ações americanas (S&P 500)
def obter_lista_acoes_americanas():
    try:
        url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            tabela = soup.find('table', {'id': 'constituents'})
            lista_acoes = []
            if tabela:
                linhas = tabela.find_all('tr')[1:]
                for linha in linhas:
                    colunas = linha.find_all('td')
                    if colunas:
                        codigo = colunas[0].text.strip()
                        nome_empresa = colunas[1].text.strip()
                        if '.' not in codigo:  # Ignorar tickers com '.' (e.g., BRK.B)
                            lista_acoes.append((codigo, nome_empresa))
            return lista_acoes
        else:
            print(f"Erro ao acessar a página: {response.status_code}")
            return []
    except Exception as e:
        print(f"Erro ao obter lista de ações do S&P 500: {e}")
        return []


# Função para obter as ações que pagaram mais dividendos
def obter_20_maiores_dividendos(lista_acoes):
    dividendos = []
    for ticker, nome_empresa in lista_acoes:
        try:
            acao = yf.Ticker(ticker, session=None)
            # Obtém todo o histórico de dividendos
            historico_dividendos = acao.dividends
            # Filtra apenas os dividendos de 2024 (ou do ano atual, se 'ano' for global)
            historico_dividendos_2024 = historico_dividendos[historico_dividendos.index.year == ano]
            # Caso a empresa tenha pago dividendos em 2024
            if not historico_dividendos_2024.empty:
                # Soma de todos os dividendos de 2024
                total_dividendos_2024 = historico_dividendos_2024.sum()
                # Armazena a data do último dividendo de 2024 (opcional)
                data_ultimo_dividendo = historico_dividendos_2024.index[-1]
                # Pega o preço atual da ação (último close)
                preco_atual = acao.history(period="1d")["Close"].iloc[-1]
                # Adiciona à lista para ordenarmos depois
                dividendos.append(
                    (ticker, nome_empresa, total_dividendos_2024, data_ultimo_dividendo, preco_atual)
                )
        except Exception as e:
            print(f"Erro ao obter dividendos para a ação {ticker}: {e}")
    
    # Ordena de forma decrescente pelo total de dividendos
    dividendos_ordenados = sorted(dividendos, key=lambda x: x[2], reverse=True)
    # Retorna apenas as 20 empresas com maior soma de dividendos
    return dividendos_ordenados[:20]


# Função para obter as ações que mais se valorizaram nos últimos 3 meses
def obter_20_maiores_valorizacoes(lista_acoes):
    valorizacoes = []
    for ticker, nome_empresa in lista_acoes:
        try:
            acao = yf.Ticker(ticker, session=session)
            historico = acao.history(period="3mo")
            historico_dividendos = acao.dividends
            historico_dividendos_2024 = historico_dividendos[historico_dividendos.index.year == ano]
            if not historico_dividendos_2024.empty:
                if not historico.empty and len(historico) > 1:
                    preco_inicial = historico["Close"].iloc[0]
                    preco_final = historico["Close"].iloc[-1]
                    valorizacao = ((preco_final - preco_inicial) / preco_inicial) * 100
                    data_preco_final = historico.index[-1]
                    valorizacoes.append((ticker, nome_empresa, valorizacao, preco_final, data_preco_final))
        except Exception as e:
            print(f"Erro ao obter histórico para a ação {ticker}: {e}")
    
    valorizacoes_ordenadas = sorted(valorizacoes, key=lambda x: x[2], reverse=True)
    return valorizacoes_ordenadas[:20]


# Função principal para listar as 20 ações com maiores dividendos e 20 com maior valorização
def main():
    lista_acoes = obter_lista_acoes_americanas()
    if lista_acoes:
        print("\nAs 20 ações que mais pagaram dividendos recentemente:")
        maiores_dividendos = obter_20_maiores_dividendos(lista_acoes)
        for ticker, nome_empresa, dividendo, data_dividendo, preco_atual in maiores_dividendos:
            print(f"Ação: {ticker} ({nome_empresa}), Total Dividendos Pago em {ano}: $ {dividendo:.2f}, Data do último dividendo: {data_dividendo.strftime('%d/%m/%Y')}, Preço Atual: $ {preco_atual:.2f}")
        
        print("\nAs 20 ações que mais se valorizaram nos últimos 3 meses:")
        maiores_valorizacoes = obter_20_maiores_valorizacoes(lista_acoes)
        for ticker, nome_empresa, valorizacao, preco_atual, data_preco in maiores_valorizacoes:
            print(f"Ação: {ticker} ({nome_empresa}), Valorização: {valorizacao:.2f}%, Preço Atual: $ {preco_atual:.2f}, Data do preço atual: {data_preco.strftime('%d/%m/%Y')}")
    else:
        print("Não foi possível obter a lista de ações do S&P 500.")


if __name__ == "__main__":
    main()
