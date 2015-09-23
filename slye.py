# slye.py
# T. Wyitt Carlile
# ver.1.0.0. - June 19, 2014

from random import randrange
from graphics import GraphWin, Point, Text

from button import Button			#(win, center, width, height, label)
from dieview import DieView			#(win, center, size, type)
from player import Player			#() - named with the rename method


def main():
	#create the application window
	win = GraphWin("Slye's Dyce", 1200, 800)
	win.setCoords(0, 0, 120, 80)	

	type = gettype(win)
	playsummary(win,type)
	playgame(win, type)


def gettype(win):
	# Displays game choice for player
	# Returns the game type selected by player
	
	type = 0
	
	title1 = Text(Point(60,55),"Slye's Dyce is a wagering dice game.")
	title1.draw(win)
	title2 = Text(Point(60,45),"Would you like to play against the House or Others?")
	title2.draw(win)
	
	title3 = Text(Point(30,20),"Vs. House Coming Soon")
	title3.draw(win)
	
	housebutton = Button(win, Point(30, 30), 15, 7.5, "House")
#	housebutton.activate()
	otherbutton = Button(win, Point(90, 30), 15, 7.5, "Others")
	otherbutton.activate()
	
	pt = win.getMouse()
	while not housebutton.clicked(pt) or not otherbutton.clicked(pt):
		if housebutton.clicked(pt):
			housebutton.destroy()
			otherbutton.destroy()
			title1.undraw()
			title2.undraw()
			title3.undraw()
			return 0
		if otherbutton.clicked(pt):
			housebutton.destroy()
			otherbutton.destroy()
			title1.undraw()
			title2.undraw()
			title3.undraw()
			return 1
		pt = win.getMouse()

	
def playsummary(win,type):	

	if type == 0:
		# Placeholder would print the rules summary for the against the house version
		rule = Text(Point(60,50),"Rules placeholder 1")
#		rule.draw(win)
	else:
		# Rules summary for play against other players
		rule2 = [Text(Point(60,62.5),"Slye's Dice is a wagering dice game where the players take turns rolling"),
				 Text(Point(60,60),"five 6-sided dice in an attempt to roll the arbitrary number."),
				 Text(Point(60,57.5),"Each player is allowed three attempts."),
				 Text(Point(60,55),"If the arbitrary number appears on any of the dice, the player stops rolling."),
				 Text(Point(60,52.5),"The player's dice are totaled and that number is the player's score or hand."),
				 Text(Point(60,47.5),"If the arbitrary number is low (1-3), then a high score is preferable."),
				 Text(Point(60,45),"If the arbitrary number is high (4-6), then a low score is preferred."),
				 Text(Point(60,40),"The first player to make a hand is allowed to start the betting."),
				 Text(Point(60,37.5),"All subsequent players must match that bet in order to continue playing in the round."),
				 Text(Point(60,35),"Subsequent players that beat the previous player's score may raise the bet."),
				 Text(Point(60,30),"The first player with the best score wins the round."),
				 Text(Point(60,25),"In the event that no one makes a hand in a round, the ante is carried over."),
				 Text(Point(60,20),"Each player starts with 200 coins with which to ante and wager.")]
		for i in range(13):
			rule2[i].draw(win)
	
	continuebutton = Button(win, Point(60,10), 15, 7.5, "Continue")
	continuebutton.activate()

	pt = win.getMouse()
	while not continuebutton.clicked(pt):
		pt = win.getMouse()

	for i in range(13):
		rule2[i].undraw()
	continuebutton.destroy()	
	
def playgame(win, type):

	win.setBackground("forest green")	
	
	# call to function to get number of players and class player for each	
	numplayers, players = getplayers(win)
	
	nomlabels = [Text(Point(110,50),players[0].getname()),Text(Point(110,45),players[1].getname()),Text(Point(110,40),players[2].getname()),
				 Text(Point(110,35),players[3].getname()),Text(Point(110,30),players[4].getname()),Text(Point(110,25),players[5].getname())]
	for i in range(numplayers):
		nomlabels[i].setSize(15)
		nomlabels[i].setStyle('bold')
		nomlabels[i].setTextColor('white')
		nomlabels[i].draw(win)
	quitbutton = Button(win, Point(110,5), 7,5, "Quit")	

	# plays one series of rounds equal to the number of players,
	# where each player has a go at rolling first
	pt = win.getMouse()
	while not quitbutton.clicked(pt):	
		carryover = 0
	
		for i in range(numplayers):
			starter = i
			carryover = playoneround(win, type, numplayers, players, starter, carryover)	
		
		
		coinlabels = refreshplayers(players)	
		for i in range(numplayers): coinlabels[i].draw(win)	
	

		againmsg = Text(Point(50,50),"Play another series of round?")
		againmsg.setTextColor('white')
		againmsg.setSize(15)
		againmsg.setStyle('bold')
		againmsg.draw(win)

		againbutton = Button(win, Point(35,40), 15,7.5,"Again")
		againbutton.activate()
		quitbutton.activate()

		pt = win.getMouse()
		if againbutton.clicked(pt):
			againbutton.destroy()
			quitbutton.deactivate()
			for i in range(numplayers): 
				coinlabels[i].undraw()
			againmsg.undraw()
		pt = win.getMouse()
	
	win.close()

def playoneround(win, type, numplayers, players, starter, carryover): 

	bet = 0
	last = 0
	winner = 6

	highlow = [Text(Point(25,70),"High"), Text(Point(25,70),"Low")]
	for i in range(2):
		highlow[i].setSize(20)
		highlow[i].setStyle('bold')
	highlow[0].setTextColor('red')
	highlow[1].setTextColor('blue')

	coinlabels = refreshplayers(players)	
	
	for i in range(numplayers):
		coinlabels[i].draw(win)
	
	arbitrary = Text(Point(18,77),"Arbitrary Number")
	arbitrary.setSize(15)
	arbitrary.setStyle('bold')
	arbitrary.draw(win)
	# sets the arbitrary number die
	adie = DieView(win, Point(10,70),8,1)
	adie.build()
	adie.roll()	
	if adie.getValue() > 3:
		top = 31
		adie.recolor(2)
		highlow[1].draw(win)
	else:
		top = 0
		adie.recolor(1)
		highlow[0].draw(win)

	ante = anteup(win, players, numplayers)	

	pot = ante + bet + carryover

	potmsg = Text(Point(105,75),"{0}".format(pot))
	potmsg.setSize(20)
	potmsg.setTextColor('yellow')
	potmsg.setStyle('bold')
	potmsg.draw(win)

	# These three lines update the coin counts for the players
	for i in range(numplayers): coinlabels[i].undraw()
	coinlabels = refreshplayers(players)
	for i in range(numplayers): coinlabels[i].draw(win)

	for i in range(numplayers):
		if (starter + i) >= numplayers:
			whosgo = starter + i - numplayers
		else:
			whosgo = starter + i
		roll, made, folded, bet, top, last, winner = oneturn(win, players, whosgo, adie, bet, top, last, numplayers, winner)
		for i in range(numplayers): coinlabels[i].undraw()
		coinlabels = refreshplayers(players)
		for i in range(numplayers): coinlabels[i].draw(win)
		pot = ante + bet + carryover
		potmsg.undraw()
		potmsg = Text(Point(105,75),"{0}".format(pot))
		potmsg.setSize(20)
		potmsg.setTextColor('yellow')
		potmsg.setStyle('bold')
		potmsg.draw(win)
		
	if winner == 6:
		carryover = pot
		winlabel = Text(Point(50,50),"No one won this round.")
		winlabel.draw(win)
	else:
		players[winner].update(pot)
		winlabel = Text(Point(50,50),"{0} won the round.".format(players[winner].getname()))
		winlabel.draw(win)
		
	win.getMouse()
#	for i in range(numplayers): coinlabels[i].undraw()
#	coinlabels = refreshplayers(players)
#	for i in range(numplayers): coinlabels[i].draw(win)
		
	potmsg.undraw()
	for i in range(2):
		highlow[i].undraw()
	for i in range(numplayers): coinlabels[i].undraw()
	winlabel.undraw()
	return carryover


def oneturn(win, players, whosgo, adie, bet, top, last, numplayers, winner):
	# Draw the interface widgets
	dice = [DieView(win, Point(20,40), 10,0), DieView(win, Point(35,40), 10,0), DieView(win, Point(50,40), 10,0),
   			DieView(win, Point(65,40), 10,0), DieView(win, Point(80,40), 10,0)]

	curplayer = Text(Point(15,55), "Current Player: {0}".format(players[whosgo].getname()))
	curplayer.draw(win)
	
	made = 0
	folded = 0
	roll = 0
	playing = numplayers
	last += 1

#	for i in range(6):
#		if anted[i] == True:
#			playing = playing + 1

	wager = Text(Point(70,60),"{0}".format(bet))
	wager.setSize(15)
	wager.setStyle('bold')
	wager.setTextColor('white')
	wager.draw(win)	

	tobeat = Text(Point(60, 75), "{0}".format(top))
	tobeat.setStyle('bold')
	tobeat.setTextColor('white')
	tobeat.setSize(20)
	tobeat.draw(win)
	
	# This section checks if there is a wager in place that must be matched
	if bet > 0:	
		matchbutton = Button(win, Point(35,40), 15, 7.5, "Match Bet")
		matchbutton.activate()
		foldbutton = Button(win, Point(65,40),15, 7.5, "Fold")
		foldbutton.activate()
		
		pt = win.getMouse()
		while not matchbutton.clicked(pt) or not foldbutton.clicked(pt):
			if matchbutton.clicked(pt):
				players[whosgo].update(-bet)
				bet = bet *2
				wager.undraw()
				wager = Text(Point(70,60),"{0}".format(bet))
				wager.setSize(15)
				wager.setStyle('bold')
				wager.setTextColor('white')
				wager.draw(win)
				matchbutton.destroy()
				foldbutton.destroy()
				break
			if foldbutton.clicked(pt):
				folded = 1
				matchbutton.destroy()
				foldbutton.destroy()
				break
			pt = win.getMouse()
			
	if folded == 0:
		count = 0		
		rollbutton = Button(win, Point(50,25), 10, 5, "Roll Dice")
		rollbutton.activate()
		rollmsg = Text(Point(15,50),"{0}".format(count))
		rollmsg.draw(win)

		pt = win.getMouse()
		while count < 3:
			if rollbutton.clicked(pt):
				count += 1
				rollmsg.undraw()
				rollmsg = Text(Point(15,50),"{0}".format(count))
				rollmsg.draw(win)
				for i in range(5):
					if dice[i].exists() == 1:
						dice[i].roll()
					else:
						dice[i].build()
						dice[i].roll()
				
				for n in range(5):
					if dice[n].getValue() == adie.getValue():
						rollbutton.deactivate()
						made = 1
						if adie.getValue() > 3:
							dice[n].recolor(2)
						else:
							dice[n].recolor(1)
#						break
				if made == 1:
					for k in range(5):
						roll = roll + dice[k].getValue()
					break							
				if count == 3:
					break
			pt = win.getMouse()
		rollbutton.destroy()
	
		if made == 1:
			if (adie.getValue() > 3 and roll < top) or (adie.getValue() < 4 and roll > top):
				top = roll
				winner = whosgo
				tobeat.undraw()
				tobeat = Text(Point(60, 75), "{0}".format(top))
				tobeat.setStyle('bold')
				tobeat.setTextColor('white')
				tobeat.setSize(20)
				tobeat.draw(win)

				if last < playing:
					mademsg = Text(Point(50,55),"You dice value is {0}".format(roll))
					mademsg.draw(win)
					betmsg = Text(Point(50,50),"Would you like to place a wager?")
					betmsg.draw(win)
			
					betbutton = Button(win, Point(40,25), 10, 5, "Bet")
					betbutton.activate()
						
					donebutton = Button(win, Point(60,25), 10, 5, "Done")
					donebutton.activate()

					pt = win.getMouse()
					while not donebutton.clicked(pt):
						if betbutton.clicked(pt):
							bet = bet + 1
							players[whosgo].update(-1)
							wager.undraw()
							wager = Text(Point(70,60),"{0}".format(bet))
							wager.setSize(15)
							wager.setStyle('bold')
							wager.setTextColor('white')
							wager.draw(win)
						pt = win.getMouse()
				
					mademsg.undraw()
					betmsg.undraw()
					wager.undraw()	
					donebutton.destroy()
					betbutton.destroy()
					for i in range(5):
						dice[i].destroy()
						
				else:
					mademsg = Text(Point(50,55),"You dice value is {0}".format(roll))
					mademsg.draw(win)
					youwin = Text(Point(50,50),"You've won the round!")
					youwin.draw(win)
					
					nextbutton = Button(win, Point(60,25), 10, 5, "Next")
					nextbutton.activate()
					
					pt = win.getMouse()
					while not nextbutton.clicked(pt):
						pt = win.getMouse()

					wager.undraw()
					mademsg.undraw()
					youwin.undraw()	
					nextbutton.destroy()
					for i in range(5):
						dice[i].destroy()
					
										
			else:
				nottop = Text(Point(50,55), "Sorry, you didn't beat the score.")
				nottop.draw(win)
			
				nextbutton = Button(win, Point(60,25), 10, 5, "Next")
				nextbutton.activate()
		
				pt = win.getMouse()
				while not nextbutton.clicked(pt):
					pt = win.getMouse()
			
				nottop.undraw()
				wager.undraw()	
				nextbutton.destroy()
				for i in range(5):
					dice[i].destroy()
					
		else:
			nohand = Text(Point(50,55), "Sorry, you didn't make a hand.")
			nohand.draw(win)
			
			nextbutton = Button(win, Point(60,25), 10, 5, "Next")
			nextbutton.activate()
		
			pt = win.getMouse()
			while not nextbutton.clicked(pt):
				pt = win.getMouse()
				
			nohand.undraw()
			wager.undraw()	
			nextbutton.destroy()
			for i in range(5):
				dice[i].destroy()
		
		for i in range(5):
			dice[i].destroy()
		curplayer.undraw()
		wager.undraw()
		rollmsg.undraw()
		tobeat.undraw()
		return roll, made, folded, bet, top, last, winner
	else:
		curplayer.undraw()
		wager.undraw()
		tobeat.undraw()
		return roll, made, folded, bet, top, last, winner


def getplayers(win):
	numplayers = 2
	players = [Player(),Player(),Player(),Player(),Player(),Player()]

	msgs = [Text(Point(30,45),"Two Players"), Text(Point(45,45),"Three Players"), Text(Point(60,45),"Four Players"),
			Text(Point(75,45),"Five Players"), Text(Point(90,45),"Six Players")]
	buttons = [Button(win, Point(30,35),10,5,"2"), Button(win, Point(45,35),10,5,"3"), Button(win, Point(60,35),10,5,"4"),
			   Button(win, Point(75,35),10,5,"5"), Button(win, Point(90,35),10,5,"6")]
	
	for i in range(5):
		msgs[i].draw(win)
		buttons[i].activate()

	pt = win.getMouse()
	while (not buttons[0].clicked(pt) or not buttons[1].clicked(pt) or not buttons[2].clicked(pt)
      or not buttons[3].clicked(pt) or not buttons[4].clicked(pt)):
		if buttons[0].clicked(pt):
			numplayers = 2
			break
		elif buttons[1].clicked(pt):
			numplayers = 3
			break
		elif buttons[2].clicked(pt):
			numplayers = 4
			break
		elif buttons[3].clicked(pt):
			numplayers = 5
			break
		elif buttons[4].clicked(pt):
			numplayers = 6
			break
		pt = win.getMouse()
	
	for i in range(5):
		msgs[i].undraw()
		buttons[i].destroy()

	nameprompt = Text(Point(60,50),"Please enter the player names on the command line.")
	nameprompt.draw(win)

	for i in range(numplayers):
		nom = input("Please enter the name of player {0}: ".format(i+1))
		players[i].rename(nom)
	
	nameprompt.undraw()
	return numplayers, players
	
def refreshplayers(players):

	coinlabels = [Text(Point(115,47.5),players[0].getcoin()),Text(Point(115,42.5),players[1].getcoin()),Text(Point(115,37.5),players[2].getcoin()),
				  Text(Point(115,32.5),players[3].getcoin()),Text(Point(115,27.5),players[4].getcoin()),Text(Point(115,22.5),players[5].getcoin())]
	for i in range(6):
		coinlabels[i].setSize(15)
		coinlabels[i].setStyle('bold')
		coinlabels[i].setTextColor('white')

	return coinlabels


def anteup(win, players, numplayers):
	playerante = [Text(Point(30,45),players[0].getname()),Text(Point(40,45),players[1].getname()),Text(Point(50,45),players[2].getname()),
				  Text(Point(60,45),players[3].getname()),Text(Point(70,45),players[4].getname()),Text(Point(80,45),players[5].getname())]
	antebuttons = [Button(win,Point(30,40),7,4,"Ante"), Button(win,Point(40,40),7,4,"Ante"), Button(win,Point(50,40),7,4,"Ante"), 
	 			   Button(win,Point(60,40),7,4,"Ante"), Button(win,Point(70,40),7,4,"Ante"), Button(win,Point(80,40),7,4,"Ante")]
	
	continuebutton = Button(win, Point(60,20), 15, 7.5, "Continue")
	
	anted = [False, False, False, False, False, False]
	ante = 0
	
	for i in range(numplayers):
		playerante[i].draw(win)
		antebuttons[i].activate()

	for i in range(len(antebuttons)):
		if not antebuttons[i].getactive():
			antebuttons[i].destroy()

	pt = win.getMouse()
	while not continuebutton.clicked(pt):
		if (antebuttons[0].getactive() == False and antebuttons[1].getactive() == False and 
		    antebuttons[2].getactive() == False and antebuttons[3].getactive() == False and
			antebuttons[4].getactive() == False and antebuttons[5].getactive() == False):
			continuebutton.activate()
		if antebuttons[0].clicked(pt):
			players[0].update(-1)
			anted[0] = True
			ante = ante + 1
			antebuttons[0].deactivate()
		if antebuttons[1].clicked(pt):
			players[1].update(-1)
			anted[1] = True
			ante = ante + 1
			antebuttons[1].deactivate()
		if antebuttons[2].clicked(pt):
			players[2].update(-1)
			anted[2] = True
			ante = ante + 1
			antebuttons[2].deactivate()
		if antebuttons[3].clicked(pt):
			players[3].update(-1)
			anted[3] = True
			ante = ante + 1
			antebuttons[3].deactivate()			
		if antebuttons[4].clicked(pt):
			players[4].update(-1)
			anted[4] = True
			ante = ante + 1
			antebuttons[4].deactivate()
		if antebuttons[5].clicked(pt):
			players[5].update(-1)
			anted[5] = True
			ante = ante + 1
			antebuttons[5].deactivate()			
		pt = win.getMouse()
		
	for i in range(numplayers):
		playerante[i].undraw()
		antebuttons[i].destroy()
	continuebutton.destroy()
	return ante							# anted option for later iteration 
	
		

if __name__ == '__main__': main()