#!/usr/bin/env python3
"""
Enterprise Defensive Security Toolkit - Main Entry Point
Cross-platform defensive security solution with web dashboard
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

class ToolkitManager:
    """Main toolkit manager for controlling all components"""
    
    def __init__(self):
        self.running = False
        self.components = {}
        logger.info(f"Initializing Enterprise Defensive Security Toolkit on {PLATFORM}")
    
    def start(self):
        """Start all toolkit components"""
        logger.info("Starting Enterprise Defensive Security Toolkit...")
        
        try:
            # Import components
            from core.system_monitor import SystemMonitor
            from core.log_analyzer import LogAnalyzer
            from core.threat_intelligence import ThreatIntelligence
            from core.alert_engine import AlertEngine
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
            
            # Start monitoring
            for name, component in self.components.items():
                if hasattr(component, 'start'):
                    logger.info(f"Starting {name}...")
                    component.start()
            
            # Start web dashboard
            logger.info("Starting Web Dashboard...")
            app = create_app(self.components)
            
            logger.info("="*60)
            logger.info("Enterprise Defensive Security Toolkit Started")
            logger.info("Web Dashboard: http://localhost:8080")
            logger.info("Default credentials: admin / admin123")
            logger.info("="*60)
            
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
        logger.info("Enterprise Defensive Security Toolkit Status")
        logger.info(f"Platform: {PLATFORM}")
        logger.info(f"Running: {self.running}")
        logger.info("Components:")
        
        for name, component in self.components.items():
            status = "Running" if self.running else "Stopped"
            logger.info(f"  - {name}: {status}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Enterprise Defensive Security Toolkit',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
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
        logger.info("\nShutting down...")
        sys.exit(0)
