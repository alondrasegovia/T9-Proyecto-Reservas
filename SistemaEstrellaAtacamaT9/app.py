# Archivo principal (ejecuta la app Flask)


from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",           # usuario de MySQL
        password="9568",# contraseña de MySQL
        database="estrella_atacama",
        port=3307             
    )

# --- Rutas principales ---
@app.route("/hotel/<int:hotel_id>")
def detalle_hotel(hotel_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM hoteles WHERE id = %s", (hotel_id,))
    hotel = cursor.fetchone()
    cursor.execute("SELECT * FROM habitaciones WHERE hotel_id = %s", (hotel_id,))
    habitaciones = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("detalle_hotel.html", hotel=hotel, habitaciones=habitaciones)

@app.route("/tour/<int:tour_id>")
def detalle_tour(tour_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tours WHERE id = %s", (tour_id,))
    tour = cursor.fetchone()
    cursor.execute("SELECT * FROM opciones_tour WHERE tour_id = %s", (tour_id,))
    opciones = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("detalle_tour.html", tour=tour, opciones=opciones)

@app.route("/")
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM hoteles")
    hoteles = cursor.fetchall()
    cursor.execute("SELECT * FROM tours")
    tours = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("index.html", hoteles=hoteles, tours=tours)

@app.route("/reserva/<tipo>/<int:item_id>/<sub_item>", methods=["GET", "POST"])
def reserva(tipo, item_id, sub_item):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    item = None
    seleccion = None

    if tipo == "hotel":
        cursor.execute("SELECT * FROM hoteles WHERE id = %s", (item_id,))
        item = cursor.fetchone()
        # You need to fetch habitaciones from another table if you have them in MySQL
        # seleccion = ... (fetch the correct habitacion)
    elif tipo == "tour":
        cursor.execute("SELECT * FROM tours WHERE id = %s", (item_id,))
        item = cursor.fetchone()
        # seleccion = ... (fetch the correct opcion)

    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        # Save reservation in MySQL
        cursor.execute(
            "INSERT INTO reservas (email) VALUES (%s)", (email,)
        )
        conn.commit()
        cursor.close()
        conn.close()
        reserva = {
            "tipo": tipo,
            "item": item["nombre"],
            "usuario": nombre,
            "email": email
        }
        return render_template("confirmacion.html", reserva=reserva)

    cursor.close()
    conn.close()
    return render_template("reserva.html", tipo=tipo, item=item, seleccion=seleccion)

@app.route("/membresia", methods=["GET", "POST"])
def membresia():
    mensaje = None
    rank = None
    user_reservas = 0

    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        numero = request.form["numero"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # Check if member exists
        cursor.execute("SELECT * FROM miembros WHERE email = %s", (email,))
        miembro = cursor.fetchone()
        if miembro:
            cursor.execute(
                "UPDATE miembros SET nombre=%s, numero=%s, password=%s WHERE email=%s",
                (nombre, numero, password, email)
            )
        else:
            cursor.execute(
                "INSERT INTO miembros (nombre, email, numero, password) VALUES (%s, %s, %s, %s)",
                (nombre, email, numero, password)
            )
        conn.commit()
        # Count reservations
        cursor.execute("SELECT COUNT(*) as total FROM reservas WHERE email = %s", (email,))
        user_reservas = cursor.fetchone()["total"]
        # Determine rank
        if user_reservas >= 10:
            rank = "Diamante"
        elif user_reservas >= 5:
            rank = "Oro"
        else:
            rank = "Plata"
        mensaje = "¡Datos guardados correctamente!"
        cursor.close()
        conn.close()
        return render_template("membresia.html", mensaje=mensaje, rank=rank, user_reservas=user_reservas, nombre=nombre)

    return render_template("membresia.html")


if __name__ == "__main__":
    app.run(debug=True)