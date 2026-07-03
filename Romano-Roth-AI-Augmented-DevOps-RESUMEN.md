# Resumen estructurado — *AI-Augmented DevOps with Platform Engineering*

- **Ponente:** Romano Roth — Chief of DevOps & Partner en Zühlke (23 años), presidente de DevOps Days, organizador del DevOps Meetup Zürich (+2.500 subs), autor del libro *The Cybernetic Enterprise* (previsto para agosto).
- **Evento:** DevDays Europe / DevOps Pro / CyberWise 2025 · ~40 min.
- **Tesis central:** *"AI no es el futuro y DevOps tampoco lo es — el futuro es cibernético."*

---

## 1. La tesis: el futuro es *cibernético*, no "AI"

- Estamos **atrapados en un hype de AI**. La AI no arreglará procesos, organización, tecnología ni gobierno rotos: `AI will NOT fix your broken processes, organization, technology and governance`.
- El futuro es la **empresa cibernética**: un sistema adaptativo donde **procesos + organización + tecnología + gobierno + AI + humanos** operan en **bucles de feedback constantes** para adaptarse, mejorar y sostener los objetivos de negocio.
- Rol del ingeniero DevOps: **construir la fundación** que permite al negocio alcanzar sus metas — no saltar al siguiente juguete de AI porque todos lo hacen.

## 2. El hype de la AI (evidencia y advertencias)

- **Brecha inversión vs. ingreso (2025):** ~$1.000 B invertidos vs. ~$120 B de ingreso estimado. Alguien pagará esa brecha; refleja las *ganancias de eficiencia esperadas*.
- **Analogía dotcom:** recuerda el estallido de la burbuja puntocom (marzo 2000); percibe un patrón similar.
- **Señales de corrección:** el CEO de Klarna revierte el reemplazo de soporte por AI (problemas de calidad, vuelve a contratar humanos); ROI de AI decepcionante y muchas empresas abandonan sus prototipos.
- **Preguntas retóricas al público:** casi nadie ha dejado que una AI construya *sola* un sistema complejo (ej. control de tráfico aéreo). La AI funciona bien para "Hello World", no para sistemas complejos autónomos.
- Matiz: **la AI es excelente** y la usa a diario; el llamado es a **cortar la niebla** y ver qué importa de verdad.

## 3. Industrialización del software → Platform Engineering

- El sector se mueve hacia la **estandarización vía plataformas**: cómo se construyen los productos digitales, con un catálogo claro de servicios/productos.
- **Target Operating Model:**
  - Antes: *product teams* con stack tecnológico enorme y toda la carga cognitiva → demasiada complejidad.
  - Ahora: equipos con **stack pequeño**, enfocados solo en su producto/feature, apoyados por una **plataforma self-service**.

### Modelo de dos capas
| Capa | Quién | Qué hace |
|------|-------|----------|
| **Platform team** | Construye la **plataforma cibernética** (producto *interno*) | Genera valor para los product teams |
| **Product teams** | Clientes de la plataforma | End-to-end ("build it & run it" = DevOps real), generan valor al cliente final |

- **Sin ticket-ops:** la plataforma es **self-service** y trae todas las herramientas/capacidades.
- **Ejemplo (observabilidad):** el platform team ofrece la *capacidad* (Grafana/Prometheus, dashboards por defecto); el product team la usa para monitorizar **su** app (tiene la responsabilidad end-to-end).
- **Advertencia:** platform engineering **NO es solo montar Backstage**.

## 4. La "plataforma flotante" (Floating Platform)

- Concepto de **Gregor Hohpe** (*Platform Strategy* — recomendado como must-read).
- **Integrar todas las herramientas/clouds a través de la plataforma**, nunca las herramientas entre sí → así puedes **reemplazar cualquier herramienta** sin quedar atrapado (vendor lock-in).
  - Ejemplo: GitLab (que ama) pierde ~$50 M/trimestre y hay rumores de venta → conviene poder deshacerse de la herramienta si hace falta.
- **No duplicar features** en la plataforma (si no, se convierte en otro tool más); solo integrar.
- Diseño con **Domain-Driven Design**, subdominios, capa de **procesamiento/automatización** (lo difícil, donde muchas empresas fracasan), bloques de integración unificados y **adaptadores**.
- **Alcance completo:** la plataforma va **de la ideación hasta producción** (dev cloud con API mocks + datos sintéticos, y otra instancia idéntica en on-prem / prod cloud). El error común: verla como "una cosa de developers".
- Soporta **cloud, multi-cloud y on-prem** (motivo emergente: resiliencia geopolítica → poder mover cargas entre clouds u on-prem).

## 5. La AI dentro de la plataforma = una *capacidad*

- La AI **no es el centro**: es **una capacidad más** que la plataforma provee de forma **segura y gobernada** a toda la empresa.
- **Stack de AI en la plataforma:**
  1. **Aplicaciones:** chatbots, datos sintéticos de prueba, asistentes de código, gestión de conocimiento.
  2. **Herramientas:** prompt engineering, vector databases, soluciones "golden path" para RAG.
  3. **Model hub:** versionado de modelos.
  4. **Infra GenAI:** cloud u **on-prem** (tendencia creciente: data centers propios hospedando LLMs).

## 6. Demo — plataforma real (Zühlke + banco privado de Liechtenstein)

Métricas en vivo: **461 usuarios, 15 partners, 26 spaces, 13 clústeres Kubernetes**, con costes visibles.

- **Concepto de Partner:** onboarding/offboarding de clientes o vendors **en segundos** (vía Microsoft Entra ID, *bring-your-own-identity*) — vs. semanas en muchas empresas. Al integrar todo por la plataforma flotante, se dan/quitan accesos a todas las herramientas de golpe.
- **Concepto de Space:** zona de red (hub-spoke) donde el cliente crea su propio clúster K8s o VMs.
- **Seguridad platform-wide:** escaneo de repos (licencias, *secret detection*), *container scanning* con análisis de imágenes por AI — se **impone seguridad desde la plataforma**, no solo en pipelines CI/CD.
- **Golden path templates:** crear repos desde plantillas que definen app + interfaz REST + infra.
- **Observabilidad out-of-the-box:** logs, Tempo (microservicios), dashboards pre-cargados; el product team solo escribe a *stdout*.
- **Service catalog self-service:** p. ej. pedir una base de datos con un clic → aprovisionada con backups/passwords estandarizados y gobernados (preferentemente vía IaC).
- **AI gobernada:** acceso a OpenAI de forma governed (antes era "el infierno", con el CISO alarmado). Sobre eso construyeron: chatbot on-prem (sin sacar datos a la cloud), *reference finder* (buscar entre miles de proyectos), proyecto de prompts reutilizables y plataforma de formación interna.
- **Resultado:** nueva app **en producción en ~15 min** (certificados, backups, todo estandarizado) y **CISO satisfecho**.

## 7. Conclusión

- Pasar de la **"ticket-ops"** (esperar semanas por infra) a una **fábrica cibernética** donde los servicios se sirven listos "de la estantería".
- **Empresa cibernética** = sistema regulado en evolución continua, con feedback loops donde humanos + AI colaboran y mejoran el sistema.
- Receta: cortar la niebla → **construir la fundación con Platform Engineering** → **plataforma cibernética flotante** → la **AI como capacidad** encima.
- Cierre: *"El futuro pertenece a quienes dominan la sinfonía entre organización, proceso, tecnología, gobierno y AI. Ese es el futuro de DevOps."*

## 8. Q&A destacado

- **¿La AI reemplazará al platform team?** No (por ahora). Un LLM solo mimetiza respuestas/mejores casos; una plataforma es un sistema complejo. Sus ingenieros expertos incluso **desactivan Copilot** al crear cosas nuevas porque "mete basura".
- **¿Volverse cloud-agnostic?** No lo *impone*, pero muchas empresas buscan **resiliencia** (contexto geopolítico US) para poder mover cargas a on-prem u otro cloud.
- **¿Cuándo montar un platform team?** A partir de **~5 product teams (≈50 personas)**. Por debajo, no compensa.

---

## Ideas clave para recordar

1. **AI ≠ futuro; cibernético = futuro.** La AI no arregla lo que ya está roto.
2. **Platform Engineering es la fundación**, con equipos de plataforma (producto interno) y product teams self-service.
3. **Floating platform:** integra herramientas *a través de* la plataforma, sin duplicar features → evita lock-in.
4. **Cubre de ideación a producción**, no solo desarrollo.
5. **AI = capacidad gobernada** sobre la plataforma, no el protagonista.
6. **Umbral:** ~5 product teams / 50 personas para justificar una plataforma.
