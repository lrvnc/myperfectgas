import matplotlib.pyplot as plt
from matplotlib.collections import EllipseCollection
from matplotlib.path import Path
import numpy as np

from objects.common import Rectangle
from objects.particles import Particles

class Scene():
  def __init__(self, id: str, width: float = 100, height: float = 50, title: str = 'Simulation') -> None:
    self.id = id
    self.corners= Rectangle.compute_rectangle(center=[0,0], width=width, height=height)
    self.title = title
    self.create_canvas()
    self.objects = {}
    self.particles = {}

  def create_canvas(self) -> None:
    self.fig = plt.figure(figsize=[10,10])
    self.ax = self.fig.subplots()
    self.ax.set(
      xlim=[self.corners[:,0].min(), self.corners[:,0].max()],
      ylim=[self.corners[:,1].min(), self.corners[:,1].max()],
      xticks=[],
      yticks=[],
      aspect='equal',
      title=self.title
    )

  def render_frame(self, draw_velocities: bool = True) -> None:
    # Plot objects
    for obj in self.objects.values():
        self.ax.plot(*obj.corners[:,:2].T, color=obj.color, lw=1.2)

    # Plot particles
    for ptcles in self.particles.values():
      widths, heights, angles = 2*ptcles.radius, 2*ptcles.radius, 0.0
      collection = EllipseCollection(
                                      widths, heights, angles, units='x', offsets=ptcles.positions,
                                      offset_transform=self.ax.transData, cmap='nipy_spectral', edgecolor = 'black',
                                      facecolor=ptcles.color
                                    )
      self.ax.add_collection(collection)
    
    if draw_velocities:
      self.draw_particle_velocities()

  def draw_particle_velocities(self) -> None:
    for ptcle in self.particles.values():
      positions, velocities = ptcle.positions, ptcle.velocities
      self.ax.quiver(positions[:, 0], positions[:, 1], velocities[:, 0], velocities[:, 1],
                     angles='xy', scale_units='xy', scale=1, color='black', width=0.0025)
      
  def add_rectangle(self, id: str, center: list, width: float, height: float, color: str) -> None:
    self.objects[id] = Rectangle(id=id, center=center, width=width, height=height, color=color)

  def add_particles(self, id: str, n_particles: int, mass: float, radius: float, vlim: list,
                    parent_object_id: str = None, color: str = None) -> None:
      #! GPTo1-preview fixed this function
      if parent_object_id is not None:
          # Use the corners of the parent object to define the placement area
          corners = self.objects[parent_object_id].corners[:, :2]
      else:
          # Use the scene's corners if no parent object is specified
          corners = self.corners[:, :2]

      # Create a Path object representing the polygon area where particles can be placed
      polygon_path = Path(corners)

      # Determine the bounding box of the placement area
      x_min, x_max = corners[:, 0].min(), corners[:, 0].max()
      y_min, y_max = corners[:, 1].min(), corners[:, 1].max()

      # Retrieve positions and radii of existing particles
      existing_positions = self.get_all_particle_positions()
      if existing_positions is None:
          existing_positions = np.empty((0, 2))  # Initialize with no existing positions
      existing_radii = self.get_all_particle_radii()
      if existing_radii is None:
          existing_radii = np.empty((0, 1))  # Initialize with no existing radii

      new_positions = []  # List to store positions of new particles
      new_radii = []      # List to store radii of new particles

      max_tries = 1000  # Maximum number of attempts to place each particle
      for i in range(n_particles):
          tries = 0
          while tries < max_tries:
              # Generate a random position within the bounding box, adjusted for particle radius
              x_pos = np.random.uniform(x_min + radius, x_max - radius)
              y_pos = np.random.uniform(y_min + radius, y_max - radius)
              pos = np.array([x_pos, y_pos])

              # Check if the position is inside the defined polygon area
              if not polygon_path.contains_point(pos):
                  tries += 1
                  continue

              # Check for overlap with existing particles
              if existing_positions.size > 0:
                  # Calculate distances to all existing particles
                  distances = np.sqrt(np.sum((existing_positions - pos) ** 2, axis=1))
                  # Check if any distances are less than the sum of the radii (indicating overlap)
                  if np.any(distances < (existing_radii.flatten() + radius)):
                      tries += 1
                      continue

              # If no overlap and inside the area, accept the position
              existing_positions = np.vstack([existing_positions, pos])
              existing_radii = np.vstack([existing_radii, radius])
              new_positions.append(pos)
              new_radii.append(radius)
              break  # Exit the while loop and proceed to place the next particle

          if tries == max_tries:
              # If max attempts reached without placing the particle, print a message
              print(f"Could not place particle {i}")
              continue

      # Total number of particles successfully placed
      n_placed_particles = len(new_positions)
      if n_placed_particles == 0:
          print("No particles were placed.")
          return  # Exit the function if no particles could be placed

      # Convert lists to numpy arrays for further processing
      positions = np.array(new_positions)
      radii = np.array(new_radii).reshape(-1, 1)
      velocities = np.random.uniform(vlim[0], vlim[1], (n_placed_particles, 2))  # Random velocities within limits
      masses = mass * np.ones(n_placed_particles)  # Masses for all new particles

      # Add the new particles to the scene's particle collection
      self.particles[id] = Particles(
          id=id,
          n_particles=n_placed_particles,
          positions=positions,
          velocities=velocities,
          radius=radii,
          mass=masses,
          color=color
      )
 
  def get_all_particle_radii(self):
    return np.vstack([p.radius for p in self.particles.values()]) if len(self.particles) > 0 else None
  
  def get_all_particle_positions(self):
    return np.vstack([p.positions for p in self.particles.values()]) if len(self.particles) > 0 else None


if __name__ == '__main__':
  scene = Scene(id='world', width=200, height=100)
  scene.add_rectangle(id='box', center=[0,0], width=100, height=50, color='k')
  scene.add_particles(
    id='H',
    n_particles=5,
    mass=5,
    radius=5,
    vlim=[-5, 5],
    parent_object_id='box',
    color='blue'
  )
  scene.add_particles(
    id='He',
    n_particles=4,
    mass=4,
    radius=4,
    vlim=[-5, 5],
    parent_object_id='box',
    color='yellow'
  )
  scene.add_particles(
    id='Ne',
    n_particles=3,
    mass=3,
    radius=3,
    vlim=[-5, 5],
    parent_object_id='box',
    color='green'
  )
  scene.render_frame()
  plt.show()