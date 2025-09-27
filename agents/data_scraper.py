"""
MEM_AGENT Data Scraper Module
Advanced web scraping and data collection system
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import asyncio
import aiohttp
from urllib.parse import urljoin, urlparse
import re

@dataclass
class ScrapedData:
    """Data structure for scraped content"""
    url: str
    title: str
    content: str
    metadata: Dict[str, Any]
    timestamp: datetime
    source_type: str

class MEMAgentDataScraper:
    """Advanced data scraper for MEM_AGENT system"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.scraped_data = []
        self.logger = logging.getLogger(__name__)
        
    def scrape_website(self, url: str, selectors: Dict[str, str] = None) -> ScrapedData:
        """Scrape a single website with custom selectors"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract data using selectors
            title = self._extract_title(soup, selectors)
            content = self._extract_content(soup, selectors)
            metadata = self._extract_metadata(soup, url)
            
            scraped_data = ScrapedData(
                url=url,
                title=title,
                content=content,
                metadata=metadata,
                timestamp=datetime.now(),
                source_type='website'
            )
            
            self.scraped_data.append(scraped_data)
            self.logger.info(f"Successfully scraped: {url}")
            return scraped_data
            
        except Exception as e:
            self.logger.error(f"Error scraping {url}: {str(e)}")
            return None
    
    def scrape_multiple_urls(self, urls: List[str], delay: float = 1.0) -> List[ScrapedData]:
        """Scrape multiple URLs with delay between requests"""
        results = []
        for url in urls:
            data = self.scrape_website(url)
            if data:
                results.append(data)
            time.sleep(delay)  # Respectful scraping
        return results
    
    async def async_scrape(self, urls: List[str]) -> List[ScrapedData]:
        """Asynchronous scraping for better performance"""
        async with aiohttp.ClientSession() as session:
            tasks = [self._async_scrape_single(session, url) for url in urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            return [r for r in results if isinstance(r, ScrapedData)]
    
    async def _async_scrape_single(self, session: aiohttp.ClientSession, url: str) -> Optional[ScrapedData]:
        """Scrape a single URL asynchronously"""
        try:
            async with session.get(url) as response:
                content = await response.text()
                soup = BeautifulSoup(content, 'html.parser')
                
                return ScrapedData(
                    url=url,
                    title=self._extract_title(soup),
                    content=self._extract_content(soup),
                    metadata=self._extract_metadata(soup, url),
                    timestamp=datetime.now(),
                    source_type='website'
                )
        except Exception as e:
            self.logger.error(f"Async scraping error for {url}: {str(e)}")
            return None
    
    def scrape_api_endpoints(self, base_url: str, endpoints: List[str]) -> List[Dict]:
        """Scrape API endpoints for data"""
        results = []
        for endpoint in endpoints:
            try:
                url = urljoin(base_url, endpoint)
                response = self.session.get(url)
                response.raise_for_status()
                
                data = {
                    'endpoint': endpoint,
                    'url': url,
                    'data': response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
                    'status_code': response.status_code,
                    'timestamp': datetime.now().isoformat()
                }
                results.append(data)
                
            except Exception as e:
                self.logger.error(f"API scraping error for {endpoint}: {str(e)}")
        
        return results
    
    def scrape_social_media(self, platform: str, query: str) -> List[Dict]:
        """Scrape social media platforms (placeholder for API integration)"""
        # This would integrate with social media APIs
        # For now, return mock data structure
        return [{
            'platform': platform,
            'query': query,
            'posts': [],
            'timestamp': datetime.now().isoformat()
        }]
    
    def scrape_news_sources(self, sources: List[str]) -> List[ScrapedData]:
        """Scrape news sources for business intelligence"""
        news_data = []
        for source in sources:
            data = self.scrape_website(source, {
                'title': 'h1, .headline, .title',
                'content': '.article-content, .story-body, .content',
                'author': '.author, .byline',
                'date': '.date, .timestamp, time'
            })
            if data:
                data.source_type = 'news'
                news_data.append(data)
        return news_data
    
    def scrape_competitor_analysis(self, competitor_urls: List[str]) -> Dict[str, Any]:
        """Scrape competitor websites for analysis"""
        analysis = {
            'competitors': [],
            'common_keywords': [],
            'pricing_info': [],
            'features': [],
            'timestamp': datetime.now().isoformat()
        }
        
        for url in competitor_urls:
            data = self.scrape_website(url)
            if data:
                competitor_info = {
                    'url': url,
                    'title': data.title,
                    'content_length': len(data.content),
                    'metadata': data.metadata
                }
                analysis['competitors'].append(competitor_info)
        
        return analysis
    
    def _extract_title(self, soup: BeautifulSoup, selectors: Dict[str, str] = None) -> str:
        """Extract title from HTML"""
        if selectors and 'title' in selectors:
            element = soup.select_one(selectors['title'])
            return element.get_text(strip=True) if element else ""
        
        # Default selectors
        title_selectors = ['h1', 'title', '.headline', '.title']
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        return ""
    
    def _extract_content(self, soup: BeautifulSoup, selectors: Dict[str, str] = None) -> str:
        """Extract main content from HTML"""
        if selectors and 'content' in selectors:
            element = soup.select_one(selectors['content'])
            return element.get_text(strip=True) if element else ""
        
        # Default content extraction
        content_selectors = [
            'article', '.article-content', '.content', 
            '.post-content', '.story-body', 'main'
        ]
        
        for selector in content_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        
        # Fallback to body content
        body = soup.find('body')
        return body.get_text(strip=True) if body else ""
    
    def _extract_metadata(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """Extract metadata from HTML"""
        metadata = {
            'url': url,
            'domain': urlparse(url).netloc,
            'meta_description': '',
            'meta_keywords': '',
            'links': [],
            'images': [],
            'word_count': 0
        }
        
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            metadata['meta_description'] = meta_desc.get('content', '')
        
        # Meta keywords
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords:
            metadata['meta_keywords'] = meta_keywords.get('content', '')
        
        # Extract links
        links = soup.find_all('a', href=True)
        metadata['links'] = [urljoin(url, link['href']) for link in links[:50]]  # Limit to 50 links
        
        # Extract images
        images = soup.find_all('img', src=True)
        metadata['images'] = [urljoin(url, img['src']) for img in images[:20]]  # Limit to 20 images
        
        # Word count
        text_content = soup.get_text()
        metadata['word_count'] = len(text_content.split())
        
        return metadata
    
    def save_scraped_data(self, filename: str = None) -> str:
        """Save scraped data to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"scraped_data_{timestamp}.json"
        
        data_to_save = []
        for item in self.scraped_data:
            data_to_save.append({
                'url': item.url,
                'title': item.title,
                'content': item.content,
                'metadata': item.metadata,
                'timestamp': item.timestamp.isoformat(),
                'source_type': item.source_type
            })
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Scraped data saved to {filename}")
        return filename
    
    def get_business_intelligence(self, target_domains: List[str]) -> Dict[str, Any]:
        """Generate business intelligence from scraped data"""
        bi_data = {
            'market_analysis': {},
            'competitor_insights': {},
            'content_analysis': {},
            'trends': {},
            'recommendations': []
        }
        
        # Analyze scraped data for business insights
        for data in self.scraped_data:
            if data.metadata.get('domain') in target_domains:
                # Extract business insights
                bi_data['content_analysis'][data.url] = {
                    'word_count': data.metadata.get('word_count', 0),
                    'title': data.title,
                    'has_pricing': 'price' in data.content.lower(),
                    'has_contact': any(word in data.content.lower() for word in ['contact', 'phone', 'email']),
                    'has_social': any(platform in data.content.lower() for platform in ['facebook', 'twitter', 'linkedin', 'instagram'])
                }
        
        return bi_data

# Example usage and testing
if __name__ == "__main__":
    scraper = MEMAgentDataScraper()
    
    # Test scraping
    test_urls = [
        "https://example.com",
        "https://httpbin.org/html"
    ]
    
    print("Testing MEM_AGENT Data Scraper...")
    results = scraper.scrape_multiple_urls(test_urls)
    print(f"Scraped {len(results)} URLs successfully")
    
    # Save data
    filename = scraper.save_scraped_data()
    print(f"Data saved to {filename}")
