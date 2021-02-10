import time
import random
import pygame
import threading
from person import Person
from datetime import datetime

def percentage(part, whole):
	Percentage = 100 * float(part)/float(whole)
	return str(Percentage) + '%'

def calculateCases(people):
	recovered = 0
	infected = 0
	healthy = 0
	for boi in people:
		if boi.status == "sick":
			infected += 1
		elif boi.status == "recovered":
			recovered += 1
		else:
			healthy += 1
	return (healthy, infected, recovered)

def timeToEradicate(start):
	now = datetime.now()
	seconds = (now - start).total_seconds()
	print(f"Time to eradicate: {seconds}")

def statistics(numPeople, healthy, infected, recovered):
	print(f"Healthy: {healthy} people     | {percentage(healthy, numPeople)}")
	print(f"Infected: {infected} people   | {percentage(infected, numPeople)}")
	print(f"Recovered: {recovered} people | {percentage(recovered, numPeople)}")

def main():
	pygame.init()
	WIDTH = HEIGHT = 600
	screen = pygame.display.set_mode([WIDTH, HEIGHT])
	pygame.display.set_caption('Virus Simulation')
	screen.fill(pygame.Color("grey"))

	clock = pygame.time.Clock()
	MAX_FPS = 30
	numPeople = 150
	factorOfPeopleSocialDistancing = 0

	running = True
	bufferSpawn = 10

	patientZero = Person(random.randint(bufferSpawn, WIDTH-bufferSpawn), 
						 random.randint(bufferSpawn, HEIGHT-bufferSpawn), "sick", False)
	people = [patientZero]
	for i in range(numPeople -1):
		socialDistancing = False
		if i < factorOfPeopleSocialDistancing * numPeople:
			socialDistancing = True 

		colliding = True
		while colliding:
			person = Person(random.randint(bufferSpawn, WIDTH-bufferSpawn), 
							random.randint(bufferSpawn, HEIGHT-bufferSpawn), "healthy", socialDistancing)
			colliding = False 
			for boi in people:
				if person.checkColidingWithOther(boi):
					colliding = True
					break

		people.append(person)

	start = datetime.now()
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		for person in people:
			person.update(screen, people)

		screen.fill(pygame.Color("grey"))
		for person in people:
			person.draw(screen)
		pygame.display.flip()

		clock.tick(MAX_FPS)
		healthy, infected, recovered = calculateCases(people)
		statistics(numPeople, healthy, infected, recovered)
		threadStatistics = threading.Thread(target=statistics(numPeople, healthy, infected, recovered)).start()

		if infected == 0:
			statistics(numPeople, healthy, infected, recovered)
			timeToEradicate(start)
			time.sleep(10)
			running = False 

	pygame.quit()

main()