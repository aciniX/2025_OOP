import unittest
from unittest.mock import MagicMock
from Player import Player
from Objects import Objects
import pygame
import math

# Unit Testing
# Definition: Tests individual methods or functions in isolation, ensuring they work as expected.
# Focus: Test methods like Player.Movement, Projectile.Movement, Wall.GetRect, etc., mocking dependencies 
# (e.g., pygame.Surface, pygame.image).
#
# Testing will mock Pygame's surface and sprite to avoid rendering issues.

class TestPlayerUnit(unittest.TestCase):
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

    def test_movement_player0_right(self):
        # Test Player 0 moving right (angle decreases with 'd' key)
        keys = {pygame.K_a: False, pygame.K_d: True, pygame.K_LEFT: False, pygame.K_RIGHT: False}
        initial_pos = self.player.GetPos()
        initial_angle = self.player.GetAngle()
        self.player.Movement(keys)
        # Check angle decreases by rotation_speed (3 degrees)
        self.assertEqual(self.player.GetAngle(), initial_angle - 3, 
                         "Player angle should decrease by 3 degrees when 'd' key is pressed")
        # Check position updates based on angle (90 - 3 = 87 degrees)
        rad = math.radians(87)
        expected_x = initial_pos[0] + math.cos(rad) * 2  # speed = 2
        expected_y = initial_pos[1] - math.sin(rad) * 2
        self.assertAlmostEqual(self.player.GetPos()[0], expected_x, 5, "Player x-position should update based on angle 87 degrees")
        self.assertAlmostEqual(self.player.GetPos()[1], expected_y, places=5, msg="Player y-position should update based on angle 87 degrees")

    def test_movement_player0_left(self):
        # Test Player 0 moving left (angle increases with 'a' key)
        keys = {pygame.K_a: True, pygame.K_d: False, pygame.K_LEFT: False, pygame.K_RIGHT: False}
        initial_pos = self.player.GetPos()
        initial_angle = self.player.GetAngle()
        self.player.Movement(keys)
        # Check angle increases by rotation_speed (3 degrees)
        self.assertEqual(self.player.GetAngle(), initial_angle + 3, 
                         "Player angle should increase by 3 degrees when 'a' key is pressed")
        # Check position updates based on angle (90 + 3 = 93 degrees)
        rad = math.radians(93)
        expected_x = initial_pos[0] + math.cos(rad) * 2  # speed = 2
        expected_y = initial_pos[1] - math.sin(rad) * 2
        self.assertAlmostEqual(self.player.GetPos()[0], expected_x, 5, msg="Player x-position should update based on angle 93 degrees")
        self.assertAlmostEqual(self.player.GetPos()[1], expected_y, places=5, msg="Player y-position should update based on angle 93 degrees")

    def test_can_shoot_within_cooldown(self):
        # Test shooting within cooldown period
        pygame.time.get_ticks = MagicMock(return_value=1000)
        self.player.UpdateLastShotTime()  # Set last shot time to 1000
        pygame.time.get_ticks = MagicMock(return_value=1200)
        self.assertFalse(self.player.CanShoot(), 
                         "Player should not be able to shoot within 500ms cooldown (time = 1200ms)")

    def test_can_shoot_after_cooldown(self):
        # Test shooting after cooldown period
        pygame.time.get_ticks = MagicMock(return_value=1000)
        self.player.UpdateLastShotTime()  # Set last shot time to 1000
        pygame.time.get_ticks = MagicMock(return_value=1500)
        self.assertTrue(self.player.CanShoot(), 
                        "Player should be able to shoot after 500ms cooldown (time = 1500ms)")

if __name__ == '__main__':
    unittest.main(verbosity=2)