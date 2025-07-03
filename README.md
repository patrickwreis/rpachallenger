# RPA Challenger

Automação do desafio RPA Challenge com múltiplas opções de execução: Selenium e Playwright. O projeto permite baixar, preencher e submeter o formulário do site [rpachallenge.com](https://rpachallenge.com) de forma automatizada.

## Funcionalidades
- **Dual Mode**: Selenium ou Playwright
- **Download automático** do arquivo Excel do desafio
- **CLI completa** com argumentos `--mode` e `--headless`
- **Múltiplas formas de execução**: terminal, VS Code, tasks
- **Log detalhado** de execução com tempo total

## Requisitos
- Python 3.12+
- Google Chrome instalado

## Instalação

**Via pip (recomendado):**
```sh
pip install -r requirements.txt
```

**Via Poetry (opcional):**
```sh
poetry install
```

**Para Playwright:**
```sh
python -m playwright install  # ou: poetry run playwright install
```

## Alternativa: Instalação com requirements.txt

Se preferir não usar o Poetry, você pode instalar as dependências diretamente com pip usando o arquivo `requirements.txt`:

```sh
pip install -r requirements.txt
```

## Como Usar

### CLI (Terminal)
```sh
# Básico
python main.py                                    # Selenium padrão
python main.py --mode playwright                  # Playwright
python main.py --mode selenium --headless         # Selenium headless
python main.py --mode playwright --headless       # Playwright headless

# Com Poetry
poetry run python main.py --mode playwright --headless
```

### VS Code
- **Run**: Clique em "Run" no `main.py` (usa Selenium padrão)
- **Tasks**: Use as tasks configuradas para argumentos específicos

## Estrutura do Projeto
```
├── main.py                # Script principal com CLI
├── settings.py            # Configurações do projeto
├── requirements.txt       # Dependências pip
├── pyproject.toml         # Configuração Poetry
├── challenge.xlsx         # Arquivo Excel (gerado automaticamente)
└── README.md              # Este arquivo
```

## Notas
- O arquivo `challenge.xlsx` é baixado automaticamente
- ChromeDriver é gerenciado automaticamente pelo Selenium 4+
- O parâmetro `--headless` funciona em ambos os modos
- Poetry: https://python-poetry.org/docs/#installation

## Autor
Patrick Reis (<patrickwreis@gmail.com>)

## Licença
MIT License
