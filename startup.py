#!/usr/bin/python

import getpass
import os, sys, pwd
import grp
import pickle
import datetime
import time as t
from os.path import expanduser
import os.path
import operator 

# Predelam limity na dnesek
# CanLog - podle dnesnich limitu
# HasTime - zda jeste ma nejaky cas

# Skript se pusti po startu
# Vycte si z domaci slozky uzivatele PICKLE soubor s nastavenim
# Zjisti, zda muze byt uzivatel prihlasen
# Na zaklade vysledku bud uzivatele odhlasi (bacha na rerun skript po prihlaseni) nebo pusti smycku cekani a prepisu

# Notification po prihlaseni
# Notification kazdych X minut




# Pokud neexistuje, tak ho zapiseme
# Pokud existuje, tak otevreme pickle, najdeme nejvyssi zapis, bereme o jednu vyssi, zapiseme a kazdou minutu inkrementujeme




def check_stats(home):
  data = {0 : "00-00-0000"}
  if not (os.path.isfile(home+"/.tk_stats.p")):
	pickle.dump(data,open(home+"/.tk_stats.p","wb"))

def check_data(home):
  data = {}
  if not (os.path.isfile(home+"/.tk_settings.p")):
	pickle.dump(data,open(home+"/.tk_settings.p","wb"))

def get_username():
    return pwd.getpwuid(os.getuid())

def print_dialog(head, message):
  # KDE 3+
  #os.system("kdialog --title '"+head+"' --passivepopup '"+message+"' 3")
  os.system("notify-send '"+head+"' '"+message+"' --icon=dialog-information")

###############################################################################
username = getpass.getuser()
userid = os.getuid()
now = datetime.datetime.now()
home = expanduser("~")

check_stats(home)
check_data(home)

data = pickle.load(open(home+"/.tk_settings.p","rb"))	# Nactu konfiguraci uzivatele
stats = pickle.load(open(home+"/.tk_stats.p","rb"))

if (data == {}):
	sys.exit()

stats_id = max(stats.iteritems(), key=operator.itemgetter(0))[0]+1
print stats_id

stats[stats_id] = {"date" : str(now.day)+"."+str(now.month)+"."+str(now.year),"time" : 1}

print stats

today_day = (now.weekday()+2)%7
manage_today = data['settings'][today_day]['banned']
time = data['settings'][today_day]['time']
print "Use of pc for today: ",time
today = now.strftime("%d-%m-%y")

###############################################################################
# Pokud skript dnes jeste nebezel, tak prepiseme aktualni hodnoty

if not ('current_day' in data):
  data['current_day'] = -1
  data['today_limit'] = -1
  
if (data['current_day'] != today):
  print "Prenastavuji limity"
  data['current_day'] = today
  data['today_limit'] = time
  
###############################################################################
# Pokud se uzivatel muze prihlasit v tuto hodinu
hour_range = []
can_use = 1
now_time = int(str(now.hour)+str(now.minute))
for a in manage_today.split(","):
  interval = a.split("-")
  if (now_time > int(interval[0]) and now_time > int(interval[1])):
	can_use = 0
  print a

print now_time
#print hour_range, now.hour

if (can_use):
  print "Muze ze prihlasit"
else:
  print "Logout!!"
# <LOGOUT>

time = int(data['today_limit'])

###############################################################################
# Dialog po prihlaseni
head = "Welcome user "+get_username()[4]
message = "You have only "+str(time)+" minutes left for today."
print_dialog(head,message)
###############################################################################

while (time > 0):
  t.sleep(5)
  time = time - 1
  data['today_limit'] = time
  pickle.dump(data,open(home+"/.tk_settings.p","wb"))
  stats[stats_id]['time'] = stats[stats_id]['time'] + 1
  pickle.dump(stats,open(home+"/.tk_stats.p","wb"))
  head = "Time is going down"
  message = "You have only "+str(time)+" minutes left!"
  print_dialog(head,message)

# Logout user
# os.system("dbus-send --session --dest=org.kde.ksmserver --type=method_call --print-reply /KSMServer org.kde.KSMServerInterface.logout int32:0 int32:0 int32:0")