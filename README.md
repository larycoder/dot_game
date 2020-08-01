# Dot Game
=======================================================
## Build on python
## Simple game to understand more about flask framework

# Description
## The game purpose:
- You have a dot. It is not a normal dot, that is actually a car. But it do not have engine, so the car could not run.
- You have to write th engine for the car so that it can run.

## The structure:
You have 3 parts:
- The editor so that you can write your own engine
- The render window where you can see your dot (car)
- The instruction window where you can see some predefine block of engine

## How can you write the engine:
The car has 2 attribute:
- The list of car attribute: color, shape, direction (WARNING: attributes could be change in future)
- The current position of car: x, y

Therefor, the engine will be a function receive 2 parameters:
1. List of car attributes
2. 2 current position of car

The output expect of engine will also be:
1. New list of car attributes
2. new current location of car

Since this is a web application, the native language of engine will be javascript