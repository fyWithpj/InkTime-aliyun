# 照片库路径（你自己的相册目录）
# 如果使用 NAS，请指向 NAS 挂载点下的路径，例如：
# macOS: "/Volumes/photo/相册"
# Windows: "Z:/相册" 或 "\\192.168.1.100\photo\相册"
# Linux: "/mnt/nas/photo"
IMAGE_DIR = "./test"

# ==================== NAS 挂载配置（可选）====================
# 如果照片库在 NAS 上，可以配置以下选项以支持自动重挂载
# 注意：当前自动重挂载逻辑主要针对 macOS，Windows/Linux 用户可能需要手动挂载

# NAS 挂载 URL（用于自动重挂载）
# macOS 示例：
#   NAS_MOUNT_URL = "afp://192.168.1.100/photo"  # AFP 协议
#   NAS_MOUNT_URL = "smb://192.168.1.100/photo"  # SMB 协议
# Windows/Linux 用户通常不需要配置此项（使用系统挂载）
NAS_MOUNT_URL = ""

# NAS 挂载点路径（用于检测挂载状态）
# macOS 默认: "/Volumes/photo"
# Windows: 通常是 "Z:" 或网络驱动器路径
# Linux: "/mnt/nas" 或 "/media/nas"
NAS_MOUNT_POINT = "/Volumes/photo"

# NAS 重试配置（当检测到掉盘时）
NAS_RETRY_TIMES = 3          # 重试次数
NAS_RETRY_SLEEP_SEC = 2.0    # 每次重试间隔（秒）

# 数据库路径（建议保持默认）
DB_PATH = "./photos.db"

# VLM 模型接口配置
# 阿里云通义千问 DashScope API
API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
MODEL_NAME = "qwen-vl-flash"  # 或 qwen-vl-max, qwen-vl-plus
API_KEY = "sk-ae38e35b76744da8a831b8b2b88ef9f4"

# 注意：如果使用本地 LM Studio，请使用以下配置：
# API_URL = "http://127.0.0.1:1234/v1/chat/completions"
# MODEL_NAME = "qwen3-vl-32b-instruct"
# API_KEY = ""

# 每次最多处理多少张的图片
BATCH_LIMIT = None

# 请求超时时间（秒）
TIMEOUT = 600

# 为防止照片隐私泄露，建议为 ESP32 下载路径加一个随机前缀作为密钥
# 前缀修改后，请同步修改 esp32/ink-display-7C-photo/ink-display-7C-photo.ino 固件中的 DAILY_PHOTO_PATH_PREFIX 字段）
DOWNLOAD_KEY = "yourdownloadkey"

# Flask 静态服务
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 8765
# 是否开启照片库 WebUI（前期检验提示词选片效果时使用，跑通后建议关闭）
ENABLE_REVIEW_WEBUI = True

# 离线中文城市名索引，使用 geonames 数据制作
WORLD_CITIES_CSV = "./data/world_cities_zh.csv"

# 网格大小（纬度/经度度数）；越大越快但精度略差。1.0 对大多数场景够用。
CITY_GRID_DEG = 1.0

# 你的“常驻常驻”坐标（用于判断是否为旅行期间照片，从而对评分进行小幅加成）
# 照片 GPS 距离常驻地超过 HOME_RADIUS_KM，则视为“异地”
# 默认值给了深圳市中心附近（不改也能保持原行为的大致效果）
HOME_LAT = 22.543096
HOME_LON = 114.057865
HOME_RADIUS_KM = 60.0

# 最大接受距离（公里），超出则认为“不在任何城市附近”
CITY_MAX_DISTANCE_KM = 100.0

# 墨水屏渲染 BIN 文件输出目录
BIN_OUTPUT_DIR = "./output"

# 自定义字体路径（为空则退回默认字体）
FONT_PATH = ""

# 每日选片“精彩度”阈值
MEMORY_THRESHOLD = 70.0

# 每日挑选的照片数量
DAILY_PHOTO_QUANTITY = 5