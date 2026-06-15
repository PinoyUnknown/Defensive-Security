#!/usr/bin/env python3
"""
Web Dashboard - Enhanced Web Vulnerability Scanner
Real-time security monitoring with detailed attack analysis

Developed by: White Hat - PinoyUnknown
GitHub: https://github.com/PinoyUnknown
Instagram: https://instagram.com/pinoyunknown
"""

import logging
from flask import Flask, render_template, jsonify, request, session
from functools import wraps
from datetime import datetime, timedelta
import json
from typing import Dict, Any, Callable, Optional

logger = logging.getLogger(__name__)

DEVELOPER_INFO = {
    'name': 'White Hat - PinoyUnknown',
    'github': 'https://github.com/PinoyUnknown',
    'instagram': 'https://instagram.com/pinoyunknown',
    'version': '1.0.0'
}

class Dashboard:
    """Web dashboard for security monitoring with URL scanning"""
    
    def __init__(self, components: Dict[str, Any]):
        self.components = components
        self.app = Flask(__name__, template_folder='templates')
        self.app.secret_key = 'your-secret-key-change-this'
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def index():
            return render_template('index.html', developer_info=DEVELOPER_INFO)
        
        # ============ Developer Info Route ============
        @self.app.route('/api/developer-info')
        def api_developer_info():
            """Get developer information"""
            return jsonify(DEVELOPER_INFO)
        
        # ============ System Status Routes ============
        @self.app.route('/api/status')
        def api_status():
            """Get system status"""
            system_monitor = self.components.get('system_monitor')
            if system_monitor:
                return jsonify(system_monitor.get_system_metrics())
            return jsonify({}), 500
        
        @self.app.route('/api/alerts')
        def api_alerts():
            """Get alerts"""
            alert_engine = self.components.get('alert_engine')
            limit = request.args.get('limit', 100, type=int)
            if alert_engine:
                return jsonify({
                    'alerts': alert_engine.get_alerts(limit=limit),
                    'statistics': alert_engine.get_statistics()
                })
            return jsonify({}), 500
        
        @self.app.route('/api/logs')
        def api_logs():
            """Get logs"""
            log_analyzer = self.components.get('log_analyzer')
            limit = request.args.get('limit', 100, type=int)
            if log_analyzer:
                return jsonify({
                    'logs': log_analyzer.get_logs(limit=limit),
                    'statistics': log_analyzer.get_statistics()
                })
            return jsonify({}), 500
        
        @self.app.route('/api/threats')
        def api_threats():
            """Get threat intelligence"""
            threat_intel = self.components.get('threat_intelligence')
            if threat_intel:
                return jsonify(threat_intel.get_statistics())
            return jsonify({}), 500
        
        @self.app.route('/api/check-ip/<ip>')
        def api_check_ip(ip):
            """Check IP reputation"""
            threat_intel = self.components.get('threat_intelligence')
            if threat_intel:
                return jsonify(threat_intel.check_ip(ip))
            return jsonify({}), 500
        
        @self.app.route('/api/check-domain/<domain>')
        def api_check_domain(domain):
            """Check domain reputation"""
            threat_intel = self.components.get('threat_intelligence')
            if threat_intel:
                return jsonify(threat_intel.check_domain(domain))
            return jsonify({}), 500
        
        # ============ Web Vulnerability Scanner Routes ============
        @self.app.route('/api/scan-url', methods=['POST'])
        def api_scan_url():
            """Scan a URL for vulnerabilities and attacks"""
            try:
                data = request.json
                url = data.get('url')
                
                if not url:
                    return jsonify({
                        'status': 'error',
                        'message': 'URL is required'
                    }), 400
                
                web_scanner = self.components.get('web_vulnerability_scanner')
                if web_scanner:
                    result = web_scanner.scan_url(url)
                    return jsonify(result)
                
                return jsonify({
                    'status': 'error',
                    'message': 'Web Scanner not available'
                }), 500
            
            except Exception as e:
                logger.error(f"Error in scan URL: {e}")
                return jsonify({
                    'status': 'error',
                    'message': str(e)
                }), 500
        
        @self.app.route('/api/scan-results')
        def api_scan_results():
            """Get scan results history"""
            web_scanner = self.components.get('web_vulnerability_scanner')
            limit = request.args.get('limit', 50, type=int)
            
            if web_scanner:
                return jsonify({
                    'results': web_scanner.get_scan_results(limit=limit),
                    'count': len(web_scanner.get_scan_results())
                })
            return jsonify({}), 500
        
        @self.app.route('/api/attacker-ips')
        def api_attacker_ips():
            """Get all tracked attacker IPs"""
            web_scanner = self.components.get('web_vulnerability_scanner')
            
            if web_scanner:
                stats = web_scanner.get_attacker_statistics()
                return jsonify(stats)
            return jsonify({}), 500
        
        @self.app.route('/api/attacker-ips/<ip>')
        def api_attacker_ip_details(ip):
            """Get details about a specific attacker IP"""
            web_scanner = self.components.get('web_vulnerability_scanner')
            
            if web_scanner:
                attacker_ips = web_scanner.get_attacker_ips()
                if ip in attacker_ips:
                    return jsonify({
                        'ip': ip,
                        'attacks': attacker_ips[ip],
                        'count': len(attacker_ips[ip])
                    })
                
                return jsonify({
                    'status': 'not_found',
                    'message': f'IP {ip} not found in attack records'
                }), 404
            
            return jsonify({}), 500

def create_app(components: Dict[str, Any]) -> Flask:
    """Create and configure Flask application"""
    dashboard = Dashboard(components)
    return dashboard.app
