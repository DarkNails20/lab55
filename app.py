from flask import Flask, request, jsonify

app = Flask(__name__)

users = [
    {
        "id": 1,
        "name": "Danial",
        "email": "danial@example.com"
    }
]


@app.route("/api/users", methods=["GET"])
def get_users():
    return jsonify(users)


@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    user = {
        "id": len(users) + 1,
        "name": name,
        "email": email
    }

    users.append(user)

    return jsonify(user), 201


@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    global users

    for user in users:
        if user["id"] == user_id:
            users.remove(user)
            return jsonify({"message": "User deleted"})

    return jsonify({"error": "User not found"}), 404


def dangerous_function(user_input):
    return eval(user_input)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)