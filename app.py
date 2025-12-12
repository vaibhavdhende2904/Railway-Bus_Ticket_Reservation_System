from flask import Flask, render_template, request, redirect, session
# from models.models import db, User, Bus, Train, Booking
from models.models import db, User, Bus, Train, Booking

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# ---------- INITIALIZATION (Flask 3.x compatible) ----------
def create_tables():
    db.create_all()

    # Add sample buses
    if not Bus.query.first():
        b1 = Bus(name="Express Bus", source="Pune", destination="Mumbai", seats=40, price=300)
        b2 = Bus(name="Sleeper Bus", source="Nagpur", destination="Pune", seats=30, price=700)
        db.session.add_all([b1, b2])
        db.session.commit()

    # Add sample trains
    if not Train.query.first():
        t1 = Train(name="Intercity Express", source="Pune", destination="Mumbai", seats=200, price=150)
        t2 = Train(name="Rajdhani", source="Delhi", destination="Mumbai", seats=300, price=900)
        db.session.add_all([t1, t2])
        db.session.commit()


# Run initialization before the first request (Flask 3.x safe)
with app.app_context():
    create_tables()


# ---------- HOME ----------
@app.route('/')
def home():
    if "user" not in session:
        return redirect('/login')
    return render_template("index.html", username=session['user'])


# ---------- LOGIN ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['user'] = username
            return redirect('/')
        return "Invalid Credentials!"
    return render_template("login.html")


# ---------- REGISTER ----------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            return "User already exists!"

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return redirect('/login')

    return render_template("register.html")


@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect("/login")


# ---------- BUS ----------
@app.route('/buses')
def buses():
    if "user" not in session: return redirect('/login')
    data = Bus.query.all()
    return render_template("buses.html", buses=data)


@app.route('/book_bus/<id>', methods=['GET','POST'])
def book_bus(id):
    if "user" not in session: return redirect('/login')
    bus = Bus.query.get(id)

    if request.method=="POST":
        seats = int(request.form['seats'])
        total = seats * bus.price

        booking = Booking(user=session['user'], transport_type="Bus",
                          transport_name=bus.name, source=bus.source,
                          destination=bus.destination, seats=seats,
                          total_price=total)

        db.session.add(booking)
        db.session.commit()
        return redirect('/bookings')

    return render_template("book_bus.html", bus=bus)


# ---------- TRAIN ----------
@app.route('/trains')
def trains():
    if "user" not in session: return redirect('/login')
    data = Train.query.all()
    return render_template("trains.html", trains=data)


@app.route('/book_train/<id>', methods=['GET','POST'])
def book_train(id):
    if "user" not in session: return redirect('/login')
    train = Train.query.get(id)

    if request.method=="POST":
        seats = int(request.form['seats'])
        total = seats * train.price

        booking = Booking(user=session['user'], transport_type="Train",
                          transport_name=train.name, source=train.source,
                          destination=train.destination, seats=seats,
                          total_price=total)
        db.session.add(booking)
        db.session.commit()
        return redirect('/bookings')

    return render_template("book_train.html", train=train)


# ---------- BOOKINGS ----------
@app.route('/bookings')
def get_bookings():
    if "user" not in session: return redirect('/login')
    data = Booking.query.filter_by(user=session['user']).all()
    return render_template("bookings.html", bookings=data)

# ---------- BOOKINGS ----------
@app.route('/cancel/<int:id>')
def cancel_ticket(id):
    if "user" not in session:
        return redirect('/login')

    booking = Booking.query.get_or_404(id)

    if booking.user != session['user']:
        return "Unauthorized!"

    booking.status = "Cancelled"
    db.session.commit()

    return redirect('/bookings')

#pdf ticket

@app.route('/ticket/<int:id>')
def ticket(id):
    if "user" not in session:
        return redirect('/login')

    booking = Booking.query.get_or_404(id)

    if booking.user != session['user']:
        return "Unauthorized!"

    return render_template("ticket.html", booking=booking)



if __name__ == "__main__":
    app.run(debug=True)
