# PROJECT_SPEC.md — FinansChecker

> **Etapa SDD:** 2. Especificación  
> **Propósito:** definir qué construir, para quién, con qué requisitos y cómo comprobarlo.

| Campo | Valor |
|---|---|
| Proyecto | FinansChecker |
| Versión | 1.0 |
| Responsables | Juan Camilo Valle Calle, Jordy Alejandro Ramírez Sierra, Daniel Stiven Cardona Espinal |
| Fecha | [2026-11-25] |
| Estado | Borrador |

## 1. Descripción general

[FinansChecker es una app para detectar fraudes financieros y/o movimientos sospechosos, resuelve el problema de muchas personas cuyas cuentas bancarias no les avisa o alerta de movimientos sospechiosos o transacciones muy inusuales, permitiendo tener mas control de el dinero que entra y sale de nuestro bolsillo digital, esta app esta dirijida a cualquier usuario que necesite controlar sus cuentas y movimientos para tener mayor seguridad.] 


## 2. Objetivos

### Objetivo general

[Desarrollar FinansChecker, una aplicación web que use inteligencia artificial para detectar transacciones sospechosas y alertar al usuario, dándole más control y seguridad sobre el dinero que entra y sale de sus cuentas digitales]

### Objetivos específicos

1. Entrenar un modelo de IA que asigne un puntaje de riesgo a cada transacción y la clasifique como aprobada, en revisión o sospechosa.
2. Construir una API que registre las transacciones, las evalúe y guarde los resultados y las alertas en la base de datos.
3. Diseñar una interfaz que muestre las transacciones, las alertas con el motivo de cada una y un resumen visual de los movimientos.
4. Desplegar la aplicación en la nube para que funcione desde cualquier navegador.

## 3. Usuarios y necesidades

- **Usuarios:** [Cualquier usuario que necesite manejar sus cuentas]
- **Problema:** [Problemas de seguridad en sus cuentas bancarias, ya que la mayoría no te avisa o simplemente te cobra o entrega dinero]
- **Beneficio esperado:** [La seguridad del dinero, ya que al reportar lo más crítico, podremos ver si en algún momento se hizo un movimiento inusual y tomar medidas para no perder dinero]

## 4. Alcance

## 4. Alcance

### Incluye

- Simulación de transacciones desde la app (transferencias, pagos, retiros y compras en línea).
- Evaluación automática del riesgo de cada transacción con IA y reglas.
- Alertas con el motivo por el que una transacción se considera sospechosa.
- Lista de transacciones con su estado (aprobada, en revisión, sospechosa).
- Dashboard con resumen y gráficas de los movimientos.
- Generación de datos de prueba y entrenamiento del modelo.
- Despliegue en Render con base de datos en Neon.

### No incluye

- Conexión con bancos o cuentas reales.
- Registro de usuarios e inicio de sesión (se usan usuarios de prueba).
- Pagos o movimientos de dinero reales.
- Notificaciones por correo, SMS o push.
- Aplicación móvil nativa.
- Reentrenamiento del modelo desde la interfaz.

## 5. Requisitos funcionales

### RF-01 — Simular transacción

- **Descripción:** el sistema permite crear una transacción de prueba desde un formulario.
- **Entrada:** usuario, tipo de transacción, monto en COP, cuenta destino, ciudad y canal.
- **Salida:** la transacción queda guardada y se muestra su resultado de riesgo.

### RF-02 — Evaluar riesgo

- **Descripción:** el sistema calcula un puntaje de riesgo (0–100) con el modelo de IA y las reglas, y asigna un estado.
- **Entrada:** datos de la transacción y el historial del usuario.
- **Salida:** puntaje y estado: aprobada (0–39), en revisión (40–69) o sospechosa (70–100).

### RF-03 — Generar alerta

- **Descripción:** el sistema crea una alerta cuando una transacción queda en revisión o sospechosa.
- **Entrada:** resultado de la evaluación de riesgo.
- **Salida:** alerta guardada con el nivel de riesgo y los motivos (ej.: "monto 8 veces mayor a su promedio").

### RF-04 — Listar transacciones

- **Descripción:** el sistema muestra las transacciones ordenadas de la más reciente a la más antigua, con su estado en colores.
- **Entrada:** filtro opcional por estado.
- **Salida:** tabla con fecha, usuario, tipo, monto, puntaje y estado.

### RF-05 — Ver detalle de alerta

- **Descripción:** el sistema muestra la información completa de una transacción marcada y por qué se marcó.
- **Entrada:** selección de una alerta o transacción.
- **Salida:** datos de la transacción, puntaje de riesgo y lista de motivos.

### RF-06 — Mostrar dashboard

- **Descripción:** el sistema presenta un resumen general de la actividad.
- **Entrada:** acceso a la página principal.
- **Salida:** total de transacciones, porcentaje sospechoso, monto total, gráfica de transacciones por día y por estado.

### RF-07 — Cargar datos de prueba

- **Descripción:** un script genera usuarios y transacciones simuladas (incluidos casos de fraude) y entrena el modelo.
- **Entrada:** ejecución del script por el equipo.
- **Salida:** datos cargados en Neon y modelo entrenado guardado en el proyecto.

## 6. Requisitos no funcionales

- **RNF-01 (Rendimiento):** [la evaluación de una transacción (RF-02) responde en menos de 2 segundos con el backend ya activo en Render el primer acceso después de 15 minutos sin uso puede tardar hasta 1 minuto mientras el servidor arranca]
- **RNF-02 (Seguridad):** [ninguna clave ni cadena de conexión aparece en el repositorio, la API rechaza datos inválidos con un mensaje claro y solo acepta peticiones del dominio del frontend y la conexión con Neon usa SSL.]
- **RNF-03 (Usabilidad):** [el usuario puede simular una transacción y ver su resultado en menos de 3 pasos, los estados se distinguen por color y texto: verde: aprobada, amarillo: en revisión, rojo: sospechosa y la app muestra mensajes de carga y de error comprensibles]
- **RNF-04 (Mantenibilidad):** [el código sigue las convenciones de la sección 4, Clean Architecture en el backend y Feature First en el frontend, la API está documentada en /docs y el README explica cómo ejecutar y desplegar el proyecto]
- **RNF-05 (Compatibilidad):** [la app funciona en las versiones actuales de Chrome, Edge y Firefox, y se adapta a pantallas de computador y celular]

## 7. Tecnologías

| Tecnología | Función | Obligatoria |
|---|---|---|
| **Lenguajes** | | |
| Python | Backend, generación de datos y modelo de IA | Sí |
| TypeScript | Frontend | Sí |
| SQL | Crear tablas y consultar datos en PostgreSQL | Sí |
| **Bibliotecas/Frameworks** | | |
| Uvicorn | Servidor que ejecuta la API | Sí |
| Pydantic | Validación de datos de la API | Sí |
| psycopg | Conexión de Python con PostgreSQL | Sí |
| scikit-learn | Modelo de IA (Random Forest) para el puntaje de riesgo | Sí |
| Faker | Generación de usuarios y transacciones de prueba | Sí |
| React Router | Navegación entre vistas | Sí |
| Axios | Comunicación entre el frontend y la API | Sí |
| Recharts | Gráficas del dashboard | Sí |
| pytest | Pruebas automáticas del backend | No |
| FastAPI | API REST del backend | Sí |
| React | Interfaz web del frontend | Sí |
| **Herramientas** | | |
| PostgreSQL (Neon) | Base de datos en la nube | Sí |
| Vite | Crear, ejecutar y compilar el frontend | Sí |
| Git + GitHub | Control de versiones y repositorio | Sí |
| Render | Despliegue del backend y del frontend | Sí |

## 8. Arquitectura propuesta

- **Estilo arquitectónico:** cliente-servidor. Un frontend web (SPA en React) consume una API REST (FastAPI) que se conecta a una base de datos PostgreSQL en la nube. El backend sigue Clean Architecture y el frontend sigue Feature First.
- **Motivo:** separar la interfaz, la lógica de detección y los datos permite que cada integrante trabaje en una parte sin afectar a las demás, mantiene la lógica de IA protegida en el backend y facilita desplegar el frontend y el backend por separado en Render.
- **Componentes principales:** [Frontend (React + TypeScript): dashboard, transacciones, simulador y alertas.
API REST (FastAPI): recibe, valida y responde las peticiones.
Motor de riesgo: modelo de IA (scikit-learn) más reglas de negocio.
Base de datos (PostgreSQL en Neon): usuarios, transacciones y alertas.
Scripts: generación de datos de prueba y entrenamiento del modelo]

> La arquitectura técnica detallada se desarrolla en `PLAN.md`.

## 9. Estructura inicial de carpetas

```text
FinansChecker/
├── CONSTITUTION.md
├── PROJECT_SPEC.md
├── PLAN.md
├── TASKS.md
├── README.md
├── .gitignore
├── backend/
│   ├── app/
│   │   ├── domain/
│   │   ├── application/
│   │   ├── infrastructure/
│   │   └── api/
│   ├── scripts/
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── features/
│   │   └── shared/
│   ├── package.json
│   └── .env.example
└── database/
    └── schema.sql
```

## 10. Módulos

### Módulo 1 — Transacciones

- **Responsabilidad:** registrar, validar y consultar las transacciones simuladas.
- **Funciones:** formulario del simulador, validación de datos, guardado en la base de datos, listado con filtro por estado.
- **Requisitos relacionados:** RF-01, RF-04

### Módulo 2 — Motor de riesgo

- **Responsabilidad:** evaluar cada transacción y decidir su nivel de riesgo.
- **Funciones:** cálculo de variables (monto vs. promedio, hora, frecuencia, destino nuevo), predicción con el modelo de IA, aplicación de reglas, asignación de puntaje (0–100) y estado.
- **Requisitos relacionados:** RF-02

### Módulo 3 — Alertas

- **Responsabilidad:** crear y mostrar las alertas de transacciones en revisión o sospechosas.
- **Funciones:** generación de la alerta con sus motivos, listado de alertas, vista de detalle.
- **Requisitos relacionados:** RF-03, RF-05

### Módulo 4 — Dashboard

- **Responsabilidad:** mostrar un resumen visual de la actividad.
- **Funciones:** cálculo de estadísticas (totales, porcentaje sospechoso, monto total), gráficas por día y por estado.
- **Requisitos relacionados:** RF-06

### Módulo 5 — Datos y entrenamiento

- **Responsabilidad:** preparar los datos de prueba y el modelo de IA.
- **Funciones:** generación de usuarios y transacciones con Faker (incluidos casos de fraude), carga en Neon, entrenamiento y guardado del modelo, cálculo de métricas (precisión, recall).
- **Requisitos relacionados:** RF-07

## 11. Entidades y datos principales

| Entidad o dato | Atributo | Tipo | Propósito |
|---|---|---|---|
| **User** | `id` | SERIAL (PK) | Identificador único del usuario |
| | `name` | VARCHAR(100) | Nombre ficticio generado con Faker |
| | `city` | VARCHAR(60) | Ciudad habitual, para detectar movimientos desde otras ciudades |
| | `created_at` | TIMESTAMP | Fecha de creación |
| **Transaction** | `id` | SERIAL (PK) | Identificador único de la transacción |
| | `user_id` | INTEGER (FK → User) | Usuario que hace la transacción |
| | `type` | VARCHAR(20) | `transfer`, `payment`, `withdrawal` u `online_purchase` |
| | `amount` | NUMERIC(14,2) | Monto en COP |
| | `destination_account` | VARCHAR(30) | Cuenta destino simulada, para detectar destinos nuevos |
| | `city` | VARCHAR(60) | Ciudad desde donde se hace |
| | `channel` | VARCHAR(20) | `app`, `web` o `atm` |
| | `created_at` | TIMESTAMP | Fecha y hora, para detectar horarios inusuales y frecuencia |
| | `risk_score` | SMALLINT | Puntaje de riesgo de 0 a 100 |
| | `status` | VARCHAR(20) | `approved`, `review` o `suspicious` |
| **Alert** | `id` | SERIAL (PK) | Identificador único de la alerta |
| | `transaction_id` | INTEGER (FK → Transaction) | Transacción que generó la alerta |
| | `level` | VARCHAR(20) | `review` o `suspicious` |
| | `reasons` | TEXT[] | Motivos de la alerta (ej.: "monto 8 veces mayor a su promedio") |
| | `created_at` | TIMESTAMP | Fecha de creación |

## 12. Gestión de estado

- **Estados que cambian:** [en el frontend, los datos cargados (transacciones, alertas y estadísticas), el filtro por estado, el formulario del simulador, el resultado de la última simulación, la alerta seleccionada y los estados de carga y error, en el backend, el risk_score y el status que recibe cada transacción al ser evaluada y las alertas que genera]
- **Cómo se administrarán:** [en el frontend, con useState y useEffect dentro de hooks propios de cada feature (useTransactions, useAlerts, useDashboard, useSimulator), volviendo a pedir los datos a la API después de cada simulación; en el backend, la API no guarda estado entre peticiones, todo lo persistente vive en PostgreSQL (Neon) y el modelo de IA se carga en memoria una sola vez al iniciar el servidor]
- **Si no aplica:** no se usa una librería de estado global (Redux, Zustand) ni Context, porque cada feature maneja sus propios datos y la aplicación es pequeña.

## 13. Interfaz de usuario

## 13. Interfaz de usuario

- **Tipo:** Web (adaptable a computador y celular).
- **Pantalla o vista 1 — Dashboard:** [tarjetas con total de transacciones, porcentaje sospechoso y monto total, gráfica de transacciones por día y gráfica por estado, acceso rápido a las últimas alertas]
- **Pantalla o vista 2 — Transacciones:** [tabla con fecha, usuario, tipo, monto, puntaje y estado en colores, filtro por estado, al hacer clic en una fila se abre su detalle]
- **Pantalla o vista 3 — Simulador:** [formulario con usuario, tipo, monto, cuenta destino, ciudad y canal, botón "Simular transacción",muestra el resultado con puntaje, estado y motivos]
- **Pantalla o vista 4 — Alertas:** [lista de transacciones en revisión o sospechosas, vista de detalle con los datos de la transacción, el puntaje y los motivos de la alerta]
- **Accesibilidad básica:** [los estados se indican con color y texto, nunca solo con color, buen contraste entre texto y fondo, todos los campos del formulario tienen etiqueta, los errores se muestran junto al campo correspondient y se puede navegar con teclado]

## 14. Navegación y flujo

1. [El usuario abre el Simulador, llena el formulario y presiona "Simular transacción"]
2. [El frontend revisa que los campos estén completos y la API valida los datos con Pydantic, si algo es inválido, se muestra el error junto al campo]
3. [El backend calcula las variables, el modelo de IA y las reglas asignan el puntaje y el estado, se guarda la transacción en Neon y, si corresponde, se crea la alerta]
4. [La app muestra el resultado con su color, puntaje y motivos, y la transacción aparece en las vistas de Transacciones, Alertas y Dashboard]

**Ejemplo FinansChecker:** simular transacción → evaluar riesgo con IA → mostrar estado y motivos → ver la alerta en el dashboard.

## 15. Persistencia de datos

- **Datos que deben guardarse:** [usuarios de prueba, transacciones con su risk_score y status, alertas con sus motivos, y el modelo de IA entrenado]
- **Ubicación:** usuarios, transacciones y alertas en la base de datos PostgreSQL de Neon; el modelo entrenado en un archivo .joblib dentro de el backend.
- **Duración:** [durante todo el desarrollo, los datos se pueden reiniciar ejecutando el script de datos de prueba]
- **Protección:** [solo el backend accede a la base de datos, con conexión SSL, credenciales en variables de entorno y consultas con parámetros, no se guardan datos reales]

## 16. Reglas de negocio

- **RN-01:** [toda transacción se evalúa antes de guardarse y recibe un puntaje de 0 a 100 que combina el modelo de IA y las reglas, ese puntaje no se modifica después]
- **RN-02:** [el estado depende del puntaje (0–39 `approved`, 40–69 `review`, 70–100 `suspicious`) y solo se crea una alerta, con al menos un motivo, cuando el estado es review o suspicious]
- **RN-03:** [el monto debe estar entre $1 y $50.000.000 COP, y son motivos de riesgo un monto mayor a 5 veces el promedio del usuario, 3 o más transacciones en 10 minutos, horario entre 12:00 a. m. y 5:00 a. m., cuenta destino nueva y ciudad distinta a la habitual]

## 17. Restricciones negativas

El sistema **NO** debe:

- [Guardar una transacción sin evaluarla, calcular el riesgo en el frontend ni mostrar una alerta sin sus motivos]
- [Mostrar al usuario detalles técnicos de los errores ni bloquear, mover o retener dinero real]

## 18. Manejo de errores

| Situación | Comportamiento esperado |
|---|---|
| [Datos inválidos en el simulador, monto vacío, negativo o mayor al máximo, o usuario inexistente] | [La API rechaza la petición y el frontend muestra el error junto al campo, por ejemplo: "El monto debe estar entre $1 y $50.000.000"] |
| [Falla del servidor, de la base de datos o del modelo de IA, o backend dormido en Render] | [El frontend muestra "Conectando con el servidor…" o "No pudimos procesar la transacción, intenta de nuevo" con un botón para reintentar, sin mostrar detalles técnicos] |

## 19. Criterios de aceptación

- **CA-01:** [Al simular una transacción válida, en menos de 2 segundos se muestra su puntaje (0–100), su estado con el color correspondiente y, si aplica, sus motivos]
- **CA-02:** [Una transacción que cumple condiciones de fraude de RN-03 (por ejemplo, monto 8 veces mayor al promedio a las 3:00 a. m.) queda en `review` o `suspicious` y aparece en Alertas con al menos un motivo]
- **CA-03:** [El dashboard muestra los mismos totales que la base de datos y se actualiza después de cada simulación]

**Ejemplo FinansChecker:** si el motor de riesgo devuelve un puntaje de 85, la transacción se muestra en rojo como suspicious, con sus motivos y una alerta nueva en el dashboard, esto no implica garantizar la detección de todos los fraudes reales
## 20. Casos de prueba

| ID | Requisito | Escenario | Resultado esperado |
|---|---|---|---|
| CP-01 | RF-01 | [Simular una transferencia de $150.000 COP con todos los campos completos] | [La transacción se guarda y se muestra su resultado] |
| CP-02 | RF-02 | [Simular un monto 8 veces mayor al promedio del usuario, a las 3:00 a. m., a una cuenta nueva] | [Puntaje entre 70 y 100, estado suspicious en rojo] |

## 21. Instrucciones para la IA

1. Leer `CONSTITUTION.md` y este documento.
2. Respetar el alcance y las tecnologías autorizadas.
3. No inventar funcionalidades ni dependencias.
4. Preguntar ante contradicciones.
5. Desarrollar tareas de `TASKS.md` una por una.
6. Explicar cambios y relacionarlos con requisitos.
7. Reportar pruebas ejecutadas y pendientes por separado.

# 22. Orden recomendado de implementación

1. [Preparación: crear el repositorio con las ramas main y develop, la estructura de carpetas, la base de datos en Neon con schema.sql, los archivos .env.example y los datos de prueba con Faker]
2. [Módulo principal: construir el motor de riesgo en el backend (entrenamiento del modelo con scikit-learn, reglas de negocio y cálculo del puntaje), y la API con FastAPI para transacciones, alertas y estadísticas]
3. [Interfaz e integración: desarrollar en React con TypeScript las vistas de Dashboard, Transacciones, Simulador y Alertas, conectarlas a la API con Axios y desplegar el backend y el frontend en Render]
4. [Pruebas: verificar los casos de prueba y los criterios de aceptación, tanto en local como en la versión desplegada]
5. [Documentación: completar el README con los pasos para ejecutar y desplegar el proyecto, revisar la documentación de la API en /docs y actualizar TASKS.md con lo terminado]

## 23. Resultado esperado

[FinansChecker funcionando en una URL pública de Render: el usuario abre el dashboard y ve el resumen de los movimientos con gráficas, en el simulador crea una transacción y, en menos de 2 segundos, ve su puntaje de riesgo y su estado en verde, amarillo o rojo, con los motivos cuando es sospechosa, la transacción queda guardada en Neon y aparece en las vistas de Transacciones, Alertas y Dashboard]

## 24. Definición de terminado

- [ ] Requisitos obligatorios implementados.
- [ ] Restricciones respetadas.
- [ ] Criterios de aceptación verificados.
- [ ] Casos de prueba documentados.
- [ ] Errores y limitaciones conocidos registrados.
- [ ] Código y documentación disponibles.

## 25. Registro de cambios

| Versión | Fecha | Modificación | Responsable |
|---|---|---|---|
| 1.0 | [Fecha] | Especificación inicial | [Nombre] |