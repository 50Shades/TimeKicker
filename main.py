# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Tue May 12 14:04:59 2015
#	  by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui, uic
import pwd, grp
import pickle, operator

form_class = uic.loadUiType("main.ui")[0]			   # Load the UI
dial1 = uic.loadUiType("dial1.ui")[0]				 	# Load the UI

class MyForm(QtGui.QDialog, dial1):

	def __init__(self, parent=None, id_profile = None):
		QtGui.QWidget.__init__(self, parent)
		self.setupUi(self)
		self.data = parent.data
		
		#print parent.data['profiles']
		self.id_profile = id_profile
		print self.id_profile
		#QtCore.QObject.connect(self.ui.pushButton, QtCore.SIGNAL('clicked()'), self.popup)	 
		if (id_profile):
			self.load_data()
	
	def set_combobox(self,combo,val):
		val = str(val)
		index = combo.findText(val)
		if(index != -1):
			combo.setCurrentIndex(index)

	def load_data(self):
	  
		self.name.setText(self.data['profiles'][self.id_profile]['name'])
		
		self.set_combobox(self.no_type,self.data['profiles'][self.id_profile]['not'])
		self.set_combobox(self.no_interval,self.data['profiles'][self.id_profile]['noi'])
		self.set_combobox(self.logout_type,self.data['profiles'][self.id_profile]['lot'])
	  
		sett = self.data['profiles'][self.id_profile]['settings']
		self.su_banned.setText(sett[1]['banned'])
		self.mo_banned.setText(sett[2]['banned'])
		self.tu_banned.setText(sett[3]['banned'])
		self.we_banned.setText(sett[4]['banned'])
		self.th_banned.setText(sett[5]['banned'])
		self.fr_banned.setText(sett[6]['banned'])
		self.sa_banned.setText(sett[7]['banned'])

		for a in range(7):
			index = a + 1
			if (index == 1):
			  comboH = self.su_hours
			  comboM = self.su_mins
			elif (index == 2):
			  comboH = self.mo_hours
			  comboM = self.mo_mins
			elif (index == 3):
			  comboH = self.tu_hours
			  comboM = self.tu_mins
			elif (index == 4):
			  comboH = self.we_hours
			  comboM = self.we_mins
			elif (index == 5):
			  comboH = self.th_hours
			  comboM = self.th_mins
			elif (index == 6):
			  comboH = self.fr_hours
			  comboM = self.fr_mins
			elif (index == 7):
			  comboH = self.sa_hours
			  comboM = self.sa_mins

			if(sett[index]['time'] != "None"):
				self.set_combobox(comboH, int(sett[index]['time']) / 60)
				self.set_combobox(comboM, int(sett[index]['time']) % 60)

		
	def new_profile(self,new_id):
		name = self.name.text()
		
		notif = self.no_type.currentText()
		notifi = self.no_interval.currentText()
		logout = self.logout_type.currentText()
		
		su_banned = self.su_banned.text()
		mo_banned = self.mo_banned.text()
		tu_banned = self.tu_banned.text()
		we_banned = self.we_banned.text()
		th_banned = self.th_banned.text()
		fr_banned = self.fr_banned.text()
		sa_banned = self.sa_banned.text()
		
		su_time = str(int(self.su_hours.currentText())*60+int(self.su_mins.currentText()))
		mo_time = str(int(self.mo_hours.currentText())*60+int(self.mo_mins.currentText()))
		tu_time = str(int(self.tu_hours.currentText())*60+int(self.tu_mins.currentText()))
		we_time = str(int(self.we_hours.currentText())*60+int(self.we_mins.currentText()))
		th_time = str(int(self.th_hours.currentText())*60+int(self.th_mins.currentText()))
		fr_time = str(int(self.fr_hours.currentText())*60+int(self.fr_mins.currentText()))
		sa_time = str(int(self.sa_hours.currentText())*60+int(self.sa_mins.currentText()))


		self.data['profiles'][new_id] = {"id" : str(new_id), "name" : name, "not" : notif, "noi" : notifi, "lot" : logout,  "settings" : {
								1 : {"banned" : su_banned, "time" : su_time}, 
								2 : {"banned" : mo_banned, "time" : mo_time}, 
								3 : {"banned" : tu_banned, "time" : tu_time}, 
								4 : {"banned" : we_banned, "time" : we_time}, 
								5 : {"banned" : th_banned, "time" : th_time}, 
								6 : {"banned" : fr_banned, "time" : fr_time}, 
								7 : {"banned" : sa_banned, "time" : sa_time}
							}}
	
	def accept(self):
		if not (self.id_profile):
			new_id = max(self.data['profiles'].iteritems(), key=operator.itemgetter(0))[0]+1
			print "Adding new profile with ID:",new_id
			self.new_profile(new_id)
		else:
			print "Editing profile with ID:",self.id_profile
			self.new_profile(self.id_profile)
		self.close()


class MyWindowClass(QtGui.QMainWindow, form_class):
	def __init__(self, parent=None):
		self.data = self.reload_data()
		QtGui.QMainWindow.__init__(self, parent)
		self.setupUi(self)
		self.actionQuit.triggered.connect(self.quit)
		#self.statistics_btn.clicked.connect(self.show_stats)
		#self.profiles_overview_btn.clicked.connect(self.show_dial1)
		### Profiles
		self.btn_profiles_edit.clicked.connect(self.edit_profiles)
		self.btn_profiles_add.clicked.connect(self.add_profiles)
		self.btn_profiles_delete.clicked.connect(self.delete_profiles)
		### Profiles
		self.btn_uprofiles_assign.clicked.connect(self.edit_user_profiles)
		self.btn_uprofiles_delete.clicked.connect(self.delete_user_profiles)
		#self.btn_CtoF.clicked.connect(self.btn_CtoF_clicked)  # Bind the event handlers
		#self.btn_FtoC.clicked.connect(self.btn_FtoC_clicked)  #   to the buttons
		self._dialog = None
		
		self.fill_profiles()
		self.fill_user_profiles()

	######################################################################################
	def reload_data(self):
		all_data = {'profiles' :
						{5 :
							{"id" : "5", "name" : "Profile name", "not" : "KDE", "noi" : "10", "lot" : "Soft",  "settings" : {
								1 : {"banned" : "1230-1630", "time" : "80"}, 
								2 : {"banned" : "1330-1730", "time" : "70"}, 
								3 : {"banned" : "1430-1830", "time" : "60"}, 
								4 : {"banned" : "1530-1930", "time" : "50"}, 
								5 : {"banned" : "1630-2030", "time" : "40"}, 
								6 : {"banned" : "1730-2130", "time" : "30"}, 
								7 : {"banned" : "1830-2230", "time" : "20"}
							}},
						6 :
							{"id" : "6", "name" : "Childrens", "not" : "PyQt", "noi" : "5", "lot" : "Hard", "settings" : {
								1 : {"banned" : "1230-1630", "time" : "80"}, 
								2 : {"banned" : "1330-1730", "time" : "70"}, 
								3 : {"banned" : "1430-1830", "time" : "60"}, 
								4 : {"banned" : "1530-1930", "time" : "50"}, 
								5 : {"banned" : "1630-2030", "time" : "40"}, 
								6 : {"banned" : "1730-2130", "time" : "30"}, 
								7 : {"banned" : "1830-2230", "time" : "20"}
							}}
						},
					'user_profiles' :
						{1000:5 , 155:6},
					'group_profiles' :
						{1000:5 , 155:5}
					}
		pickle.dump( all_data, open( "config.p", "wb" ) )
		return pickle.load( open( "config.p", "rb" ) )

	def save_data(self):
		pickle.dump( self.data, open( "config.p", "wb" ) )
		#return pickle.load( open( "config.p", "rb" ) )
	######################################################################################
	####################### PROFILES #####################################################
	# Filling profile table with data
	def fill_profiles(self):
		# Read all filters from PICKEL and show
		self.table_profiles.setRowCount(0)
		entries = []
		for a in self.data['profiles']:
			entries.append((self.data['profiles'][a]['id'],self.data['profiles'][a]['name']))

		self.table_profiles.setRowCount(len(entries))
		self.table_profiles.setColumnCount(len(entries[0]))
		for i, row in enumerate(entries):
			for j, col in enumerate(row):
				#print i, j, col
				item = QtGui.QTableWidgetItem(col)
				self.table_profiles.setItem(i, j, item)

	# Edit existin profile for time managemant
	def edit_profiles(self):
		prof_row = self.table_profiles.currentIndex().row()
		# If profile is selected in table
		if (prof_row >= 0):
			print "Editing profile ID:",self.table_profiles.item(prof_row,0).text()
		else:
			return
		id_prof = int(self.table_profiles.item(prof_row,0).text())
		myapp= MyForm(self,id_prof)
		myapp.exec_()
		self.save_data()
		self.fill_profiles()

	# Delete profiles - recursively with all settings
	def delete_profiles(self):
		prof_row = self.table_profiles.currentIndex().row()
		# If profile is selected in table
		if (prof_row >= 0):
			print "Delete profile ID:",self.table_profiles.item(prof_row,0).text()
		else:
			return
		
		pid = int(self.table_profiles.item(prof_row,0).text())
		del self.data['profiles'][pid]
		self.save_data()
		self.fill_profiles()
		
		# Modal windows YES OR NO ...

	def add_profiles(self):
		myapp= MyForm(self,None)
		myapp.exec_()
		
		# print myapp.su_banned.text()
		# self.data['profiles'][new_id] = {"id" : str(new_id), "name" : "Coca cola"+str(new_id), "settings" : {"monday" : "1230-1630"}}
		self.save_data()
		self.fill_profiles()
		pass
	######################################################################################
	####################### USER PROFILES ################################################
	# Filling profile table with data
	def fill_user_profiles(self):
		# Find all users and by user ID read pickle and assign
		entries = []

		for p in pwd.getpwall():
			if p[2] >= 1000:
				print p[0], grp.getgrgid(p[3])[0], p[2]
				entries.append((str(p[2]),p[0],"None"))
		
		# Read all filters from PICKEL and show
		self.table_user_profiles.setRowCount(len(entries))
		self.table_user_profiles.setColumnCount(len(entries[0]))
		for i, row in enumerate(entries):
			for j, col in enumerate(row):
				#print i, j, col
				item = QtGui.QTableWidgetItem(col)
				self.table_user_profiles.setItem(i, j, item)

	# Edit existin profile for time managemant
	def edit_user_profiles(self):
		prof_row = self.table_user_profiles.currentIndex().row()
		# If profile is selected in table
		if (prof_row >= 0):
			print "Editing user filter settings:",self.table_user_profiles.item(prof_row,0).text()
		else:
			return
	
	# Delete profiles - recursively with all settings
	def delete_user_profiles(self):
		prof_row = self.table_user_profiles.currentIndex().row()
		# If profile is selected in table
		if (prof_row >= 0):
			print "Delete user filter settings:",self.table_user_profiles.item(prof_row,0).text()
		else:
			return	
	######################################################################################
	def quit(self):
		print "exit"
		sys.exit()
		
	def show_stats(self):
		print "Stats"
		if self._dialog is None:
			self._dialog = QtGui.QDialog(self)
			self._dialog.resize(200, 100)
			self._dialog.setModal(True)
		self._dialog.show()
		
	def show_dial1(self):
		myapp= MyForm(self)
		myapp.show()
 
	def btn_FtoC_clicked(self):				  # FtoC button event handler
		fahr = self.spinFahr.value()			 #
		cel = (fahr - 32)						 #
		self.editCel.setText(str(cel))		   #
 
app = QtGui.QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()