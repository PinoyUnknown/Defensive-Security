#!/usr/bin/env python3
"""
Web Dashboard - FastAPI-based web interface
Real-time security monitoring and management
"""

import logging
from flask import Flask, render_template, jsonify, request, session
from functools import wraps
from datetime import datetime, timedelta
import json
from typing import Dict, Any, Callable

logger = logging.getLogger(__name__)

class Dashboard:
    """Web dashboard for security monitoring"""
    
    def __init__(self, components: Dict[str, Any]):
        self.components = components
        self.app = Flask(__name__)
        self.app.secret_key = 'your-secret-key-change-this'
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def index():
            return render_template('index.html')
        
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

def create_app(components: Dict[str, Any]) -> Flask:
    """Create and configure Flask application"""
    dashboard = Dashboard(components)
    return dashboard.app
