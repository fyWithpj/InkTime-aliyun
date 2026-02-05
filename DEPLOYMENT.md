# InkTime 服务器部署指南

本文档提供在空白 Linux 服务器上部署 InkTime 项目的完整步骤。

## 系统要求

- **操作系统**: Ubuntu 20.04/22.04 LTS（推荐）或 CentOS 7/8
- **Python**: 3.10 或更高版本
- **内存**: 建议 4GB+（如果运行本地 VLM 模型需要更多）
- **存储**: 根据照片库大小决定
- **网络**: 可访问互联网（用于调用云端 VLM API）

## 一、系统环境准备

### 1.1 更新系统包

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get upgrade -y
```

**CentOS/RHEL:**
```bash
sudo yum update -y
# 或 CentOS 8+
sudo dnf update -y
```

### 1.2 安装 Python 3.10+

**Ubuntu 22.04 (默认已包含 Python 3.10):**
```bash
sudo apt-get install -y python3 python3-pip python3-venv
```

**Ubuntu 20.04 (需要添加 PPA):**
```bash
sudo apt-get install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install -y python3.10 python3.10-venv python3.10-dev python3-pip
```

**CentOS 7:**
```bash
sudo yum install -y python3 python3-pip
```

**CentOS 8+:**
```bash
sudo dnf install -y python3 python3-pip
```

### 1.3 安装 exiftool（可选但推荐）

**Ubuntu/Debian:**
```bash
sudo apt-get install -y libimage-exiftool-perl
```

**CentOS/RHEL:**
```bash
sudo yum install -y perl-Image-ExifTool
# 或 CentOS 8+
sudo dnf install -y perl-Image-ExifTool
```

验证安装：
```bash
    exiftool -ver
```

## 二、项目部署

### 2.1 创建项目目录

```bash
# 创建项目目录（可根据需要修改路径）
sudo mkdir -p /opt/inktime
sudo chown $USER:$USER /opt/inktime
cd /opt/inktime
```

### 2.2 上传项目文件

**方式一：使用 Git（如果项目在 Git 仓库）**

如果项目已经在 Git 仓库中：
```bash
git clone <your-repo-url> .
```

如果目录已存在且已有 Git 仓库：
```bash
# 检查现有 remote
git remote -v

# 如果 remote origin 已存在，可以：
# 方案1：更新现有的 remote URL
git remote set-url origin <your-repo-url>

# 方案2：删除后重新添加
git remote remove origin
git remote add origin <your-repo-url>

# 然后拉取代码
git pull origin main
# 或
git pull origin master
```

**方式二：使用 SCP 上传**
```bash
# 在本地机器执行
scp -r /path/to/InkTime/* user@server:/opt/inktime/
```

**方式三：使用 rsync**
```bash
rsync -avz /path/to/InkTime/ user@server:/opt/inktime/
```

### 2.3 创建 Python 虚拟环境

```bash
# 确保在项目根目录
cd /opt/inktime/InkTime-aliyun  # 或你的实际项目目录
pwd  # 确认当前目录

# 检查是否已有虚拟环境
ls -la | grep venv

# 如果不存在，创建虚拟环境
python3 -m venv venv

# 如果创建成功，激活虚拟环境
source venv/bin/activate

# 验证激活（命令提示符前应显示 (venv)）
which python  # 应该显示 venv/bin/python
```

**常见问题：**
- 如果 `source venv/bin/activate` 报错 "No such file or directory"，说明虚拟环境未创建
- 先执行 `python3 -m venv venv` 创建虚拟环境
- 确保在项目根目录执行（有 `requirements.txt` 的目录）

### 2.4 安装 Python 依赖

```bash
# 确保在虚拟环境中
pip install --upgrade pip
pip install -r requirements.txt
```

验证安装：
```bash
python3 -c "import flask, requests, PIL; print('依赖安装成功')"
```

## 三、配置文件设置

### 3.1 创建配置文件

```bash
cp config-example.py config.py
vi config.py  # 或使用 nano config.py
```

### 3.2 必须配置的项

编辑 `config.py`，至少配置以下项：

```python
# 照片库路径（必须）
IMAGE_DIR = "/path/to/your/photos"  # 修改为实际路径

# VLM 模型接口（必须）
API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
MODEL_NAME = "qwen-vl-flash"
API_KEY = "sk-ae38e35b76744da8a831b8b2b88ef9f4"  # 你的 API Key

# ESP32 下载密钥（建议修改）
DOWNLOAD_KEY = "your_random_key_here"  # 生成一个随机字符串

# 常驻地坐标（可选，用于判断旅行照片）
HOME_LAT = 22.543096  # 修改为你的常驻地纬度
HOME_LON = 114.057865  # 修改为你的常驻地经度

# NAS 配置（如果使用 NAS）
NAS_MOUNT_URL = ""  # 如: "smb://192.168.1.100/photo"
NAS_MOUNT_POINT = "/mnt/nas"  # NAS 挂载点
```

### 3.3 如果使用 NAS

**挂载 NAS（以 SMB 为例）:**
```bash
# 安装 SMB 客户端
sudo apt-get install -y cifs-utils  # Ubuntu
# 或
sudo yum install -y cifs-utils  # CentOS

# 创建挂载点
sudo mkdir -p /mnt/nas

# 挂载 NAS
sudo mount -t cifs //192.168.1.100/photo /mnt/nas \
    -o username=your_user,password=your_pass,uid=$(id -u),gid=$(id -g)

# 设置开机自动挂载（可选）
echo "//192.168.1.100/photo /mnt/nas cifs username=your_user,password=your_pass,uid=$(id -u),gid=$(id -g) 0 0" | sudo tee -a /etc/fstab
```

## 四、首次运行

### 4.1 分析照片

```bash
cd /opt/inktime
source venv/bin/activate

# 首次分析照片（会调用 VLM 模型，耗时较长）
python3 analyze_photos.py
```

**注意事项：**
- 首次运行会扫描所有照片，根据照片数量可能需要数小时
- 程序支持断点续跑，可以随时中断，下次运行会跳过已处理的照片
- 确保 VLM API 服务可用（阿里云 API 或本地 LM Studio）

### 4.2 渲染每日照片

```bash
# 生成"历史上的今天"照片
python3 render_daily_photo.py
```

### 4.3 启动 Web 服务器

```bash
# 启动服务器（前台运行，用于测试）
python3 server.py
```

访问 WebUI：
- Review 页面: `http://服务器IP:8765/review`
- 配置页面: `http://服务器IP:8765/config`

**测试完成后，按 Ctrl+C 停止服务器**

## 五、生产环境部署（使用 systemd）

### 5.1 创建 systemd 服务文件

```bash
sudo vi /etc/systemd/system/inktime-server.service
```

内容如下（**请修改路径**）：

```ini
[Unit]
Description=InkTime Server
After=network.target

[Service]
Type=simple
# 修改为你的项目路径
WorkingDirectory=/opt/inktime
ExecStart=/opt/inktime/venv/bin/python /opt/inktime/server.py
Restart=always
RestartSec=3
User=inktime
Group=inktime
StandardOutput=journal
StandardError=journal

# 环境变量（可选）
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target
```

### 5.2 创建专用用户（可选但推荐）

```bash
sudo useradd -r -s /bin/bash -d /opt/inktime inktime
sudo chown -R inktime:inktime /opt/inktime
```

### 5.3 启动服务

```bash
# 重新加载 systemd
sudo systemctl daemon-reload

# 启用开机自启
sudo systemctl enable inktime-server

# 启动服务
sudo systemctl start inktime-server

# 查看状态
sudo systemctl status inktime-server

# 查看日志
sudo journalctl -u inktime-server -f
```

### 5.4 设置定时任务（每日渲染）

```bash
# 修改脚本中的项目路径
vi /opt/inktime/scripts/daily_render.sh
# 将 PROJECT_DIR 改为: PROJECT_DIR="/opt/inktime"

# 设置执行权限
chmod +x /opt/inktime/scripts/daily_render.sh

# 创建日志目录
mkdir -p /opt/inktime/logs

# 编辑 crontab
crontab -e

# 添加以下行（每天凌晨 5 点执行）
0 5 * * * /opt/inktime/scripts/daily_render.sh
```

## 六、防火墙配置

如果服务器有防火墙，需要开放端口：

**Ubuntu (ufw):**
```bash
sudo ufw allow 8765/tcp
sudo ufw reload
```

**CentOS (firewalld):**
```bash
sudo firewall-cmd --permanent --add-port=8765/tcp
sudo firewall-cmd --reload
```

## 七、验证部署

### 7.1 检查服务状态

```bash
# 检查服务是否运行
sudo systemctl status inktime-server

# 检查端口是否监听
sudo netstat -tlnp | grep 8765
# 或
sudo ss -tlnp | grep 8765
```

### 7.2 测试 Web 界面

在浏览器访问：
- `http://服务器IP:8765/review` - 照片浏览页面
- `http://服务器IP:8765/config` - 配置管理页面

### 7.3 检查日志

```bash
# 查看服务日志
sudo journalctl -u inktime-server -n 50

# 查看渲染日志
tail -f /opt/inktime/logs/render.log
```

## 八、常见问题

### 8.1 服务启动失败

```bash
# 检查配置文件是否存在
ls -l /opt/inktime/config.py

# 检查 Python 路径
/opt/inktime/venv/bin/python --version

# 手动运行查看错误
cd /opt/inktime
source venv/bin/activate
python3 server.py
```

### 8.2 照片分析失败

- 检查 VLM API 是否可访问
- 检查 API_KEY 是否正确
- 检查照片目录路径是否正确
- 查看错误日志

### 8.3 权限问题

```bash
# 确保项目目录权限正确
sudo chown -R inktime:inktime /opt/inktime
sudo chmod -R 755 /opt/inktime
```

## 九、维护命令

```bash
# 重启服务
sudo systemctl restart inktime-server

# 停止服务
sudo systemctl stop inktime-server

# 查看服务日志
sudo journalctl -u inktime-server -f

# 手动运行照片分析
cd /opt/inktime
source venv/bin/activate
python3 analyze_photos.py

# 手动运行每日渲染
python3 render_daily_photo.py
```

## 十、安全建议

1. **关闭 WebUI（生产环境）**
   - 编辑 `config.py`，设置 `ENABLE_REVIEW_WEBUI = False`
   - 重启服务

2. **使用 HTTPS**
   - 配置 Nginx 反向代理
   - 使用 Let's Encrypt 证书

3. **限制访问**
   - 使用防火墙限制 IP 访问
   - 或使用 VPN/内网访问

4. **保护 API Key**
   - 不要将 `config.py` 提交到版本控制
   - 考虑使用环境变量存储敏感信息

## 完成！

部署完成后，你的 InkTime 服务应该：
- ✅ 自动启动并保持运行
- ✅ 每天自动生成"历史上的今天"照片
- ✅ 提供 ESP32 下载接口
- ✅ 可通过 WebUI 查看和管理（如启用）

如有问题，请查看日志文件排查。
