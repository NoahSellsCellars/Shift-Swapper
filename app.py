from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Shift

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shifts.db'
app.config['SECRET_KEY'] = 'secret_key'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

"""Authentication Section"""
@app.route('/login', methods=['GET', 'POST'])
#Login
def login():
    #Check if the user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        user_username = request.form.get('username')
        user_password = request.form.get('password')

        user = User.query.filter_by(username=user_username).first()

        if user and user.password == user_password:
            login_user(user)
            return redirect(url_for('index'))
        
        return redirect(url_for('login'))

    else:
        return render_template('login.html')

#Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

#Sign Up
@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    #If the user is already logged in, they can't sign up
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        new_username = request.form.get('new_username')
        new_password = request.form.get('new_password')
        confirm_new_password = request.form.get('confirm_new_password')

        #Check for existing user
        existing_user = User.query.filter_by(username=new_username).first()
        if existing_user:
            flash('Username already exists! Please choose another.')
            return render_template('signup.html')

        #Make sure the passwords match
        if new_password != confirm_new_password:    
            flash('Passwords must match!')
            return render_template('signup.html')
        
        #Create and add new user
        new_user = User(username=new_username, password=new_password)
        db.session.add(new_user)
        db.session.commit()
        
        #Log the user in and show a success message
        login_user(new_user)
        flash(f'Account created! Welcome, {new_user.username}.')
        return redirect(url_for('index'))
    
    return render_template('signup.html')

"""Main Section"""
@app.route('/')
def index():
    shifts_from_db = Shift.query.filter_by(is_up_for_trade=True).all()

    return render_template('index.html', shifts=shifts_from_db)

@app.route('/my_shifts')
@login_required
def my_shifts():
    my_shifts_from_db = Shift.query.filter_by(user_id=current_user.id).all()

    return render_template('my_shifts.html', shifts=my_shifts_from_db)

"""Feature Section"""
@app.route('/take_shift/<int:shift_id>', methods=['POST'])
@login_required
def take_shift(shift_id):
    shift = Shift.query.get_or_404(shift_id)

    if shift.user_id == current_user.id:
        flash("You cannot take your own shift!")
        return redirect(url_for('index'))
    else:
        shift.user_id = current_user.id
        #Once taken, shift is no longer up for trade
        shift.is_up_for_trade = False

        db.session.commit()

        flash(f"Sucess! You have taken the shift for {shift.start_time.strftime('%b %d')}")
        return redirect(url_for('index'))

@app.route('/post_shift/<int:shift_id>', methods=['POST'])
@login_required
def post_shift(shift_id):
    shift = Shift.query.get_or_404(shift_id)

    if shift.user_id != current_user.id:
        flash("This shift does not belong to you")
        return redirect(url_for('my_shifts'))
    else:
        shift.is_up_for_trade = True

        db.session.commit()

        flash(f"Sucess! You have posted your shift for {shift.start_time.strftime('%b %d')}")
        return redirect(url_for('my_shifts'))
    
@app.route('/keep_shift/<int:shift_id>', methods=['POST'])
@login_required
def keep_shift(shift_id):
    shift = Shift.query.get_or_404(shift_id)

    if shift.user_id != current_user.id:
        flash("This shift does not belong to you")
        return redirect(url_for('my_shifts'))
    else:
        shift.is_up_for_trade = False

        db.session.commit()

        flash(f"You have sucessfully withdrawn the post for your shift on {shift.start_time.strftime('%b %d')} ")
        return redirect(url_for('my_shifts'))

"""Execution Section"""
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
    