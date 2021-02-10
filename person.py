import random
import pygame
import math

minMovement = 0.5
maxSpeed = 3
colors = {"healthy":"white", "sick":"red", "recovered":"blue"}


class Person():
	def __init__(self, x, y, status, socialDistancing):
		self.x = x
		self.y = y
		self.status = status
		self.socialDistancing = socialDistancing
		self.radius = 6
		self.vx = self.vy = 0
		self.turnSick = 0
		self.recoveryTime = random.randint(100, 150)

		if not self.socialDistancing:
			while -minMovement < self.vx < minMovement and -minMovement < self.vy < minMovement:
				self.vx = random.uniform(-maxSpeed, maxSpeed)
				self.vy = random.uniform(-maxSpeed, maxSpeed)

	def move(self):
		if not self.socialDistancing:
			self.x += self.vx
			self.y += self.vy

	def update(self, screen, people):
		self.move()
		if self.status == "sick":
			self.turnSick += 1
			if self.turnSick == self.recoveryTime:
				self.status = "recovered"
		self.checkColidingWithWall(screen)
		for other in people:
			if self != other:
				if self.checkColidingWithOther(other):
					self.updateCollisionVelocities(other)
					if self.status == "sick" and other.status == "healthy":
						other.status = "sick"
					elif other.status == "sick" and self.status == "healthy":
						self.status = "sick"

	def draw(self, screen):
		pygame.draw.circle(screen, pygame.Color(colors[self.status]), (round(self.x), round(self.y)), self.radius)

	def checkColidingWithWall(self, screen):
		if self.x + self.radius >= screen.get_width() and self.vx > 0:
			self.vx *= -1
		elif self.x - self.radius <= 0 and self.vx < 0:
			self.vx *= -1
		if self.y + self.radius >= screen.get_height() and self.vy > 0:
			self.vy *= -1
		elif self.y - self.radius <= 0 and self.vy < 0:
			self.vy *= -1

	def checkColidingWithOther(self, other):
		distance = math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2))
		if distance <= self.radius + other.radius:
			return True
		return False

	def updateCollisionVelocities(self, other):
		if not self.socialDistancing and not other.socialDistancing:
			auxVX, auxVY = self.vx, self.vy  
			self.vx, self.vy = other.vx, other.vy
			other.vx, other.vy = auxVX, auxVY
		elif other.socialDistancing:
			magV = math.sqrt(math.pow(self.vx, 2) + math.pow(self.vy, 2))
			tempVector = (self.vx + (self.x - other.x), self.vy + (self.y - other.y))
			magTempVector = math.sqrt(math.pow(tempVector[0], 2) + math.pow(tempVector[1], 2))
			normTempVector = (tempVector[0]/magTempVector, tempVector[1]/magTempVector)
			self.vx = normTempVector[0] * magV
			self.vy = normTempVector[1] * magV