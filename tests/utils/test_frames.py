import unittest
import sys
import os

# デバッグ情報を表示
print(f"Python path: {sys.path}")
print(f"Current directory: {os.getcwd()}")

try:
    from drnonsilentxml.utils.frames import frames
    print("Successfully imported frames module")
except ImportError as e:
    print(f"Error importing frames module: {e}")
    raise

class TestFrames(unittest.TestCase):
    """Test case for frames module."""

    def test_frames_conversion(self):
        """Test frames conversion from milliseconds to frame count."""
        # 1 second at 30fps should be 30 frames
        self.assertEqual(frames(1000, 30, 30), "30")
        
        # 1 second at 60fps input, 30fps output should be 30 frames
        self.assertEqual(frames(1000, 60, 30), "30")
        
        # 500ms at 30fps should be 15 frames
        self.assertEqual(frames(500, 30, 30), "15")
        
        # 0ms should be 0 frames
        self.assertEqual(frames(0, 30, 30), "0")
        
        # Different input/output fps
        self.assertEqual(frames(1000, 24, 60), "60")
        
        # NTSC framerate 29.97
        self.assertEqual(frames(1000, 30, 29.97), "29")  # Rounded down
        
        # Check large millisecond values
        self.assertEqual(frames(10000, 30, 30), "300")  # 10 seconds = 300 frames

if __name__ == '__main__':
    unittest.main()
