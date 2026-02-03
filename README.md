# Telegram Anime Automation System

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configuration**
   - Rename `.env.example` to `.env`
   - Fill in your API_ID, API_HASH, Tokens, and Mongo URI.
   - `DB_CHANNEL_ID`: ID of the private channel where files are uploaded.
   - `ADMINS`: Space separated IDs of admins.
   - `FILE_BOT_USERNAME`: Username of your File Delivery Bot (without @).

3. **Running Locally**
   **Windows:**
   Run `start_bots.bat`

   **Linux/Mac:**
   ```bash
   python3 file_bot.py &
   python3 index_bot.py &
   ```

## Docker Deployment (VPS)

1. **Install Docker & Docker Compose**
   ```bash
   sudo apt update
   sudo apt install docker.io docker-compose -y
   ```

2. **Configure Environment**
   Create a `.env` file in the project root with the same variables as `.env.example`.
   **Important:** If using the internal mongodb service, set `MONGO_URI=mongodb://mongodb:27017`

3. **Deploy**
   ```bash
   docker-compose up -d --build
   ```

4. **Check Status**
   ```bash
   docker-compose ps
   docker-compose logs -f
   ```

5. **Stop**
   ```bash
   docker-compose down
   ```

## Features

- **Auto Indexing**: Upload a file to the DB Channel, and it appears in the bot automatically.
- **Smart Parsing**: Detects Anime Name, Season, Episode, Quality from filename/caption.
- **Navigation**: Home, Trending, Library, Favorites.
- **File Delivery**: Silent bot sends files via deep link.
- **Admin Panel**: Use `/admin` in Index Bot (Admin only).
- **Manual Indexing**: Use `/index` to re-scan the channel.

## Important Note
- Ensure both bots are Admins in the `DB_CHANNEL_ID`.
- Ensure `index_bot` is Admin in `FORCE_JOIN_CHANNEL_ID` if used.
