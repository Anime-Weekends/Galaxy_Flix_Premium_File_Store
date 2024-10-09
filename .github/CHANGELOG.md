# CHANGELOG

## Version: 3.0.0 | 09-10-2024 (Friday)
---

### Enhancements
- **Enhanced Features**:
   - All existing features from v1 and v2 have been enhanced by approximately 30%.
   - Unlike the previous version, admins now have permissions to handle banned user commands.
   - Provided a hyperlink to the database channel in messages while executing the `/genlink` and `/batch` commands for easy access.
- **Database Operations**: Drastically changed database operations for improved performance and reliability. Added `motor` library in `requirements.txt`: it provides Async driver for MongoDB (Non-blocking database operation)

- **New Files Added in plugins**:
  - `autoDelete.py`: Created for better readability and management of deletion operations.
  - `request_forcesub.py`: Implemented to handle force subscription requests more efficiently.
- **File Updates**: Made minor changes in `helper_func.py`, `start.py`, `advance_query.py`, `advance_features.py`, and `bot_cmd.py` files to optimize the code. Included all other `files` where decorator parameters are aligned in an optimal way for faster response and less resource consumption.

### Formatting Improvements
- **Advance Formatting Support**: Added `pyrofork` in `requirements.txt` for better formatting and support.
- **Text Formatting**: Enhanced text formatting in the existing `FORMATS.py` file, improving clarity and usability.

### New Features
- **Request Force Subscription**: Introduced the highly demanding feature to handle request force subscriptions in version 3. All required settings and helper evennt are added in the file `request_forcesub.py` for smooth operation of request forcesub.

---
### 🧑‍💻 Updated by King
> Contact: [King (Shidoteshika)](https://t.me/Shidoteshika1)

### Next Update
> The next update will be made after thoroughly checking the features in the bot and will be implemented regularly if changes are needed or based on user demands.
