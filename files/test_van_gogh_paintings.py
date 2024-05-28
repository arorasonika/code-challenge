from html_to_json_parser import JSONExtractor, JSONComparator
import pytest

class TestVanGoghPaintingsHtmlToJson:

    def test_scrolling_carousel(self):
        extractor = JSONExtractor('van-gogh-paintings.html')
        extracted_data = extractor.extract_data()
        extractor.write_json(extracted_data, 'generated-array-van-gogh-paintings.json')

        generated_file = JSONComparator.load_json_file('generated-array-van-gogh-paintings.json')
        expected_file = JSONComparator.load_json_file('expected-array.json')

        result = False
        if generated_file:
            result = JSONComparator.compare_json(generated_file, expected_file)
        print(result)
        assert result is True, "JSON data matches. The generated array is as expected."

# Additional configuration for pytest to run this script
if __name__ == "__main__":
    pytest.main()
