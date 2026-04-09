# SG Academia 🏋️ — Versão Web

## Rodar localmente

```bash
cd sg_academia
python -m pip install -r requirements.txt
python app.py
```
Abra: **http://localhost:5000**

---

## Hospedar online (grátis) — Render.com

1. Crie conta em https://render.com
2. Clique em **New → Web Service**
3. Faça upload do projeto ou conecte ao GitHub
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
   - **Environment:** Python 3
5. Clique em **Deploy** — em minutos estará online com um link público

### Variáveis de ambiente (opcional)
| Variável | Valor |
|---|---|
| `PORT` | 5000 (padrão) |
| `FLASK_ENV` | `production` |

---

## Hospedar online — Railway.app

1. Crie conta em https://railway.app
2. **New Project → Deploy from GitHub**
3. O Railway detecta Python automaticamente
4. Deploy em 1 clique ✅

---

## Estrutura

```
sg_academia/
├── app.py          ← servidor Flask + API REST
├── database.py     ← SQLite
├── services.py     ← lógica de negócio + Pandas
├── templates/      ← HTML (Jinja2)
├── static/         ← CSS + JS
├── data/           ← banco criado automaticamente
├── reports/        ← relatórios exportados
└── requirements.txt
```

## API disponível

| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/metricas` | Cards do dashboard |
| GET | `/api/alunos?q=` | Lista alunos (com filtro) |
| GET | `/api/aluno/:id` | Dados de um aluno |
| POST | `/api/cadastrar` | Cadastrar aluno |
| POST | `/api/editar/:id` | Editar aluno |
| POST | `/api/desativar/:id` | Soft delete |
| POST | `/api/plano/toggle/:id` | Ativar/Suspender plano |
| GET | `/api/exportar/csv` | Download CSV |
| GET | `/api/exportar/excel` | Download Excel |
| GET | `/api/health` | Health check |
