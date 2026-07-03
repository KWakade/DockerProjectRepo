from flask import Flask, render_template, request, redirect, jsonify
import psycopg2

app = Flask(__name__)

DB_NAME="userdb"
DB_USER="postgres"
DB_PASSWORD="Password123"
DB_HOST="localhost"
DB_PORT="5432"


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )


# Display Web Page
@app.route("/")
def home():
    return render_template("index.html")


# POST Operation
@app.route("/adduser", methods=["POST"])
def add_user():

    username = request.form["username"]
    email = request.form["email"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO users (username, email)
        VALUES (%s, %s)
        """,
        (username, email)
    )

    conn.commit()

    cur.close()
    conn.close()

    return redirect("/")


# GET Operation
@app.route("/users", methods=["GET"])
def get_users():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, username, email
        FROM users
        ORDER BY id
        """
    )

    rows = cur.fetchall()

    users = [
        {
            "id": row[0],
            "username": row[1],
            "email": row[2]
        }
        for row in rows
    ]

    cur.close()
    conn.close()

    return jsonify(users)


if __name__ == "__main__":
    app.run(debug=True)