import numpy as np

class Particles:
  def __init__(self, id: str, n_particles: int, positions: np.array = None, velocities: np.array = None, radius: np.array = None, mass: np.array = None, color: str = 'blue') -> None:
    self.id = id
    self.positions = positions
    self.velocities = velocities
    self.radius = radius
    self.mass = mass
    self.n_particles = n_particles
    self.color = color
