# runtime_config.py
# All rights reserved to SOLO
# Manage runtime owner and sudo users in config_runtime.json
import json, os

_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config_runtime.json")

_default = {
    "OWNER_ID": 7722416548,
    "SUDO_USERS": [7722416548]
}

def _ensure():
    if not os.path.exists(_CONFIG_PATH):
        save(_default)
    return load()

def load():
    try:
        with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return dict(_default)

def save(cfg):
    with open(_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)

def get_owner():
    cfg = _ensure()
    return int(cfg.get("OWNER_ID", 7722416548))

def set_owner(new_id):
    cfg = _ensure()
    cfg["OWNER_ID"] = int(new_id)
    if int(new_id) not in cfg.get("SUDO_USERS", []):
        cfg.setdefault("SUDO_USERS", []).append(int(new_id))
    save(cfg)

def get_sudo_users():
    cfg = _ensure()
    return set(int(x) for x in cfg.get("SUDO_USERS", []) or [])

def add_sudo(user_id):
    cfg = _ensure()
    su = cfg.setdefault("SUDO_USERS", [])
    if int(user_id) not in su:
        su.append(int(user_id))
        save(cfg)
        return True
    return False

def remove_sudo(user_id):
    cfg = _ensure()
    su = cfg.setdefault("SUDO_USERS", [])
    if int(user_id) in su:
        su.remove(int(user_id))
        save(cfg)
        return True
    return False

def list_sudo():
    return list(get_sudo_users())
