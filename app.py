from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy


# Create application and connection to the database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///charging_statistics.db'
db = SQLAlchemy(app)
app.secret_key = 'XXXXXXXXXX'


# Create model of the table structure
class Stats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    charging_point_number = db.Column(db.Integer, nullable=False)
    transaction_start = db.Column(db.Text)
    charge_start = db.Column(db.Text)
    charge_end = db.Column(db.Text)
    transaction_end = db.Column(db.Text)
    start_wh = db.Column(db.Integer)
    end_wh = db.Column(db.Integer)
    total_wh = db.Column(db.Integer)
    connect_time = db.Column(db.Integer)

    # return id when created
    def __repr__(self):
        return '<Task %r>' % self.id


# Create default route
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        starting_datetime = request.form["starting_date"]
        ending_datetime = request.form["ending_date"]
        if len(starting_datetime) == 0 or len(ending_datetime) == 0:
            data = Stats.query.all()
            flash("Incorrect date limiters")
            return render_template('index.html', data=data)
        else:
            data = Stats.query \
                .filter(Stats.transaction_start >= starting_datetime) \
                .filter(Stats.transaction_end <= ending_datetime).all()
            return render_template('index.html', data=data)
    else:
        data = Stats.query.all()
        return render_template('index.html', data=data)


if __name__ == "__main__":
    app.run(debug=True)
