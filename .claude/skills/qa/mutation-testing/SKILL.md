---
name: mutation-testing
description: >-
  Ejecuta mutation testing para medir la EFECTIVIDAD de los tests (no solo cobertura), identifica mutantes supervivientes y refuerza las aserciones para matarlos. Úsala para "mutation testing", "qué tan buenos son mis tests", "mutantes supervivientes".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Skill: Mutation Testing

La cobertura dice qué se ejecuta; la mutación dice qué se **verifica**. Un mutante superviviente = un cambio que rompe el código y ningún test lo detecta = aserción débil o ausente.

## Workflow

```
1. Detectar/seleccionar la herramienta de mutación del lenguaje
2. Ejecutar sobre el módulo crítico objetivo (no todo el repo: es costoso)
3. Recoger el mutation score y la lista de mutantes supervivientes
4. Por cada superviviente: identificar la aserción faltante y añadir/reforzar el test que lo mata
5. Re-ejecutar; reportar score antes→después y mutantes equivalentes (justificados)
```

## Herramientas

| Lenguaje | Herramienta |
|----------|-------------|
| Python | mutmut, cosmic-ray |
| JS/TS | Stryker |
| Java | PIT (pitest) |
| Go | go-mutesting |
| .NET | Stryker.NET |
| Ruby | mutant |
| PHP | Infection |

## Calidad

- Enfocar en código crítico (lógica financiera, auth, validación); la mutación global es cara.
- Distinguir mutantes equivalentes (no se pueden matar) y documentarlos en vez de forzar tests.
- Objetivo: subir el mutation score, no solo la cobertura.

## Anti-Patterns (Never Do)

- Nunca correr mutación sobre todo el repo a ciegas (coste/tiempo).
- Nunca matar mutantes con aserciones triviales que no reflejan comportamiento real.
- Nunca modificar el source para reducir mutantes.
- Nunca ignorar supervivientes en código de seguridad/dinero.
