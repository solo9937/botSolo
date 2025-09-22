# SOLO - Factory Deployment Notes
This package is prepared for deployment in a factory installer.

## Features Added
- `runtime_config.py` + `config_runtime.json` runtime management.
- `admin_commands.py` for owner/sudo commands.
- Rights unified: All rights reserved to SOLO.
- Cleaned sources.

## Example usage in your bot framework
```
from admin_commands import handle_setowner, handle_addsudo, handle_remsudo, handle_listsudo

# wire into your command handlers depending on your library
```

## Default Config
OWNER_ID = 7722416548
SUDO_USERS = [7722416548]
