import unittest
from unittest.mock import MagicMock
import pygame
from gameTest import UpdateScore, GetScore, GameOver, pScores

# Black Box Testing
# Definition: Tests based on inputs and expected outputs without knowledge of internal code.
# Focus: Test game functionality from a user perspective, e.g., score updates, player death.

class TestGameBlackBox(unittest.TestCase):
    def setUp(self):
        # Mock Pygame dependencies
        pygame.init = MagicMock()
        pygame.font.init = MagicMock()
        # Initialize global variables
        global pScores, score
        pScores = [0, 0]
        score = 0  # Reset score directly, assuming global score variable

    # Tests score updates and game over behavior based on expected outcomes 
    # (e.g., score increments, Player 1 gets points when Player 0 dies).
    # No internal code knowledge is assumed.
    def test_score_increment(self):
        # Test incrementing the score
        UpdateScore(10)
        self.assertEqual(GetScore(), 10, 
                         "Score should be incremented to 10 after UpdateScore(10)")
        UpdateScore(5)
        self.assertEqual(GetScore(), 15, 
                         "Score should be incremented to 15 after additional UpdateScore(5)")

    def test_score_reset(self):
        # Test resetting the score via GameOver
        UpdateScore(20)
        GameOver(0)  # Use GameOver to reset score (assumes it resets score)
        self.assertEqual(GetScore(), 0, 
                         "Score should be reset to 0 after GameOver")

    def test_game_over_score_update_player0_dies(self):
        # Test score update when Player 0 dies
        UpdateScore(100)
        GameOver(0)  # Player 0 dies, Player 1 gets score
        self.assertEqual(pScores[1], 100, 
                         "Player 1 score should be updated to 100 when Player 0 dies")
        self.assertEqual(GetScore(), 0, 
                         "Game score should be reset to 0 after GameOver")

    def test_game_over_score_update_player1_dies(self):
        # Test score update when Player 1 dies
        UpdateScore(50)
        GameOver(1)  # Player 1 dies, Player 0 gets score
        self.assertEqual(pScores[0], 50, 
                         "Player 0 score should be updated to 50 when Player 1 dies")
        self.assertEqual(GetScore(), 0, 
                         "Game score should be reset to 0 after GameOver")

if __name__ == '__main__':
    unittest.main(verbosity=2)