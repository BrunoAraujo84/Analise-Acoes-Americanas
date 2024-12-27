import yfinance as yf
import warnings

# Suprimindo avisos
warnings.filterwarnings('ignore')

# função de obter dividendos de uma determinada ação americana
def obter_dividendo(ticker_simbolo):
    try:
        ticker_simbolo = ticker_simbolo.upper()
        acao = yf.Ticker(ticker_simbolo)
        historico_dividendos = acao.dividends
        informacoes = acao.info
        nome_empresa = informacoes.get('longName', 'Nome da empresa não disponível')
        preco_atual = informacoes.get('regularMarketPrice', None)
        
        if not historico_dividendos.empty:
            ultimo_dividendo = historico_dividendos.iloc[-1]
            data_ultimo_dividendo = historico_dividendos.index[-1]
            
            if len(historico_dividendos) > 1:
                penultimo_dividendo = historico_dividendos.iloc[-2]
                variacao = ultimo_dividendo - penultimo_dividendo
                if variacao > 0:
                    status_variacao = "houve um aumento"
                    print(f"O último dividendo pago pela ação {nome_empresa} ({ticker_simbolo}) foi: $ {ultimo_dividendo:.2f} na data: {data_ultimo_dividendo.strftime('%d/%m/%Y')}. Em relação ao penúltimo dividendo, {status_variacao} de $ {abs(variacao):.2f}.")
                elif variacao < 0:
                    status_variacao = "houve uma diminuição"
                    print(f"O último dividendo pago pela ação {nome_empresa} ({ticker_simbolo}) foi: $ {ultimo_dividendo:.2f} na data: {data_ultimo_dividendo.strftime('%d/%m/%Y')}. Em relação ao penúltimo dividendo, {status_variacao} de $ {abs(variacao):.2f}.")
                else:
                    status_variacao = "o valor se manteve"
                    print(f"O último dividendo pago pela ação {nome_empresa} ({ticker_simbolo}) foi: $ {ultimo_dividendo:.2f} na data: {data_ultimo_dividendo.strftime('%d/%m/%Y')}. Em relação ao penúltimo dividendo, {status_variacao}.")
            else:
                print(f"O último dividendo pago pela ação {nome_empresa} ({ticker_simbolo}) foi: $ {ultimo_dividendo:.2f} na data: {data_ultimo_dividendo.strftime('%d/%m/%Y')}.")
            
            if preco_atual is not None:
                print(f"O valor atual da ação {nome_empresa} ({ticker_simbolo}) é: $ {preco_atual:.2f}")
            else:
                print(f"O valor atual da ação {nome_empresa} ({ticker_simbolo}) não está disponível.")
        else:
            print(f"A ação {ticker_simbolo} não paga dividendos ou a informação não está disponível.")
    except Exception as e:
        print(f"Erro ao obter dados para a ação {ticker_simbolo}: {e}")

# Função que interage com o usuário na tomada de decisão
def main():
    while True:
        ticker_simbolo = input("Digite o símbolo da ação (ou 'sair' para encerrar): ")
        if ticker_simbolo.lower() == 'sair':
            break
        obter_dividendo(ticker_simbolo)

if __name__ == "__main__":
    main()