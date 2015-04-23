#!/usr/bin/env python3
from enum import IntEnum
from time import sleep
import random
from numpy.random import poisson

class State(IntEnum):
    queuing = 1
    riding = 2
    
class Direction(IntEnum):
    up = 1
    stationary = 0
    down = -1

class Person(object):
    def __init__(self, destination, start = 0):
        self.destination = destination
        self.start = start
        self.queue_ticks = 0
        self.ride_ticks = 0
        self.state = State.queuing
    
    def __repr__(self):
        return "S:{} D:{} T:{} Q:{} R:{}".format(self.start, self.destination, self.queue_ticks + self.ride_ticks, self.queue_ticks, self.ride_ticks)
        
    def incinerate(self):
        global people
        people.remove(self)
        print("{}. AAaaaa...".format(self))
    
    def tick(self):
        if self.state == State.queuing:
            self.queue_ticks += 1
        elif self.state == State.riding:
            self.ride_ticks += 1
        
class Queue(object):
    def __init__(self, level, poisson = False, rate = 0):
        self.level = level
        self.people = list()
        self.poisson = poisson
        self.rate = rate
    
    def __repr__(self):
        return self.people
        
    def tick(self, people, queues):
        if self.poisson == True:
            return people.update({Person(random.sample(queues).level, start = self.level) for x in range(0, poisson(rate))})
            
class Elevator(object):
    def __init__(self, capacity, home = 0):
        self.level = home
        self.direction = Direction.stationary
        self.home = home
        self.capacity = capacity
        self.people = set()
    
    def __len__(self):
        return len(self.people)
    
    def add_person(self, person):
        if len(self) < self.capacity:
            self.people.add(person)
            person.state = State.riding
            return True
        return False
    
    def tick(self):
        self.level += self.direction
        print(self.level)
        
def tick():
    global world_time
    world_time += 1
    for person in people:
        person.tick()
    for elevator in elevators:
        elevator.tick()
    sleep(0.5)

def main():
    global world_time, queues, people, elevators
    world_time = 0
    
    queues = [Queue(x) for x in range(0,6)] # create 6 floors, 0-5
    people = {Person(x) for x in range(1,6)} # create 5 people on floor 0, each going to a different floor 1-5
    people.update({Person(3) for x in range(1,6)}) # create 5 more people on floor 0, each going to 3
    for person in sorted(list(people), key=lambda k: random.random()): # shuffles the set as a list in place
        queues[person.start].people.append(person) # people join the appropriate queues
    elevators = [Elevator(3)] # create one 3-person elevator
    
    while people:
        for elevator in elevators:
            ###
            # People exit then enter elevators
            ###
            old_people = elevator.people
            elevator.people = {person for person in elevator.people if not person.destination == elevator.level}
            for person in old_people.difference(elevator.people):
                person.incinerate()
            while len(queues[elevator.level].people) != 0:
                entering = queues[elevator.level].people.pop(0)
                if not elevator.add_person(entering):
                    queues[elevator.level].people[0:0] = [entering]
                    break  
            ###
            # Elevators now pick their direction to travel
            ###
            if len(elevator.people) != 0:
                elevator.direction = Direction.up
            elif len(elevator.people) == 0 and elevator.level != 0:
                elevator.direction = Direction.down
            else:
                elevator.direction = Direction.stationary
        
        tick()
            

if __name__ == "__main__":
    main()
