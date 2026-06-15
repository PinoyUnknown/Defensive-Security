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
import subprocess
import json
from pathlib import Path
from datetime import datetime

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

# Version tracking file
VERSION_FILE = Path('.version')

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
            status = "✅ Running" if self.running else "🛑 Stopped"
            logger.info(f"  {status} - {name}")
    
    def update(self):
        """Update the toolkit from Git repository"""
        logger.info("="*70)
        logger.info("🔄 Updating Enterprise Defensive Security Toolkit...")
        logger.info("="*70)
        
        try:
            # Check if git is available
            try:
                subprocess.run(['git', '--version'], capture_output=True, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                logger.error("❌ Git is not installed or not in PATH")
                logger.error("Please install Git: https://git-scm.com/download")
                return False
            
            # Check if we're in a git repository
            logger.info("\n📋 Checking if this is a Git repository...")
            result = subprocess.run(
                ['git', 'rev-parse', '--git-dir'],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode != 0:
                logger.error("❌ This directory is not a Git repository")
                logger.info("\n💡 To initialize a Git repository, run:")
                logger.info("   git clone https://github.com/PinoyUnknown/Defensive-Security.git")
                return False
            
            logger.info("✅ Git repository detected")
            
            # Get current branch
            logger.info("\n📚 Checking current branch...")
            branch_result = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                capture_output=True,
                text=True,
                check=True
            )
            current_branch = branch_result.stdout.strip()
            logger.info(f"   Current branch: {current_branch}")
            
            # Check for uncommitted changes
            logger.info("\n🔍 Checking for uncommitted changes...")
            status_result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True,
                text=True,
                check=True
            )
            
            if status_result.stdout.strip():
                logger.warning("⚠️  You have uncommitted changes:")
                logger.warning(status_result.stdout)
                logger.info("\n❓ Do you want to stash these changes? (y/n)")
                user_input = input("> ").strip().lower()
                
                if user_input == 'y':
                    logger.info("💾 Stashing changes...")
                    subprocess.run(['git', 'stash'], check=True)
                    logger.info("✅ Changes stashed")
                else:
                    logger.info("⚠️  Update cancelled. Please commit or stash your changes first.")
                    return False
            else:
                logger.info("✅ No uncommitted changes")
            
            # Fetch latest changes
            logger.info("\n📥 Fetching latest changes from repository...")
            subprocess.run(['git', 'fetch', 'origin'], check=True)
            logger.info("✅ Fetch completed")
            
            # Check if there are updates available
            logger.info("\n🔎 Checking for available updates...")
            diff_result = subprocess.run(
                ['git', 'diff', 'HEAD', f'origin/{current_branch}'],
                capture_output=True,
                text=True,
                check=True
            )
            
            if not diff_result.stdout.strip():
                logger.info("✅ You are already up to date!")
                logger.info(f"   Version: {DEVELOPER_INFO['version']}")
                return True
            
            logger.info(f"📦 Updates available for {current_branch} branch")
            
            # Show what will be updated
            logger.info("\n📝 Files that will be updated:")
            log_result = subprocess.run(
                ['git', 'log', f'HEAD..origin/{current_branch}', '--oneline', '--name-status'],
                capture_output=True,
                text=True,
                check=True
            )
            logger.info(log_result.stdout)
            
            # Pull latest changes
            logger.info("\n⬇️  Pulling latest changes...")
            pull_result = subprocess.run(
                ['git', 'pull', 'origin', current_branch],
                capture_output=True,
                text=True,
                check=False
            )
            
            if pull_result.returncode != 0:
                logger.error("❌ Error pulling changes:")
                logger.error(pull_result.stderr)
                return False
            
            logger.info(pull_result.stdout)
            logger.info("✅ Pull completed successfully")
            
            # Check if requirements need to be updated
            if 'requirements' in pull_result.stdout or 'requirements.txt' in pull_result.stdout:
                logger.info("\n📦 Detected changes in requirements.txt")
                logger.info("❓ Do you want to update Python dependencies? (y/n)")
                user_input = input("> ").strip().lower()
                
                if user_input == 'y':
                    logger.info("\n📥 Installing/updating Python dependencies...")
                    try:
                        subprocess.run(
                            [sys.executable, '-m', 'pip', 'install', '--upgrade', '-r', 'requirements.txt'],
                            check=True
                        )
                        logger.info("✅ Dependencies updated successfully")
                    except subprocess.CalledProcessError as e:
                        logger.error("❌ Error updating dependencies:")
                        logger.error(str(e))
                        return False
            
            # Update version file
            self._write_version_file()
            
            logger.info("\n" + "="*70)
            logger.info("✅ Update completed successfully!")
            logger.info("="*70)
            logger.info("\n💡 To restart the toolkit with the latest version:")
            logger.info("   python main.py start")
            logger.info("\n👨‍💻 Developed by: White Hat - PinoyUnknown")
            logger.info(f"   GitHub: {DEVELOPER_INFO['github']}")
            logger.info(f"   Instagram: {DEVELOPER_INFO['instagram']}")
            logger.info("="*70)
            
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Error during update: {e}")
            logger.error(str(e.stderr) if e.stderr else "")
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected error during update: {e}", exc_info=True)
            return False
    
    def _write_version_file(self):
        """Write version information to file"""
        try:
            version_info = {
                'version': DEVELOPER_INFO['version'],
                'last_updated': datetime.now().isoformat(),
                'platform': PLATFORM,
                'developer': DEVELOPER_INFO['name']
            }
            
            with open(VERSION_FILE, 'w') as f:
                json.dump(version_info, f, indent=2)
        except Exception as e:
            logger.warning(f"Could not write version file: {e}")
    
    def check_updates(self):
        """Check if updates are available without installing them"""
        logger.info("="*70)
        logger.info("🔍 Checking for available updates...")
        logger.info("="*70)
        
        try:
            # Check if git is available
            try:
                subprocess.run(['git', '--version'], capture_output=True, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                logger.error("❌ Git is not installed or not in PATH")
                return False
            
            # Get current branch
            branch_result = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                capture_output=True,
                text=True,
                check=True
            )
            current_branch = branch_result.stdout.strip()
            
            # Fetch latest
            subprocess.run(['git', 'fetch', 'origin'], check=True)
            
            # Check for differences
            diff_result = subprocess.run(
                ['git', 'diff', 'HEAD', f'origin/{current_branch}'],
                capture_output=True,
                text=True,
                check=True
            )
            
            if diff_result.stdout.strip():
                logger.info("\n✅ Updates are available!")
                logger.info(f"   Branch: {current_branch}")
                logger.info("\n📝 Recent commits:")
                log_result = subprocess.run(
                    ['git', 'log', f'HEAD..origin/{current_branch}', '--oneline'],
                    capture_output=True,
                    text=True,
                    check=True
                )
                logger.info(log_result.stdout)
                logger.info("\n💡 To update, run: python main.py update")
                return True
            else:
                logger.info("\n✅ You are already up to date!")
                logger.info(f"   Version: {DEVELOPER_INFO['version']}")
                logger.info(f"   Branch: {current_branch}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error checking for updates: {e}")
            return False

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
  python main.py update             # Update from Git repository
  python main.py check-updates      # Check for available updates
  python main.py export --format json  # Export logs
        '''
    )
    
    parser.add_argument(
        'command',
        choices=['start', 'stop', 'status', 'update', 'check-updates', 'export', 'threat-scan', 'update-threats'],
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
    elif args.command == 'update':
        success = manager.update()
        sys.exit(0 if success else 1)
    elif args.command == 'check-updates':
        manager.check_updates()
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
