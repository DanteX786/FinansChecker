# TASKS.md — FinansChecker

> **Etapa SDD:** planificación de tareas e implementación  
> **Propósito:** dividir el plan en tareas pequeñas, ordenadas y verificables

| Campo | Valor |
|---|---|
| Proyecto | FinansChecker |
| Versión | 1.0 |
| Responsables | Juan Camilo Valle Calle, Jordy Alejandro Ramírez Sierra, Daniel Stiven Cardona Espinal |
| Fecha | [2026-11-25] |

## 1. Objetivo

[Organizar la construcción de FinansChecker en tareas pequeñas y verificables, desde la preparación del repositorio y la base de datos hasta el despliegue en Render y la presentación, siguiendo lo definido en CONSTITUTION.md, PROJECT_SPEC.md y PLAN.md]

## 2. Reglas de ejecución

1. Leer CONSTITUTION.md, PROJECT_SPEC.md y PLAN.md
2. Seguir el orden y las dependencias entre tareas
3. Implementar una tarea verificable a la vez
4. No agregar funcionalidades no especificadas
5. Ejecutar y registrar las pruebas disponibles
6. Marcar una tarea completa solo con evidencia

## 3. Estados

- **Pendiente:** aún no iniciada
- **En progreso:** en desarrollo
- **Bloqueada:** no puede continuar
- **En revisión:** requiere validación
- **Completada:** cumple el criterio y tiene evidencia

## 4. Fase 1 — Preparación

### T01 — [Preparar repositorio y estructura]

- **Objetivo:** [Dejar el repositorio listo con las ramas de Git Flow y la estructura de carpetas definida en PLAN.md]
- **Requisitos relacionados:** [RNF-02, RNF-04]
- **Archivos afectados:** [docs/, backend/, frontend/, database/, .gitignore, README.md, backend/.env.example, frontend/.env.example]
- **Dependencias:** [Ninguna]
- **Responsable:** [Juan Camilo Valle Calle]
- **Estado:** Pendiente

**Actividades:**

- [ ] [Crear las ramas develop, feature/backend-ai, feature/frontend y feature/database-deploy]
- [ ] [Crear la estructura de carpetas, el .gitignore con .env incluido y los archivos .env.example sin valores reales]

**Criterio de finalización:** [El repositorio tiene las ramas creadas, la estructura completa y ningún archivo .env subido]

**Evidencia:** [Captura de las ramas en GitHub y commit inicial]

### T02 — [Crear base de datos y datos de prueba]

- **Objetivo:** [Crear las tablas en Neon y cargar usuarios y transacciones simuladas con casos de fraude]
- **Requisitos:** [RF-07, RNF-02]
- **Dependencias:** [T01]
- **Responsable:** [Daniel Stiven Cardona Espinal]
- **Estado:** Pendiente

- [ ] [Crear el proyecto en Neon, ejecutar database/schema.sql en su editor SQL y generar los datos con backend/scripts/seed_data.py]
- [ ] [Verificar en el editor SQL de Neon que las tablas users, transactions y alerts tengan datos]

**Criterio de finalización:** [Las tres tablas existen en Neon y tienen usuarios y transacciones de prueba, incluidas transacciones con patrones de fraude]

**Evidencia:** [Captura de la consulta en el editor SQL de Neon]

## 5. Fase 2 — Desarrollo del núcleo

### T03 — [Motor de riesgo con IA]

- **Objetivo:** [Entrenar el modelo y construir el motor que asigna puntaje, estado y motivos a cada transacción]
- **Módulo:** [Motor de riesgo, Datos y entrenamiento]
- **Requisito:** [RF-02, RF-07]
- **Dependencias:** [T01, T02]
- **Estado:** Pendiente

- [ ] Crear archivos necesarios
- [ ] Implementar funcionalidad
- [ ] Manejar errores previstos
- [ ] Ejecutar prueba correspondiente

**Criterio de finalización:** [El script train_model.py guarda model.joblib y muestra precisión y recall, y el motor devuelve un puntaje entre 0 y 100 con su estado según RN-02 y sus motivos según RN-03]

**Evidencia:** [Métricas del entrenamiento en consola y resultado de CP-02]

### T04 — [API de transacciones, alertas y estadísticas]

- **Objetivo:** [Construir los endpoints de FastAPI que registran, evalúan y consultan transacciones, alertas y estadísticas]
- **Requisito:** [RF-01, RF-03, RF-04, RF-05, RF-06]
- **Dependencias:** [T03]
- **Estado:** Pendiente

- [ ] [Implementar los casos de uso y los repositorios con psycopg y consultas con parámetros]
- [ ] [Crear los endpoints GET /health, GET /users, POST /transactions, GET /transactions, GET /transactions/{id}, GET /alerts y GET /stats con validación de Pydantic]
- [ ] [Probar los endpoints en /docs con datos válidos e inválidos]

**Criterio de finalización:** [Al enviar una transacción a POST /transactions se guarda en Neon con su puntaje y estado, se crea la alerta cuando corresponde y los datos inválidos se rechazan con error 422]

**Evidencia:** [Capturas de /docs y resultado de CP-01]

## 6. Fase 3 — Interfaz e integración

### T05 — [Implementar interfaz]

- **Objetivo:** [Crear en React con TypeScript las vistas de Dashboard, Transacciones, Simulador y Alertas]
- **Requisito:** [RF-01, RF-04, RF-05, RF-06, RNF-03, RNF-05]
- **Estado:** Pendiente

- [ ] Crear controles de la interfaz
- [ ] Conectar los módulos
- [ ] Mostrar errores comprensibles
- [ ] Probar el recorrido del usuario

**Criterio de finalización:** [Las cuatro vistas funcionan con React Router, muestran los estados en verde, amarillo y rojo con texto, y se ven bien en computador y celular]

**Evidencia:** [Capturas de las cuatro vistas]

### T06 — [Integración y despliegue]

- **Objetivo:** [Conectar el frontend con la API y publicar la aplicación en Render]
- **Dependencias:** [T03, T04, T05]
- **Estado:** Pendiente

- [ ] Integrar componentes
- [ ] Verificar entradas y salidas
- [ ] Registrar defectos de integración

**Criterio de finalización:** [El backend funciona como Web Service y el frontend como Static Site en Render, con las variables de entorno configuradas, y una transacción simulada desde la URL pública se guarda en Neon y aparece en todas las vistas]

## 7. Fase 4 — Pruebas

### T07 — Ejecutar pruebas

- **Objetivo:** validar los criterios de aceptación
- **Estado:** Pendiente

- [ ] Ejecutar casos normales
- [ ] Ejecutar casos de error
- [ ] Registrar resultados observados
- [ ] Comparar con los criterios de aceptación
- [ ] Corregir defectos prioritarios
- [ ] Repetir las pruebas afectadas

**Criterio de finalización:** [CP-01 y CP-02 aprobados, CA-01, CA-02 y CA-03 cumplidos en local y en la versión desplegada, y sin errores críticos abiertos]

**Evidencia:** [Matriz de pruebas con resultados y capturas]

## 8. Fase 5 — Documentación y entrega

### T08 — Documentación

- [ ] Completar README.md
- [ ] Documentar instalación y ejecución
- [ ] Explicar funcionalidades
- [ ] Registrar limitaciones y errores conocidos

**Estado:** Pendiente

### T09 — Entrega final

- [ ] Revisar todos los criterios de aceptación
- [ ] Comprobar restricciones
- [ ] Organizar el repositorio
- [ ] Preparar demostración
- [ ] Entregar evidencias

**Estado:** Pendiente

## 9. Registro de errores

| ID | Error | Tarea relacionada | Estado |
|---|---|---|---|
| BUG-01 | [Sin errores registrados] | [No aplica] | Pendiente |

## 10. Resumen de avance

| Tarea | Responsable | Estado | Evidencia |
|---|---|---|---|
| T01 | [Juan Camilo Valle Calle] | Pendiente | [Enlace] |
| T02 | [Daniel Stiven Cardona Espinal] | Pendiente | [Enlace] |
| T03 | [Juan Camilo Valle Calle] | Pendiente | [Enlace] |
| T04 | [Juan Camilo Valle Calle] | Pendiente | [Enlace] |
| T05 | [Jordy Alejandro Ramírez Sierra] | Pendiente | [Enlace] |
| T06 | [Daniel Stiven Cardona Espinal] | Pendiente | [Enlace] |
| T07 | [Equipo] | Pendiente | [Enlace] |
| T08 | [Equipo] | Pendiente | [Enlace] |
| T09 | [Juan Camilo Valle Calle] | Pendiente | [Enlace] |

## 11. Checklist final

- [ ] Tareas obligatorias terminadas y comprobadas
- [ ] Requisitos implementados
- [ ] Restricciones respetadas
- [ ] Pruebas documentadas
- [ ] Errores críticos resueltos
- [ ] Código y documentación entregados

## 12. Cierre

- **Estado del proyecto:** [Pendiente]
- **Tareas completadas:** [0]
- **Pruebas ejecutadas:** [0]
- **Errores pendientes:** [0]
- **Observaciones:** [Se actualiza al terminar el proyecto]