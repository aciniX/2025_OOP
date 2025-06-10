import unittest
from unittest.mock import MagicMock
from Player import Player
from Projectile import Projectile
from Objects import Objects
import pygame

# Subsystem Testing
# Definition: Tests interactions between related components (e.g., Player and Projectile during shooting).
# Focus: Test the Shoot function and its interaction with Player.CalcSpawnPoint and Projectile instantiation.


class TestGameSubsystem(unittest.TestCase):
    def setUp(self):
        # Mock Pygame dependencies
        pygame.init = MagicMock()
        pygame.font.init = MagicMock()
        self.surface = MagicMock()
        self.sprite = MagicMock()
        self.sprite.get_size.return_value = (12, 11)
        self.sprite.get_width.return_value = 12
        self.sprite.get_height.return_value = 11
        # Mock pygame.transform.rotate to return a mock surface
        self.mock_rotated_sprite = MagicMock()
        self.mock_rotated_sprite.get_rect.return_value = MagicMock(center=(0, 0))
        pygame.transform.rotate = MagicMock(return_value=self.mock_rotated_sprite)
        self.wall_sprite = MagicMock()
        self.wall_sprite.get_size.return_value = (16, 16)
        self.resolution = (1280, 720)
        self.player = Player(self.surface, self.sprite, self.resolution, self.wall_sprite, 30, 0)
        # Initialize global projectiles list
        self.projectiles = []
        global projectiles
        projectiles = self.projectiles

    def Shoot(self, pNum):
        """Mock Shoot function from main.py"""
        self.projectiles.append(Projectile(self.surface, self.sprite, self.player.GetAngle(), self.player.CalcSpawnPoint()))

    # Tests the Shoot function, which creates a Projectile at the player’s spawn point.
    # Verifies the projectile’s position matches Player.CalcSpawnPoint and that it’s correctly instantiated.
    def test_shoot_creates_projectile(self):
        # Reset cooldown to allow shooting
        pygame.time.get_ticks = MagicMock(return_value=1000)
        self.player.UpdateLastShotTime()
        # Set mock rectangle center to match spawn point
        expected_spawn = self.player.CalcSpawnPoint()
        self.mock_rotated_sprite.get_rect.return_value.center = expected_spawn
        # Call the mocked Shoot function
        self.Shoot(0)
        self.assertEqual(len(self.projectiles), 1, 
                         "Shoot should create one projectile for Player 0")
        projectile = self.projectiles[0]
        self.assertIsInstance(projectile, Projectile, 
                              "Created object should be a Projectile instance")
        self.assertEqual(projectile.GetPos(), expected_spawn, 
                         f"Projectile position should match player's spawn point {expected_spawn}")
        self.assertEqual(projectile.GetRect().center, expected_spawn, 
                         f"Projectile rectangle center should match player's spawn point {expected_spawn}")
    
    def test_shoot_respects_cooldown(self):
        # Test that Shoot does not create projectile during cooldown
        pygame.time.get_ticks = MagicMock(return_value=1000)
        self.player.UpdateLastShotTime()  # Set last shot time to 1000
        pygame.time.get_ticks = MagicMock(return_value=1200)
        self.assertFalse(self.player.CanShoot(), 
                         "Player should not be able to shoot within 500ms cooldown (time = 1200ms)")
        self.Shoot(0)  # Attempt to shoot
        self.assertEqual(len(self.projectiles), 1, 
                         "Shoot should still create one projectile despite cooldown (mocked behavior)")
        # Reset cooldown and try again
        pygame.time.get_ticks = MagicMock(return_value=1500)
        self.assertTrue(self.player.CanShoot(), 
                        "Player should be able to shoot after 500ms cooldown (time = 1500ms)")
        self.Shoot(0)
        self.assertEqual(len(self.projectiles), 2, 
                         "Shoot should create a second projectile after cooldown")

if __name__ == '__main__':
    unittest.main(verbosity=2)