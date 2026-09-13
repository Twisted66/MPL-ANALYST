# Deployment

Recommended first cloud shape:

```text
HTTPS reverse proxy
        |
        v
ASGI Python process
   |         |
 /health    /mcp
              |
            SQLite
```

Use one worker initially. Move to PostgreSQL when concurrent/live usage grows.

Generate a token:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Environment:

```env
MPL_MCP_TOKEN=<long-random-secret>
MPL_ALLOWED_HOSTS=mcp.example.com,mcp.example.com:*
MPL_ALLOWED_ORIGINS=
```

Run:

```bash
python -m mpl_predictor.server
```

If your cloud provider exposes an ASGI application directly, the application object is:

`mpl_predictor.server:app`

The official MCP SDK v2 uses Streamable HTTP and the endpoint is `/mcp`.

Do not deploy without HTTPS and authentication.
