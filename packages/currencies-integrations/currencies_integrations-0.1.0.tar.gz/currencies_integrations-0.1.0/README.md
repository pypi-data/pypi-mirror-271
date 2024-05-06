![logo do projeto](docs/assets/logo_d1.png){ width="300" .center }
# Cotações diversas

## Como instalar o projeto

Para instalação do cli do projeto recomendamos que use o `pipx` para fazer essa instalação:

```bash
pipx install currencies-integrations
```

Embora isso seja somente uma recomendação! Você também pode instalar o projeto com o gerenciador de sua preferência. Como o pip:

```bash
pip install currencies-integrations
```

## Como usar?

### Dolar

Você pode chamar as cotações via linha de comando. Por exemplo:


```bash
cotacoes dolar-comercial
```

O formato retornado será bem simples. 

```
┏━━━━━━━━━━━━━━━┓
┃ USD Comercial ┃
┡━━━━━━━━━━━━━━━┩
│ R$ 5.1125     │
└───────────────┘
```