# FinansChecker

Aplicación web que detecta transacciones sospechosas con inteligencia artificial. Cada transacción recibe un puntaje de riesgo de 0 a 100 calculado por un modelo Random Forest y unas reglas de negocio, y queda **aprobada** (0 a 39), **en revisión** (40 a 69) o **sospechosa** (70 a 100), con los motivos de la decisión.

> Todos los datos son simulados con fines académicos. La app no se conecta a bancos ni mueve dinero real.

Proyecto desarrollado con Spec-Driven Development. La especificación completa está en [docs/](docs/):
[CONSTITUTION.md](docs/CONSTITUTION.md), [PROJECT_SPEC.md](docs/PROJECT_SPEC.md), [PLAN.md](docs/PLAN.md) y [TASKS.md](docs/TASKS.md).

## Tecnologías

| Parte | Tecnologías |
|---|---|
| Backend | Python 3.13, FastAPI, Uvicorn, Pydantic, psycopg |
| IA | scikit-learn (Random Forest) más reglas de negocio |
| Datos de prueba | Faker |
| Frontend | React 19, TypeScript, Vite, React Router, Axios, Recharts |
| Base de datos | PostgreSQL en Neon |
| Despliegue | Render (Web Service y Static Site) |

## Estructura

```text
FinansChecker/
├── docs/                 Documentos SDD
├── database/schema.sql   Tablas de la base de datos
├── backend/
│   ├── app/
│   │   ├── domain/          Entidades, variables y reglas de riesgo (sin dependencias externas)
│   │   ├── application/     Casos de uso e interfaces
│   │   ├── infrastructure/  psycopg, carga del modelo y configuración
│   │   └── api/             Rutas de FastAPI y esquemas de Pydantic
│   ├── ml/model.joblib      Modelo entrenado
│   ├── scripts/             Generador de datos, entrenamiento y carga en la base
│   └── tests/               Pruebas con pytest
├── frontend/src/
│   ├── app/                 Rutas y punto de entrada
│   ├── features/            dashboard, transactions, simulator, alerts
│   └── shared/              Cliente de la API, componentes, tipos y utilidades
└── render.yaml           Configuración de despliegue en Render
```

## Cómo funciona el motor de riesgo

1. Se calculan variables comparando la transacción con el historial del usuario: monto frente a su promedio, hora, cantidad de transacciones en 10 minutos, cuenta destino nueva y ciudad distinta a la habitual.
2. El modelo Random Forest da una probabilidad de fraude (0 a 100).
3. Las reglas de RN-03 suman puntos y generan los motivos:

| Regla | Puntos |
|---|---|
| Monto mayor a 5 veces el promedio del usuario | 40 |
| 3 o más transacciones en 10 minutos | 35 |
| Transacción entre las 12:00 a. m. y las 5:00 a. m. | 25 |
| Cuenta destino nueva para el usuario | 20 |
| Ciudad distinta a la habitual | 15 |

4. Puntaje final = 50% modelo + 50% reglas, limitado a 100. Si queda en revisión o sospechosa se crea una alerta con al menos un motivo.

Con los datos simulados, el modelo combinado con las reglas detecta el 94% de los fraudes con un 94% de precisión.

## Ejecutar en local

### Requisitos

- Python 3.11 o superior
- Node.js 22 o superior
- Una base de datos en [Neon](https://neon.tech) (plan gratuito)

### 1. Base de datos

En el panel de Neon abre el **SQL Editor**, pega el contenido de `database/schema.sql` y ejecútalo. Copia la cadena de conexión desde el botón **Connect**.

### 2. Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Copia `backend/.env.example` como `backend/.env` y pega tu cadena de conexión en `DATABASE_URL`.

```bash
python -m scripts.train_model   # entrena el modelo (opcional, ya viene entrenado)
python -m scripts.seed_data     # carga 30 usuarios y unas 1.300 transacciones de prueba
uvicorn app.main:app --reload   # API en http://localhost:8000
```

La documentación de la API queda en http://localhost:8000/docs.

> El script `seed_data` borra los datos anteriores, sirve para reiniciar la demo.

### 3. Frontend

```bash
cd frontend
npm install
```

Copia `frontend/.env.example` como `frontend/.env` y ejecuta:

```bash
npm run dev   # http://localhost:5173
```

### 4. Pruebas

```bash
cd backend
pip install -r requirements-dev.txt
python -m pytest
```

Para incluir la prueba de integración (CP-01 y CP-02 contra una base real con datos cargados), define `TEST_DATABASE_URL` con una base de pruebas, no con la de producción.

## Despliegue en Render

El archivo `render.yaml` define los dos servicios. En Render: **New** → **Blueprint** → elige el repositorio.

Variables que hay que llenar en el panel:

| Servicio | Variable | Valor |
|---|---|---|
| finanschecker-api | `DATABASE_URL` | Cadena de conexión de Neon |
| finanschecker-api | `CORS_ORIGINS` | URL del frontend, ej. `https://finanschecker-web.onrender.com` |
| finanschecker-web | `VITE_API_URL` | URL del backend, ej. `https://finanschecker-api.onrender.com` |

Si `VITE_API_URL` cambia, hay que volver a desplegar el frontend, porque Vite la incluye al compilar.

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/health` | Estado de la API y del modelo |
| GET | `/users` | Usuarios de prueba con su promedio y cuenta habitual |
| POST | `/transactions` | Evalúa y guarda una transacción (RF-01, RF-02, RF-03) |
| GET | `/transactions?status=` | Lista de transacciones, filtro opcional por estado (RF-04) |
| GET | `/transactions/{id}` | Detalle con los motivos (RF-05) |
| GET | `/alerts` | Alertas en revisión o sospechosas |
| GET | `/stats` | Resumen para el dashboard (RF-06) |

## Para la presentación

- Abre la app 1 o 2 minutos antes: el backend gratuito de Render se apaga tras 15 minutos sin uso y tarda hasta un minuto en arrancar. Mientras tanto la app muestra "Conectando con el servidor…".
- En el Simulador, los botones **Transacción normal** y **Transacción sospechosa** llenan el formulario con los casos CP-01 y CP-02.

## Limitaciones conocidas

- Los datos y el modelo son simulados, el puntaje no garantiza detectar fraudes reales.
- El modelo se entrena con los mismos patrones que genera el simulador de datos.
- El campo opcional de fecha y hora del simulador existe para poder probar casos como CP-02 (3:00 a. m.) a cualquier hora.

## Equipo

- Juan Camilo Valle Calle (DanteX786): backend e IA, aprobación de pull requests
- Daniel Stiven Cardona Espinal: base de datos, datos de prueba y despliegue
- Jordy Alejandro Ramírez Sierra: frontend
