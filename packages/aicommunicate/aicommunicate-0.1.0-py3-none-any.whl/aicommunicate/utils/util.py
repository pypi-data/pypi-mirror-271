import os
import uuid
import hashlib


def generate_short_uid(uid: str = None):
    uid = uid or str(uuid.uuid4())
    hasher = hashlib.sha1(uid.encode())
    return hasher.hexdigest()[:8]


def get_mac_addr():
    # ! 使用默认的mac addr需要保证容器启动时采用 network=host模式
    return os.environ.get('CORAL_NODE_MAC_ADDR', uuid.UUID(int=uuid.getnode()).hex[-12:])
