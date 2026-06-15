# Enterprise Defensive Security Toolkit

**A Powerful, Cross-Platform, Robust Defensive Security Solution**



Version 2
<img width="1920" height="1080" alt="Screenshot_20260615_160446" src="https://github.com/user-attachments/assets/48262730-ce5c-4ae2-906d-62c555478b9e" />

## Overview

The Enterprise Defensive Security Toolkit is a comprehensive Python-based security monitoring and defense system designed for enterprise environments. It provides real-time threat detection, system monitoring, log aggregation, and a web-based dashboard for security management.

### Key Features

✅ **Cross-Platform Support** — Windows, Linux, macOS
✅ **Real-Time Monitoring** — System processes, network connections, file integrity
✅ **Advanced Log Analysis** — Pattern detection, anomaly detection
✅ **Web Dashboard** — Real-time security insights and alerts
✅ **Alert System** — Instant notifications for suspicious activity
✅ **Threat Intelligence Integration** — IP reputation, domain blocking
✅ **Performance Optimized** — Minimal resource footprint
✅ **Enterprise-Ready** — Scalable, reliable, production-tested

## System Requirements

- **Python**: 3.10+
- **OS**: Linux (Ubuntu 20.04+), Windows 10/11, macOS 11+
- **RAM**: Minimum 2GB (4GB+ recommended)
- **Storage**: 1GB for logs and database
- **Database**: SQLite (default) or PostgreSQL (production)

## Installation

### Quick Start

```bash
# Clone the repository
git clone https://github.com/PinoyUnknown/Defensive-Security.git
cd Defensive-Security

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the toolkit
python main.py
```

### Web Dashboard Access

```
http://localhost:8080
Default credentials: admin / admin123
```

## Architecture

```
┌─────────────────────────────────────────┐
│     Enterprise Defensive Toolkit        │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────��────────────────────────────┐  │
│  │   Web Dashboard (Flask/FastAPI)   │  │
│  │   - Real-time monitoring          │  │
│  │   - Alert management              │  │
│  │   - Threat intelligence           │  │
│  └───────────────────────────────────┘  │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │    Core Security Engines          │  │
│  │  ┌──────────────────────────────┐ │  │
│  │  │ System Monitor               │ │  │
│  │  │ - Process monitoring         │ │  │
│  │  │ - Network connections        │ │  │
│  │  │ - File integrity             │ │  │
│  │  └──────────────────────────────┘ │  │
│  │  ┌──────────────────────────────┐ │  │
│  │  │ Log Analyzer                 │ │  │
│  │  │ - Log aggregation            │ │  │
│  │  │ - Pattern detection          │ │  │
│  │  │ - Anomaly detection          │ │  │
│  │  └──────────────────────────────┘ │  │
│  │  ┌──────────────────────────────┐ │  │
│  │  │ Threat Intelligence          │ │  │
│  │  │ - IP reputation              │ │  │
│  │  │ - Domain filtering           │ │  │
│  │  │ - Known IOCs                 │ │  │
│  │  └──────────────────────────────┘ │  │
│  │  ┌──────────────────────────────┐ │  │
│  │  │ Alert Engine                 │ │  │
│  │  │ - Real-time alerts           │ │  │
│  │  │ - Severity scoring           │ │  │
│  │  │ - Notifications              │ │  │
│  │  └──────────────────────────────┘ │  │
│  └───────────────────────────────────┘  │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │    Data Layer                     │  │
│  │  - SQLite/PostgreSQL              │  │
│  │  - Time-series metrics            │  │
│  │  - Log storage                    │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

## Configuration

Edit `config.yaml` to customize:

```yaml
system:
  monitor_interval: 5  # seconds
  log_retention: 30    # days
  performance_mode: high
  
alerts:
  enabled: true
  thresholds:
    cpu_usage: 80
    memory_usage: 85
    disk_usage: 90
    network_connections: 1000

threat_intelligence:
  enabled: true
  update_interval: 3600  # seconds
  ip_reputation_api: true
```

## Usage

### Start the Toolkit

```bash
python main.py
```

### Monitor System Health

Access the dashboard at `http://localhost:8080` for:
- Real-time system metrics
- Active alerts
- Network connections
- Process analysis
- Log viewer

### CLI Commands

```bash
# View system status
python main.py status

# Start monitoring
python main.py start

# Stop monitoring
python main.py stop

# Export logs
python main.py export --format json --output report.json

# Run threat scan
python main.py threat-scan

# Update threat intelligence
python main.py update-threats
```

## Performance Optimization

- **Async Processing** — Non-blocking operations for minimal latency
- **Connection Pooling** — Efficient database connections
- **Caching Layer** — In-memory caching for frequently accessed data
- **Resource Limits** — Configurable monitoring intervals and retention
- **Multi-threading** — Parallel processing of independent tasks

## Security Best Practices

1. Change default credentials immediately
2. Run on a dedicated security server
3. Use HTTPS for web dashboard
4. Enable firewall rules (allow only admin access to dashboard)
5. Regular backup of security logs
6. Keep threat intelligence updated
7. Monitor the toolkit itself for tampering

## Components

### 1. System Monitor (`system_monitor.py`)
- Process monitoring
- Network connection tracking
- File integrity monitoring
- System resource usage

### 2. Log Analyzer (`log_analyzer.py`)
- Multi-source log aggregation
- Pattern recognition
- Anomaly detection
- Threat correlation

### 3. Threat Intelligence (`threat_intelligence.py`)
- IP reputation lookups
- Domain filtering
- Known IOC detection
- Real-time threat feeds

### 4. Alert Engine (`alert_engine.py`)
- Real-time alerting
- Severity scoring
- Multi-channel notifications (email, webhook, dashboard)
- Alert correlation and deduplication

### 5. Web Dashboard (`app.py`)
- FastAPI backend for high performance
- Real-time WebSocket updates
- RESTful API
- Vue.js frontend

## API Endpoints

```
GET    /api/status              - System status
GET    /api/alerts              - List alerts
GET    /api/processes           - Active processes
GET    /api/network/connections - Network connections
GET    /api/logs                - System logs
POST   /api/scan/threat         - Start threat scan
GET    /api/metrics             - Performance metrics
POST   /api/threat-intel/update - Update threat intelligence
```

## Troubleshooting

### High CPU Usage
- Increase `monitor_interval` in config
- Reduce `log_retention` period
- Enable `performance_mode: high`

### Dashboard Not Loading
- Check firewall rules
- Verify port 8080 is available
- Check logs: `tail -f logs/app.log`

### Missing Alerts
- Verify alert thresholds in config
- Check alert engine service: `python main.py status`
- Review alert logs

## Contributing

Contributions welcome! Please:
1. Create a feature branch
2. Test thoroughly on Windows and Linux
3. Submit a pull request with documentation

## License

MIT License - See LICENSE file

## Support

For issues and feature requests: [GitHub Issues](https://github.com/PinoyUnknown/Defensive-Security/issues)

---

**Enterprise Defensive Security Toolkit** - Defend Your Company with Confidence
