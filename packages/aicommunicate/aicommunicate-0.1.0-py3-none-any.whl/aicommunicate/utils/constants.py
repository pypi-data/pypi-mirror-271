import os


# 节点配置文件变量
CORAL_NODE_CONFIG_PATH = os.environ.get("CORAL_NODE_CONFIG_PATH")
# 节点配置Base64环境变量
CORAL_NODE_BASE64_DATA = os.environ.get("CORAL_NODE_BASE64_DATA")

DEFAULT_NO_TOPIC = "/no_topic"
DEFAULT_NO_RECEVIER_MSG = "#no_recevier#"

# 所有node统一挂载的路径
MOUNT_PATH = os.environ.get("CORAL_PIPE_MOUNT_DIR", f"{os.environ['HOME']}/.coral")

# 共享内存配置
# lock dir
LOCK_DIR = os.path.join(MOUNT_PATH, "lock")
os.makedirs(LOCK_DIR, exist_ok=True)

# shared memory 数据类型
SHARED_DATA_TYPE = "shm://"
# shared memory save dir
SHARED_MEMORY_ID_STORE_DIR = os.path.join(MOUNT_PATH, "shared_memory_ids")
os.makedirs(SHARED_MEMORY_ID_STORE_DIR, exist_ok=True)
# shared memory lock file
DELETE_SHARED_MEMORY_LOCK = os.path.join(LOCK_DIR, "shared_memory_delete.lock")

# 节点共享内存过期时间
CORAL_NODE_SHARED_MEMORY_EXPIRE = int(
    os.environ.get("CORAL_NODE_SHARED_MEMORY_EXPIRE", 20)
)

# 节点注册环境变量
NODE_ID = os.environ.get("CORAL_NODE_NAME")
NODE_VERSION = os.environ.get("CORAL_NODE_VERSION")
NODE_IMAGE = os.environ.get("CORAL_NODE_DOCKER_IMAGE")
REGISTER_URL = os.environ.get("CORAL_NODE_REGISTER_URL")

# 是否开启共享内存
ENABLE_SHARED_MEMORY = os.environ.get("CORAL_NODE_ENABLE_SHARED_MEMORY")

# 激活码
ACTIVATION_TYPE = os.environ.get("CORAL_NODE_ACTIVATION_TYPE", "device")
ACTIVATION_CODE = os.environ.get("CORAL_NODE_ACTIVATION_CODE")
ACTIVATION_CODE_FP = os.environ.get("CORAL_NODE_ACTIVATION_CODE_PATH", os.path.join(MOUNT_PATH, "activation_code.txt"))
