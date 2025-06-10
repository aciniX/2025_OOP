import unittest
from unittest.mock import MagicMock
from Player import Player
from Wall import Walls
from Objects import Objects
from gameTest import GenerateWall, GetDistance
import pygame

# White Box Testing
# Definition: Tests with full knowledge of the code, targeting specific paths and conditions.
# Focus: Test edge cases and specific logic, e.g., Player.IsOffScreen boundary conditions or GenerateWall distance check.

class TestPlayerWhiteBox(unittest.TestCase):
    def setUp(self):
         # Mock Pygame dependencies
        pygame.init = MagicMock()
        pygame.font.init = MagicMock()
        self.surface = MagicMock()
        self.sprite = MagicMock()
        self.sprite.get_size.return_value = (12, 11)
        self.sprite.get_width.return_value = 12
        self.sprite.get_height.return_value = 11
        self.wall_sprite = MagicMock()
        self.wall_sprite.get_size.return_value = (16, 16)
        self.resolution = (1280, 720)
        self.player = Player(self.surface, self.sprite, self.resolution, self.wall_sprite, 30, 0)
        
        # Initialize global variables
        global lastWall, lastSpawnPoint, walls
        lastWall = [None, None]
        lastSpawnPoint = [None, None]
        walls = []

    # Tests Player.IsOffScreen for boundary conditions (e.g., x or y outside screen bounds).
    def test_player_outside_left_bound(self):
        self.player.SetPos(-1, 100)
        self.assertTrue(self.player.IsOffScreen(1280, 720), 
                        "Player should be outside left bound (x = -1)")

    def test_player_outside_right_bound(self):
        self.player.SetPos(1281, 100)
        self.assertTrue(self.player.IsOffScreen(1280, 720), 
                        "Player should be outside right bound (x = 1281)")

    def test_player_outside_top_bound(self):
        self.player.SetPos(100, -1)
        self.assertTrue(self.player.IsOffScreen(1280, 720), 
                        "Player should be outside top bound (y = -1)")

    def test_player_outside_bottom_bound(self):
        self.player.SetPos(100, 721)
        self.assertTrue(self.player.IsOffScreen(1280, 720), 
                        "Player should be outside bottom bound (y = 721)")

    def test_player_within_bounds(self):
        self.player.SetPos(100, 100)
        self.assertFalse(self.player.IsOffScreen(1280, 720), 
                         "Player should be within screen bounds (x = 100, y = 100)")

    # Tests GenerateWall to ensure walls are only created when the distance from the last spawn point exceeds wallSpacing/2, 
    # based on the GetDistance condition.
    def test_generate_wall_distance_check(self):
        self.player.SetPos(600, 300)
        GenerateWall(0)
        self.assertEqual(len(walls), 1, "First wall should be created at initial position")
        self.player.SetPos(610, 310)
        GenerateWall(0)
        self.assertEqual(len(walls), 1, "No new wall should be created for small movement")
        self.player.SetPos(630, 330)
        GenerateWall(0)
        self.assertEqual(len(walls), 2, "New wall should be created for large movement")

if __name__ == '__main__':
    unittest.main(verbosity=2)