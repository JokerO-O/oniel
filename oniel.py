from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)

# Configuración de la clave secreta para sesiones
app.secret_key = os.urandom(24)

# Usuarios de ejemplo
usuarios = {
    'admin': 'admin123',
    'user1': 'password123'
}

@app.route('/')
def home():
    # Si el usuario está logueado, redirigimos al calendario
    if 'username' in session:
        return redirect(url_for('calendar'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Si el usuario ya está logueado, lo redirigimos al calendario
    if 'username' in session:
        return redirect(url_for('calendar'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Verificamos si las credenciales son correctas
        if username in usuarios and usuarios[username] == password:
            session['username'] = username
            return redirect(url_for('calendar'))
        else:
            return render_template('login.html', error="Usuario o contraseña incorrectos")
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Comprobamos si el usuario ya existe
        if username in usuarios:
            return render_template('register.html', error="El usuario ya existe")
        
        # Añadimos el nuevo usuario
        usuarios[username] = password
        session['username'] = username
        return redirect(url_for('calendar'))
    
    return render_template('register.html')

@app.route('/calendar')
def calendar():
    # Verificamos si el usuario está logueado
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('calendar.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # Si la solicitud es POST, cerramos la sesión
    if request.method == 'POST':
        session.pop('username', None)
        return redirect(url_for('login'))
    return redirect(url_for('calendar'))  # Si la solicitud es GET, redirigimos al calendario

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
