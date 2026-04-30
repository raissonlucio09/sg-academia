from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from database import inicializar_banco
import services
import os

app = Flask(__name__)
inicializar_banco()
CORS(app)  # Permite requisições de qualquer origem (frontend separado ou hospedagem externa)


@app.before_request
def _atualizar():
    services.atualizar_status()


# ── Páginas ──────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")


# ── Health check (útil para hospedagem) ─────────────────────────
@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "app": "SG Academia"})


# ── Métricas & dados ─────────────────────────────────────────────
@app.route("/api/metricas")
def api_metricas():
    return jsonify(services.metricas())

@app.route("/api/alunos")
def api_alunos():
    return jsonify(services.listar_alunos(request.args.get("q", "")))

@app.route("/api/aluno/<int:id_aluno>")
def api_get_aluno(id_aluno):
    a = services.get_aluno(id_aluno)
    return jsonify(a) if a else (jsonify({"error": "Não encontrado"}), 404)

@app.route("/api/grafico")
def api_grafico():
    return jsonify(services.matriculas_por_mes())


# ── Escrita ──────────────────────────────────────────────────────
@app.route("/api/cadastrar", methods=["POST"])
def api_cadastrar():
    ok, msg = services.cadastrar_aluno(request.json)
    return jsonify({"ok": ok, "msg": msg}), (200 if ok else 400)

@app.route("/api/editar/<int:id_aluno>", methods=["POST"])
def api_editar(id_aluno):
    ok, msg = services.editar_aluno(id_aluno, request.json)
    return jsonify({"ok": ok, "msg": msg}), (200 if ok else 400)

@app.route("/api/desativar/<int:id_aluno>", methods=["POST"])
def api_desativar(id_aluno):
    services.desativar_aluno(id_aluno)
    return jsonify({"ok": True})

@app.route("/api/plano/toggle/<int:id_plano>", methods=["POST"])
def api_toggle_plano(id_plano):
    ok, resultado = services.alternar_status_plano(id_plano)
    return jsonify({"ok": ok, "novo_status": resultado}), (200 if ok else 404)


# ── Exportação ───────────────────────────────────────────────────
@app.route("/api/exportar/csv")
def api_csv():
    return send_file(services.exportar_csv(), as_attachment=True)

@app.route("/api/exportar/excel")
def api_excel():
    return send_file(services.exportar_excel(), as_attachment=True)


# ── Inicialização ────────────────────────────────────────────────
if __name__ == "__main__":
    inicializar_banco()
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV", "development") == "development"
    print(f"\n✅  SG Academia rodando em: http://localhost:{port}\n")
    app.run(debug=debug, host="0.0.0.0", port=port)
