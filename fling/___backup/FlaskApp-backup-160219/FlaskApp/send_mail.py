import smtplib
import getpass

smtpObj = smtplib.SMTP_SSL('smtp.gmail.com', 465)
my_id = "zedleaf0@gmail.com"
my_pass = getpass.win_getpass('Password: ')
smtpObj.login(my_id, my_pass)

recip = input("Recipient: ")
msg = input("Message:\n")
smtpObj.sendmail(my_id, recip, msg)

smtpObj.quit()
