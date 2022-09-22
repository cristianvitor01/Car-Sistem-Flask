from flask import Flask, render_template, redirect, url_for, flash, abort, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email
from sqlalchemy.sql.expression import func

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ce4288ac61ec58ef3cb244e94d46ec8c'

bootstrap = Bootstrap5(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ---- Tabelas ----
class Person(db.Model):
    __tablename__ = "persons"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    age = db.Column(db.String(250), nullable=False)
    address = db.Column(db.String(250), nullable=False)

    cars = db.relationship("Car", back_populates="owner")


class Car(db.Model):
    __tablename__ = "cars"
    id = db.Column(db.Integer, primary_key=True)

    owner_id = db.Column(db.Integer, db.ForeignKey("persons.id"))
    owner = db.relationship("Person", back_populates="cars")

    title = db.Column(db.String(250), unique=True, nullable=False)
    model = db.Column(db.String(250), nullable=False)
    color = db.Column(db.String(250), nullable=False)


COLOR_CHOICES = [('yellow', 'yellow'), ('blue', 'blue'), ('grey', 'grey')]
MODEL_CHOICES = [('hatch', 'hatch'), ('sedan', 'sedan'), ('convertible', 'convertible')]


def person_choices():
    persons = Person.query.all()
    person_name_lst = [(person.name, person.name) for person in persons]
    print(person_name_lst)
    return person_name_lst


# ---- Formulaŕios ----
class AssignForm(FlaskForm):
    person = SelectField("", choices=person_choices, validators=[DataRequired()])
    title = StringField("Titulo", validators=[DataRequired()])
    color = SelectField("Cor", choices=COLOR_CHOICES, validators=[DataRequired()])
    model = SelectField("Modelo", choices=MODEL_CHOICES, validators=[DataRequired()])
    submit = SubmitField("Cadastrar")


class PersonForm(FlaskForm):
    name = StringField(label='Nome', validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    address = StringField(label='Endereço', validators=[DataRequired()])
    age = IntegerField(label='Idade', validators=[DataRequired()])
    submit = SubmitField(label='Cadastrar')

# ---- Rotas ----
@app.before_first_request
def create_table():
    db.create_all()


@app.route('/')
def home_view():
    persons = Person.query.all()
    return render_template('pages/opportunity-table.html', persons=persons)


@app.route('/owned-cars')
def person_owned_cars_view():
    persons = Person.query.all()
    return render_template('pages/owned-table.html', persons=persons)


@app.route('/add-person', methods=['GET', 'POST'])
def add_person_view():
    form = PersonForm()
    if form.validate_on_submit():
        new_person = Person(
            name=form.name.data,
            email=form.email.data,
            age=form.age.data,
            address=form.address.data,
        )
        db.session.add(new_person)
        db.session.commit()
        return redirect(url_for("home_view"))
    return render_template('pages/person-form.html', form=form)


@app.route('/assign', methods=['GET', 'POST'])
def assign_car_person_view():
    form = AssignForm()
    if form.validate_on_submit():
        person = form.person.data
        car_title = form.title.data
        car_color = form.color.data
        car_model = form.model.data
        print(person, car_title, car_color, car_model)
        person_data = Person.query.filter_by(name=person).first()
        if person_data:
            if len(person_data.cars) < 3:
                query = Car.query.filter_by(owner=person_data, title=car_title, color=car_color, model=car_model).first()
                if query:
                    flash('Esta pessoa já possui este carro!', 'danger')
                else:
                    new_car = Car(owner=person_data, title=car_title, color=car_color, model=car_model)
                    db.session.add(new_car)
                    db.session.commit()
                    flash('Carro adicionado ao proprietário', 'success')
            else:
                flash('Esta pessoa já tem 3 carros', 'danger')
    return render_template('pages/assign-form.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)
