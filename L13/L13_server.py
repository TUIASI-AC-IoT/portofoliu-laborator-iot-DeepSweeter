from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)
from datetime import timedelta
from functools import wraps

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "SidiousIsPal..." 
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

jwt = JWTManager(app)

# Store the user in a dictionary of dictionaries(duh)
users = {
    "user1": {"password": "parola1", "role": "admin"},
    "user2": {"password": "parola2", "role": "owner"},
    "user3": {"password": "parolaX", "role": "owner"},
}

# Invalidate tokens
revoked_tokens = set()

# === POST /auth ===
@app.route("/auth", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = users.get(username)
    if user and user["password"] == password:
        access_token = create_access_token(identity={"username": username, "role": user["role"]})
        return jsonify(token=access_token), 200
    return jsonify(msg="Invalid credentials"), 401

# === GET /auth/jwtStore ===
@app.route("/auth/jwtStore", methods=["GET"])
@jwt_required()
def validate_token():
    token_identity = get_jwt_identity()
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")

    if token in revoked_tokens:
        return jsonify(msg="Token not found"), 404

    return jsonify(role=token_identity["role"]), 200

# === DELETE /auth/jwtStore ===
@app.route("/auth/jwtStore", methods=["DELETE"])
@jwt_required()
def logout():
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    revoked_tokens.add(token)
    return jsonify(msg="Logged out"), 200


# === GET /sensor/data (Owner/Admin only) ===
@app.route("/sensor/data", methods=["GET"])
@role_required(["owner", "admin"])
def read_sensor_data():
    return jsonify(data="Sensor: Temperature = 23.5°C, Humidity = 40%"), 200

# === POST /sensor/config (Admin only) ===
@app.route("/sensor/config", methods=["POST"])
@role_required(["admin"])
def update_sensor_config():
    config_data = request.get_json()
    # Simulare salvare configurare
    return jsonify(msg="Config updated", new_config=config_data), 200

# === Default route for unauthorized access ===
@app.errorhandler(401)
def unauthorized(e):
    return jsonify(msg="Authentication necessary"), 401

# === Run server ===
if __name__ == "__main__":
    app.run()
