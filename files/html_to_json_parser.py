import json
import re
from bs4 import BeautifulSoup

class JSONExtractor:
    def __init__(self, html_file_path):
        self.html_file_path = html_file_path
        self.soup = None
        self.load_html()

    def load_html(self):
        with open(self.html_file_path, 'r', encoding='utf-8') as file:
            self.soup = BeautifulSoup(file, 'html.parser')

    def extract_data(self):
        carousel_elements = self.soup.find('g-scrolling-carousel').find_all('a', class_='klitem')
        result_carousel_elements = []
        for element in carousel_elements:
            attributes = self.process_element(element)
            result_carousel_elements.append(attributes)
        images = self.get_all_images()
        for elem in result_carousel_elements:
            self.get_image(elem, images)
        title = self.get_title()
        return {title: result_carousel_elements}

    def process_element(self, element):
        attributes = {}
        html_attributes = {attr: element[attr] for attr in element.attrs}
        
        attributes['name'] = html_attributes["aria-label"]
        extensions = re.findall(r'\((\d+)\)', html_attributes["title"])
        if extensions:
            attributes['extensions'] = extensions
        attributes['link'] = "https://www.google.com" + html_attributes["href"]
        g_img = {g_img.parent.name: {attr: g_img[attr] for attr in g_img.attrs} for g_img in element.find('g-img')}
        if g_img:
            attributes['image'] = g_img['g-img']["id"]
        return attributes

    def get_all_images(self):
        script_elements = self.soup.find_all('script')
        results = {}
        pattern = r'var\s+s\s*=\s*"([^"]+)"\s*;\s*var\s+ii\s*=\s*\[([^]]+)\]\s*;'
        for script in script_elements:
            matches = re.findall(pattern, script.string, re.DOTALL)
            for match in matches:
                s_value, ii_value = match
                ii_value = ii_value.replace('"', '').split(',')
                for val in ii_value:
                    results[val] = s_value
        return results

    def get_image(self, elem, images):
        if 'image' in elem:
            image_id = elem['image']
            if image_id in images:
                elem['image'] = images[image_id].replace("\\", "")
            else:
                elem['image'] = None

    def get_title(self):
        span_tags = self.soup.find_all('span', attrs={'data-elabel': True})
        data_elabel = 'unknown'
        for tag in span_tags:
            data_elabel = tag['data-elabel']
        return data_elabel.lower()

    def write_json(self, data, filename):
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)

class JSONComparator:
    @staticmethod
    def load_json_file(json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def compare_json(json1, json2):
        return json1 == json2

def main():
    extractor = JSONExtractor('van-gogh-paintings.html')
    extracted_data = extractor.extract_data()
    extractor.write_json(extracted_data, 'generated-array-van-gogh-paintings.json')

    generated_file = JSONComparator.load_json_file('generated-array-van-gogh-paintings.json')
    expected_file = JSONComparator.load_json_file('expected-array.json')

    if generated_file:
        result = JSONComparator.compare_json(generated_file, expected_file)
        print("JSON data matches." if result else "JSON data does not match.")
    else:
        print("No JSON data found in the HTML file.")

if __name__ == "__main__":
    main()
