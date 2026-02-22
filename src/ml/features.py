import re
from urllib.parse import urlparse

class FeatureExtractor:
    def __init__(self):
        self.suspicious_keywords = [
            "urgent", "verify", "account suspended", "login", "password", 
            "click here", "update", "bank", "security alert", "confirm"
        ]

    def extract_features(self, email_text: str) -> dict:
        """
        Extracts heuristic features from the email text.
        """
        features = {}
        
        # 1. Check for suspicious keywords
        keyword_count = sum(1 for keyword in self.suspicious_keywords if keyword in email_text.lower())
        features['keyword_count'] = keyword_count
        
        # 2. Extract URLs
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', email_text)
        features['url_count'] = len(urls)
        
        # 3. Check for IP address in URLs (common in phishing)
        features['ip_in_url'] = 1 if any(re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url) for url in urls) else 0
        
        # 4. Length of email
        features['email_length'] = len(email_text)
        
        return features

    def get_url_domains(self, email_text: str) -> list:
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', email_text)
        domains = []
        for url in urls:
            try:
                domain = urlparse(url).netloc
                domains.append(domain)
            except:
                continue
        return domains
