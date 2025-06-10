import unittest
from unittest.mock import MagicMock
import pygame
from Player import Player
from Wall import Walls
from Objects import Objects
from gameTest import CheckCollisions, NewGame

# Grey Box Testing
# Definition: Combines black box and white box approaches, with partial knowledge of internal logic.
# Focus: Test interactions like collision detection with some understanding of the code’s structure 
# (e.g., CheckCollisions uses colliderect).

class TestGameGreyBox(unittest.TestCase):
    def setUp(self):
        # Mock Pygame dependencies
        pygame.init = MagicMock()
        pygame.font.init = MagicMock()
        pygame.Rect = MagicMock(return_value=MagicMock())
        # Mock pygame.transform.rotate to avoid TypeError
        self.mock_rotated_sprite = MagicMock()
        self.mock_rotated_sprite.get_rect.return_value = MagicMock(center=(0, 0))
        pygame.transform.rotate = MagicMock(return_value=self.mock_rotated_sprite)
        # Mock pygame.transform.scale
        pygame.transform.scale = MagicMock(return_value=MagicMock(get_size=MagicMock(return_value=(12, 11))))
        self.surface = MagicMock()
        self.sprite = MagicMock()
        self.sprite.get_size.return_value = (12, 11)
        self.sprite.get_width.return_value = 12
        self.sprite.get_height.return_value = 11
        # Mock playerSprite list to match main.py
        global playerSprite
        playerSprite = [self.sprite, self.sprite]  # Two mocked sprites
        self.wall_sprite = MagicMock()
        self.wall_sprite.get_size.return_value = (16, 16)
        global wallSprite, resolution, wallSpacing
        wallSprite = self.wall_sprite
        resolution = (1280, 720)
        wallSpacing = 30
        global players, walls, projectiles, dead
        players = []
        walls = []
        projectiles = []
        dead = [False, False]
        NewGame()  # Initialize two players

        # Initialise global variables
        # global players, walls, projectiles, dead
        players = []
        walls = []
        projectiles = []
        dead = [False, False]

        # Instantiate players
        players.append(Player(self.surface, self.sprite, self.resolution, self.wall_sprite, 30, 0))
        players.append(Player(self.surface, self.sprite, self.resolution, self.wall_sprite, 30, 1))

    # Tests CheckCollisions for player-wall collisions, knowing it uses colliderect but focusing on input (positions) 
    # and output (death state, cleared objects).
    # Assumes partial knowledge of collision logic to set up overlapping rectangles.
    def test_player_wall_collision(self):
        # Test player-wall collision
        self.assertGreater(len(players), 0, "Players list should not be empty after NewGame")
        players[0].SetPos(100, 100)
        walls.append(Walls(self.surface, self.wall_sprite, (100, 100), 0))
        players[0].GetRect = MagicMock(return_value=pygame.Rect(100, 100, 12, 11))
        walls[0].GetRect = MagicMock(return_value=pygame.Rect(100, 100, 16, 16))
        players[0].GetRect().colliderect = MagicMock(return_value=True)
        CheckCollisions()
        self.assertTrue(dead[0], "Player 0 should be marked as dead after hitting a wall")
        self.assertEqual(len(players), 0, 
                         "Players list should be cleared after collision triggers GameOver")
        self.assertEqual(len(walls), 0, 
                         "Walls list should be cleared after collision triggers GameOver")

    def test_no_collision_no_death(self):
        # Test no collision case
        self.assertGreater(len(players), 0, "Players list should not be empty after NewGame")
        players[0].SetPos(100, 100)
        walls.append(Walls(self.surface, self.wall_sprite, (200, 200), 0))
        players[0].GetRect = MagicMock(return_value=pygame.Rect(100, 100, 12, 11))
        walls[0].GetRect = MagicMock(return_value=pygame.Rect(200, 200, 16, 16))
        players[0].GetRect().colliderect = MagicMock(return_value=False)
        CheckCollisions()
        self.assertFalse(dead[0], "Player 0 should not be marked as dead when no collision occurs")
        self.assertGreater(len(players), 0, "Players list should not be cleared when no collision occurs")

if __name__ == '__main__':
    unittest.main(verbosity=2)