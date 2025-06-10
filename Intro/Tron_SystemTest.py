import unittest
from unittest.mock import MagicMock
import pygame
import Wall
from gameTest import NewGame, Shoot, GenerateWall, CheckCollisions, GameOver, UpdatePScore, GetScore

# System Testing
# Definition: Tests the entire game system as a black box, focusing on end-to-end behavior.
# Focus: Simulate a game cycle (e.g., player movement, shooting, collisions) to ensure the game works as intended.

class TestGameSystem(unittest.TestCase):
    def setUp(self):
        # Mock Pygame dependencies
        pygame.init = MagicMock()
        pygame.font.init = MagicMock()
        pygame.display.set_mode = MagicMock()
        pygame.display.get_surface = MagicMock(return_value=MagicMock())
        # Mock pygame.transform.rotate and pygame.transform.scale
        self.mock_rotated_sprite = MagicMock()
        self.mock_rotated_sprite.get_rect.return_value = MagicMock(center=(0, 0))
        pygame.transform.rotate = MagicMock(return_value=self.mock_rotated_sprite)
        pygame.transform.scale = MagicMock(return_value=MagicMock(get_size=MagicMock(return_value=(12, 11))))
        self.surface = pygame.display.get_surface()
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
        global players, projectiles, walls, pScores
        players = []
        projectiles = []
        walls = []
        pScores = [0, 0]
        NewGame()  # Initialize two players


    # Simulates a full game cycle: player movement, shooting, wall generation, and collision detection.
    # Verifies that GameOver clears objects and updates scores correctly.
    def test_game_cycle_movement_and_shooting(self):
        # Test player movement and shooting
        self.assertGreater(len(players), 0, "Players list should not be empty after NewGame")
        keys = {pygame.K_w: True, pygame.K_a: False, pygame.K_d: False, pygame.K_LEFT: False, pygame.K_RIGHT: False}
        initial_pos = players[0].GetPos()
        players[0].Movement(keys)
        self.assertNotEqual(players[0].GetPos(), initial_pos, 
                            "Player 0 position should change after movement with 'w' key")
        pygame.time.get_ticks = MagicMock(return_value=1000)
        players[0].UpdateLastShotTime()
        Shoot(0)  # Player 0 shoots
        self.assertEqual(len(projectiles), 1, 
                         "Projectile should be created after Player 0 shoots")

    def test_game_cycle_wall_generation(self):
        # Test wall generation
        self.assertGreater(len(players), 0, "Players list should not be empty after NewGame")
        initial_walls = len(walls)
        GenerateWall(0)  # Generate a wall for Player 0
        self.assertEqual(len(walls), initial_walls + 1, 
                         "Wall should be created for Player 0")

    def test_game_cycle_collision_and_game_over(self):
        # Test collision and game over
        self.assertGreater(len(players), 0, "Players list should not be empty after NewGame")
        players[0].SetPos(100, 100)
        walls.append(Wall(self.surface, self.wall_sprite, (100, 100), 0))
        players[0].GetRect = MagicMock(return_value=pygame.Rect(100, 100, 12, 11))
        walls[0].GetRect = MagicMock(return_value=pygame.Rect(100, 100, 16, 16))
        players[0].GetRect().colliderect = MagicMock(return_value=True)
        initial_score = GetScore()
        UpdatePScore(1, initial_score)  # Simulate score update
        CheckCollisions()
        self.assertEqual(len(players), 0, 
                         "Players list should be cleared after collision triggers GameOver")
        self.assertEqual(len(walls), 0, 
                         "Walls list should be cleared after collision triggers GameOver")
        self.assertEqual(len(projectiles), 0, 
                         "Projectiles list should be cleared after collision triggers GameOver")
        self.assertEqual(pScores[1], initial_score, 
                         "Player 1 score should be updated with current score after Player 0 collision")

if __name__ == '__main__':
    unittest.main(verbosity=2)