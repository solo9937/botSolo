# admin_commands.py
# All rights reserved to SOLO
from runtime_config import get_owner, set_owner, add_sudo, remove_sudo, list_sudo

def is_owner(user_id):
    return int(user_id) == int(get_owner())

def get_owner_and_sudo():
    s = set(list_sudo())
    s.add(get_owner())
    return s

def handle_setowner(bot, message, args):
    sender = message.from_user.id if hasattr(message, 'from_user') else getattr(message, 'from_user_id', None)
    if not is_owner(sender):
        return {"status": "error", "msg": "Unauthorized"}
    try:
        new_id = int(args.strip())
        set_owner(new_id)
        return {"status": "ok", "msg": f"OWNER set to {new_id}"}
    except:
        return {"status": "error", "msg": "Invalid ID"}

def handle_addsudo(bot, message, args):
    sender = message.from_user.id if hasattr(message, 'from_user') else getattr(message, 'from_user_id', None)
    if not is_owner(sender):
        return {"status": "error", "msg": "Unauthorized"}
    try:
        uid = int(args.strip())
        added = add_sudo(uid)
        return {"status": "ok", "msg": "Added" if added else "Already in list"}
    except:
        return {"status": "error", "msg": "Invalid ID"}

def handle_remsudo(bot, message, args):
    sender = message.from_user.id if hasattr(message, 'from_user') else getattr(message, 'from_user_id', None)
    if not is_owner(sender):
        return {"status": "error", "msg": "Unauthorized"}
    try:
        uid = int(args.strip())
        removed = remove_sudo(uid)
        return {"status": "ok", "msg": "Removed" if removed else "Not found"}
    except:
        return {"status": "error", "msg": "Invalid ID"}

def handle_listsudo(bot, message, args=None):
    sender = message.from_user.id if hasattr(message, 'from_user') else getattr(message, 'from_user_id', None)
    if not is_owner(sender):
        return {"status": "error", "msg": "Unauthorized"}
    lst = list_sudo()
    return {"status": "ok", "msg": f"SUDO_USERS: {lst}"}
