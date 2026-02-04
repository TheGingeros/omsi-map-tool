import pytest
from pyomsi.parsers.base_parser import OmsiBaseParser

# Mock file system, maybe integrate mock files TODO
from unittest.mock import patch, mock_open

SAMPLE_OMSI_CONTENT = r"""
[version]
2.0

[friendlyname]
Test Map

[spline]
Splines\Marcel\street.sli
1
2
"""

def test_parser_yields_correct_blocks():
    # Simulate opeaning a file with the data above
    with patch("builtins.open", mock_open(read_data=SAMPLE_OMSI_CONTENT)):
        parser = OmsiBaseParser("dummy_path.map")
        
        # Get all lines as blocks
        blocks = list(parser.parse_blocks())
        
        # TEST 1: All the blocks were loaded?
        assert len(blocks) == 3
        
        # TEST 2: Is the first block the version?
        keyword, data = blocks[0]
        assert keyword == "version"
        assert data[0] == "2.0"
        
        # TEST 3: spline block?
        keyword, data = blocks[2]
        assert keyword == "spline"
        assert len(data) == 3