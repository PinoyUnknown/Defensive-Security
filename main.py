#!/usr/bin/env python3
"""
Enterprise Defensive Security Toolkit - Main Entry Point
Cross-platform defensive security solution with web dashboard and vulnerability scanner

Developed by: White Hat - PinoyUnknown
GitHub: https://github.com/PinoyUnknown
Instagram: https://instagram.com/pinoyunknown
"""

import sys
import os
import argparse
import logging
from pathlib import Path

# Platform detection
PLATFORM = sys.platform
IS_WINDOWS = PLATFORM == 'win32'
IS_LINUX = PLATFORM.startswith('linux')
IS_MACOS = PLATFORM == 'darwin'

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Developer Information
DEVELOPER_INFO = {
    'name': 'White Hat - PinoyUnknown',
    'github': 'https://github.com/PinoyUnknown',
    'instagram': 'https://instagram.com/pinoyunknown',
    'version': '1.0.0',
    'description': 'Enterprise Defensive Security Toolkit'
}

class ToolkitManager:
    """Main toolkit manager for controlling all components"""
    
    def __init__(self):
        self.running = False
        self.components = {}
        logger.info(f"Initializing {DEVELOPER_INFO['description']} on {PLATFORM}")
    
    def start(self):
        """Start all toolkit components"""
        logger.info("Starting Enterprise Defensive Security Toolkit...")
        
        try:
            # Import components
            from core.system_monitor import SystemMonitor
            from core.log_analyzer import LogAnalyzer
            from core.threat_intelligence import ThreatIntelligence
            from core.alert_engine import AlertEngine
            from core.web_vulnerability_scanner import WebVulnerabilityScanner
            from web.app import create_app
            
            # Initialize components
            logger.info("Initializing System Monitor...")
            self.components['system_monitor'] = SystemMonitor()
            
            logger.info("Initializing Log Analyzer...")
            self.components['log_analyzer'] = LogAnalyzer()
            
            logger.info("Initializing Threat Intelligence...")
            self.components['threat_intelligence'] = ThreatIntelligence()
            
            logger.info("Initializing Alert Engine...")
            self.components['alert_engine'] = AlertEngine()
            
            logger.info("Initializing Web Vulnerability Scanner...")
            self.components['web_vulnerability_scanner'] = WebVulnerabilityScanner()
            
            # Start monitoring components
            for name, component in self.components.items():
                if hasattr(component, 'start'):
                    logger.info(f"Starting {name}...")
                    component.start()
            
            # Start web dashboard
            logger.info("Starting Web Dashboard...")
            app = create_app(self.components)
            
            logger.info("="*70)
            logger.info(f"{DEVELOPER_INFO['description']} v{DEVELOPER_INFO['version']}")
            logger.info("="*70)
            logger.info("Enterprise Defensive Security Toolkit Started Successfully!")
            logger.info("")
            logger.info("🌐 Web Dashboard: http://localhost:8080")
            logger.info("👤 Default Login: admin / admin123")
            logger.info("")
            logger.info("✅ Active Features:")
            logger.info("   • System & Process Monitoring")
            logger.info("   • Log Analysis & Threat Detection")
            logger.info("   • Web URL Scanning & Vulnerability Detection")
            logger.info("   • Attacker IP Tracking & Identification")
            logger.info("   • Real-time Alerts & Notifications")
            logger.info("   • Threat Intelligence Integration")
            logger.info("")
            logger.info("👨‍💻 Developed by: White Hat - PinoyUnknown")
            logger.info(f"   GitHub: {DEVELOPER_INFO['github']}")
            logger.info(f"   Instagram: {DEVELOPER_INFO['instagram']}")
            logger.info("="*70)
            
            self.running = True
            app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
            
        except Exception as e:
            logger.error(f"Error starting toolkit: {e}", exc_info=True)
            sys.exit(1)
    
    def stop(self):
        """Stop all toolkit components"""
        logger.info("Stopping toolkit components...")
        
        for name, component in self.components.items():
            if hasattr(component, 'stop'):
                try:
                    logger.info(f"Stopping {name}...")
                    component.stop()
                except Exception as e:
                    logger.error(f"Error stopping {name}: {e}")
        
        self.running = False
        logger.info("Toolkit stopped")
    
    def status(self):
        """Display toolkit status"""
        logger.info(f"{DEVELOPER_INFO['description']} - Status Report")
        logger.info(f"Version: {DEVELOPER_INFO['version']}")
        logger.info(f"Platform: {PLATFORM}")
        logger.info(f"Running: {self.running}")
        logger.info("\nActive Components:")
        
        for name, component in self.components.items():
            status = "✅ Running" if self.running else "⛔ Stopped"
            logger.info(f"  {status} - {name}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description=f"{DEVELOPER_INFO['description']} v{DEVELOPER_INFO['version']}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f'''\nDeveloped by: White Hat - PinoyUnknown
GitHub: {DEVELOPER_INFO['github']}
Instagram: {DEVELOPER_INFO['instagram']}

Examples:
  python main.py start              # Start all components
  python main.py stop               # Stop all components
  python main.py status             # Show status
  python main.py export --format json  # Export logs
        '''
    )
    
    parser.add_argument(
        'command',
        choices=['start', 'stop', 'status', 'export', 'threat-scan', 'update-threats'],
        help='Command to execute'
    )
    parser.add_argument('--format', choices=['json', 'csv'], default='json', help='Export format')
    parser.add_argument('--output', default='report.json', help='Output file')
    
    args = parser.parse_args()
    
    manager = ToolkitManager()
    
    if args.command == 'start':
        manager.start()
    elif args.command == 'stop':
        manager.stop()
    elif args.command == 'status':
        manager.status()
    elif args.command == 'export':
        logger.info(f"Exporting logs to {args.output} in {args.format} format")
    elif args.command == 'threat-scan':
        logger.info("Running threat scan...")
    elif args.command == 'update-threats':
        logger.info("Updating threat intelligence...")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n\n🛑 Shutting down...")
        sys.exit(0)
