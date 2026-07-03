# MCP-SETUP.md — Configuración de MCP (JIRA + GitHub + markitdown)

Guía paso a paso para conectar los agentes del framework a sistemas reales vía **MCP
(Model Context Protocol)**. Al terminar, los agentes podrán leer/crear issues en **JIRA**
y crear ramas/PRs en **GitHub**, siempre bajo los guardrails de [`../CLAUDE.md`](../CLAUDE.md)
y el gobierno de [`GOVERNANCE.md`](./GOVERNANCE.md).

> **Regla de oro (`CLAUDE.md` §5):** las credenciales se inyectan por **variable de
> entorno** (`${VAR}`), nunca se hardcodean en `.mcp.json` ni se commitean. `.env` está
> en `.gitignore` — verifícalo antes de escribir tokens.

---

## 0. Mapa rápido — ¿dónde está cada cosa?

| Qué | Dónde | Contiene |
|-----|-------|----------|
| Definición de los servers MCP | [`../.mcp.json`](../.mcp.json) | qué server, transporte y qué `${VAR}` consume cada uno |
| Plantilla de variables | [`../.env.example`](../.env.example) | lista de variables a rellenar (sin valores) |
| Tus credenciales reales | `../.env` *(local, git-ignored)* | los tokens de verdad — **no se commitea** |
| Guardrails que aplican | [`../CLAUDE.md`](../CLAUDE.md) §1, §2, §5 | prohibiciones (no merge, no push a protegidas, no secretos) |
| Permisos de herramientas | [`../.claude/settings.json`](../.claude/settings.json) | allow/ask/deny de Bash y MCP |

---

## 1. Requisitos previos

| Herramienta | Para qué | Verificar |
|-------------|----------|-----------|
| [`uv`](https://docs.astral.sh/uv/) (`uvx`) | corre el server `mcp-atlassian` (JIRA) | `uvx --version` |
| Claude Code | host de los MCP | `claude --version` |
| (opcional) [`direnv`](https://direnv.net/) | carga `.env` al entrar al directorio | `direnv version` |

GitHub usa el **server remoto oficial** (HTTP), así que **no** requiere Docker ni binario local.

---

## 2. Servers configurados en `.mcp.json`

```jsonc
{
  "mcpServers": {
    "atlassian": {                          // JIRA
      "command": "uvx",
      "args": ["mcp-atlassian"],
      "env": {
        "JIRA_URL": "${JIRA_URL}",
        "JIRA_USERNAME": "${JIRA_USERNAME}",
        "JIRA_API_TOKEN": "${JIRA_API_TOKEN}"
      }
    },
    "github": {                             // GitHub (remoto, HTTP)
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer ${GITHUB_TOKEN}",
        "X-MCP-Toolsets": "repos,issues,pull_requests,actions"
      }
    },
    "markitdown": {                         // ingesta documental (sin credenciales)
      "command": "uvx",
      "args": ["markitdown-mcp"]
    }
  }
}
```

- **`atlassian`** → server [`mcp-atlassian`](https://github.com/sooperset/mcp-atlassian), lanzado con `uvx`.
- **`github`** → [GitHub MCP Server](https://github.com/github/github-mcp-server) en modo **remoto**.
  El header `X-MCP-Toolsets` limita las herramientas expuestas (least-privilege, `CLAUDE.md` §2).
- **`markitdown`** → [markitdown-mcp](https://github.com/microsoft/markitdown/tree/main/packages/markitdown-mcp) (Microsoft), lanzado con `uvx`.
  Convierte PDF/Office/HTML/imágenes a Markdown (`convert_to_markdown`). **No usa credenciales** —
  no lleva `${VAR}` ni entrada en `.env`. Corre en local con los permisos de tu usuario, así que
  puede leer rutas `file://` locales; úsalo solo con documentos que ya tienes derecho a leer.
  Por RBAC ([`GOVERNANCE.md`](./GOVERNANCE.md) §1) es de **Product** y **Compliance** (ingesta de
  requisitos y evidencia).

---

## 3. Obtener las credenciales

### 3.1 JIRA (Atlassian Cloud)

1. Ve a **https://id.atlassian.com/manage-profile/security/api-tokens**.
2. *Create API token* → copia el valor (solo se muestra una vez).
3. Necesitas tres datos:
   - `JIRA_URL` → tu instancia, p. ej. `https://tuempresa.atlassian.net`
   - `JIRA_USERNAME` → tu email de Atlassian
   - `JIRA_API_TOKEN` → el token recién creado

### 3.2 GitHub (PAT fine-grained)

1. Ve a **GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens**.
2. *Generate new token*:
   - **Repository access** → solo los repos que el framework va a tocar (no "All").
   - **Permissions** (mínimos para el flujo issue→story→.feature→PR):

     | Permiso | Acceso | Por qué |
     |---------|--------|---------|
     | Contents | **Read & write** | crear ramas `feature/*`, commitear |
     | Pull requests | **Read & write** | abrir PRs (nunca mergear, `CLAUDE.md` §1.3) |
     | Issues | **Read & write** | enlazar/comentar issues |
     | Actions | **Read** | leer estado de CI / gates |
     | Metadata | **Read** | obligatorio por GitHub |
3. Copia el token → será `GITHUB_TOKEN`.

> La protección de `main`/`develop`/`release/*` la imponen las **branch protection rules**
> del repo en GitHub, **no** el MCP. Configúralas para que ningún PR se mergee sin revisión humana.

---

## 4. Rellenar `.env`

`.env` ya existe (copiado de `.env.example`). Edítalo y pon los valores reales:

```bash
# --- Atlassian / JIRA ---
JIRA_URL=https://tuempresa.atlassian.net
JIRA_USERNAME=tu@email.com
JIRA_API_TOKEN=ATATT...               # token del paso 3.1

# --- Git host ---
GITHUB_TOKEN=github_pat_...           # PAT fine-grained del paso 3.2
```

Verifica que git lo ignora (debe imprimir `.env`):

```bash
git check-ignore .env
```

---

## 5. Cargar las variables al entorno

> **Importante:** Claude Code expande `${VAR}` desde el **entorno del proceso al arrancar**;
> **no** lee `.env` por sí solo. Hay que exportar las variables antes de lanzar `claude`.

### Opción A — manual (rápida)

**bash / zsh:**

```bash
cd ~/Documents/DevOps/ai-agents-framework
set -a; source .env; set +a     # exporta todas las vars del .env
claude                          # lánzalo en esta misma shell
```

**fish** (no entiende `KEY=value` ni `source .env`):

```fish
cd ~/Documents/DevOps/ai-agents-framework
for line in (cat .env | grep -vE '^\s*(#|$)')
    set -gx (string split -m1 = -- $line)
end
claude
```

### Opción B — direnv (automática, recomendada) ✅

direnv parsea `.env` él mismo, así que **funciona igual en bash, zsh y fish** (no
depende de la sintaxis del shell). Es lo que usa este proyecto.

```bash
# 1. instalar direnv una vez (ej. linuxbrew):  brew install direnv
# 2. enganchar el hook a tu shell (una sola vez):
#      bash → echo 'eval "$(direnv hook bash)"'      >> ~/.bashrc
#      zsh  → echo 'eval "$(direnv hook zsh)"'       >> ~/.zshrc
#      fish → echo 'direnv hook fish | source'       >> ~/.config/fish/config.fish

cd ~/Documents/DevOps/ai-agents-framework
echo 'dotenv' > .envrc          # carga .env automáticamente al entrar (ya creado)
direnv allow                    # autoriza este .envrc (se pide una vez)
```

A partir de aquí, cada vez que entres al directorio las variables se cargan solas; al
salir, se descargan. Tras añadir el hook, **abre una shell nueva** (o recárgala) para
que tome efecto. `.envrc` solo contiene `dotenv` (sin secretos), así que es seguro commitearlo.

---

## 6. Verificar la conexión

Dentro de Claude Code:

```
/mcp
```

Deberías ver:

```
atlassian   ✓ connected
github      ✓ connected
```

Prueba rápida de extremo a extremo:

```
> lista mis proyectos de JIRA
> lista los repos a los que tengo acceso en GitHub
```

---

## 7. Troubleshooting

| Síntoma | Causa probable | Solución |
|---------|----------------|----------|
| `atlassian` no conecta | `uvx` no instalado o vars JIRA vacías | `uvx --version`; reexporta `.env` y relanza |
| `401 / 403` en JIRA | token expirado o `JIRA_USERNAME` ≠ email | regenera token (3.1); usa el email, no el display name |
| `github` no conecta | `GITHUB_TOKEN` no exportado | confirma con `echo ${GITHUB_TOKEN:+set}` → debe imprimir `set` |
| `403` al crear PR/rama | faltan permisos en el PAT | revisa scopes (3.2): Contents/PR/Issues = RW |
| Variables "definidas" pero MCP no las ve | exportaste **después** de abrir Claude Code | el entorno se lee al arrancar → **relanza** `claude` |
| Push a `main` rechazado | branch protection (correcto y esperado) | crea rama `feature/PROJ-XXX` y abre PR (`CLAUDE.md` §1.3) |

---

## 8. Checklist

- [ ] `uvx` instalado.
- [ ] Token de JIRA creado y `JIRA_URL/USERNAME/API_TOKEN` en `.env`.
- [ ] PAT fine-grained de GitHub creado con los scopes mínimos y `GITHUB_TOKEN` en `.env`.
- [ ] `git check-ignore .env` confirma que **no** se commitea.
- [ ] Variables cargadas (`source .env` o `direnv`) y `claude` relanzado.
- [ ] `/mcp` muestra `atlassian` y `github` como **connected**.
- [ ] Branch protection activa en `main`/`develop`/`release/*`.

---

Documentos relacionados: [`../README.md`](../README.md) · [`../CLAUDE.md`](../CLAUDE.md) · [`./GOVERNANCE.md`](./GOVERNANCE.md) · [`./ARCHITECTURE.md`](./ARCHITECTURE.md)
