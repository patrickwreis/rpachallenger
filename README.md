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

> **Nota:** Este projeto utiliza o [Poetry](https://python-poetry.org/) para gerenciar dependências e ambientes virtuais. Se você nunca usou o Poetry, siga as instruções abaixo para instalar e utilizar.

### Instalando o Poetry

1. **Via comando oficial (recomendado):**
   ```sh
   curl -sSL https://install.python-poetry.org | python3 -
   ```
   Ou, no Windows (PowerShell):
   ```powershell
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
   ```
   Após instalar, feche e reabra o terminal, e verifique:
   ```sh
   poetry --version
   ```

2. **Clone o repositório:**
   ```sh
   git clone https://github.com/seu-usuario/rpachallenger.git
   cd rpachallenger
   ```

3. **Instale as dependências:**
   ```sh
   poetry install
   ```
   > O Poetry instalará todas as dependências, incluindo `selenium`, `playwright`, `openpyxl`, `pandas` e outras.

4. **(Opcional) Instale os browsers do Playwright:**
   ```sh
   poetry run playwright install
   ```

## Como Usar

### Via Terminal (CLI)
Execute o script principal escolhendo o modo de execução:

```sh
poetry run python main.py --mode selenium    # Executa usando Selenium (padrão)
poetry run python main.py --mode playwright  # Executa usando Playwright
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

## Autor
- Patrick Reis (<patrickwreis@gmail.com>)

## Licença
Este projeto está licenciado sob os termos da licença MIT.
