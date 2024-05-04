# INEGIExplorer
INEGIExplorer is a Python library that enables users to explore INEGI data without constraints, providing developers with a higher level of automation and freedom to access public information.

## Installation

You can install INEGIExplorer via pip:

```bash
pip install inegi_explorer
```

## Usage

The object explorer mimics the organization at the [official site](https://www.inegi.org.mx/app/indicadores/)


```python
from inegi_explorer import Explorer

# Create an instance of Explorer
explorer = Explorer()

#print the explorer
print(explorer)
```

The output shows the subjects you can access:
```output
Tema: Origen - Estados Unidos Mexicanos (T-0700-0--1)
    Tema: Banco de Indicadores - Estados Unidos Mexicanos (T-0700-0000-6)
    Tema: Banco de Indicadores Económicos (BIE) - Estados Unidos Mexicanos (T-0700-999999999999-0)
    Tema: Indicadores por Entidad Federativa - Estados Unidos Mexicanos (T-0700-0000-7)
    Tema: Indicadores de Bienestar por Entidad Federativa - Estados Unidos Mexicanos (T-0700-0000-8)
```

You can handle this subjects as items from a list.

```python
# the first element is the "Banco de Indicadores"
bi = explorer[0]
print(bi)
```
```output
Tema: Banco de Indicadores - Estados Unidos Mexicanos (T-0700-0000-6) 
    Tema: Demografía y Sociedad - Estados Unidos Mexicanos (T-0700-379-6)
    Tema: Economía y Sectores Productivos - Estados Unidos Mexicanos (T-0700-380-6)
    Tema: Geografía y Medio Ambiente - Estados Unidos Mexicanos (T-0700-381-6)
    Tema: Gobierno, Seguridad y Justicia - Estados Unidos Mexicanos (T-0700-382-6)
```

When you get to an indicator you can use the fetch method to download the data as a pd.Series.
```python
indicator = bi[0][0][0][0]
print(indicator)
```

```output
Indicador: Razón entre niñas y niños en la enseñanza primaria - Estados Unidos Mexicanos (I-0700-6300000246-6) 
    Indicador: Razón entre niñas y niños en la enseñanza primaria - Estados Unidos Mexicanos - Aguascalientes (I-07000001-6300000246-6)
    Indicador: Razón entre niñas y niños en la enseñanza primaria - Estados Unidos Mexicanos - Baja California (I-07000002-6300000246-6)
    Indicador: Razón entre niñas y niños en la enseñanza primaria - Estados Unidos Mexicanos - Baja California Sur (I-07000003-6300000246-6)
    Indicador: Razón entre niñas y niños en la enseñanza primaria - Estados Unidos Mexicanos - Campeche (I-07000004-6300000246-6)
    Indicador: Razón entre niñas y niños en la enseñanza primaria - Estados Unidos Mexicanos - Coahuila de Zaragoza (I-07000005-6300000246-6)
    Indicador: Razón entre niñas y niños en la enseñanza primaria - Estados Unidos Mexicanos - Colima (I-07000006-6300000246-6)
    Indicador: Razón entre niñas y niños en la enseñanza primaria - Estados Unidos Mexicanos - Chiapas (I-07000007-6300000246-6)
    Indicador: Razón entre niñas y niños en la enseñanza primaria - Estados Unidos Mexicanos - Chihuahua (I-07000008-6300000246-6)
    Indicador: Razón entre niñas y niños en la enseñanza primaria - Estados Unidos Mexicanos - Ciudad de México (I-07000009-6300000246-6)
    Indicador: Razón entre niñas y niños en la enseñanza primaria - Estados Unidos Mexicanos - Durango (I-07000010-6300000246-6)
    Indicador: Razón entre niñas y niños en la enseñanza primaria - Estados Unidos Mexicanos - Guanajuato (I-07000011-6300000246-6)
    Indicador: Razón entre niñas y niños en la enseñanza primaria - Estados Unidos Mexicanos - Guerrero (I-07000012-6300000246-6)
    Indicador: Razón entre niñas y niños en la enseñanza primaria - Estados Unidos Mexicanos - Hidalgo (I-07000013-6300000246-6)
    Indicador: Razón entre niñas y niños en la enseñanza primaria - Estados Unidos Mexicanos - Jalisco (I-07000014-6300000246-6)
    Indicador: Razón entre niñas y niños en la enseñanza primaria - Estados Unidos Mexicanos - México (I-07000015-6300000246-6)
    Indicador: Razón entre niñas y niños en la enseñanza primaria - Estados Unidos Mexicanos - Michoacán de Ocampo (I-07000016-6300000246-6)
    Indicador: Razón entre niñas y niños en la enseñanza primaria - Estados Unidos Mexicanos - Morelos (I-07000017-6300000246-6)
    Indicador: Razón entre niñas y niños en la enseñanza primaria - Estados Unidos Mexicanos - Nayarit (I-07000018-6300000246-6)
    Indicador: Razón entre niñas y niños en la enseñanza primaria - Estados Unidos Mexicanos - Nuevo León (I-07000019-6300000246-6)
    Indicador: Razón entre niñas y niños en la enseñanza primaria - Estados Unidos Mexicanos - Oaxaca (I-07000020-6300000246-6)
    Indicador: Razón entre niñas y niños en la enseñanza primaria - Estados Unidos Mexicanos - Puebla (I-07000021-6300000246-6)
    Indicador: Razón entre niñas y niños en la enseñanza primaria - Estados Unidos Mexicanos - Querétaro (I-07000022-6300000246-6)
    Indicador: Razón entre niñas y niños en la enseñanza primaria - Estados Unidos Mexicanos - Quintana Roo (I-07000023-6300000246-6)
    Indicador: Razón entre niñas y niños en la enseñanza primaria - Estados Unidos Mexicanos - San Luis Potosí (I-07000024-6300000246-6)
    Indicador: Razón entre niñas y niños en la enseñanza primaria - Estados Unidos Mexicanos - Sinaloa (I-07000025-6300000246-6)
    Indicador: Razón entre niñas y niños en la enseñanza primaria - Estados Unidos Mexicanos - Sonora (I-07000026-6300000246-6)
    Indicador: Razón entre niñas y niños en la enseñanza primaria - Estados Unidos Mexicanos - Tabasco (I-07000027-6300000246-6)
    Indicador: Razón entre niñas y niños en la enseñanza primaria - Estados Unidos Mexicanos - Tamaulipas (I-07000028-6300000246-6)
    Indicador: Razón entre niñas y niños en la enseñanza primaria - Estados Unidos Mexicanos - Tlaxcala (I-07000029-6300000246-6)
    Indicador: Razón entre niñas y niños en la enseñanza primaria - Estados Unidos Mexicanos - Veracruz de Ignacio de la Llave (I-07000030-6300000246-6)
    Indicador: Razón entre niñas y niños en la enseñanza primaria - Estados Unidos Mexicanos - Yucatán (I-07000031-6300000246-6)
    Indicador: Razón entre niñas y niños en la enseñanza primaria - Estados Unidos Mexicanos - Zacatecas (I-07000032-6300000246-6)
```
```python
indicator.fetch()
```
This will return a pd.Series with only the data from the indicator 'Indicador: Razón entre niñas y niños en la enseñanza primaria - Estados Unidos Mexicanos (I-0700-6300000246-6)'. To get the aggregates you can pass the param app as True.

```python
indicator.fetch(agg=True)
```

This will return all indicators shown for each state in a pd.DataFrame.

You can also fetch subjects and get a pd.DataFrame with all the indicators inside each of the subjects.

Once you have identified a subject or indicator that you want to use frequently, you can save its ID and build it using the class method `from_id`.

```python
from inegi_explorer import Explorer

indicator = Explorer.from_id("I-07000032-6300000246-6")
indicator.fetch()
```

To get the id of a subject or indicator you can use the attribute id
```python
print(indicator.id)
```
```output
I-07000032-6300000246-6
```

For more detailed usage examples and advanced features, please refer to the [demo.ipynb](demo.ipynb) notebook.

## Contributing

Thank you for your interest in contributing to INEGIExplorer! We welcome contributions from the community to help improve our project.

### Reporting Bugs or Issues

If you encounter a bug or issue with the project, please open a GitHub issue in our issue tracker. Be sure to include relevant details such as steps to reproduce, expected behavior, and actual behavior.

### Requesting Features

If you have an idea for a new feature or improvement, please open a GitHub issue in our issue tracker and label it as a feature request. We appreciate your feedback and will consider it for future development.

### Submitting Pull Requests

We welcome pull requests from the community to help fix bugs, implement new features, or improve existing code. Before submitting a pull request, please:

- Fork the repository and create your own branch from the `main` branch.
- Make sure your code follows our code formatting and style conventions.
- Write clear and concise commit messages.
- Test your changes thoroughly.

Once your changes are ready, submit a pull request to the `main` branch of the main repository. Be sure to include a detailed description of your changes and reference any related GitHub issues.


## License

This project is licensed under the [MIT License](LICENSE). By contributing to this project, you agree to abide by the terms of this license.

