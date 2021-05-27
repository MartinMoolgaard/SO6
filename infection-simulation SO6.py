import tkinter as tk
import tkinter.ttk as ttk
import time
import random
import sys
n = 100

class Person(object):
    # Constructor: creates a new person/agent
    def __init__(self, canvas, x, y, fill):
        # Calculate parameters for the oval/circle to be drawn
        r = 4 
        x0 = x-r
        y0 = y-r
        x1 = x+r
        y1 = y+r

        # Initialize the agents attributrs
        self.x = x
        self.y = y
        self.infected = False
        self.mundbind = False
        self.hjemmebind = False
        if random.random() > 0.8:
            self.mundbind = True
        elif random.random() > 0.8:
            self.hjemmebind = True
        self.immune = False
        self.infect_timer = 0

        self.canvas = canvas
        self.id = canvas.create_oval(x0,y0,x1,y1, fill=fill, outline='')

    #bevægelses mønstre
    def move(self):
        dx = random.choice([-3, 3])
        dy = random.choice([-3, 3])


        self.canvas.move(self.id, dx, dy)
        self.x = self.x + dx
        self.y = self.y + dy


    def check_infected(self, persons):
        for person in persons:
            if self.infected == False:
                d = ((self.x - person.x)**2 + (self.y - person.y)**2)**(1/2)
            
                if d < 30 and person.infected == True and self.hjemmebind == True and self.immune == False:
                    self.infect()

                if d < 30 and person.infected == True and self.mundbind == True and self.immune == False:
                    self.infect()


                if d < 30 and person.infected == True and self.mundbind == False and self.hjemmebind == False and self.immune == False:
                    self.infect()


    def infect(self):  
        self.infected = True
        self.infect_timer = 250
        self.canvas.itemconfig(self.id, fill='red')

    def check_immune(self):
        self.infect_timer -=1
        if self.infect_timer ==0:
            self.immunitize()

    def immunitize(self):
        self.immune = True
        self.infected = False
        self.canvas.itemconfig(self.id,fill='blue')



class App(object):
    def __init__(self, master, **kwargs):

        # Create the canvas on which the agents are drawn
        self.master = master
        self.canvas = tk.Canvas(self.master, width=800, height=700,background='white')
        self.canvas.pack()

        # Create a reset button for the simulation
        self.but_reset = ttk.Button(master, text = "Reset", command=self.init_sim)
        self.but_reset.pack(side=tk.BOTTOM)

        # Start / init the simulation
        self.init_sim()

        self.master.after(0, self.update)
        self.frame=0

    def update(self):
        hjemmebind = 0
        intetbind = 0
        mundbind = 0


        # Update / move each agent
        for person in self.persons:
            person.move()
            person.check_infected(self.persons)
            person.check_immune()
            if person.hjemmebind == True:
                hjemmebind += 1
            if person.mundbind == True:
                mundbind += 1
            if person.hjemmebind and person.mundbind == False:
                intetbind += 1
        if self.frame %20 == 0:
            print("antal med godkendt mundbind", mundbind)
            print("antal uden mundbind", intetbind)
            print("antal med hjemmebind", hjemmebind)
            



        # Count number of infected persons
        ni = 0
        for p in self.persons:
            if p.infected:
                ni += 1
        if self.frame %20 == 0:
            print("Number of infected persons:", ni)


        self.master.after(100, self.update)
        self.frame += 1


    # Start / init simulation (clear all agents and create new ones)
    def init_sim(self):
        self.canvas.delete('all')
        self.persons = []

        for i in range(n):
            x = random.randint(0,800)
            y = random.randint(0,800)
            p = Person(self.canvas, x, y, 'black')
            if random.uniform(0,1) < 0.05:
                p.infect()

            self.persons.append(p)

        self.canvas.pack()

        
# Create the Tkinter application and run it
root = tk.Tk()
app = App(root)
start=time.time()
root.mainloop()
end=time.time()
print("Frames:",app.frame)
print("Runtime:",end-start)
print("Framerate:", app.frame/(end-start))