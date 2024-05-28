import pytest
from unittest.mock import mock_open, patch
from html_to_json_parser import JSONExtractor, JSONComparator

class TestJSONExtractor:
    @pytest.fixture
    def setup_extractor(self):
        # Mocking HTML content for testing the functions in html_to_json_parser.py
        html_content = """
        <g-scrolling-carousel>
            <a class="klitem" aria-label="Artwork1" title="Artwork (2000)" href="/link1">
                <g-img id="img1"></g-img>
            </a>
            <a class="klitem" aria-label="Artwork2" title="Artwork (2001)" href="/link2">
                <g-img id="img2"></g-img>
            </a>
        </g-scrolling-carousel>
        """
        with patch('builtins.open', mock_open(read_data=html_content)):
            extractor = JSONExtractor('mock_file.html')
            yield extractor

    def test_html_loading(self, setup_extractor):
        assert setup_extractor.soup is not None, "Soup should be initialized."

    def test_data_extraction(self, setup_extractor):
        data = setup_extractor.extract_data()
        assert type(data) is dict, "Data should be a dictionary."
        assert 'unknown' in data, "Data should contain a key from the elabel."
        assert len(data['unknown']) == 2, "There should be two elements extracted."

    @patch('builtins.open', new_callable=mock_open)
    def test_json_writing(self, mock_file, setup_extractor):
        setup_extractor.write_json({'test': 'data'}, 'test.json')
        mock_file.assert_called_once_with('test.json', 'w')

class TestJSONComparator:
    @patch('builtins.open', mock_open(read_data='{"test": "data"}'))
    def test_load_json_file(self):
        result = JSONComparator.load_json_file('mock_file.json')
        assert result == {'test': 'data'}, "JSON loading should return the correct data."

    def test_compare_json(self):
        result = JSONComparator.compare_json({'test': 'data'}, {'test': 'data'})
        assert result is True, "JSON comparison should be True for identical objects."
        result = JSONComparator.compare_json({'test': 'data'}, {'test': 'data2'})
        assert result is False, "JSON comparison should be False for different objects."

# Additional configuration for pytest to run this script
if __name__ == "__main__":
    pytest.main()
