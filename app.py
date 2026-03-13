from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "Hello from Flask!",
        "status": "running"
    })

@app.route("/health")
def health():
    # Kubernetes uses this to check if the pod is alive (liveness probe)
    return jsonify({"status": "healthy"}), 200

@app.route("/ready")
def ready():
    # Kubernetes uses this to check if the pod is ready to receive traffic (readiness probe)
    return jsonify({"status": "ready"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)