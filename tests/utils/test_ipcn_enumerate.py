import unittest
from drnonsilentxml.utils.ipcn_enumerate import ipcn_enumerate

class TestIpcnEnumerate(unittest.TestCase):
    """Test case for ipcn_enumerate module."""

    def test_empty_list(self):
        """Test with an empty list."""
        result = list(ipcn_enumerate([]))
        self.assertEqual(result, [])
        
    def test_single_element(self):
        """Test with a single element."""
        result = list(ipcn_enumerate([1]))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (0, None, 1, None))
        
    def test_two_elements(self):
        """Test with two elements."""
        result = list(ipcn_enumerate([1, 2]))
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], (0, None, 1, 2))
        self.assertEqual(result[1], (1, 1, 2, None))
        
    def test_multiple_elements(self):
        """Test with multiple elements."""
        result = list(ipcn_enumerate([10, 20, 30, 40]))
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], (0, None, 10, 20))
        self.assertEqual(result[1], (1, 10, 20, 30))
        self.assertEqual(result[2], (2, 20, 30, 40))
        self.assertEqual(result[3], (3, 30, 40, None))

if __name__ == '__main__':
    unittest.main()
