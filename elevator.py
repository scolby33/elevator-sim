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
        return "L:{} P:{} R:{}".format(self.level, self.poisson, self.rate)
    
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
    
    def __repr__(self):
        return "L:{} C:{} H:{}".format(self.level, self.capacity, self.home)
    
    def add_person(self, person):
        if len(self) < self.capacity:
            self.people.add(person)
            person.state = State.riding
            return True
        return False
    
    def tick(self):
        self.level += self.direction
        print(self.level)
        
class BuildingModel(object):
    def __init__(self, floors, elevators):
        self.queues = {Queue(*args) for args in floors}
        self.elevators = {Elevator(*args) for args in elevators}
        self.people = set()
        self.world_time = 0

    def tick(self):
        while True:
            self.world_time += 1
            for person in self.people:
                person.tick()
            for queue in self.queues:
                self.people = queue.tick(self.people, self.queues)
            for elevator in self.elevators:
                elevator.tick()
            sleep(0.5)
    
    def add_person(self, person):
        pass

def main():
    floors = [(0, True, 1), (1,), (2, True), (3, False)]
    elevators = [(2,), (3,)]
    
    BuildingModel(floors, elevators)

if __name__ == "__main__":
    main()
