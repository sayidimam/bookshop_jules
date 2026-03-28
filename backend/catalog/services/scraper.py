import requests
from bs4 import BeautifulSoup
import json
from decimal import Decimal

class WafilifeScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def scrape(self, url):
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch URL: {response.status_code}")

        soup = BeautifulSoup(response.content, 'html.parser')

        # 1. Try to find JSON-LD
        json_ld_data = {}
        script_tag = soup.find('script', type='application/ld+json')
        if script_tag:
            try:
                json_ld_data = json.loads(script_tag.string)
            except json.JSONDecodeError:
                pass

        # 2. Extract Data
        data = {
            'title': self._get_title(soup, json_ld_data),
            'authors': self._get_authors(soup, json_ld_data),
            'publisher': self._get_publisher(soup, json_ld_data),
            'description': self._get_description(soup, json_ld_data),
            'sale_price': self._get_sale_price(soup, json_ld_data),
            'regular_price': self._get_regular_price(soup, json_ld_data),
            'image_url': self._get_image_url(soup, json_ld_data),
            'page_count': self._get_page_count(soup, json_ld_data),
            'edition': self._get_edition(soup, json_ld_data),
            'language': self._get_language(soup, json_ld_data),
            'categories': self._get_categories(soup, json_ld_data),
        }

        # Fallback: If regular price is missing, assume it's same as sale price
        if not data['regular_price'] and data['sale_price']:
            data['regular_price'] = data['sale_price']

        return data

    def _get_title(self, soup, ld):
        if ld.get('name'):
            return ld['name']
        return soup.find('h1').text.strip() if soup.find('h1') else ''

    def _get_authors(self, soup, ld):
        authors = []
        if ld.get('author'):
            auths = ld['author']
            if isinstance(auths, list):
                authors = [a.get('name') for a in auths]
            elif isinstance(auths, dict):
                authors = [auths.get('name')]

        # Fallback to DOM if empty
        if not authors:
            # Example logic, might need adjustment based on real HTML structure
            # Looking for links under "লেখক :"
            pass
        return authors

    def _get_publisher(self, soup, ld):
        if ld.get('publisher'):
            pub = ld['publisher']
            if isinstance(pub, dict):
                return pub.get('name')
            return str(pub)
        return ''

    def _get_description(self, soup, ld):
        if ld.get('description'):
            return ld['description']
        # Fallback to meta description
        meta = soup.find('meta', {'name': 'description'})
        return meta['content'] if meta else ''

    def _get_sale_price(self, soup, ld):
        if ld.get('offers'):
            return Decimal(ld['offers'].get('price', 0))
        return Decimal(0)

    def _get_regular_price(self, soup, ld):
        # Wafilife usually puts regular price in a <del> tag near the price
        # The user provided HTML shows: <del class="mx-1 text-brand-dark text-opacity-70">৪১৪৳</del>
        del_tag = soup.find('del')
        if del_tag:
            price_text = del_tag.text.strip().replace('৳', '').replace(',', '')
            # Convert Bengali digits to English if necessary, though Decimal usually fails on Bengali digits
            # Simple mapping
            return self._parse_bengali_number(price_text)
        return None

    def _get_image_url(self, soup, ld):
        if ld.get('image'):
            imgs = ld['image']
            if isinstance(imgs, list):
                return imgs[0]
            return str(imgs)
        return ''

    def _get_page_count(self, soup, ld):
        if ld.get('numberOfPages'):
            return int(ld['numberOfPages'])
        return None

    def _get_edition(self, soup, ld):
        if ld.get('edition'):
            return ld['edition']
        return ''

    def _get_language(self, soup, ld):
        if ld.get('inLanguage'):
            return ld['inLanguage']
        return 'Bangla'

    def _get_categories(self, soup, ld):
        if ld.get('category'):
            return [ld['category']]
        return []

    def _parse_bengali_number(self, text):
        bn_to_en = str.maketrans('০১২৩৪৫৬৭৮৯', '0123456789')
        text = text.translate(bn_to_en)
        try:
            return Decimal(text)
        except:
            return None
