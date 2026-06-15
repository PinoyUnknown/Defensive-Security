#!/usr/bin/env python3
"""
System Monitor - Real-time system and process monitoring
Cross-platform monitoring for Windows, Linux, macOS
"""

import psutil
import threading
import time
import logging
import json
from datetime import datetime
from collections import deque
from typing import Dict, List, Any
import sys

logger = logging.getLogger(__name__)

PLATFORM = sys.platform
IS_WINDOWS = PLATFORM == 'win32'
IS_LINUX = PLATFORM.startswith('linux')

class SystemMonitor:
    """Monitor system resources and processes in real-time"""
    
    def __init__(self, interval: int = 5, history_size: int = 1000):
        self.interval = interval
        self.running = False
        self.thread = None
        self.history = deque(maxlen=history_size)
        self.process_baseline = {}
        self.suspicious_processes = []
        
        logger.info(f"SystemMonitor initialized on {PLATFORM}")
    
    def start(self):
        """Start monitoring"""
        if self.running:
            logger.warning("Monitor already running")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        logger.info("System Monitor started")
    
    def stop(self):
        """Stop monitoring"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("System Monitor stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.running:
            try:
                metrics = self.get_system_metrics()
                self.history.append(metrics)
                
                # Check for anomalies
                self._check_anomalies(metrics)
                
                time.sleep(self.interval)
            except Exception as e:
                logger.error(f"Error in monitor loop: {e}", exc_info=True)
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system metrics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            metrics = {
                'timestamp': datetime.now().isoformat(),
                'cpu': {
                    'percent': cpu_percent,
                    'count': psutil.cpu_count(),
                    'freq': psutil.cpu_freq().current if psutil.cpu_freq() else 0
                },
                'memory': {
                    'total': memory.total,
                    'used': memory.used,
                    'available': memory.available,
                    'percent': memory.percent
                },
                'disk': {
                    'total': disk.total,
                    'used': disk.used,
                    'free': disk.free,
                    'percent': disk.percent
                },
                'processes': self._get_process_info(),
                'network': self._get_network_info(),
                'boot_time': datetime.fromtimestamp(psutil.boot_time()).isoformat()
            }
            
            return metrics
        
        except Exception as e:
            logger.error(f"Error getting system metrics: {e}")
            return {}
    
    def _get_process_info(self) -> List[Dict]:
        """Get information about running processes"""
        processes = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'status': proc.info['status'],
                        'cpu_percent': proc.info['cpu_percent'],
                        'memory_percent': proc.info['memory_percent']
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        
        except Exception as e:
            logger.error(f"Error getting process info: {e}")
        
        # Sort by CPU usage
        return sorted(processes, key=lambda x: x.get('cpu_percent', 0), reverse=True)[:50]
    
    def _get_network_info(self) -> Dict[str, Any]:
        """Get network connection information"""
        try:
            net_if = psutil.net_if_stats()
            net_io = psutil.net_io_counters()
            connections = psutil.net_connections()
            
            return {
                'interfaces': len(net_if),
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'active_connections': len(connections),
                'connection_states': self._get_connection_states(connections)
            }
        
        except Exception as e:
            logger.error(f"Error getting network info: {e}")
            return {}
    
    def _get_connection_states(self, connections: List) -> Dict[str, int]:
        """Count connections by state"""
        states = {}
        
        for conn in connections:
            state = conn.status
            states[state] = states.get(state, 0) + 1
        
        return states
    
    def _check_anomalies(self, metrics: Dict):
        """Check for anomalies in metrics"""
        try:
            # High CPU usage
            if metrics['cpu']['percent'] > 80:
                logger.warning(f"High CPU usage: {metrics['cpu']['percent']}%")
            
            # High memory usage
            if metrics['memory']['percent'] > 85:
                logger.warning(f"High memory usage: {metrics['memory']['percent']}%")
            
            # High disk usage
            if metrics['disk']['percent'] > 90:
                logger.warning(f"High disk usage: {metrics['disk']['percent']}%")
            
            # Check for suspicious processes
            self._check_suspicious_processes(metrics.get('processes', []))
        
        except Exception as e:
            logger.error(f"Error checking anomalies: {e}")
    
    def _check_suspicious_processes(self, processes: List[Dict]):
        """Check for suspicious process names and behaviors"""
        suspicious_keywords = [
            'cmd', 'powershell', 'wmic', 'mimikatz', 'psexec',
            'nc', 'ncat', 'wget', 'curl', 'python', 'perl'
        ]
        
        for proc in processes:
            name = proc.get('name', '').lower()
            
            if any(keyword in name for keyword in suspicious_keywords):
                if proc['cpu_percent'] > 50 or proc['memory_percent'] > 50:
                    logger.warning(f"Suspicious process detected: {proc['name']} (PID: {proc['pid']})")
                    self.suspicious_processes.append(proc)
    
    def get_history(self, limit: int = 100) -> List[Dict]:
        """Get monitoring history"""
        return list(self.history)[-limit:]
    
    def get_status(self) -> Dict[str, Any]:
        """Get current monitor status"""
        return {
            'running': self.running,
            'interval': self.interval,
            'history_size': len(self.history),
            'suspicious_processes': len(self.suspicious_processes)
        }
