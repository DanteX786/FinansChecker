# CONSTITUTION.md — FinansChecker

> **Etapa SDD:** 1. Constitución  
> **Propósito:** definir reglas y restricciones para el equipo y los agentes de IA.

| Campo | Valor |
|---|---|
| Proyecto | FinansChecker |
| Versión | 1.0 |
| responsables | Juan Camilo Valle Calle, Jordy Alejandro Ramírez sierra, Daniel Stiven Cardona Espinal |
| Fecha | [2026-11-25] |
| Estado | Borrador |

## 1. Propósito

Está constitución está planeada y dirigida para el público general para detectar fraudes de finanzas en las cuentas bancarias usando la IA como motor, ya sea para controlar movimientos o posibles cobros no autorizados 	

## 2. Tecnologías obligatorias
| Tecnología | Uso | Justificación |
|---|---|---|

**Lenguaje**
| Python| Backend y motor de la IA | Es un lenguaje universal y versátil para la IA |
| TypeScript | Frontend con react | Lenguaje muy versátil de trabajar y de diseño |
| SQL | Crear la base de datos en neon, consultas de transacciones, estadísticas y alertas| Bases de datos fáciles y de dominio universal, aparte de ser gratuito y rapido |

**Biblioteca/framework**
| FastApi | Api para tomar las transacciones, evaluarlas con IA y devolver el resultado | Facilidad para el despliegue y sinergia con Python|
| Uvicorn | Servidor para ejecutar la API | Es el servidor recomendado para FastAPI|
| Pydantic | Validaciones de datos en la API | viene Integrado con FastApi  y valida datos|
|psycopg| Conectar la base de datos con python| Conector predeterminado de PostgreSQL |
| scikit-learn| Modelo de IA que calcula el riesgo de fraude de cada transacción| Es la biblioteca de machine learnign más usada y sencilla de entender |
| Faker | Generar usuarios y transacciones de prueba con casos de fraude | Datos muy realistas sin usar datos reales de verdad |
| React | Interfaz web | Es el framework más usado y trabaja con componentes reutilizables || 
| React router| Navegador entre las vistas del aplicativo | Organiza la app por paginas sin recargar la web |
| Axios | Enlace entre frontend y API |Simplifica peticiones de HTTP |
| Recharts | Grafias del dashboard | Poco código y se ve profesional |

**Herramienta**
| PostgreSQL (Neon)| Base de datos en la nube | Base de datos gratuita sencilla y consistente con python |
| Vite |Crear, correr y compilar el React |Arranca muy rápido y recarga los datos en tiempo real|
| Git + GitHub | Control de versiones, ramas y repositorio del proyecto | Guarda el historial y Render despliega directamente desde GitHub | 
| Render | Despliegue del aplicativo | Tiene plan gratuito y publica la app con una URL pública |

## 3. Principios de desarrollo
- **Organización modular:** el proyecto se divide en módulos con una sola función cada uno, en el backend rutas de la API, motor de riesgo (IA), acceso a la base de datos y generador de datos de prueba, en el frontend van páginas, componentes reutilizables, servicio de conexión con la API y tipos de TypeScript.
- **Separación de responsabilidades:** cada capa hace solo su parte, el frontend muestra información y envía datos, la API valida y coordina, el motor de riesgo decide si una transacción es sospechosa y la capa de base de datos solo guarda y consulta.
- **Manejo de errores:** los datos inválidos se rechazan con un mensaje claro (validación con Pydantic), los errores del servidor o de la base de datos devuelven un mensaje general, sin mostrar detalles internos, en el frontend nunca se queda en blanco, muestra estados de carga y mensajes amigables cuando algo falla o el servidor está despertando.
- **Pruebas y documentación:** antes de entregar se prueban los casos principales, una transacción normal se aprueba, una sospechosa se marca como fraude y un dato inválido se rechaza, la API queda documentada automáticamente en `/docs` y el proyecto incluye un README con los pasos para ejecutarlo y desplegarlo.

## 4. Convenciones de programación
- **Archivos:** Python en snake_case.py, componentes de React en PascalCase.tsx, hooks en useCamelCase.ts, servicios y utilidades en camelCase.ts, tablas SQL en snake_case
- **Variables y funciones:** snake_case en Python, camelCase en TypeScript y UPPER_SNAKE_CASE para constantes y nombres en inglés.
- **Clases y módulos:** Clases, interfaces, tipos y componentes en PascalCase, módulos de Python en snake_case, un componente por archivo.
- **Comentarios:** en español, solo cuando expliquen el *por qué*, docstrings en los casos de uso y en las reglas del motor de riesgo, sin código comentado.
- **Estructura:** Criterios para separar responsabilidades:
- Backend con Clean Architecture: el dominio y los casos de uso no dependen de FastAPI, psycopg ni scikit-learn, esas tecnologías quedan en las capas externas.
- Frontend con Feature First: cada funcionalidad tiene su carpeta propia, lo compartido va en shared y una feature no importa archivos de otra.
- La lógica de negocio nunca va en las rutas de la API ni en los componentes de React.

## 5. Restricciones no negociables

El proyecto **NO** debe:
- Usar datos bancarios reales ni conectarse a bancos o APIs bancarias reales todas las transacciones son simuladas.
- Guardar contraseñas, claves o la cadena de conexión de Neon en el código, ni subir el archivo .env a GitHub.
- Poner la lógica de detección de fraude en el frontend ni en las rutas de la API, solo vive en el dominio y los casos de uso del backend.
- Usar tecnologías que no estén en la sección 2 sin acuerdo de todo el equipo.
- Subir cambios directamente a main, todo entra por develop mediante pull request.
- Depender de servicios de pago, todo debe funcionar con los planes gratuitos de Neon y Render.

## 6. Seguridad y privacidad

- **Datos tratados:** solo datos simulados generados con Faker, usuarios ficticios, transacciones (monto en COP, tipo, fecha y hora, cuenta destino, canal) y los resultados del análisis (puntaje de riesgo, estado y alertas).
- **Datos que no se deben guardar:** datos personales o bancarios reales, números de tarjeta, documentos de identidad, contraseñas en texto plano ni direcciones IP reales.
- **Validaciones obligatorias:** el backend valida todo con Pydantic monto mayor a 0 y dentro de un máximo, tipo de transacción dentro de la lista permitida, usuario existente, fecha válida y campos obligatorios completos, el frontend también valida el formulario, pero la validación del backend es la que manda
- **Servicios externos permitidos:** Si, Neon y Render, con conexión cifrada (SSL), no se envían transacciones a APIs externas para evaluarlas y la API solo acepta peticiones del dominio del frontend (CORS).
- **Manejo de secretos y credenciales:** la cadena de conexión y demás claves van en variables de entorno en local en un archivo .env, el repositorio solo incluye un .env.example sin valores reales. Si una clave se filtra, se cambia de inmediato.

## 7. Reglas para el uso de IA

1. Leer `CONSTITUTION.md` y `PROJECT_SPEC.md` antes de implementar.
2. Respetar las tecnologías y restricciones aprobadas.
3. No agregar funcionalidades por iniciativa propia.
4. Solicitar aclaraciones ante contradicciones o decisiones importantes sin resolver.
5. Trabajar en una tarea verificable a la vez.
6. Explicar los archivos creados o modificados.
7. No declarar pruebas exitosas sin evidencia de ejecución.
8. Informar riesgos, limitaciones y decisiones técnicas.

## 8. Control de versiones

- **Repositorio:** https://github.com/DanteX786/FinansChecker.git 
- **Ramas:**el main guarda la versión estable que se despliega, la develop es la rama de trabajo y hay 3 ramas temporales feature/, una por integrante y nombradas según su tarea: feature/backend-ai, feature/frontend y feature/database-deploy, Las crean desde levelop en local los integrantes, una vez finalizado el trabajo vuelven a develop y al terminar el desarrollo se eliminan
- **Commits:** en inglés, cortos y sencillos, con el formato type: description, por ejemplo ‘”feat: add transaction simulator”, ‘’fix: validate negative amounts”, “docs: update README”.
- **Revisiones:** todo cambio entra por pull request, Juan Camilo Valle Calle (DanteX786) revisa y aprueba todos los pull requests de las ramas temporales a develop y al finalizar el aplicativo de develop a main.

## 9. Gestión de cambios
1. Registrar la modificación propuesta.
2. Justificarla.
3. Evaluar su impacto en especificación, plan y pruebas.
4. Obtener aprobación.
5. Actualizar los archivos afectados.

| Fecha | Regla modificada | Justificación | Aprobó |
|---|---|---|---|
| [Fecha] | [Regla] | [Motivo] | [Nombre] |

## 10. Checklist de aprobación

- [ ] Tecnologías definidas.
- [ ] Principios y convenciones documentados.
- [ ] Restricciones explícitas.
- [ ] Seguridad y privacidad consideradas.
- [ ] Reglas para la IA aprobadas.
- [ ] Constitución revisada por el equipo.

**Estado final:** [Borrador / En revisión / Aprobada]
