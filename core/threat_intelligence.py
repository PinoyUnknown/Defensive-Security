#!/usr/bin/env python3
"""
Threat Intelligence - IP reputation, domain filtering, IOC detection
Real-time threat feed updates and lookups
"""

import logging
import threading
import time
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set
from collections import defaultdict
import json

logger = logging.getLogger(__name__)

class ThreatIntelligence:
    """Manage threat intelligence feeds and lookups"""
    
    def __init__(self, update_interval: int = 3600):
        self.running = False
        self.thread = None
        self.update_interval = update_interval
        
        # Threat data storage
        self.malicious_ips: Set[str] = set()
        self.malicious_domains: Set[str] = set()
        self.known_iocs: Set[str] = set()  # Indicators of Compromise
        self.ip_reputation: Dict[str, Dict] = {}  # Cache
        
        # Feed sources
        self.feeds = {
            'abuse_ip_db': {
                'url': 'https://api.abuseipdb.com/api/v2/blacklist',
                'enabled': True,
                'timeout': 30
            },
            'urlhaus': {
                'url': 'https://urlhaus-api.abuse.ch/v1/urls/recent/',
                'enabled': True,
                'timeout': 30
            }
        }
        
        logger.info("ThreatIntelligence initialized")
    
    def start(self):
        """Start threat intelligence updates"""
        if self.running:
            logger.warning("ThreatIntelligence already running")
            return
        
        self.running = True
        # Initial load
        self._update_feeds()
        
        # Start background update thread
        self.thread = threading.Thread(target=self._update_loop, daemon=True)
        self.thread.start()
        logger.info("ThreatIntelligence started")
    
    def stop(self):
        """Stop threat intelligence updates"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("ThreatIntelligence stopped")
    
    def _update_loop(self):
        """Background thread for updating threat feeds"""
        while self.running:
            try:
                self._update_feeds()
                time.sleep(self.update_interval)
            except Exception as e:
                logger.error(f"Error in update loop: {e}", exc_info=True)
    
    def _update_feeds(self):
        """Update threat feeds from external sources"""
        logger.info("Updating threat intelligence feeds...")
        
        for feed_name, feed_config in self.feeds.items():
            if not feed_config['enabled']:
                continue
            
            try:
                logger.info(f"Fetching {feed_name}...")
                
                if feed_name == 'abuse_ip_db':
                    self._update_abuseipdb()
                elif feed_name == 'urlhaus':
                    self._update_urlhaus()
                    
            except Exception as e:
                logger.error(f"Error updating {feed_name}: {e}")
    
    def _update_abuseipdb(self):
        """Update AbuseIPDB IP blacklist"""
        try:
            # In production, use proper API key
            # For now, using public list
            response = requests.get(
                'https://sslbl.abuse.ch/blacklist/',
                timeout=10
            )
            
            if response.status_code == 200:
                ips = response.text.strip().split('\n')
                self.malicious_ips.update(ips)
                logger.info(f"Updated {len(ips)} malicious IPs")
                
        except Exception as e:
            logger.error(f"Error updating AbuseIPDB: {e}")
    
    def _update_urlhaus(self):
        """Update URLhaus malicious URLs"""
        try:
            response = requests.get(
                self.feeds['urlhaus']['url'],
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                urls = data.get('query_status', [])
                
                for item in urls:
                    if isinstance(item, dict):
                        domain = item.get('url', '').split('/')[2]
                        if domain:
                            self.malicious_domains.add(domain)
                
                logger.info(f"Updated {len(self.malicious_domains)} malicious domains")
                
        except Exception as e:
            logger.error(f"Error updating URLhaus: {e}")
    
    def check_ip(self, ip: str) -> Dict[str, Any]:
        """Check if IP is malicious"""
        # Check cache first
        if ip in self.ip_reputation:
            cache = self.ip_reputation[ip]
            if datetime.fromisoformat(cache['timestamp']) > datetime.now() - timedelta(hours=24):
                return cache
        
        is_malicious = ip in self.malicious_ips
        
        result = {
            'ip': ip,
            'is_malicious': is_malicious,
            'timestamp': datetime.now().isoformat(),
            'source': 'local_feeds'
        }
        
        self.ip_reputation[ip] = result
        return result
    
    def check_domain(self, domain: str) -> Dict[str, Any]:
        """Check if domain is malicious"""
        is_malicious = domain.lower() in self.malicious_domains
        
        return {
            'domain': domain,
            'is_malicious': is_malicious,
            'timestamp': datetime.now().isoformat(),
            'source': 'local_feeds'
        }
    
    def check_ioc(self, ioc: str) -> bool:
        """Check if value is a known IOC"""
        return ioc in self.known_iocs
    
    def add_malicious_ip(self, ip: str):
        """Manually add IP to malicious list"""
        self.malicious_ips.add(ip)
        logger.warning(f"Added {ip} to malicious IPs")
    
    def add_malicious_domain(self, domain: str):
        """Manually add domain to malicious list"""
        self.malicious_domains.add(domain.lower())
        logger.warning(f"Added {domain} to malicious domains")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get threat intelligence statistics"""
        return {
            'malicious_ips': len(self.malicious_ips),
            'malicious_domains': len(self.malicious_domains),
            'known_iocs': len(self.known_iocs),
            'last_updated': datetime.now().isoformat(),
            'feeds_enabled': sum(1 for f in self.feeds.values() if f['enabled'])
        }
    
    def get_feeds_status(self) -> Dict[str, Dict]:
        """Get status of all threat feeds"""
        return self.feeds
