from flask import Flask, render_template, request, url_for, redirect, flash

from wtforms import Form, TextField, DateField, PasswordField, validators
from wtforms.validators import DataRequired, Length
from passlib.hash import sha256_crypt

from cms import content
from MySQLdb import escape_string as thwart
from dbconn import connection

import datetime
import gc

DEST_DICT = content()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")

@app.route('/flights/')
def flights():
    return render_template("flights.html")

    
#------- REG FORM -------

class regform(Form):
    fname = TextField('First Name', validators=[DataRequired(),Length(min=4, max=20)])
    lname = TextField('Last Name', validators=[DataRequired(),Length(min=4, max=20)])
    email = TextField('Email', validators=[DataRequired(),Length(min=6, max=50)])
    mob = TextField('Mob No.', validators=[DataRequired(),Length(min=10, max=14)])
    dob = DateField('Date Of Birth', format='%d-%m-%Y', validators=[DataRequired()])
    
@app.route('/registration', methods = ['GET', 'POST'])
def registration():
    try:
        form = regform(request.form)
        if request.method == "POST" and form.validate():
            fname = form.fname.data
            lname = form.lname.data
            email = form.email.data
            mob = form.mob.data
            dob = form.dob.data
            
            c, conn = connection()
            
            c.execute("insert into cinfo(c_fname, c_lname, email, mob, dob) values(%s, %s, %s, %s, %s)", (thwart(fname), thwart(lname), thwart(email), thwart(mob), dob))
            
            flash("Confirmation")
            c.close()
            conn.close()
            
            return redirect(url_for('/payment'))
        
        else:
            flash("Error")
            return render_template("registration.html", form=form)
        
    except Exception as e:
        return(str(e))


#------- PAYMENT FORM -------

class payform(Form):
    fullname = TextField('Full Name', validators=[DataRequired(),Length(min=6, max=50)])
    card = TextField('card', validators=[DataRequired(),Length(min=11, max=14)])
    cvv = TextField('cvv', validators=[DataRequired(),Length(min=2, max=3)])
    expdate = DateField('XD', format='%d-%m-%Y', validators=[DataRequired()])
    
    
@app.route('/paytest', methods = ['GET','POST'])
def paytest():
    try:
        form = payform(request.form)
        if request.method == "POST" and form.validate():
            fullname = form.fullname.data
            card = form.card.data
            cvv = form.cvv.data
            expdate = form.expdate.data
            
            c, conn = connection()
            
            c.execute("insert into payinfo(fullname, card, cvv, xd) values(%s, %s, %s, %s)", (thwart(fullname), thwart(card), thwart(cvv), expdate))
            print("Done")
            
            conn.commit()
            flash("Confirmation")
            c.close()
            conn.close()
            gc.collect()
            
            return redirect(url_for('success'))
        
        else:
            flash("Error")
            return render_template("payment.html", form=form)
        
    except Exception as e:
        return(str(e))

"""class payform(Form):
    fullname = TextField('Full Name', validators=[DataRequired(),Length(min=6, max=50)])
    card = TextField('Card No.', validators=[DataRequired(),Length(min=11, max=14)])
    cvv = TextField('CVV', validators=[DataRequired(),Length(min=3, max=3)])
    expdate = DateField('Expiry Date', validators=[DataRequired()])


@app.route('/payment', methods = ['GET','POST'])
def payment():
    try:
        form = payform(request.form)
        if request.method == "POST" and form.validate():
            fullname = form.fullname.data
            card = form.card.data
            cvv = form.cvv.data
            expdate = form.expdate.data
            
            #c, conn = connection()
            
            query = c.execute("insert into payinfo (fullname, card, cvv, expdate) values(%s, %d, %d, %s)", (thwart(fullname), thwart(card), cvv, expdate))
            
            conn.commit()

            flash("Confirmation")
            c.close()
            conn.close()
            gc.collect()
            return redirect(url_for('success'))

        else:
            flash("Error!")
            return render_template("payment.html", form=form)
            
    except Exception as e:
        return(str(e))"""
        
        
@app.route('/success', methods = ['GET','POST'])
def success():
    return render_template("success.html")


@app.route('/test/')
def test():
    return render_template("test.html", DEST_DICT = DEST_DICT)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error-404.html")
    
@app.errorhandler(500)
def page_not_found(e):
    return render_template("error-500.html")

    
if __name__=="__main__":
    app.secret_key = 'L34F'
    app.run(debug=True)
