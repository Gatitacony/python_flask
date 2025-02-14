from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.models import User, Note
from flask_login import login_user, login_required, logout_user, current_user
from app.forms import LoginForm, RegistrationForm, NoteForm
from werkzeug.security import generate_password_hash, check_password_hash
 

@app.route('/', methods=['GET', 'POST'])
def home():
    register_form = RegistrationForm()
    login_form = LoginForm()

    if request.method == 'POST':
        if 'register' in request.form:  # Si se está enviando el formulario de registro
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']

            # Verificar si el usuario ya existe
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash("El usuario ya existe.", "danger")
                return redirect(url_for('home'))

            # Crear un nuevo usuario
            new_user = User(username=username, email=email)
            new_user.set_password(password)  # Se asegura de hashear la contraseña

            db.session.add(new_user)
            db.session.commit()

            flash("Registro exitoso, ahora puedes iniciar sesión.", "success")
            return redirect(url_for('home'))  # Redirige a la página de inicio después del registro

        elif 'login' in request.form:  # Si se está enviando el formulario de login
            email = request.form['email']
            password = request.form['password']

            # Buscar el usuario en la base de datos
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):  # Corregido para usar el método del modelo
                login_user(user)
                flash("Login exitoso", "success")
                return redirect(url_for('dashboard'))
            else:
                flash("Correo o contraseña incorrectos", "danger")

    return render_template('home.html', register_form=register_form, login_form=login_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    note_form = NoteForm()
    edit_id = request.args.get('edit', type=int)
    
    if edit_id:
        note = Note.query.get_or_404(edit_id)
        if note.user_id != current_user.id:
            flash('No tienes permiso para editar esta nota.', 'danger')
            return redirect(url_for('dashboard'))
        note_form = NoteForm(obj=note)
    
    if note_form.validate_on_submit():
        if edit_id:
            note = Note.query.get_or_404(edit_id)
            note.title = note_form.title.data
            note.content = note_form.content.data
            flash('Nota actualizada!', 'success')
        else:
            note = Note(title=note_form.title.data, content=note_form.content.data, user_id=current_user.id)
            db.session.add(note)
            flash('Nota creada!', 'success')
        db.session.commit()
        return redirect(url_for('dashboard'))

    if request.method == 'POST' and 'delete' in request.form:
        note_id = request.form['delete']
        note = Note.query.get_or_404(note_id)
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('Nota eliminada!', 'success')
        else:
            flash('No tienes permiso para eliminar esta nota.', 'danger')
        return redirect(url_for('dashboard'))

    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', notes=notes, note_form=note_form, edit_id=edit_id)