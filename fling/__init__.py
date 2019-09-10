from flask import Flask, render_template, request, url_for, redirect, flash

# Forms
from wtforms import Form, TextField, TextAreaField, SelectField, DateField, PasswordField, validators
from wtforms.validators import DataRequired, Length
from passlib.hash import sha256_crypt

# Content / DB
from cms import content, rate
from MySQLdb import escape_string as thwart
from dbconn import connection

# etc
import requests
import datetime
import gc

# Route Classification
NORTH5 = [ 'HK', 'TK', 'LN', 'TO' ]
SOUTH5 = [ 'NY', 'BR', 'MB', 'DB', 'BR' ]
north5 = 0
south5 = 0
cross5 = 0

source = ""
destination = ""
quantity = 0
plane = ""

RATE = rate()
CONTENT = content()

#----------------------------------------- A P P ------------------------------------------

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")

#--------- BOOKING FORM ---------

class bookform(Form):
    source = SelectField(u'Source', choices=[('NY','New York'),('BR','Brasilia'),('TO','Toronto'),('MB','Mumbai'),('TK','Tokyo'),('HK','Hong Kong'),('DB','Dubai'),('LN','London')])
    destination = SelectField(u'Destination', choices=[('TO','Toronto'),('BR','Brasilia'),('NY','New York'),('MB','Mumbai'),('TK','Tokyo'),('HK','Hong Kong'),('DB','Dubai'),('LN','London')])
    quantity = SelectField(u'Quantity', choices=[(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10)])

@app.route('/book', methods = ['GET', 'POST'])
def book():
    try:
        form = bookform(request.form)
        if request.method == "POST":
            global quantity, RATE, dist, total

            global source, destination

            source = form.source.data
            destination = form.destination.data

            quantity = int(form.quantity.data)

            global north5, south5, cross5

            if (source and destination in NORTH5 and north5 < 100 - quantity) or (source and destination in SOUTH5 and south5 < 100 - quantity) and (cross5 < 100 - quantity):

                url = 'https://www.distance24.org/route.json?stops=' + str(source) + '|' + str(destination)
                r = requests.get(url)
                dist = r.json()['distance']

                total = dist * RATE * quantity


                return redirect(url_for('billinfo'))

        else:
            return render_template("book.html", form=form)
            flash("Error!")

    except Exception as e:
        return(str(e))

#--------- BILL INFO ---------

@app.route('/billinfo', methods = ['GET', 'POST'])
def billinfo():
    if request.referrer == 'http://localhost:5000/book':
        try:
            return render_template("billinfo.html" ,dist=dist, RATE=RATE, total=total, quantity=quantity)

        except Exception as e:
            return(str(e))

    else:
        return render_template("error-404.html")


#--------- REG FORM ---------

class regform(Form):
    fname = TextField('First Name', validators=[DataRequired(),Length(min=4, max=20)])
    lname = TextField('Last Name', validators=[DataRequired(),Length(min=4, max=20)])
    email = TextField('Email', validators=[DataRequired(),Length(min=6, max=50)])
    mob = TextField('Mob No.', validators=[DataRequired(),Length(min=10, max=14)])
    dob = DateField('Date Of Birth', format='%d-%m-%Y', validators=[DataRequired()])
    sp_req = TextAreaField('Special Requests', validators=[Length(max=500)])
    
@app.route('/registration', methods = ['GET', 'POST'])
def registration():
    if request.referrer == 'http://localhost:5000/billinfo' or 'http://localhost:5000/registration':
        try:
            form = regform(request.form)
            if request.method == "POST" and form.validate():
                fname = form.fname.data
                lname = form.lname.data
                email = form.email.data
                mob = form.mob.data
                dob = form.dob.data
                sp_req = form.sp_req.data

                cursor, conn = connection()

                cursor.execute("insert into cinfo(c_fname, c_lname, email, mob, dob, sp_requests) values(%s, %s, %s, %s, %s, %s)", (thwart(fname), thwart(lname), thwart(email), thwart(mob), dob, sp_req))

                conn.commit()
                flash("Confirmation")
                cursor.close()
                conn.close()

                return redirect(url_for('payment'))

            else:
                flash("Error")
                return render_template("registration.html", form=form)
            
        except Exception as e:
            return(str(e))
    else:
        return render_template("error-404.html")

#--------- PAYMENT FORM ---------

class payform(Form):
    fullname = TextField('Full Name', validators=[DataRequired(),Length(min=6, max=50)])
    card = TextField('card', validators=[DataRequired(),Length(min=11, max=14)])
    cvv = TextField('cvv', validators=[DataRequired(),Length(min=2, max=3)])
    expdate = DateField('Expiry Date', format='%d-%m-%Y', validators=[DataRequired()])
    
    
@app.route('/payment', methods = ['GET', 'POST'])
def payment():
    if request.referrer == 'http://localhost:5000/registration' or 'http://localhost:5000/payment':
        try:
            form = payform(request.form)
            if request.method == "POST" and form.validate():
                fullname = form.fullname.data
                card = form.card.data
                cvv = form.cvv.data
                expdate = form.expdate.data
                
                c, conn = connection()

                c.execute("insert into payinfo(fullname, card, cvv, expdate) values(%s, %s, %s, %s)", (thwart(fullname), thwart(card), thwart(cvv), expdate))
                
                conn.commit()
                flash("Confirmation")
                c.close()
                conn.close()
                
                global source, destination, quantity, south5, north5, cross5, plane

                if source and destination in SOUTH5:
                    south5 += quantity

                elif source and destination in NORTH5:
                    north5 += quantity
                    plane = 'North5'

                else:
                    cross5 += quantity
                    plane = 'Cross5'

                return redirect('/success')
            
            else:
                flash("Error")
                return render_template("payment.html", form=form)
            
        except Exception as e:
            return(str(e))
    else:
        return render_template("error-404.html")
        
        
@app.route('/success', methods = ['GET','POST'])
def success():
    if request.referrer == 'http://localhost:5000/payment':
        return render_template("success.html",plane=plane, south = south5, north = north5, cross = cross5)
    else:
        return render_template("error-404.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/test/')
def test():
    return render_template("test.html", DEST_DICT = DEST_DICT)

    
#--------- ERROR HANDLING ---------
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error-404.html")
    
@app.errorhandler(500)                      #Only if website goes live
def page_not_found(e):
    return render_template("error-500.html")

    
if __name__=="__main__":
    app.secret_key = 'L34F'
    app.run(debug=True)
