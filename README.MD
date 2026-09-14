https://roadmap.sh/projects/github-trending-cli

models/repository.py
Dataclass Repository con: name, description, stars, language, url
Manejar campos que pueden venir None desde la API (ej. description, language)
Test: creación del objeto, valores por defecto/None 2. exceptions.py
InvalidDurationError (duration fuera de day/week/month/year)
GithubAPIError (fallas de red, status code de error, rate limit)
Test: que las excepciones lleven mensaje claro 3. config.py
Constante BASE_URL de la API
Mapeo DURATION_TO_DAYS = {day: 1, week: 7, month: 30, year: 365}
Función validate_duration(duration) que lance InvalidDurationError si no es válido
Test: mapeo correcto, validación con valores válidos e inválidos 4. services/github_client.py
Interfaz IGithubClient (ABC) con método search_repositories(query, sort, order)
Implementación GithubClient usando requests.Session inyectada
Manejo de errores HTTP (timeout, status != 200, rate limit 403) → lanza GithubAPIError
Test: con mocks/fakes de requests, sin golpear la red real 5. services/trending_service.py
Clase TrendingService que recibe IGithubClient inyectado
Método get_trending(duration, limit):
Valida duration (usa config.validate_duration)
Calcula fecha de corte según duration
Arma el query created:>fecha
Llama al client, parsea JSON → lista de Repository
Ordena por stars descendente
Aplica limit
Test: con un FakeGithubClient, casos de duration inválida, limit mayor al total de resultados, respuesta vacía 6. formatters/console_formatter.py
Interfaz IFormatter (ABC) con método format(repositories)
Implementación ConsoleFormatter: texto legible con nombre, descripción, stars, lenguaje
Manejar lista vacía (mensaje "no se encontraron repos")
Test: input/output puro, sin mocks necesarios 7. cli.py
argparse con --duration (default week) y --limit (default 10, tipo int)
Validar que --limit sea positivo
Composition root: instancia requests.Session, GithubClient, TrendingService, ConsoleFormatter (inyección real)
Captura excepciones (InvalidDurationError, GithubAPIError) y las muestra como errores amigables, no tracebacks
if **name** == "**main**": como entry point 8. Empaquetado y documentación
requirements.txt (o pyproject.toml) con requests
README.md: instalación, uso, ejemplos (trending-repos --duration month --limit 20)
(Opcional) hacerlo instalable como comando (entry_points en setup.py/pyproject.toml) 9. Repaso final de calidad
Revisar cada clase cumple SRP (una razón para cambiar)
Revisar que TrendingService dependa de IGithubClient, no de GithubClient concreto (DIP)
Cobertura de tests razonable en cada capa
Manejo de errores de extremo a extremo probado manualmente (sin internet, duration inválida, límite raro)
