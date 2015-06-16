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
		return "Player(" + str(self.elo) +")"

	def __str__(self):
		if self.duo:
			duo_text = self.duo.ign
		else:
			duo_text = ""
		text = self.name+","+self.ign+","+self.rank+","+self.elo+","+duo_text+","+self.email+"\n"

		return text
		
	def add_duo(self,partner):
		self.duo = partner

class Block(object):
	#The team
	def __init__(self):
		self.name = ''
		self.slot1 = None
		self.slot2 = None

	def get_average_elo(self):
		total=0
		count=0
		if (self.slot1):
			total = total+int(self.slot1.elo)
			count = count+1
		if (self.slot2):
			total = total+int(self.slot2.elo)
			count = count+1

		average = total/count

		return average

	def member_count(self):
		count=0
		if (self.slot1):
			count = count+1
		if (self.slot2):
			count = count+1
		return count
	
	def add_player(self,player):
		if (self.slot1):
			if (self.slot2):
				return False		
			else:
				self.name = self.name + '/' + player.ign 
				self.slot2 = player
		else:
			self.name = self.name + player.ign
			self.slot1 = player

			
	def __repr__(self):
		return "Block()"

	def __str__(self):
		print ("------------------------------------------------------")
		print (self.name)
		print (self.slot1)
		print (self.slot2)
		print ("ELO Average: " + str(self.get_average_elo()))
		return "------------------------------------------------------"

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
							return False
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

	def blockify(self):
		blocks = []
		count = 0
		if (self.slot1.duo):
			newBlock = Block()
			newBlock.add_player(self.slot1)
			newBlock.add_player(self.slot2)
			blocks.append(newBlock)
			count = count + 2
		else:
			newBlock = Block()
			newBlock.add_player(self.slot1)
			blocks.append(newBlock)
			count = count + 1
		if (self.slot2.duo):
			if (count == 2):
				doNothing=True
			else:
				newBlock = Block()
				newBlock.add_player(self.slot2)
				newBlock.add_player(self.slot3)
				blocks.append(newBlock)
				count = count + 2
		else:
			newBlock = Block()
			newBlock.add_player(self.slot2)
			blocks.append(newBlock)
			count = count + 1
		if (self.slot3.duo):
			if (count==2):
				newBlock = Block()
				newBlock.add_player(self.slot3)
				newBlock.add_player(self.slot4)
				blocks.append(newBlock)
				count = count + 2
			else:
				doNothing=True

		else:
			newBlock = Block()
			newBlock.add_player(self.slot3)
			blocks.append(newBlock)
			count = count + 1
		if (self.slot4.duo):
			if (count==3):
				newBlock = Block()
				newBlock.add_player(self.slot4)
				newBlock.add_player(self.slot5)
				blocks.append(newBlock)
				count = count + 2
			else:
				doNothing=True

		else:
			newBlock = Block()
			newBlock.add_player(self.slot4)
			blocks.append(newBlock)
			count = count + 1
		if (count!=5):
			newBlock = Block()
			newBlock.add_player(self.slot5)
			blocks.append(newBlock)
			count = count + 1

		return blocks
			
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
		return "------------------------------------------------------"

def printPlayer(player):
	with open('dromosV2.csv', 'a') as fp:
		fp.write(player.__str__())

		
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
	no_room = False
	for z in range(0,int(number_of_teams)):
		newTeam = Team(team_names.pop())
		while (newTeam.member_count() != 5):
			if (no_room == False):
				if (top == 1):
					index = 0
				else:
					index = -1
			inspect_player = local_list[index]
# 			print(inspect_player)
			if(inspect_player.duo):
				if (newTeam.member_count() > 3 ):
					if (top ==1):
						index = index + 1
						no_room = True
					else:
						index = index - 1
						no_room = True
				else:
					newTeam.add_player(inspect_player)
					printPlayer(inspect_player)
					duo=[x for x in local_list if x.ign.lower() == inspect_player.duo.ign.lower()]
					duo = duo[0]
					newTeam.add_player(duo)
					printPlayer(duo)
					no_room = False
					local_list=[x for x in local_list if x.ign.lower() != inspect_player.ign.lower()]
					local_list=[x for x in local_list if x.ign.lower() != duo.ign.lower()]
					top = top * -1
			else:
				newTeam.add_player(inspect_player)
				printPlayer(inspect_player)
				no_room = False
				local_list=[x for 
				x in local_list if x.ign.lower() != inspect_player.ign.lower()]
				top = top * -1
				
		team_list.append(newTeam)
	return team_list

def balance_algorithm_1(top_team,bottom_team):
	difference = top_team.get_average_elo() - bottom_team.get_average_elo()
	top_Block = top_team.blockify()
	bottom_Block = bottom_team.blockify()	
	mixing_pot = top_Block + bottom_Block
	mixing_pot.sort(key=lambda x: int(x.get_average_elo()), reverse=False)
	team1 = Team(top_team.name)
	team2 = Team(bottom_team.name)
	stage = 0
	# import pdb; pdb.set_trace()
	while(len(mixing_pot)>0):
		inspect_block = mixing_pot.pop()
		if (stage == 0):
			if (inspect_block.member_count() == 2):
				team1.add_player(inspect_block.slot1)
				team1.add_player(inspect_block.slot2)
				stage = -3
			else:
				team1.add_player(inspect_block.slot1)
				stage = -2
		elif (stage == -3):
			if (inspect_block.member_count() == 2):
				team2.add_player(inspect_block.slot1)
				team2.add_player(inspect_block.slot2)
				stage = -1
			else:
				team2.add_player(inspect_block.slot1)
				stage = -2
		elif (stage == -2 ):
			if (inspect_block.member_count() == 2):
				team2.add_player(inspect_block.slot1)
				team2.add_player(inspect_block.slot2)
				stage = 2
			else:
				team2.add_player(inspect_block.slot1)
				stage = -1
		elif (stage == -1):
			if (inspect_block.member_count() == 2):
				team2.add_player(inspect_block.slot1)
				team2.add_player(inspect_block.slot2)
				stage = 3
			else:
				team2.add_player(inspect_block.slot1)
				stage = 2
		elif (stage == 3):
			if (inspect_block.member_count() == 2):
				team1.add_player(inspect_block.slot1)
				team1.add_player(inspect_block.slot2)
				stage = 1
			else:
				team1.add_player(inspect_block.slot1)
				stage = 2
		elif (stage == 2):
			if (inspect_block.member_count() == 2):
				team1.add_player(inspect_block.slot1)
				team1.add_player(inspect_block.slot2)
				stage = -2
			else:
				team1.add_player(inspect_block.slot1)
				stage = 1
		elif (stage == 1):
			if (inspect_block.member_count() ==2):
				team1.add_player(inspect_block.slot1)
				team1.add_player(inspect_block.slot2)
				stage = -3
			else:
				team1.add_player(inspect_block.slot1)
				stage = -2
		else:
			print("could not handle team creation")
			print(inspect_block)
			break
	return [team1.get_average_elo()-team2.get_average_elo(),team1,team2]

	print (top_team)
	for block in top_Block:
		print (block)
	print (bottom_team)
	for block2 in bottom_Block:
		print (block2)
	


def stage2_teambalance(team_list):
	improved_team_list = []
	local_list = team_list
	flag = True
	count = 0
	while(flag):
		local_list.sort(key=lambda x: int(x.get_average_elo()), reverse=False)
		top_team = local_list[-1]
		bottom_team = local_list[0]
		[x for x in local_list if x.name.lower() != top_team.name.lower()]
		[x for x in local_list if x.name.lower() != bottom_team.name.lower()]
		difference = top_team.get_average_elo() - bottom_team.get_average_elo()
		if (difference > 100) :
			score1 = balance_algorithm_1(top_team, bottom_team)
			local_list=[x for x in local_list if x.name.lower() != top_team.name.lower()]
			local_list=[x for x in local_list if x.name.lower() != bottom_team.name.lower()]
			local_list.append(score1[1])
			local_list.append(score1[2])
			count = count + 1
		else:
			count = count + 1
			if count > 1000:
				flag=False
			continue
	print (count)

		
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

team_list = create_teams(participants)
stage2_teambalance(team_list)
