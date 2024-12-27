## Sobre os Arquivos

Este repositório contém dois scripts Python que utilizam a biblioteca `yfinance` para analisar ações americanas. Abaixo, segue uma descrição detalhada de cada arquivo e suas funcionalidades.

### Arquivos

#### 1. **Listando_melhores_acoes_americanas.py**

Este script tem como objetivo listar as 20 ações que:
- Mais pagaram dividendos no ano atual.
- Mais se valorizaram nos últimos 3 meses.

**Funcionalidades Principais:**
1. **Obtenção de Lista de Ações:**
   - Obtém a lista de empresas do S&P 500 diretamente da Wikipédia.
   - Utiliza a biblioteca `BeautifulSoup` para fazer scraping da tabela de empresas.
2. **Análise de Dividendos:**
   - Filtra os dados de dividendos para o ano atual.
   - Calcula o total de dividendos pagos por ação.
   - Retorna as 20 empresas com maior soma de dividendos.
3. **Análise de Valorização:**
   - Calcula a valorização percentual das ações nos últimos 3 meses.
   - Retorna as 20 empresas com maior valorização percentual.
4. **Output:**
   - Exibe no console as 20 ações com maiores dividendos e as 20 com maior valorização.

**Bibliotecas Necessárias:**
- `yfinance`
- `pandas`
- `requests`
- `bs4` (BeautifulSoup)
- `datetime`
- `requests_cache`
- `warnings`

#### 2. **Pesquisa_acoes_americanas.py**

Este script permite ao usuário verificar os dividendos de uma ação específica.

**Funcionalidades Principais:**
1. **Consulta de Dividendos:**
   - Permite inserir o símbolo de uma ação e retorna:
     - O último dividendo pago e sua data.
     - A variação em relação ao penúltimo dividendo, caso exista.
2. **Consulta do Preço Atual:**
   - Exibe o preço atual da ação, caso disponível.
3. **Interação com o Usuário:**
   - O usuário pode consultar várias ações em sequência digitando seus símbolos.

**Bibliotecas Necessárias:**
- `yfinance`
- `warnings`

---

## Como Configurar e Executar

### Como Instalar as Bibliotecas Necessárias

Certifique-se de ter o Python instalado em sua máquina. Recomenda-se o uso de um ambiente virtual para gerenciar as dependências.

1. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv env
   source env/bin/activate  # Linux/Mac
   env\Scripts\activate   # Windows
   ```

2. Instale as bibliotecas necessárias com o comando abaixo:
   ```bash
   pip install yfinance pandas requests beautifulsoup4 requests-cache
   ```

3. Verifique se as bibliotecas foram instaladas corretamente:
   ```bash
   pip list
   ```

### Como Executar os Scripts

#### 1. **Listando_melhores_acoes_americanas.py**
Execute o script para listar as melhores ações em dividendos e valorização:
```bash
python Listando_melhores_acoes_americanas.py
```

#### 2. **Pesquisa_acoes_americanas.py**
Execute o script para consultar informações específicas de uma ação:
```bash
python Pesquisa_acoes_americanas.py
```

Durante a execução, insira o símbolo da ação que deseja consultar ou digite `sair` para encerrar.

---

## Observações
- Certifique-se de estar conectado à internet para que as consultas funcionem corretamente.
- Os dados dependem da disponibilidade da API `yfinance` e das informações da Wikipédia para o S&P 500.
