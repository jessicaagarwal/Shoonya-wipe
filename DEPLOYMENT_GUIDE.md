# Shoonya Wipe - Deployment Guide
## National E-Waste Management Solution

### 🚀 **Quick Deployment**

#### **Docker Deployment (Recommended)**
```bash
# 1. Clone the repository
git clone https://github.com/your-org/shoonya-wipe.git
cd shoonya-wipe

# 2. Start the application
docker compose up -d

# 3. Access the web interface
# Open browser to: http://localhost:5000
```

#### **Direct Installation**
```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Run the web interface
python main.py web

# 3. Access at http://localhost:5000
```

### 🏗️ **Production Deployment**

#### **System Requirements**
- **OS**: Ubuntu 20.04 LTS or CentOS 8+
- **CPU**: 4 cores minimum, 8 cores recommended
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 100GB SSD minimum
- **Network**: 1Gbps connection

#### **Prerequisites**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Nginx
sudo apt install nginx -y

# Install Certbot for SSL
sudo apt install certbot python3-certbot-nginx -y
```

### 🔧 **Production Configuration**

#### **1. Environment Setup**
```bash
# Create production directory
sudo mkdir -p /opt/shoonya-wipe
sudo chown $USER:$USER /opt/shoonya-wipe
cd /opt/shoonya-wipe

# Clone repository
git clone https://github.com/your-org/shoonya-wipe.git .

# Create production environment file
cat > .env << EOF
# Production Configuration
WEB_PRODUCTION_MODE=1
SHOONYA_PRODUCTION_MODE=1
DOCKER_PRODUCTION_ALLOWED=1

# Security
SECRET_KEY=$(openssl rand -hex 32)
JWT_SECRET=$(openssl rand -hex 32)

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/shoonya_wipe

# Redis
REDIS_URL=redis://localhost:6379/0

# Monitoring
PROMETHEUS_ENABLED=1
GRAFANA_ENABLED=1
EOF
```

#### **2. Docker Compose Production**
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  shoonya-wipe:
    build: .
    restart: unless-stopped
    ports:
      - "127.0.0.1:5000:5000"
    volumes:
      - ./virtual_media:/app/virtual_media
      - ./out:/app/out
      - ./exports:/app/exports
      - ./logs:/app/logs
    environment:
      - WEB_PRODUCTION_MODE=1
      - SHOONYA_PRODUCTION_MODE=1
      - DOCKER_PRODUCTION_ALLOWED=1
    depends_on:
      - postgres
      - redis
    networks:
      - shoonya-network

  postgres:
    image: postgres:15
    restart: unless-stopped
    environment:
      - POSTGRES_DB=shoonya_wipe
      - POSTGRES_USER=shoonya_user
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - shoonya-network

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    volumes:
      - redis_data:/data
    networks:
      - shoonya-network

  nginx:
    image: nginx:alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - shoonya-wipe
    networks:
      - shoonya-network

volumes:
  postgres_data:
  redis_data:

networks:
  shoonya-network:
    driver: bridge
```

#### **3. Nginx Configuration**
```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream shoonya_backend {
        server shoonya-wipe:5000;
    }

    server {
        listen 80;
        server_name your-domain.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name your-domain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers off;

        location / {
            proxy_pass http://shoonya_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /static/ {
            alias /app/static/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

### 🔐 **SSL Certificate Setup**

#### **Let's Encrypt SSL**
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

#### **Manual SSL Certificate**
```bash
# Create SSL directory
sudo mkdir -p /opt/shoonya-wipe/ssl

# Generate self-signed certificate (for testing)
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /opt/shoonya-wipe/ssl/key.pem \
    -out /opt/shoonya-wipe/ssl/cert.pem \
    -subj "/C=IN/ST=State/L=City/O=Organization/CN=your-domain.com"
```

### 📊 **Monitoring Setup**

#### **Prometheus Configuration**
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'shoonya-wipe'
    static_configs:
      - targets: ['shoonya-wipe:5000']
    metrics_path: '/metrics'
    scrape_interval: 5s
```

#### **Grafana Dashboard**
```json
{
  "dashboard": {
    "title": "Shoonya Wipe Monitoring",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "Requests/sec"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          }
        ]
      }
    ]
  }
}
```

### 🔄 **Backup Strategy**

#### **Automated Backup Script**
```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/opt/backups/shoonya-wipe"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup certificates and logs
tar -czf $BACKUP_DIR/certificates_$DATE.tar.gz /opt/shoonya-wipe/out /opt/shoonya-wipe/exports

# Backup database
docker compose exec -T postgres pg_dump -U shoonya_user shoonya_wipe > $BACKUP_DIR/database_$DATE.sql

# Backup configuration
tar -czf $BACKUP_DIR/config_$DATE.tar.gz /opt/shoonya-wipe/.env /opt/shoonya-wipe/nginx.conf

# Cleanup old backups (keep 30 days)
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete

echo "Backup completed: $DATE"
```

#### **Cron Job Setup**
```bash
# Add to crontab
crontab -e

# Add this line for daily backups at 2 AM
0 2 * * * /opt/shoonya-wipe/backup.sh >> /var/log/shoonya-backup.log 2>&1
```

### 🚀 **Deployment Commands**

#### **Start Production Environment**
```bash
# Start all services
docker compose -f docker-compose.prod.yml up -d

# Check status
docker compose -f docker-compose.prod.yml ps

# View logs
docker compose -f docker-compose.prod.yml logs -f shoonya-wipe
```

#### **Update Application**
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker compose -f docker-compose.prod.yml up -d --build

# Verify deployment
curl -f http://localhost:5000/api/status || exit 1
```

#### **Scale Application**
```bash
# Scale to 3 instances
docker compose -f docker-compose.prod.yml up -d --scale shoonya-wipe=3

# Update nginx configuration for load balancing
# (Add multiple upstream servers)
```

### 🔧 **Maintenance**

#### **Health Checks**
```bash
# Application health
curl -f http://localhost:5000/api/status

# Database health
docker compose exec postgres pg_isready -U shoonya_user

# Redis health
docker compose exec redis redis-cli ping
```

#### **Log Management**
```bash
# View application logs
docker compose logs -f shoonya-wipe

# View nginx logs
docker compose logs -f nginx

# Rotate logs
sudo logrotate /etc/logrotate.d/shoonya-wipe
```

#### **Performance Monitoring**
```bash
# Check resource usage
docker stats

# Check disk usage
df -h

# Check memory usage
free -h

# Check network usage
iftop
```

### 🛡️ **Security Hardening**

#### **Firewall Configuration**
```bash
# Install UFW
sudo apt install ufw -y

# Configure firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

#### **System Hardening**
```bash
# Disable root login
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config

# Enable fail2ban
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Update system regularly
sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure -plow unattended-upgrades
```

### 📋 **Deployment Checklist**

#### **Pre-Deployment**
- [ ] System requirements met
- [ ] SSL certificates obtained
- [ ] Domain name configured
- [ ] DNS records set up
- [ ] Firewall configured
- [ ] Backup strategy implemented

#### **Deployment**
- [ ] Code deployed
- [ ] Services started
- [ ] SSL configured
- [ ] Monitoring enabled
- [ ] Health checks passing
- [ ] Performance tested

#### **Post-Deployment**
- [ ] Documentation updated
- [ ] Team trained
- [ ] Monitoring alerts configured
- [ ] Backup verified
- [ ] Security scan completed
- [ ] Performance baseline established

### 🆘 **Troubleshooting**

#### **Common Issues**

**Service won't start:**
```bash
# Check logs
docker compose logs shoonya-wipe

# Check configuration
docker compose config

# Restart services
docker compose restart
```

**SSL certificate issues:**
```bash
# Check certificate
openssl x509 -in /opt/shoonya-wipe/ssl/cert.pem -text -noout

# Renew certificate
sudo certbot renew --force-renewal
```

**Performance issues:**
```bash
# Check resource usage
docker stats

# Check logs for errors
docker compose logs shoonya-wipe | grep ERROR

# Restart with more resources
docker compose up -d --scale shoonya-wipe=2
```

### 📞 **Support**

For deployment issues:
- **Documentation**: Check this guide and other docs
- **Logs**: Review application and system logs
- **Community**: GitHub Issues and Discussions
- **Professional**: Contact support team

---

**Shoonya Wipe** - Ready for national deployment! 🚀
