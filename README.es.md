# RSI Copiloto

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

[![RSI Copiloto](guia/assets/banner.jpg)](https://inematds.github.io/rsi-copiloto/guia/es/)

Asistente local con IA, memoria, tareas y ciclos de mejora supervisada para personas particulares, profesionales independientes y pequeñas empresas. **Proyecto separado de la [investigación RSI (en portugués)](https://inematds.github.io/rsi/guia/)**.

**[Probar demostración](https://inematds.github.io/rsi-copiloto/app/)** · **[Guía de uso](https://inematds.github.io/rsi-copiloto/guia/es/)**

La demostración usa ejemplos programados y almacenamiento del navegador. La versión local llama a una IA real mediante OpenRouter y guarda datos en SQLite. La interfaz está en portugués; la guía y el README están en PT/EN/ES.

## Ejecutar

Python 3.11+ y Git. Sin dependencias Python adicionales.

```bash
git clone https://github.com/inematds/rsi-copiloto.git
cd rsi-copiloto
python3 -m rsi.server
```

Abre **http://127.0.0.1:8765/app/**. El servidor atiende solo en loopback; uso individual.

La credencial `OPENROUTER_API_KEY` se lee del entorno o del archivo indicado por `RSI_ENV_FILE`. En el equipo del autor, también busca en `~/projetos/openpcbotv2/.env` y `~/projetos/wifi/.env`. No copies claves a este repositorio.

```bash
RSI_ENV_FILE="$HOME/.config/minhas-credenciais.env" python3 -m rsi.server
```

El archivo indicado debe contener `OPENROUTER_API_KEY`. Configuración opcional: `RSI_MODEL` (predeterminado `openai/gpt-5.4-nano`), `RSI_DAILY_CALLS` (50 intentos/día UTC), `RSI_DB`, `--port`, `--db`, `--no-scheduler`. Hasta 2.400 tokens de salida por llamada. El límite de llamadas no equivale a un tope financiero.

## Qué funciona

- Tres espacios: personal, autónomo y pequeña empresa; nueve rutinas listas para usar.
- Entregas con información faltante, fuentes de memoria, próximos pasos, tokens y coste informado.
- Tareas, conocimiento por perfil y contexto recuperado por palabras.
- Comentarios, propuesta de instrucción, comparación actual/candidata en tres casos, revisión humana, activación y reversión.
- Rutinas diarias opcionales con el servidor abierto; un fallo pausa la rutina.
- Historial, copia de seguridad JSON/restauración, tareas CSV y calendario `.ics`.

El ciclo mejora instrucciones y procesos, **no los pesos del modelo**. Las comprobaciones son estructurales, no prueban veracidad ni mejoras en el negocio. La instrucción activa se aplica a los tres espacios. La IA no envía mensajes, mueve dinero ni ejecuta comandos. Las integraciones externas y los múltiples usuarios son etapas futuras.

## Datos

SQLite en `~/.local/share/rsi-copiloto/state.sqlite3`, fuera del directorio publicado. La API recibe la solicitud, el perfil, la instrucción y hasta cinco memorias relevantes. La copia de seguridad contiene datos de los tres espacios: mantenla privada. La importación pausa las recurrencias y exige una nueva evaluación antes de activar instrucciones; se conserva el límite diario de uso local.

## Verificar

```bash
python3 -m unittest discover -s tests -v
# Opcional: prueba real de pago, hasta ocho llamadas, solo datos ficticios.
python3 -m scripts.smoke_live
```

[Plan (en portugués)](docs/PLANO-IMPLEMENTACAO.md) · [Operación (en portugués)](docs/OPERACAO.md) · [Validación (en portugués)](docs/VALIDACAO.md) · [Registro de cambios (en portugués)](CHANGELOG.md)

Proyecto abierto y gratuito de investigación y educación de [INEMA.CLUB](https://inema.club).

## Misión y LOOP-R: dos ciclos conectados.

Usted define la misión. La IA propone de una a cinco etapas. Revise el plan y pulse “Aprovar plano e executar primeira etapa” (aprobar el plan y ejecutar la primera etapa). El resultado aparece en la misma misión para su evaluación.

Pulse “Aprovar e executar próxima etapa” (aprobar y ejecutar la siguiente etapa) para continuar utilizando el resultado aprobado y su evaluación. “Corrigir esta etapa” rehace el trabajo actual. Puede pausar, recargar y retomar. Guardar en la memoria es opcional: el historial de la misión ya se conserva.

**Ejecutar → Medir → Criticar → Proponer → Probar → Validar → Promover → Repetir**

Al finalizar, consulte su nota media y la cantidad de correcciones. Pulse “Iniciar LOOP-R desta missão” (iniciar el LOOP-R de esta misión). La IA recibe esas evidencias, analiza las fallas y propone una instrucción candidata. En el laboratorio, compare las versiones, lea las respuestas, registre su evaluación y después promueva.

Las nuevas misiones usan la instrucción promovida. Las ya iniciadas conservan su versión original. Es una mejora supervisada de instrucciones y procedimientos, sin entrenar los pesos del modelo. Los tres casos generales evalúan estructura; no demuestran mejora de calidad ni resultados financieros.

La demostración pública utiliza ejemplos programados. El flujo completo funciona; use la versión local para producir el contenido real de su misión con IA.
