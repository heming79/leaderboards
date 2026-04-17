import requests
from bs4 import BeautifulSoup
from app import db, create_app
from app.models.provider import Provider
import time

class ArtificialAnalysisScraper:
    def __init__(self):
        self.base_url = 'https://artificialanalysis.ai'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrape_providers(self):
        url = f'{self.base_url}/leaderboards/providers'
        print(f'Scraping {url}...')
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            providers = self._parse_providers(soup)
            
            print(f'Found {len(providers)} providers')
            return providers
            
        except Exception as e:
            print(f'Error scraping providers: {e}')
            return []
    
    def _parse_providers(self, soup):
        providers = []
        
        provider_cards = soup.find_all('div', class_='provider-card')
        
        if not provider_cards:
            provider_cards = soup.find_all('tr', class_='provider-row')
        
        if not provider_cards:
            provider_cards = soup.find_all('div', {'data-testid': 'provider-item'})
        
        for card in provider_cards:
            provider = self._parse_provider_card(card)
            if provider:
                providers.append(provider)
        
        return providers
    
    def _parse_provider_card(self, card):
        try:
            name = self._extract_text(card, ['provider-name', 'name', 'h3', 'h4'])
            if not name:
                return None
            
            provider = {
                'name': name,
                'intelligence_index': self._extract_float(card, ['intelligence-index', 'intelligence', 'score']),
                'coding_index': self._extract_float(card, ['coding-index', 'coding']),
                'agentic_index': self._extract_float(card, ['agentic-index', 'agentic']),
                'price_per_1k_input': self._extract_price(card, ['input-price', 'price-input']),
                'price_per_1k_output': self._extract_price(card, ['output-price', 'price-output']),
                'latency_ms': self._extract_float(card, ['latency', 'latency-ms']),
                'throughput_tokens_per_sec': self._extract_float(card, ['throughput', 'tokens-per-sec']),
                'models_count': self._extract_int(card, ['models-count', 'models'])
            }
            
            return provider
            
        except Exception as e:
            print(f'Error parsing provider card: {e}')
            return None
    
    def _extract_text(self, element, classes):
        for cls in classes:
            found = element.find(class_=cls)
            if found:
                return found.get_text(strip=True)
        
        for tag in ['h3', 'h4', 'strong', 'b']:
            found = element.find(tag)
            if found:
                return found.get_text(strip=True)
        
        return None
    
    def _extract_float(self, element, classes):
        for cls in classes:
            found = element.find(class_=cls)
            if found:
                text = found.get_text(strip=True)
                return self._parse_float(text)
        
        return None
    
    def _extract_price(self, element, classes):
        for cls in classes:
            found = element.find(class_=cls)
            if found:
                text = found.get_text(strip=True)
                return self._parse_price(text)
        
        return None
    
    def _extract_int(self, element, classes):
        for cls in classes:
            found = element.find(class_=cls)
            if found:
                text = found.get_text(strip=True)
                return self._parse_int(text)
        
        return None
    
    def _parse_float(self, text):
        if not text:
            return None
        
        try:
            cleaned = ''.join(c for c in text if c.isdigit() or c == '.' or c == '-')
            return float(cleaned)
        except:
            return None
    
    def _parse_price(self, text):
        if not text:
            return None
        
        try:
            cleaned = ''.join(c for c in text if c.isdigit() or c == '.')
            return float(cleaned)
        except:
            return None
    
    def _parse_int(self, text):
        if not text:
            return None
        
        try:
            cleaned = ''.join(c for c in text if c.isdigit())
            return int(cleaned)
        except:
            return None

def scrape_and_save():
    scraper = ArtificialAnalysisScraper()
    providers = scraper.scrape_providers()
    
    if not providers:
        print('No providers found, using sample data instead')
        from app.utils.database import add_sample_data
        add_sample_data()
        return
    
    app = create_app()
    with app.app_context():
        for provider_data in providers:
            existing_provider = Provider.query.filter_by(name=provider_data['name']).first()
            
            if existing_provider:
                for key, value in provider_data.items():
                    if value is not None and hasattr(existing_provider, key):
                        setattr(existing_provider, key, value)
            else:
                provider = Provider(**provider_data)
                db.session.add(provider)
        
        db.session.commit()
        print(f'Saved {len(providers)} providers to database')

if __name__ == '__main__':
    scrape_and_save()
