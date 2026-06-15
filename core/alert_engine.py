#!/usr/bin/env python3
"""
Alert Engine - Real-time alerting and notifications
Multi-channel alerting with severity scoring
"""

import logging
import threading
import time
from datetime import datetime
from typing import Dict, List, Any, Callable, Optional
from enum import Enum
from collections import deque

logger = logging.getLogger(__name__)

class AlertChannel(Enum):
    """Alert notification channels"""
    DASHBOARD = 'dashboard'
    EMAIL = 'email'
    WEBHOOK = 'webhook'
    SYSLOG = 'syslog'
    LOG = 'log'

class AlertEngine:
    """Manage and route security alerts"""
    
    def __init__(self, max_alerts: int = 5000):
        self.running = False
        self.thread = None
        self.alerts = deque(maxlen=max_alerts)
        self.alert_rules = {}
        self.alert_handlers: Dict[AlertChannel, Callable] = {}
        self.alert_stats = {
            'total': 0,
            'by_severity': {},
            'by_type': {}
        }
        
        self._initialize_handlers()
        logger.info("AlertEngine initialized")
    
    def _initialize_handlers(self):
        """Initialize alert handlers for different channels"""
        self.alert_handlers[AlertChannel.DASHBOARD] = self._handle_dashboard_alert
        self.alert_handlers[AlertChannel.EMAIL] = self._handle_email_alert
        self.alert_handlers[AlertChannel.WEBHOOK] = self._handle_webhook_alert
        self.alert_handlers[AlertChannel.SYSLOG] = self._handle_syslog_alert
        self.alert_handlers[AlertChannel.LOG] = self._handle_log_alert
    
    def start(self):
        """Start alert engine"""
        if self.running:
            logger.warning("AlertEngine already running")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._processing_loop, daemon=True)
        self.thread.start()
        logger.info("AlertEngine started")
    
    def stop(self):
        """Stop alert engine"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("AlertEngine stopped")
    
    def _processing_loop(self):
        """Main alert processing loop"""
        while self.running:
            time.sleep(5)
    
    def create_alert(self, alert_type: str, severity: str, message: str, 
                    context: Dict[str, Any], channels: Optional[List[AlertChannel]] = None) -> Dict:
        """Create and route an alert"""
        
        if channels is None:
            channels = [AlertChannel.DASHBOARD, AlertChannel.LOG]
        
        alert = {
            'id': len(self.alerts),
            'timestamp': datetime.now().isoformat(),
            'type': alert_type,
            'severity': severity,
            'message': message,
            'context': context,
            'channels': [ch.value for ch in channels],
            'acknowledged': False
        }
        
        # Calculate severity score
        alert['severity_score'] = self._calculate_severity_score(severity)
        
        # Add to alert queue
        self.alerts.append(alert)
        
        # Update statistics
        self._update_stats(alert)
        
        # Route to channels
        for channel in channels:
            try:
                handler = self.alert_handlers.get(channel)
                if handler:
                    handler(alert)
            except Exception as e:
                logger.error(f"Error routing alert to {channel.value}: {e}")
        
        logger.info(f"Alert created: {alert_type} - {message}")
        return alert
    
    def _calculate_severity_score(self, severity: str) -> int:
        """Calculate numeric severity score"""
        scores = {
            'INFO': 1,
            'WARNING': 2,
            'CRITICAL': 3,
            'EMERGENCY': 4
        }
        return scores.get(severity.upper(), 1)
    
    def _update_stats(self, alert: Dict):
        """Update alert statistics"""
        self.alert_stats['total'] += 1
        
        severity = alert['severity']
        if severity not in self.alert_stats['by_severity']:
            self.alert_stats['by_severity'][severity] = 0
        self.alert_stats['by_severity'][severity] += 1
        
        alert_type = alert['type']
        if alert_type not in self.alert_stats['by_type']:
            self.alert_stats['by_type'][alert_type] = 0
        self.alert_stats['by_type'][alert_type] += 1
    
    def _handle_dashboard_alert(self, alert: Dict):
        """Handle dashboard alert notification"""
        # Alerts are stored in memory and displayed on dashboard
        logger.debug(f"Dashboard alert: {alert['message']}")
    
    def _handle_email_alert(self, alert: Dict):
        """Handle email alert notification"""
        if alert['severity_score'] >= 3:  # Only CRITICAL and above
            logger.info(f"Email alert would be sent: {alert['message']}")
            # In production: send actual email
    
    def _handle_webhook_alert(self, alert: Dict):
        """Handle webhook alert notification"""
        logger.info(f"Webhook alert would be sent: {alert['message']}")
        # In production: call webhook endpoint
    
    def _handle_syslog_alert(self, alert: Dict):
        """Handle syslog alert notification"""
        logger.info(f"Syslog alert: {alert['message']}")
    
    def _handle_log_alert(self, alert: Dict):
        """Handle file log alert notification"""
        logger.warning(f"Alert logged: {alert['type']} - {alert['message']}")
    
    def get_alerts(self, limit: int = 100, severity: Optional[str] = None) -> List[Dict]:
        """Get alerts with optional filtering"""
        alerts = list(self.alerts)
        
        if severity:
            alerts = [a for a in alerts if a['severity'] == severity]
        
        return sorted(alerts, key=lambda x: x['timestamp'], reverse=True)[-limit:]
    
    def acknowledge_alert(self, alert_id: int):
        """Mark alert as acknowledged"""
        for alert in self.alerts:
            if alert['id'] == alert_id:
                alert['acknowledged'] = True
                logger.info(f"Alert {alert_id} acknowledged")
                break
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get alert engine statistics"""
        return {
            'total_alerts': self.alert_stats['total'],
            'by_severity': self.alert_stats['by_severity'],
            'by_type': self.alert_stats['by_type'],
            'active_alerts': len([a for a in self.alerts if not a['acknowledged']]),
            'timestamp': datetime.now().isoformat()
        }
