#!/usr/bin/python

import sys
import fatechart
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class MythicDiceForm(QDialog):
	def __init__(self, parent=None):
		super(MythicDiceForm, self).__init__(parent)

		self.actingComboBox = QComboBox()
		self.actingComboBox.addItems(fatechart.ranklist)
		self.actingComboBox.setCurrentIndex(13)

		self.difficultyComboBox = QComboBox()
		self.difficultyComboBox.addItems(fatechart.ranklist)	
		self.difficultyComboBox.setCurrentIndex(13)

		self.oddsLabel = QLabel()
		self.updateOdds()

		self.connect(self.actingComboBox, \
			SIGNAL("currentIndexChanged(int)"),	self.updateOdds)
		self.connect(self.difficultyComboBox, \
			SIGNAL("currentIndexChanged(int)"),	self.updateOdds)

		self.outcomeLabel = QLabel("<font size=6> </font>")
		
		actingLabel = QLabel("<center><b>Acting Rank</b></center>")
		difficultyLabel = QLabel("<center><b>Difficulty Rank</b></center>")

		self.rollButton = QPushButton("Roll")
		self.connect(self.rollButton, SIGNAL("clicked()"), self.roll)

		layout = QGridLayout()
		layout.addWidget(self.outcomeLabel, 0, 0, 1, 2)
		layout.addWidget(self.oddsLabel, 1, 0, 1, 2)
		layout.addWidget(actingLabel, 2, 0)
		layout.addWidget(difficultyLabel, 2, 1)
		layout.addWidget(self.actingComboBox, 3, 0)
		layout.addWidget(self.difficultyComboBox, 3, 1)
		layout.addWidget(self.rollButton, 4, 0, 1, 2)

		self.setLayout(layout)
		self.setWindowTitle("Mythic Dice")

	def roll(self):
		# Get the ranks to roll
		act = self.actingComboBox.currentText()
		diff = self.difficultyComboBox.currentText()

		result, roll = fatechart.roll(act, diff)

		color = "black"
		if result in ("Yes", "Exceptional Yes"):
			color = "green"
		else:
			color = "red"
		outcome = "<font size=6 color=%s>%s</font>" % (color, result)
		self.outcomeLabel.setText("<center>%s  (%s)</center>" % (outcome, roll))

	def updateOdds(self):
		# Get the odds 
		vals = fatechart.get_values(self.actingComboBox.currentText(),\
				self.difficultyComboBox.currentText())
		x_yes = "-"
		yes = "-"
		x_no = "-"
		if vals[0] > 0:
			x_yes = "<font color=green>" + str(vals[0]) + "</font>"
		if vals[1] > 0:
			yes = "<b>" + str(vals[1]) + "</b>"
		if vals[1] < 100:
			x_no = "<font color=red>" + str(vals[2]) + "</b>"

		odds_text = "%s / %s / %s" % (x_yes, yes, x_no)

		self.oddsLabel.setText("<center>%s</center>" % odds_text)


app = QApplication(sys.argv)
form = MythicDiceForm()
form.show()
app.exec_()
