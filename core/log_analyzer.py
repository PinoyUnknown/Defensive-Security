#!/usr/bin/env python3
"""
Log Analyzer - Advanced log aggregation and analysis
Pattern detection, anomaly detection, threat correlation
"""

import logging
import threading
import time
import re
from datetime import datetime, timedelta
from collections import defaultdict, deque
from typing import Dict, List, Any, Optional
from enum import Enum

logger = logging.getLogger(__name__)

class AlertSeverity(Enum):
    """Alert severity levels"""
    INFO = 1
    WARNING = 2
    CRITICAL = 3
    EMERGENCY = 4

class LogAnalyzer:
    """Analyze logs from multiple sources for threats and anomalies"""
    
    def __init__(self, max_logs: int = 10000):
        self.running = False
        self.thread = None
        self.logs = deque(maxlen=max_logs)
        self.alerts = deque(maxlen=1000)
        self.patterns = self._initialize_patterns()
        self.baseline_stats = {}
        
        logger.info("LogAnalyzer initialized")
    
    def start(self):
        """Start log analysis"""
        if self.running:
            logger.warning("LogAnalyzer already running")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._analysis_loop, daemon=True)
        self.thread.start()
        logger.info("LogAnalyzer started")
    
    def stop(self):
        """Stop log analysis"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("LogAnalyzer stopped")
    
    def _initialize_patterns(self) -> Dict[str, Dict]:
        """Initialize threat detection patterns"""
        return {
            'brute_force': {
                'pattern': r'(Failed password|failed login|Invalid credentials)',
                'threshold': 5,
                'severity': AlertSeverity.CRITICAL
            },
            'sql_injection': {
                'pattern': r"(union.*select|drop\s+table|insert\s+into|update.*set|delete.*from)",
                'threshold': 1,
                'severity': AlertSeverity.CRITICAL
            },
            'xss_attempt': {
                'pattern': r"(<script|javascript:|onerror=|onclick=)",
                'threshold': 1,
                'severity': AlertSeverity.WARNING
            },
            'path_traversal': {
                'pattern': r"(\.\./|\.\\\\)",
                'threshold': 3,
                'severity': AlertSeverity.WARNING
            },
            'privilege_escalation': {
                'pattern': r"(sudo|su -|runas|UAC|privilege.*denied)",
                'threshold': 2,
                'severity': AlertSeverity.CRITICAL
            },
            'unauthorized_access': {
                'pattern': r"(Permission denied|Access denied|Unauthorized)",
                'threshold': 10,
                'severity': AlertSeverity.WARNING
            }
        }
    
    def _analysis_loop(self):
        """Main analysis loop"""
        while self.running:
            try:
                self._analyze_logs()
                self._detect_anomalies()
                self._correlate_threats()
                time.sleep(10)  # Analyze every 10 seconds
            except Exception as e:
                logger.error(f"Error in analysis loop: {e}", exc_info=True)
    
    def add_log(self, log_entry: Dict[str, Any]):
        """Add a log entry for analysis"""
        log_entry['timestamp'] = datetime.now().isoformat()
        self.logs.append(log_entry)
        
        # Perform real-time pattern matching
        self._check_patterns(log_entry)
    
    def _check_patterns(self, log_entry: Dict):
        """Check log entry against threat patterns"""
        content = str(log_entry.get('content', '')).lower()
        
        for pattern_name, pattern_info in self.patterns.items():
            if re.search(pattern_info['pattern'], content, re.IGNORECASE):
                alert = self._create_alert(
                    pattern_name,
                    pattern_info['severity'],
                    f"Pattern '{pattern_name}' detected in logs",
                    log_entry
                )
                self.alerts.append(alert)
                logger.warning(f"Alert: {alert['message']}")
    
    def _analyze_logs(self):
        """Analyze collected logs"""
        if not self.logs:
            return
        
        log_counts = defaultdict(int)
        
        for log in self.logs:
            source = log.get('source', 'unknown')
            log_type = log.get('type', 'unknown')
            key = f"{source}:{log_type}"
            log_counts[key] += 1
        
        # Check for anomalies
        for key, count in log_counts.items():
            if count > 100:
                logger.warning(f"High log volume from {key}: {count} entries")
    
    def _detect_anomalies(self):
        """Detect anomalies using statistical methods"""
        if len(self.logs) < 100:
            return
        
        # Get recent logs
        recent_logs = list(self.logs)[-100:]
        
        # Calculate baseline statistics
        error_count = sum(1 for log in recent_logs if log.get('level') == 'ERROR')
        warning_count = sum(1 for log in recent_logs if log.get('level') == 'WARNING')
        
        # Detect spikes
        if error_count > 50:
            alert = self._create_alert(
                'error_spike',
                AlertSeverity.CRITICAL,
                f"Spike in errors detected: {error_count} errors in last 100 logs",
                {'error_count': error_count}
            )
            self.alerts.append(alert)
            logger.warning(f"Alert: {alert['message']}")
    
    def _correlate_threats(self):
        """Correlate related threats"""
        # Group alerts by source IP or user
        threat_groups = defaultdict(list)
        
        for alert in list(self.alerts)[-100:]:
            key = alert.get('source', 'unknown')
            threat_groups[key].append(alert)
        
        # Check for coordinated attacks
        for source, threats in threat_groups.items():
            if len(threats) > 5:
                logger.critical(f"Potential coordinated attack from {source}: {len(threats)} threats")
    
    def _create_alert(self, alert_type: str, severity: AlertSeverity, 
                     message: str, context: Dict) -> Dict:
        """Create an alert"""
        return {
            'timestamp': datetime.now().isoformat(),
            'type': alert_type,
            'severity': severity.name,
            'message': message,
            'source': context.get('source', 'unknown'),
            'context': context
        }
    
    def get_logs(self, limit: int = 100, filters: Optional[Dict] = None) -> List[Dict]:
        """Get logs with optional filtering"""
        logs = list(self.logs)
        
        if filters:
            if 'source' in filters:
                logs = [log for log in logs if log.get('source') == filters['source']]
            if 'level' in filters:
                logs = [log for log in logs if log.get('level') == filters['level']]
        
        return logs[-limit:]
    
    def get_alerts(self, limit: int = 100, severity: Optional[AlertSeverity] = None) -> List[Dict]:
        """Get alerts with optional severity filtering"""
        alerts = list(self.alerts)
        
        if severity:
            alerts = [alert for alert in alerts if alert.get('severity') == severity.name]
        
        return alerts[-limit:]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get analysis statistics"""
        total_logs = len(self.logs)
        total_alerts = len(self.alerts)
        
        error_count = sum(1 for log in self.logs if log.get('level') == 'ERROR')
        warning_count = sum(1 for log in self.logs if log.get('level') == 'WARNING')
        
        critical_alerts = sum(1 for alert in self.alerts if alert.get('severity') == 'CRITICAL')
        
        return {
            'total_logs': total_logs,
            'total_alerts': total_alerts,
            'error_count': error_count,
            'warning_count': warning_count,
            'critical_alerts': critical_alerts,
            'timestamp': datetime.now().isoformat()
        }
