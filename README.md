# Friends Memory Timeline

A timeline application for storing and sharing memories with friends.

## Local Development

### Prerequisites

- Docker & Docker Compose v2+
- Node.js 20+ (for frontend tooling)
- Python 3.11+ (for backend tooling)

### Quick Start

```bash
# 1. Clone and enter directory
git clone https://github.com/xavu-ai/friends-memory-timeline.git
cd friends-memory-timeline

# 2. Start all services
docker compose up --build --wait

# 3. Verify services
curl http://localhost:6100/healthz          # Backend health (expect: {"status": "ok"})
curl http://localhost:8100                  # Frontend (expect: 200)

# 4. Run E2E tests
cd frontend
pnpm install
pnpm playwright install --with-deps chromium
E2E_BASE_URL=http://localhost:8100 API_BASE_URL=http://localhost:6100 \
  pnpm playwright test ../e2e/smoke.spec.ts

# 5. Tear down
docker compose down
```

### Port Mapping

| Service  | Internal | External | URL |
|----------|----------|----------|-----|
| Backend  | 6100     | 6100     | http://localhost:6100 |
| Frontend | 8100     | 8100     | http://localhost:8100 |
| PostgreSQL | 5432   | 5432     | localhost:5432 |

### API Endpoints

Base URL: `http://localhost:6100` (proxied via `/api` through frontend)

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | /api/v1/auth/verify | Verify password and get JWT | No |
| GET | /api/v1/events | List all events (newest first) | Yes |
| POST | /api/v1/events | Create event | Yes |
| GET | /api/v1/events/:id | Get single event | Yes |
| PUT | /api/v1/events/:id | Update event | Yes |
| DELETE | /api/v1/events/:id | Delete event | Yes |
| GET | /healthz | Health check | No |

### Authentication

The API uses JWT Bearer tokens. To authenticate:

```bash
# Get token
TOKEN=$(curl -s -X POST http://localhost:6100/api/v1/auth/verify \
  -H "Content-Type: application/json" \
  -d '{"password":"secret1"}' | jq -r '.token')

# Use token
curl http://localhost:6100/api/v1/events \
  -H "Authorization: Bearer $TOKEN"
```

### Default Test Passwords

The following passwords are configured by default (via `FRIEND_PASSWORDS` env var):
- `secret1`, `secret2`, `secret3`

### Common Issues

**CORS errors:** Ensure `ALLOWED_ORIGINS` env var includes `http://localhost:8100` in backend.

**Frontend can't reach backend:** Frontend proxies `/api/*` to `http://backend:6100` via `next.config.ts`. Do NOT use `NEXT_PUBLIC_BACKEND_URL`.

**Port conflicts:** If 6100 or 8100 are in use, update `docker-compose.yml` ports section.

**Database tables missing:** Tables are auto-created on backend startup via `Base.metadata.create_all()`.

### Project Structure

```
.
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/v1/      # API routes
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/    # Business logic
│   │   └── main.py      # FastAPI app
│   ├── Dockerfile
│   └── docker-compose.yml
├── frontend/             # Next.js frontend
│   ├── app/             # Next.js App Router pages
│   ├── components/      # React components
│   ├── hooks/           # Custom React hooks
│   ├── lib/             # Utilities (API client, auth)
│   ├── Dockerfile
│   └── package.json
├── e2e/                 # Playwright E2E tests
├── docker-compose.yml   # Root compose file
└── README.md
```

### Environment Variables

**Backend (`docker-compose.yml`):**
- `DATABASE_URL`: PostgreSQL connection string
- `PASSWORDS`: JSON array of valid passwords
- `ALLOWED_ORIGINS`: CORS allowed origins
- `JWT_SECRET`: Secret for JWT signing (default: dev-secret-change-in-production)

**Frontend:**
- No environment variables needed - uses Next.js rewrites for API proxying
