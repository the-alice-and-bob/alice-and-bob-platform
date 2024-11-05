# Despliegue y documentación

## Variables de entorno

| Variable              | Descripción                                       | Valor por defecto                       | Valor actual |
|-----------------------|---------------------------------------------------|-----------------------------------------|--------------|
| `CELERY_BROKER_URL`   | URL de la base de datos Redis                     | `redis://localhost:6379`                | `<secret>`   |
| `NOTION_TOKEN`        | Token de autenticación de Notion                  | `<secret>`                              | `<secret>`   |
| `NOTION_DATABASE_ID`  | ID de la base de datos de Notion                  | `<secret>`                              | `<secret>`   |
| `ANTHROPIC_API_KEY`   | API Key de la API de Anthropic                    | `<secret>`                              | `<secret>`   |
| `SUMMARY_MIN_WORDS`   | Número mínimo de palabras para generar un resumen | `100`                                   | `100`        |
| `SUMMARY_MAX_WORDS`   | Número máximo de palabras para generar un resumen | `150`                                   | `250`        |
| `LLM_ENGINE`          | Servicio de LLM a utilizar                        | `anthropic` (anthropic, openai, ollama) | `anthropic`  |
| `FORCE_PROCESS_FEEDS` | Fuerza el procesamiento de los feeds              | `false`                                 | `true`       |
| `PUSHOVER_TOKEN`      | Token de autenticación de Pushover                | `<secret>`                              | `<secret>`   |
| `PUSHOVER_USER`       | Usuario de Pushover                               | `<secret>`                              | `<secret>`   |
| `SENTRY_DSN`          | DSN de Sentry                                     | `<secret>`                              | `<secret>`   |
| `URL_TOKEN`           | Token de URL                                      | `<secret>`                              | `<secret>`   |
| `DISABLE_LLM`         | Deshabilita el uso de LLM                         | `false`                                 | `true`       |
