import spacy
import re
# import pyttsx3
import threading

nlp = spacy.load("en_core_web_sm")

SUPPORTED_UNITS = ["kg", "g", "lb", "oz", "pcs", "dozen", "pack", "ton", "bottle", "box", "liter"]

def normalize_unit(unit):
    """
    Normalize a unit by converting it to its singular form.
    """
    doc = nlp(unit)
    lemmatized = " ".join([token.lemma_ for token in doc]) 
    return lemmatized.split()[0] 

def parse_command(command):
    """
    Parse a spoken or written inventory command.
    """
    
    patterns = {
        "add": r"add\s+(\d+\.?\d*)\s*([a-zA-Z]+)\s*of\s*([\w\s]+)",
        "update": r"update\s+(\d+\.?\d*)\s*([a-zA-Z]+)\s*stock\s*of\s*([\w\s]+)",
        "remove": r"remove\s+(\d+\.?\d*)\s*([a-zA-Z]+)\s*of\s*([\w\s]+)",
        "show": r"show\s*(stock|stocks|inventory)",
        "search": r"search\s*for\s*([\w\s]+)"
    }

    for action, pattern in patterns.items():
        match = re.search(pattern, command, re.IGNORECASE)
        if match:
            if action in ["add", "update", "remove"]:
                quantity = float(match.group(1))  
                raw_unit = match.group(2).lower() 
                name = match.group(3).strip().lower()  

                normalized_unit = normalize_unit(raw_unit)

                if normalized_unit not in SUPPORTED_UNITS:
                    raise ValueError(f"Unsupported unit: {raw_unit}. Please use a valid unit.")

                return {
                    "action": action,
                    "quantity": quantity,
                    "unit": normalized_unit,
                    "name": name
                }
            elif action == "show":
                return {"action": "show"}
            
            elif action == "search":
                query = match.group(1).strip().lower()
                return {"action": "search", "query": query}
          
    raise ValueError("Could not parse the command. Please check the format.")

# tts_lock = threading.Lock()

# engine = pyttsx3.init()
# engine.setProperty('rate', 150)  
# engine.setProperty('volume', 1)

# def speak_text(text):
#     def run_tts():
#         try:
#             with tts_lock:
#                 engine.say(text)
#                 engine.runAndWait()
#         except Exception as e:
#             print(f"TTS Error: {e}")

#     tts_thread = threading.Thread(target=run_tts)
#     tts_thread.start()
