# Rebeca's Kanban board assignemnet 

## Description

Simple Kanban board, that allows to create tasks, move the column of the task and delete the tasks.

Even when joining the HTML and CSS file togeter makes it run faster, they are separated to dela with the separation of concerns. 

Exclusive use of POST METHODS for the updating. 


The tasks go automatically to the todo board, and it dosent allow the user to decide the status. This was a design choice, with the order of the board in mind, and the fact that the user can move the task to the other columns.

Instead of allowing for editing of the tasks, the user can delete the task and create a new one. This was a design choice, to mantain the simplicity of the board, and the integrity of the tasks. 

The combination of this two design choices, makes the user more concious of every task they want to update (and thus reduces makes them rething what it's posssible to do).

![alt text](/boardimage.jpg)


## Testing
The test of the application focuses on the status of the tasks.

I accounted for the posibility of the wrong method, and thus the test takes int into consideration.
I tested every action for the tasks (in multiple ways, such as deleting the a task with a different name.)

In total, as seen by the coverage, the test covers 94% of the code (mostly the functionalities of routes.py).