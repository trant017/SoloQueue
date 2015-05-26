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
			total = total+slot1.elo
			count = count+1
		if (self.slot2):
			total = total+slot2.elo
			count = count+1
		if (self.slot3):
			total = total+slot3.elo
			count = count+1
		if (self.slot4):
			total = total+slot4.elo
			count = count+1
		if (self.slot5):
			total = total+slot5.elo
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

def create_teams(players):



		
# creating the list of participants with duos tied to them
directory = "sql2.csv"
participants = []
with open(directory,'rb') as f:
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

participants.sort(key=lambda x: x.elo, reverse=False)

for attendee in participants:
	if (attendee.duo):
		newduo=[x for x in participants if x.ign.lower() == attendee.duo.lower()]
		if newduo:
			attendee.add_duo(newduo[0])
		else:
			attendee.add_duo(None)

for attendee in participants:
	print attendee
print len(participants)