from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Berita
from forms import LoginForm, RegisterForm, BeritaForm
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    berita_list = Berita.query.all()
    return render_template('index.html', berita=berita_list)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Registrasi berhasil!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        flash('Login gagal!')
    return render_template('login.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    form = BeritaForm()
    if form.validate_on_submit():
        berita = Berita(judul=form.judul.data, isi=form.isi.data)
        db.session.add(berita)
        db.session.commit()
        flash('Berita ditambahkan!')
    berita_list = Berita.query.all()
    return render_template('dashboard.html', form=form, berita=berita_list)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_berita(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    berita = Berita.query.get_or_404(id)
    form = BeritaForm(obj=berita)
    if form.validate_on_submit():
        berita.judul = form.judul.data
        berita.isi = form.isi.data
        db.session.commit()
        flash('Berita berhasil diupdate!')
        return redirect(url_for('dashboard'))
    return render_template('dashboard.html', form=form, berita=Berita.query.all())

@app.route('/delete/<int:id>')
def delete_berita(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    berita = Berita.query.get_or_404(id)
    db.session.delete(berita)
    db.session.commit()
    flash('Berita berhasil dihapus!')
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Kamu sudah logout.')
    return redirect(url_for('index'))

@app.route('/konfirmasi-hapus-akun')
def konfirmasi_hapus_akun():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('konfirmasi_hapus.html')

@app.route('/hapus-akun', methods=['POST'])
def hapus_akun():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    if user:
        db.session.delete(user)
        db.session.commit()
        session.pop('user_id', None)
        flash('Akun kamu sudah dihapus.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)