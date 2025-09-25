#!/usr/bin/env python3
"""
Web Scraper - Knowledge Acquisition for Memory Agent
Complete web scraping system with error handling
"""

import requests
from bs4 import BeautifulSoup
import time
import csv
import logging
from pathlib import Path
from urllib.parse import urljoin, urlparse
import re

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebScraper:
    """Complete web scraping system for knowledge acquisition"""
    
    def __init__(self, delay=1, timeout=10):
        self.delay = delay
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrape_url(self, url):
        """
        Scrapes text content from a webpage.
        
        Args:
            url (str): The URL to scrape
            
        Returns:
            dict: Scraped content with metadata
        """
        logger.info(f"Scraping {url}...")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            # Parse HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                element.decompose()
            
            # Extract title
            title = soup.find('title')
            title_text = title.get_text(strip=True) if title else "No title"
            
            # Extract text from paragraphs and headings
            content_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'article', 'section'])
            
            content_parts = []
            for element in content_elements:
                text = element.get_text(strip=True)
                if text and len(text) > 20:  # Filter out very short text
                    content_parts.append(text)
            
            content = '\n\n'.join(content_parts)
            
            # Clean the content
            content = self.clean_text(content)
            
            time.sleep(self.delay)  # Rate limiting
            
            return {
                'url': url,
                'title': title_text,
                'content': content,
                'success': True,
                'error': None
            }
            
        except requests.RequestException as e:
            logger.error(f"Error scraping {url}: {e}")
            return {
                'url': url,
                'title': None,
                'content': None,
                'success': False,
                'error': str(e)
            }
        except Exception as e:
            logger.error(f"Unexpected error scraping {url}: {e}")
            return {
                'url': url,
                'title': None,
                'content': None,
                'success': False,
                'error': str(e)
            }
    
    def clean_text(self, text):
        """
        Clean and normalize text content.
        """
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?;:()\-"\']', '', text)
        
        # Remove extra newlines
        text = re.sub(r'\n+', '\n', text)
        
        return text.strip()
    
    def scrape_multiple_sources(self, urls, base_filename="scraped_data"):
        """
        Scrape multiple URLs and combine into a single knowledge base file.
        
        Args:
            urls (list): List of URLs to scrape
            base_filename (str): Base filename for output
            
        Returns:
            str: Path to combined knowledge base file
        """
        all_content = []
        successful_scrapes = 0
        
        logger.info(f"Starting to scrape {len(urls)} URLs...")
        
        for i, url in enumerate(urls, 1):
            logger.info(f"Processing {i}/{len(urls)}: {url}")
            
            result = self.scrape_url(url)
            
            if result['success']:
                content_section = f"Source: {result['url']}\nTitle: {result['title']}\n\n{result['content']}"
                all_content.append(content_section)
                successful_scrapes += 1
            else:
                logger.warning(f"Failed to scrape {url}: {result['error']}")
        
        # Combine all content
        final_filename = f"{base_filename}.txt"
        combined_content = '\n\n---\n\n'.join(all_content)
        
        with open(final_filename, 'w', encoding='utf-8') as f:
            f.write(f"# Knowledge Base - Generated on {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Successfully scraped {successful_scrapes}/{len(urls)} sources\n\n")
            f.write(combined_content)
        
        logger.info(f"Combined knowledge base saved to {final_filename}")
        logger.info(f"Successfully scraped {successful_scrapes}/{len(urls)} sources")
        
        return final_filename

def scrape_multiple_sources(urls, base_filename="scraped_data"):
    """Convenience function for scraping multiple sources"""
    scraper = WebScraper()
    return scraper.scrape_multiple_sources(urls, base_filename)

if __name__ == "__main__":
    # Example usage with AI-related content
    urls = [
        "https://en.wikipedia.org/wiki/Artificial_intelligence",
        "https://en.wikipedia.org/wiki/Machine_learning",
        "https://en.wikipedia.org/wiki/Natural_language_processing",
        "https://en.wikipedia.org/wiki/Deep_learning"
    ]
    
    scraper = WebScraper()
    knowledge_file = scraper.scrape_multiple_sources(urls, "ai_knowledge_base")
    
    print(f"\n✅ Knowledge base created: {knowledge_file}")
    print("Ready for RAG system integration!")
