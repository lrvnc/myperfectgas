import numpy as np


class GenericObject:
  def __init__(self, id: str, corners: list, color: str = None) -> None:
    self.id = id
    self.corners = corners[corners[:,2].argsort()] # (x, y, ordering)
    self.color = color


class Rectangle(GenericObject):
  def __init__(self, id: str, center: list, width: float, height: float, color: str = 'k')  -> None:
    corners = self.compute_rectangle(center=center, width=width, height=height)
    super().__init__(id=id, corners=corners, color=color)

  @staticmethod
  def compute_rectangle(center, width, height) -> np.array:
      # Unpack the center coordinates
      cx, cy = center
      
      # Calculate half the side length
      half_side_x = width / 2
      half_side_y = height / 2
      
      # Calculate the corner points
      corners = np.array([
          [cx - half_side_x, cy - half_side_y, 0],  # Bottom-left
          [cx + half_side_x, cy - half_side_y, 1],  # Bottom-right
          [cx + half_side_x, cy + half_side_y, 2],  # Top-right
          [cx - half_side_x, cy + half_side_y, 3],  # Top-left
          [cx - half_side_x, cy - half_side_y, 4],  # Bottom-left
      ])
      
      return corners # (x, y, ordering)


class Square(Rectangle):
   def __init__(self, id: str, center: list, side: float, color: str) -> None:
    corners = self.compute_rectangle(center=center, width=side, height=side)
    super().__init__(id=id, corners=corners, color=color)