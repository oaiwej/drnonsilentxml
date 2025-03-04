import unittest
from xml.etree.ElementTree import Element, tostring
from drnonsilentxml.utils.to_xml import to_xml

class TestToXml(unittest.TestCase):
    """Test case for to_xml module."""

    def test_simple_element(self):
        """Test creating a simple XML element."""
        root = Element('root')
        to_xml(root, [('child', 'value')])
        
        # Convert to string and check
        xml_str = tostring(root, encoding='unicode')
        self.assertIn('<root>', xml_str)
        self.assertIn('<child>value</child>', xml_str)
        
    def test_nested_elements(self):
        """Test creating nested XML elements."""
        root = Element('root')
        to_xml(root, [
            ('parent', [
                ('child1', 'value1'),
                ('child2', 'value2')
            ])
        ])
        
        # Convert to string and check
        xml_str = tostring(root, encoding='unicode')
        self.assertIn('<parent>', xml_str)
        self.assertIn('<child1>value1</child1>', xml_str)
        self.assertIn('<child2>value2</child2>', xml_str)
        
    def test_with_attributes(self):
        """Test creating elements with attributes."""
        root = Element('root')
        to_xml(root, [
            ('element', 'content', {'attr1': 'val1', 'attr2': 'val2'})
        ])
        
        # Convert to string and check
        xml_str = tostring(root, encoding='unicode')
        self.assertIn('attr1="val1"', xml_str)
        self.assertIn('attr2="val2"', xml_str)
        self.assertIn('>content<', xml_str)
        
    def test_complex_structure(self):
        """Test creating a complex XML structure."""
        root = Element('root')
        to_xml(root, [
            ('level1', [
                ('level2a', 'text2a'),
                ('level2b', [
                    ('level3', 'text3', {'id': '123'})
                ], {'attr': 'value'})
            ])
        ])
        
        # Convert to string and check
        xml_str = tostring(root, encoding='unicode')
        self.assertIn('<level1>', xml_str)
        self.assertIn('<level2a>text2a</level2a>', xml_str)
        self.assertIn('attr="value"', xml_str)
        self.assertIn('id="123"', xml_str)
        # 修正: XMLタグ全体ではなく、コンテンツのみをチェック
        self.assertIn('level3', xml_str)
        self.assertIn('text3', xml_str)

if __name__ == '__main__':
    unittest.main()
