# RPA Challenger

Automação do desafio RPA Challenge com múltiplas opções de execução: Selenium e Playwright. O projeto permite baixar, preencher e submeter o formulário do site [rpachallenge.com](https://rpachallenge.com) de forma automatizada, com seleção de modo via CLI.

## Funcionalidades
- Download automático do arquivo Excel do desafio
- Preenchimento e submissão dos dados usando Selenium ou Playwright
- Seleção do modo de execução via linha de comando (`--mode`)
- Compatível com execução via terminal, VS Code (Run) e tasks
- Log detalhado de execução

## Requisitos
- Python 3.12+
- Google Chrome instalado (para Selenium)
- [Poetry](https://python-poetry.org/) para gerenciamento de dependências

## Instalação

Você pode instalar as dependências do projeto de duas formas:

### 1. Usando requirements.txt (pip)

O método mais simples e universal é via pip:

```sh
pip install -r requirements.txt
```

### 2. Usando Poetry (opcional)

Se você já utiliza o [Poetry](https://python-poetry.org/), pode instalar as dependências com:

```sh
poetry install
```

> Se não conhece o Poetry, utilize o método com pip acima. Caso queira saber mais ou instalar o Poetry, acesse: https://python-poetry.org/docs/#installation

### (Opcional) Instale os browsers do Playwright
Se for rodar no modo Playwright, execute:
```sh
python -m playwright install
# ou, se estiver usando Poetry:
poetry run playwright install
```

## Alternativa: Instalação com requirements.txt

Se preferir não usar o Poetry, você pode instalar as dependências diretamente com pip usando o arquivo `requirements.txt`:

```sh
pip install -r requirements.txt
```

> Atenção: O uso do Poetry é recomendado para garantir o ambiente reprodutível, mas o `requirements.txt` está disponível para facilitar testes rápidos ou integração com outros sistemas.

## Como Usar

### Via Terminal (CLI)
Execute o script principal escolhendo o modo de execução e, se desejar, o modo headless:

```sh
python main.py --mode selenium              # Executa usando Selenium (padrão)
python main.py --mode playwright            # Executa usando Playwright
python main.py --mode selenium --headless   # Selenium em modo headless
python main.py --mode playwright --headless # Playwright em modo headless
```

Se estiver usando Poetry:
```sh
poetry run python main.py --mode selenium --headless
```

### Via VS Code
- Basta clicar em "Run" no arquivo `main.py` para rodar no modo padrão (Selenium).
- Ou utilize as tasks já configuradas para rodar com argumentos.

### Via Taskipy (opcional)
Se desejar, adicione tasks customizadas no `pyproject.toml` para rodar com Taskipy:
```toml
[tool.taskipy.tasks]
run-selenium = 'python main.py --mode=selenium'
run-playwright = 'python main.py --mode=playwright'
```
E execute:
```sh
poetry run task run-selenium
poetry run task run-playwright
```

## Estrutura do Projeto
```
├── main.py                # Script principal com CLI
├── settings.py            # Configurações do projeto
├── challenge.xlsx         # Arquivo Excel baixado automaticamente
├── pyproject.toml         # Configuração do Poetry e dependências
├── poetry.lock            # Lockfile do Poetry
└── README.md              # Este arquivo
```

## Notas
- O arquivo `challenge.xlsx` é baixado automaticamente na primeira execução.
- O modo Selenium requer o ChromeDriver compatível com sua versão do Chrome (gerenciado automaticamente pelo Selenium 4+).
- O modo Playwright requer instalação dos browsers Playwright (`poetry run playwright install`).
- O log de execução é exibido no console.
- O parâmetro `--headless` pode ser usado tanto com Selenium quanto com Playwright para rodar o navegador sem interface gráfica.

## Autor
- Patrick Reis (<patrickwreis@gmail.com>)

## Licença
Este projeto está licenciado sob os termos da licença MIT.
