import matplotlib.pyplot as plt
import numpy as np

grav_const = 6.67430e-11

#class to store data about the celestial bodies
class Body:
    def __init__(self, mass, pos, vel):
        self.mass = mass
        self.position = np.array(pos, dtype=float)
        self.velocity = np.array(vel, dtype=float)
        self.force = np.array([0.0, 0.0])

#function to calculate the gravitational force between two bodies
def cal_force(body1, body2):
    distance_vect = body2.position - body1.position
    distance = np.linalg.norm(distance_vect)
    if distance == 0:
        return np.array([0.0, 0.0])
    force_mag = grav_const * body1.mass * body2.mass / distance**2
    force_dir = distance_vect/distance
    return force_mag * force_dir

#function to update the position and velocity of the bodies
def update(bodies, timestep):
    for body in bodies:
        body.force = np.array([0.0,0.0])
        for remaining in bodies:
            if body != remaining:
                body.force += cal_force(body, remaining)
    for body in bodies:
        acceleration = body.force/body.mass
        body.velocity += acceleration * timestep
        body.position += body.velocity * timestep

#function to simulate the motion of the bodies and calculate their positions
def simulate(bodies, time, timestep):
    positions = []
    for _ in range(time):
        update(bodies, timestep)
        positions.append([body.position.copy() for body in bodies])
    return np.array(positions)

#function to simulate the predefined solar system (Mercury, Venus, Earth, Mars, Sun)
def predef_simulation():
    mercury = Body(3.285e23, [0.39e11, 0], [0, 47.87e3])  # Mercury
    venus = Body(4.867e24, [0.723e11, 0], [0, 35.02e3])  # Venus
    earth = Body(5.972e24, [1.496e11, 0], [0, 29.78e3])  # Earth
    mars = Body(6.39e23, [2.279e11, 0], [0, 24.07e3])    # Mars
    sun = Body(1.989e30, [0, 0], [0, 0])                # Sun

    bodies = [mercury, venus, earth, mars, sun]
    positions = simulate(bodies, 17520, 60*60)  # Simulate for 2 years on earth

    plt.plot(positions[:, 0, 0], positions[:, 0, 1], color= "black", label="mercury")
    plt.plot(positions[:, 1, 0], positions[:, 1, 1], color = "brown", label="Venus")
    plt.plot(positions[:, 2, 0], positions[:, 2, 1], color= "blue", label="Earth")
    plt.plot(positions[:, 3, 0], positions[:, 3, 1], color="red",label="Mars")
    plt.scatter(0, 0, color="yellow", label="Sun")
    plt.legend()
    plt.show()

#function to simulate the motion of the bodies entered by the user
def variable_simulation():
    #name/label for the pivot body
    pivot_name = input("Enter the name of the body you want to orbit around: ")
    #mass of the pivot body
    pivot_mass = float(input("Enter the mass of the body you want to orbit around: "))
    pivot = Body(pivot_mass, [0, 0], [0, 0])

    #name/label, mass, position and velocity of the body to be simulated
    body1_name = input("Enter the name of the planet you want to simulate: ")
    body1_mass = float(input("Enter the mass of the planet you want to simulate: "))
    body1_pos = [float(x) for x in input("Enter the x and yposition of the planet you want to simulate: ").split(',')]
    body1_vel = [float(x) for x in input("Enter the x and y velocity of the planet you want to simulate: ").split(',')]
    body1 = Body(body1_mass, body1_pos, body1_vel)

    bodies = [body1, pivot]

    time = int(input("Enter the time you want to simulate for(in seconds): "))

    positions = simulate(bodies, time, 60*60)

    #plot the motion of the body
    plt.plot(positions[:, 0, 0], positions[:, 0, 1], color= "black", label=body1_name)
    plt.scatter(0, 0, color="yellow", label=pivot_name)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    #ask user for choice of simulation
    choice = int(input("Enter 1 for predefined simulation and 2 for custom simulation: "))
    if choice == 1:
        predef_simulation()
    elif choice == 2:
        variable_simulation()
    else:
        print("Invalid choice")