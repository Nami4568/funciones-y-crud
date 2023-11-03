from flask import Flask, render_template, request,redirect
import pymysql

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/ver")
def ver():
    cursor.execute("SELECT * FROM peliculas")
    pelis=cursor.fetchall()
    data={"peliculas":pelis}
    return render_template("verpeliculas.html",data=data)
@app.route("/agregar", methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        titulo = request.form['titulo']
        genero = request.form['genero']
        duracion = request.form['duracion']
        anio = request.form['anio']

        cursor.execute("INSERT INTO peliculas (titulo, genero, duracion, anio) VALUES (%s, %s, %s, %s)",
                (titulo, genero, duracion, anio))
        conexion.commit()

        
        mensaje = "La película se ha agregado con éxito."
        return render_template("agregarpeliculas.html", mensaje=mensaje)

    return render_template("agregarpeliculas.html")

@app.route("/eliminar", methods=['GET', 'POST'])
def eliminar():
    mensaje = None
    peliculas = None

    if request.method == 'POST':
        pelicula_id = request.form['pelicula_id']
        cursor.execute("DELETE FROM peliculas WHERE id = %s", (pelicula_id,))
        conexion.commit()
        mensaje = "La película se ha eliminado con éxito."

    cursor.execute("SELECT * FROM peliculas")
    peliculas = cursor.fetchall()

    return render_template("eliminarpeliculas.html", peliculas=peliculas, mensaje=mensaje)
@app.route("/actualizar",methods=['GET','POST'])
def actualizar():
    mensaje = None
    pelicula = None

    if request.method == 'POST':
        pelicula_id = request.form['pelicula_id']

        cursor.execute("SELECT * FROM peliculas WHERE id = %s", (pelicula_id,))
        pelicula = cursor.fetchone()

        if pelicula:
            if 'nuevo_titulo' in request.form and 'nuevo_genero' in request.form and 'nueva_duracion' in request.form and 'nuevo_anio' in request.form:
                nuevo_titulo = request.form['nuevo_titulo']
                nuevo_genero = request.form['nuevo_genero']
                nueva_duracion = request.form['nueva_duracion']
                nuevo_anio = request.form['nuevo_anio']

                cursor.execute("UPDATE peliculas SET titulo = %s, genero = %s, duracion = %s, anio = %s WHERE id = %s",
                               (nuevo_titulo, nuevo_genero, nueva_duracion, nuevo_anio, pelicula_id))
                conexion.commit()

                mensaje = "La película se ha actualizado con éxito."
            else:
                mensaje = "Debes completar todos los campos de actualización."

    return render_template("actualizarpelicula.html", mensaje=mensaje, pelicula=pelicula)

    


if __name__ == '__main__':
    conexion = pymysql.connect(host="db4free.net", user="alumnopython", password="programacionpython", db="practicasql")
    cursor = conexion.cursor()
    app.run(debug=True, port=8000)
