import os
from os import listdir
from os.path import isfile, join
import subprocess
import gzip
from distutils.spawn import find_executable
import csv


class Player(object):
	# A player that has registered for the tournament

	def __init__(self,name,ign,email,rank,elo,duo):
		self.name = name
		self.ign = ign
		self.rank = rank
		self.email = email
		self.elo = elo
		self.duo = duo

	def __repr__(self):
		return "Player()"

	def __str__(self):
		if self.duo:
			duo_text = self.duo.ign
		else:
			duo_text = ""
		text = self.name+","+self.ign+","+self.rank+","+self.elo+","+duo_text+","+self.email+"\n"

		return text
		
	def add_duo(self,partner):
		self.duo = partner



class Team(object):
	#The team
	def __init__(self, name):
		self.name = name
		self.slot1 = None
		self.slot2 = None
		self.slot3 = None
		self.slot4 = None
		self.slot5 = None

	def get_average_elo(self):
		total=0
		count=0
		if (self.slot1):
			total = total+int(self.slot1.elo)
			count = count+1
		if (self.slot2):
			total = total+int(self.slot2.elo)
			count = count+1
		if (self.slot3):
			total = total+int(self.slot3.elo)
			count = count+1
		if (self.slot4):
			total = total+int(self.slot4.elo)
			count = count+1
		if (self.slot5):
			total = total+int(self.slot5.elo)
			count = count+1

		average = total/count

		return average

	def member_count(self):
		count=0
		if (self.slot1):
			count = count+1
		if (self.slot2):
			count = count+1
		if (self.slot3):
			count = count+1
		if (self.slot4):
			count = count+1
		if (self.slot5):
			count = count+1
		return count
	
	def add_player(self,player):
		if (self.slot1):
			if (self.slot2):
				if (self.slot3):
					if (self.slot4):
						if (self.slot5):
							return false
						else:
							self.slot5 = player
					else:
						self.slot4 = player
				else:
					self.slot3 = player
			else:
				self.slot2 = player
		else:
			self.slot1 = player
			
	def __repr__(self):
		return "Team()"

	def __str__(self):
		print ("------------------------------------------------------")
		print (self.name)
		print (self.slot1)
		print (self.slot2)
		print (self.slot3)
		print (self.slot4)
		print (self.slot5)
		print ("ELO Average: " + str(self.get_average_elo()))
		print ("------------------------------------------------------")
		
def create_teams(players):
	local_list = players
	team_list = []
	if(len(local_list)%5 != 0):
		print("unable to make full teams")
		return
	number_of_teams = len(local_list)/5
	team_names= ["Islington","Dixon","Kipling","Islington2","Dixon2","Kipling2",
				"Islington3","Dixon3","Kipling3","Islington4","Dixon4","Kipling4",
				"Islington5","Dixon5","Kipling5","Islington6","Dixon6","Kipling6"
				,"Islington7","Dixon7","Kipling7","Islington8","Dixon8","Kipling8",
				"Islington9","Dixon9","Kipling9","Islington10","Dixon10","Kipling10"]
	top = 1
	for x in (0,number_of_teams):
		newTeam = Team(team_names.pop())
		while (newTeam.member_count() != 5):
			inspect_player = local_list[0]
			if(inspect_player.duo):
				if (newTeam.member_count() < 2 ):
					top = top * -1
					pass
				else:
					newTeam.add_player(inspect_player)
					duo=[x for x in local_list if x.ign.lower() == inspect_player.duo.lower()]
					duo = duo[0]
					newTeam.add_player(duo)
					local_list=[x for x in local_list if x.ign.lower() != inspect_player.ign.lower()]
					local_list=[x for x in local_list if x.ign.lower() != duo.ign.lower()]
			else:
				newTeam.add_player(inspect_player)
				local_list=[x for x in local_list if x.ign.lower() != inspect_player.ign.lower()]
				
		team_list.append(newTeam)
		print (newTeam)


		
# creating the list of participants with duos tied to them
directory = "sql2.csv"
participants = []
with open(directory) as f:
	reader = csv.reader(f)
	for row in reader:
	    name = row[0]
	    email = row[1]
	    ign = row[2]
	    rank = row[3]
	    elo = row[4]
	    if row[5]:
	    	duo = row[5]
	    else:
	    	duo = None
	    newplayer = Player(name,ign,email,rank,elo,duo)
	    participants.append(newplayer)

participants.sort(key=lambda x: int(x.elo), reverse=False)

for attendee in participants:
	if (attendee.duo):
		newduo=[x for x in participants if x.ign.lower() == attendee.duo.lower()]
		if newduo:
			attendee.add_duo(newduo[0])
		else:
			attendee.add_duo(None)

create_teams(participants)


