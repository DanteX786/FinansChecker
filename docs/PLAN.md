# PLAN.md — FinansChecker

> **Etapa SDD:** 4. Planificación  
> **Propósito:** explicar cómo se implementarán los requisitos aprobados.

| Campo | Valor |
|---|---|
| Proyecto | FinansChecker |
| Versión | 1.0 |
| Responsables | Juan Camilo Valle Calle, Jordy Alejandro Ramírez Sierra, Daniel Stiven Cardona Espinal |
| Fecha | [2026-11-25] |
| Estado | Borrador |

## 1. Objetivo del plan

[Construir FinansChecker como una aplicación web cliente-servidor, un frontend en React con TypeScript que consume una API REST en FastAPI, la cual evalúa cada transacción con un modelo de IA (scikit-learn) más reglas de negocio y guarda los resultados en PostgreSQL (Neon), El resultado es una app desplegada en Render que permite simular transacciones, ver su nivel de riesgo, revisar alertas y consultar un dashboard]

## 2. Documentos de referencia

- `CONSTITUTION.md` — versión [1.0]
- `PROJECT_SPEC.md` — versión [1.0]
- [Decisiones aprobadas en la clarificación, stack reducido sin XGBoost, pandas ni SQLAlchemy, TypeScript en el frontend, despliegue obligatorio en Render, base de datos en Neon administrada desde su editor SQL, Git Flow con main, develop y 3 ramas feature/, commits en inglés, DanteX786 aprueba los cambios]

## 3. Tecnologías y dependencias

| Tecnología | Uso | Versión acordada |
|---|---|---|
| [Python] | [Backend, datos de prueba y modelo de IA] | [3.12] |
| [TypeScript] | [Frontend] | [7.0] |
| [SQL (PostgreSQL)] | [Tablas y consultas] | [PostgreSQL 17 (Neon)] |
| [FastAPI] | [API REST] | [0.165] |
| [Uvicorn] | [Servidor de la API] | [0.54] |
| [Pydantic] | [Validación de datos] | [2.14] |
| [psycopg] | [Conexión Python–PostgreSQL] | [3.3] |
| [scikit-learn] | [Modelo Random Forest] | [1.9] |
| [Faker] | [Datos de prueba] | [40.63] |
| [React] | [Interfaz web] | [19.3] |
| [React Router] | [Navegación entre vistas] | [7.18] |
| [Axios] | [Peticiones HTTP a la API] | [1.21] |
| [Recharts] | [Gráficas del dashboard] | [3.11] |
| [Vite] | [Crear, ejecutar y compilar el frontend] | [8.3] |
| [Node.js] | [Entorno para ejecutar Vite y npm] | [22 LTS] |

- **Dependencias adicionales:** [`python-dotenv` (1.2) para leer variables de entorno en local; `joblib` (1.6, incluido con scikit-learn) para guardar y cargar el modelo; `pytest` (9.2) para pruebas automáticas, opcional.]
- **Justificación:** [`python-dotenv` evita escribir credenciales en el código; `joblib` permite que la API use el modelo sin volver a entrenarlo; `pytest` permite comprobar los casos de prueba con un solo comando. Las versiones se fijan en `requirements.txt` y `package.json`]

## 4. Arquitectura técnica

- **Arquitectura:** [Cliente-servidor con API REST, Backend con Clean Architecture (capas domain, application, infrastructure, api) y frontend con Feature First (features/ y shared/)]
- **Justificación:** [Separa la interfaz, la lógica de detección y los datos, protege la lógica de IA en el backend, permite que cada integrante trabaje en su parte y que frontend y backend se desplieguen por separado en Render]
- **Componentes:** [Frontend React (Static Site en Render), API FastAPI (Web Service en Render), motor de riesgo (modelo de IA + reglas),base de datos PostgreSQL en Neon, scripts de datos de prueba y entrenamiento]
- **Comunicación entre componentes:** [El frontend llama a la API por HTTPS con Axios, enviando y recibiendo JSON. La API solo acepta peticiones del dominio del frontend (CORS), la API se conecta a Neon con psycopg usando `DATABASE_URL` con SSL, el modelo se carga en memoria al iniciar la API, los endpoints serán GET /health, GET /users, POST /transactions, GET /transactions?status=, GET /transactions/{id}, GET /alerts, GET /stats]

## 5. Estructura de carpetas

```text
FinansChecker/
├── docs/
│   ├── CONSTITUTION.md
│   ├── PROJECT_SPEC.md
│   ├── PLAN.md
│   └── TASKS.md
├── backend/
│   ├── app/
│   │   ├── domain/            # Entidades (Transaction, Alert, RiskResult) y reglas de riesgo
│   │   ├── application/       # Casos de uso e interfaces de repositorio
│   │   ├── infrastructure/    # Repositorios con psycopg, carga del modelo, configuración
│   │   ├── api/               # Rutas de FastAPI y esquemas de Pydantic
│   │   └── main.py
│   ├── ml/
│   │   └── model.joblib       # Modelo entrenado
│   ├── scripts/
│   │   ├── seed_data.py       # Genera y carga datos de prueba
│   │   └── train_model.py     # Entrena y guarda el modelo
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── app/               # App.tsx, rutas y main.tsx
│   │   ├── features/
│   │   │   ├── dashboard/
│   │   │   ├── transactions/
│   │   │   ├── simulator/
│   │   │   └── alerts/
│   │   └── shared/            # Cliente Axios, componentes comunes, utilidades y tipos
│   ├── package.json
│   └── .env.example
├── database/
│   └── schema.sql
├── .gitignore
└── README.md
```

[Cambios respecto a PROJECT_SPEC.md: los documentos SDD se mueven a docs/ para dejar la raíz limpia; se agrega backend/ml/ para el modelo entrenado y se detallan los archivos de scripts/ y las carpetas de features/, el src/ se reemplaza por backend/ y frontend/ porque son dos proyectos que Render despliega por separado.]

## 6. Módulos y responsabilidades

### Módulo 1 — Transacciones

- **Responsabilidad:** [Registrar, validar y consultar transacciones simuladas]
- **Entradas:** [Usuario, tipo, monto, cuenta destino, ciudad y canal desde el simulador; filtro por estado desde la tabla]
- **Procesamiento:** [Validar con Pydantic, enviar al motor de riesgo, guardar con psycopg y consultar ordenado por fecha]
- **Salidas:** [Transacción guardada con puntaje y estado; listado filtrado]
- **Requisitos relacionados:** [RF-01, RF-04]

### Módulo 2 — Motor de riesgo

- **Responsabilidad:** [Calcular el puntaje de riesgo y el estado de cada transacción]
- **Entradas:** [Datos de la transacción e historial del usuario]
- **Procesamiento:** [Calcular variables (monto vs. promedio, hora, frecuencia en 10 minutos, destino nuevo, ciudad distinta), obtener la probabilidad del modelo, sumar el ajuste de reglas, limitar a 100 y asignar estado según RN-02]
- **Salidas:** [risk_score (0–100), status y lista de motivos]
- **Requisitos relacionados:** [RF-02]

### Módulo 3 — Alertas

- **Responsabilidad:** [Crear y consultar alertas de transacciones en revisión o sospechosas]
- **Entradas:** [Resultado del motor de riesgo; selección de una alerta]
- **Procesamiento:** [Crear la alerta con nivel y motivos cuando aplique; consultar alertas y su transacción]
- **Salidas:** [Alerta guardada; listado y detalle de alertas]
- **Requisitos relacionados:** [RF-03, RF-05]

### Módulo 4 — Dashboard

- **Responsabilidad:** [Entregar estadísticas de la actividad]
- **Entradas:** [Petición a GET /stats]
- **Procesamiento:** [Consultas SQL de totales, porcentaje sospechoso, monto total, transacciones por día y por estado]
- **Salidas:** [Tarjetas de resumen y gráficas en Recharts]
- **Requisitos relacionados:** [RF-06]

### Módulo 5 — Datos y entrenamiento

- **Responsabilidad:** [Preparar los datos de prueba y el modelo de IA]
- **Entradas:** [Ejecución de seed_data.py y train_model.py]
- **Procesamiento:** [Generar usuarios y transacciones con Faker, incluidos patrones de fraude, cargarlos en Neon, entrenar el Random Forest y calcular precisión y recall]
- **Salidas:** [Datos en Neon, model.joblib y métricas en consola]
- **Requisitos relacionados:** [RF-07]

## 7. Flujo técnico

1. [Recepción de entrada: el simulador envía POST /transactions con Axios]
2. [Validación: Pydantic valida los campos y la API confirma que el usuario exista]
3. [Procesamiento: el caso de uso consulta el historial del usuario y el motor de riesgo calcula puntaje, estado y motivos]
4. [Integración: el repositorio guarda la transacción en Neon y si el estado es review o suspicious, crea la alerta]
5. [Presentación o almacenamiento: la API devuelve el resultado en JSON y el frontend lo muestra con su color, las vistas de Transacciones, Alertas y Dashboard se actualizan]

**Ejemplo FinansChecker:** llenar formulario → validar → evaluar riesgo → guardar → crear alerta → mostrar resultado → actualizar dashboard

## 8. Diseño de datos

| Dato | Tipo | Origen | Destino |
|---|---|---|---|
| [Datos de la transacción (usuario, tipo, monto, destino, ciudad, canal)] | [JSON → INTEGER, VARCHAR, NUMERIC] | [Formulario del simulador] | [Tabla transactions] |
| [Historial del usuario] | [Filas de transactions] | [Neon] | [Motor de riesgo] |
| [risk_score, status] | [SMALLINT, VARCHAR] | [Motor de riesgo] | [Tabla transactions y respuesta JSON] |
| [Motivos de la alerta] | [TEXT[]] | [Reglas del motor de riesgo] | [Tabla alerts y vista de detalle] |
| [Estadísticas] | [JSON] | [Consultas SQL] | [Dashboard] |
| [Modelo entrenado] | [Archivo .joblib] | [train_model.py] | [Memoria de la API] |

- **Persistencia:** [PostgreSQL en Neon con las tablas users, transactions y alerts definidas en database/schema.sql, el modelo en backend/ml/model.joblib]
- **Validaciones:** [Monto entre $1 y $50.000.000 COP, tipo en transfer, payment, withdrawal, online_purchase, canal en app, web, atm, usuario existente, campos obligatorios, consultas SQL con parámetros]

## 9. Diseño de interfaz

- **Tipo:** [Web, adaptable a computador y celular.]
- **Pantallas:** [Dashboard, Transacciones, Simulador y Alertas (con vista de detalle)]
- **Controles principales:** [Menú de navegación, formulario del simulador con botón "Simular transacción", filtro por estado, tabla de transacciones, tarjetas de resumen y gráficas]
- **Interacciones:** [El usuario navega con el menú, en el simulador envía una transacción y ve el resultado, en Transacciones filtra y abre el detalle, en Alertas revisa los motivos, el Dashboard se actualiza con cada simulación]

## 10. Fases de implementación

### Fase 1 — Preparación

- **Objetivo:** [Dejar listo el entorno de trabajo del equipo]
- **Actividades:** [Crear repositorio y ramas, estructura de carpetas, proyecto Neon y schema.sql, .env.example, script de datos de prueba]
- **Entregable:** [Repositorio organizado y base de datos con datos de prueba]

### Fase 2 — Núcleo funcional

- **Objetivo:** [Tener el backend evaluando transacciones]
- **Actividades:** [Entrenar el modelo, implementar reglas y motor de riesgo, casos de uso, repositorios con psycopg; endpoints de FastAPI]
- **Entregable:** [API funcionando y documentada en /docs]

### Fase 3 — Interfaz e integración

- **Objetivo:** [Conectar la interfaz con la API y publicar la app]
- **Actividades:** [Crear las vistas en React con TypeScript, cliente Axios; gráficas con Recharts, despliegue del backend y del frontend en Render]
- **Entregable:** [App funcionando en una URL pública]

### Fase 4 — Validación y entrega

- **Objetivo:** [Confirmar que se cumple la especificación]
- **Actividades:** [Ejecutar casos de prueba y criterios de aceptación; corregir errores, completar README, merge de develop a main]
- **Entregable:** [Versión 1.0 en main, desplegada y documentada]

## 11. Estrategia de pruebas

- **Unitarias:** [Reglas de riesgo, asignación de estado por puntaje, límite de 100 y validación de montos]
- **Integración:** [API + base de datos: POST /transactions guarda la transacción y crea la alerta cuando corresponde]
- **Funcionales:** [Simular una transacción normal y una sospechosa desde la interfaz y verificar el resultado en todas las vistas]
- **Errores:** [Monto negativo, monto mayor al máximo, usuario inexistente y backend sin conexión]

| Requisito | Prueba | Evidencia |
|---|---|---|
| RF-01 | [CP-01: simular una transferencia válida de $150.000 COP] | [Captura del resultado y fila en transactions] |
| RF-02 | [CP-02: monto 8 veces mayor al promedio, 3:00 a. m, cuenta nueva] | [Captura con estado suspicious y puntaje ≥ 70] |

## 12. Seguridad y errores

- **Riesgos:** [Filtración de la cadena de conexión, datos inválidos o maliciosos, inyección SQL, exposición de errores internos]
- **Validaciones:** [Pydantic en todos los endpoints, consultas con parámetros, CORS limitado al dominio del frontend; .env en .gitignore]
- **Respuesta ante fallos:** [La API responde 422 para datos inválidos, 404 para recursos inexistentes, 500 o 503 con mensaje general para fallos internos, el frontend muestra mensajes amigables, estados de carga y botón de reintentar]

## 13. Riesgos técnicos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| [Backend dormido en Render durante la demo] | Medio | [Abrir la app 1–2 minutos antes y mostrar "Conectando con el servidor…"] |
| [Modelo poco preciso por usar datos sintéticos] | Medio | [Combinar el modelo con reglas claras y generar patrones de fraude bien definidos] |
| [Filtración de credenciales] | Alto | [Variables de entorno, .gitignore y cambio inmediato de claves si se filtran] |
| [Conflictos al integrar ramas] | Medio | [Feature First y Clean Architecture para separar el trabajo, integración frecuente en develop] |
| [Error de CORS entre Render frontend y backend] | Bajo | [Configurar la URL del frontend como variable de entorno del backend] |

## 14. Control de versiones

- **Repositorio:** [https://github.com/DanteX786/FinansChecker.git]
- **Rama principal:** [main]
- **Estrategia de integración:** [develop es la rama de trabajo. Hay 3 ramas temporales (feature/backend-ai, feature/frontend, feature/database-deploy) que salen de develop y vuelven a ella por pull request, al cerrar cada fase se hace merge de develop a main]
- **Reglas para commits y revisiones:** [Commits en inglés, cortos, con formato type: description, ej. feat: add transaction simulator, todo cambio entra por pull request aprobado por Juan Camilo Valle Calle (DanteX786)]

## 15. Criterios para iniciar la implementación

- [ ] Constitución aprobada.
- [ ] Especificación revisada.
- [ ] Preguntas críticas de clarificación resueltas.
- [ ] Arquitectura y dependencias aprobadas.
- [ ] Responsabilidades de módulos definidas.
- [ ] Estrategia de pruebas definida.

## 16. Decisiones técnicas

| Fecha | Decisión | Justificación | Responsable |
|---|---|---|---|
| [2026-11-25] | [Usar Random Forest de scikit-learn en lugar de XGBoost] | [Suficiente para demostrar la idea y más fácil de explicar] | [Equipo] |
| [2026-11-25] | [Usar psycopg con SQL directo en lugar de SQLAlchemy] | [Más simple y deja visible el SQL] | [Equipo] |
| [2026-11-25] | [Usar datos simulados con Faker] | [No se usan datos reales y no depende de descargas externas] | [Equipo] |
| [2026-11-25] | [Desplegar backend como Web Service y frontend como Static Site en Render] | [Ambos gratuitos, el Static Site no se duerme] | [Equipo] |
| [2026-11-25] | [Estado local con hooks por feature, sin Redux ni Context] | [La app es pequeña y cada feature maneja sus datos] | [Equipo] |

## 17. Resultado esperado

[Un repositorio con backend/ (Clean Architecture), frontend/ (Feature First), database/schema.sql y la documentación SDD en docs/, la API en Render evalúa cada transacción en menos de 2 segundos con el modelo de IA y las reglas, guarda el resultado en Neon y crea alertas con motivos, el frontend en Render muestra el dashboard, las transacciones, el simulador y las alertas, con estados en verde, amarillo y rojo]