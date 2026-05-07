 SG Academia 


 Estrutura

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
