# Suggestions and ideas for next offering of OpenReproLab

While OpenReproLab is ongoing, we refrain from modifying past labs (even to improve them). This avoids breaking things for students who have already completed past labs. Small fixes and small additions to lab instructions are accepted, since they do not break things.

This documents lists suggestions and ideas for the next offering of OpenReproLab. These improvements can be implemented for the next offering, in a new repository.

## Lab 01 (ABC of reproducible numerical science)

### Python modules and notebooks

We had the goal to introduce the use of Python module as a tool to make code clearer and more reusable.

Modules and packages are definitely the way to go, but we made the mistake (or what is potentially a mistake), to introduce modules in Jupyter notebooks in the first lab, while students were not yet experienced with notebooks. What happened multiple times was that a student would:

 - Create the notebook
 - Create a non-working version of the module
 - Import this module from the notebook
 - Fix the module
 - Re-import the module in the notebook, without restarting the kernel, which actually does not import the updated module

An option would have been to explain to students that they have to restart the kernel of a notebook when a module used by the notebook is updated.

But more generally, introducing notebooks and modules at the same time may not have been the wisest of ideas?
