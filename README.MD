# GitHub Trending CLI

https://roadmap.sh/projects/github-trending-cli

Herramienta de línea de comandos (CLI) que consulta la API REST de GitHub para mostrar los repositorios más populares dentro de un rango de tiempo determinado (día, semana, mes o año).

Como GitHub no expone un endpoint oficial de "trending", esta herramienta lo simula utilizando la [Search API](https://docs.github.com/en/rest/search/search#search-repositories): busca repositorios creados dentro del rango solicitado, ordenados por cantidad de estrellas.

## Características

- Filtrado por rango de tiempo: `day`, `week`, `month`, `year`.
- Límite configurable de resultados a mostrar.
- Salida en texto plano, legible desde cualquier terminal.
- Manejo robusto de errores (fallas de red, errores de la API, argumentos inválidos).
- No requiere autenticación (usa endpoints públicos de la API de GitHub).

## Requisitos

- Python 3.10 o superior

## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/tu-usuario/github-trending-cli.git
   cd github-trending-cli
   ```

2. (Recomendado) Crea y activa un entorno virtual:

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux / macOS
   source venv/bin/activate
   ```

3. Instala las dependencias:

   ```bash
   python -m pip install -r requirements.txt
   ```

   Si además quieres correr los tests o contribuir al desarrollo:

   ```bash
   python -m pip install -r requirements-dev.txt
   ```

## Uso

```bash
python cli.py --duration <day|week|month|year> --limit <número>
```

### Argumentos

| Argumento    | Descripción                                              | Valores permitidos             | Default |
| ------------ | -------------------------------------------------------- | ------------------------------ | ------- |
| `--duration` | Rango de tiempo a considerar para buscar repos recientes | `day`, `week`, `month`, `year` | `week`  |
| `--limit`    | Cantidad máxima de repositorios a mostrar                | Entero positivo                | `10`    |

### Ejemplo de uso

```bash
python cli.py --duration month --limit 20
```

### Ejemplo de salida

```
NavierStokesAndEuler
  Estrellas: 1889
  Lenguaje: Lean
  Descripción: Lean certificates accompanying Navier-Stokes and Euler results
  URL: https://github.com/openai/NavierStokesAndEuler

Edge0
  Estrellas: 1695
  Lenguaje: Python
  Descripción: Sin descripción
  URL: https://github.com/Edge0-AI/Edge0
```

## Manejo de errores

- Si `--duration` recibe un valor no permitido, la herramienta lo rechaza antes de hacer cualquier llamada a la API.
- Si `--limit` es menor o igual a cero, se informa el error sin realizar la búsqueda.
- Si ocurre un problema de red o la API de GitHub responde con un error (por ejemplo, límite de peticiones excedido), se muestra un mensaje claro en lugar de un traceback.

## Ejecutar los tests

```bash
python -m pytest tests/ -v
```

## Arquitectura del proyecto

El proyecto está organizado en capas siguiendo principios SOLID, con inyección de dependencias para facilitar el testing:

```
├── cli.py                        # Punto de entrada: parseo de argumentos y composition root
├── config.py                     # Constantes y validación de duration (Enum DurationOption)
├── exceptions.py                 # Jerarquía de excepciones del dominio
├── models/
│   └── repository.py             # Entidad Repository
├── services/
│   ├── github_client.py          # IGithubClient + GithubClient (acceso HTTP a la API)
│   └── trending_service.py       # Orquestación: valida, consulta, parsea, ordena y limita
├── formatters/
│   ├── base.py                   # IFormatter
│   └── console_formatter.py      # Presentación en texto plano
└── tests/                        # Tests unitarios por módulo
```

Cada capa depende de abstracciones (`IGithubClient`, `IFormatter`) en lugar de implementaciones concretas, lo que permite testear la lógica de negocio sin realizar llamadas de red reales y facilita extender la herramienta (por ejemplo, agregar un formato de salida en JSON) sin modificar el código existente.

## Licencia

MIT
