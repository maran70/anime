import re

class Parser:
    @staticmethod
    def parse_info(filename: str, caption: str = ""):
        # 1. Read caption first, else filename
        text_to_parse = caption if caption else filename
        if not text_to_parse:
            return None

        # 2. Remove [bracket text], extensions
        clean_text = re.sub(r'\[.*?\]', '', text_to_parse)
        clean_text = re.sub(r'\.(mkv|mp4|avi|flv|webm)', '', clean_text, flags=re.IGNORECASE)
        
        # 3. Detect Season & Episode (SxxExx)
        # Regex for S01E01, S1E1, etc.
        # Use simple pattern specified in prompt rules
        seek_pattern = r'(?i)S(\d+)E(\d+)'
        match = re.search(seek_pattern, clean_text)
        
        if not match:
            return None
            
        season = int(match.group(1))
        episode = int(match.group(2))
        
        # ANIME NAME LOGIC: Take ONLY text BEFORE SxxExx
        # Match matches SxxExx, so we take string before start of match
        raw_name = clean_text[:match.start()]
        
        # Clean up name: remove episode titles (usually after SxxExx, so already safe), clean dots/underscores
        anime_name = raw_name.replace('.', ' ').replace('_', ' ').strip()
        # Remove trailing hyphens or separators
        anime_name = re.sub(r'[-–]+$', '', anime_name).strip()
        
        # 4. Detect Quality
        quality = "Unknown"
        if "1080p" in clean_text: quality = "1080p"
        elif "720p" in clean_text: quality = "720p"
        elif "480p" in clean_text: quality = "480p"
        
        # 5. Detect Audio
        audio = "Original" # Default
        lower_text = clean_text.lower()
        if "multi" in lower_text: audio = "Multi"
        elif "dual" in lower_text: audio = "Dual"
        elif "japanese" in lower_text or "jap" in lower_text: audio = "Japanese"
        elif "english" in lower_text or "eng" in lower_text: audio = "English"
        elif "tamil" in lower_text: audio = "Tamil"
        
        return {
            "anime_name": anime_name,
            "season": season,
            "episode": episode,
            "quality": quality,
            "audio": audio
        }
