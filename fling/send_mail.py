import smtplib
import getpass

smtpObj = smtplib.SMTP_SSL('smtp.gmail.com', 465)
my_id = "flingairlines@gmail.com"
my_pass = "0medaniu$%(FL!NG"
smtpObj.login(my_id, my_pass)

recip = ["zedxin0@gmail.com"]
msg = "Congratulations!\nYour seat is booked. Check with your Card Authenticator to confirm."
smtpObj.sendmail(my_id, recip, msg)
