import os
import json
import requests

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

POLL_TEMPLATES = [
    {"q": "How many study hours did you hit today? ⏳",    "a": ["0h (Rest day) 😴",     "1-3h (Good start) 💡",     "3-6h (Solid work) 🔨",    "6-8h (Impressive) 🔥",        "8-10h (Beast mode) ⚡",     "10-12h (Legend) 🚀",       "12h+ (Unstoppable) 👑"]},
    {"q": "Deep Work hours today? 🧠",                     "a": ["0h (Recharge) 📵",     "1-3h (Building habit) 🌱", "3-6h (Locked in) 🔒",     "6-8h (Flow state) 🌊",        "8-10h (Academic weapon) ⚔️","10-12h (Genius level) 💎",  "12h+ (Superhuman) 🏆"]},
    {"q": "Total focused study time? ⏱️",                  "a": ["0h (Off day) 💀",      "1-3h (Progress made) 🕐",  "3-6h (Consistent) 🕒",    "6-8h (Dedicated) 🕓",         "8-10h (Committed) 🕔",      "10-12h (Elite focus) 🕕",  "12h+ (God tier) 🕛"]},
    {"q": "Productive study hours today? 🤥",              "a": ["0h (Honest rest) 😅",  "1-3h (Small wins) 👍",     "3-6h (Strong effort) 💪",  "6-8h (Fire output) 🔥",       "8-10h (Crushing it) ⚡",    "10-12h (Champion) 🎯",      "12h+ (Absolute legend) 💯"]},
    {"q": "Actual study time (be honest)? 📊",             "a": ["0h (Recovery) 🤡",     "1-3h (Starting strong) 🐌","3-6h (Solid grind) 🆗",    "6-8h (Intense work) 😤",      "8-10h (Peak performance) 🥵","10-12h (Unmatched) 🦾",    "12h+ (Next level) 🧠"]},
    {"q": "Study hours grinded today? 📝",                 "a": ["0h (Break day) 🏖️",   "1-3h (Good effort) 📖",    "3-6h (Making moves) ✍️",   "6-8h (Serious grind) 🔄",     "8-10h (Dominating) 🧹",     "10-12h (Scholar mode) 📚",  "12h+ (Certified genius) 🎓"]},
    {"q": "How long did you study? ⏳",                    "a": ["0h (Chill day) 💤",    "1-3h (Early bird) 🌅",     "3-6h (Day warrior) ☀️",    "6-8h (Evening grinder) 🌆",   "8-10h (Night owl) 🌃",      "10-12h (Full cycle) 🌌",   "12h+ (Time bender) ✨"]},
    {"q": "Study session duration today? ⌚",              "a": ["0h (Resting) 🛌",      "1-3h (Walking forward) 🚶","3-6h (Running hard) 🏃",   "6-8h (Cycling through) 🚴",   "8-10h (Lifting heavy) 🏋️", "10-12h (Superhero) 🦸",    "12h+ (Titan status) 🔱"]},
    {"q": "Time spent studying? 📖",                       "a": ["0h (Pause) 😶",        "1-3h (Writing history) 📝","3-6h (Page turner) 📕",    "6-8h (Book master) 📗",        "8-10h (Knowledge seeker) 📘","10-12h (Wisdom holder) 📙","12h+ (Library itself) 📚"]},
    {"q": "Today's study grind hours? 💪",                 "a": ["0h (Smile break) 🫠",  "1-3h (Happy start) 🙂",    "3-6h (Cheerful grind) 😊", "6-8h (Grinning wide) 😁",     "8-10h (Star struck) 🤩",    "10-12h (Cool cat) 😎",     "12h+ (Gold medalist) 🥇"]},
    {"q": "Hours of focused work? 🎯",                     "a": ["0h (Float day) 🎈",    "1-3h (Big tent) 🎪",       "3-6h (Artist) 🎨",         "6-8h (Performer) 🎭",          "8-10h (Director) 🎬",       "10-12h (Bullseye) 🎯",     "12h+ (Trophy hunter) 🏅"]},
    {"q": "Study time tracker? ⏲️",                        "a": ["0h (Stop) 🟥",         "1-3h (Warming up) 🟧",     "3-6h (Caution ready) 🟨",  "6-8h (Go green) 🟩",           "8-10h (Blue sky) 🟦",       "10-12h (Purple reign) 🟪", "12h+ (All colors) 🟫"]},
    {"q": "How much did you grind? 🔥",                    "a": ["0h (Ice cool) 🧊",     "1-3h (Temp rising) 🌡️",   "3-6h (Heating up) 🌡️",    "6-8h (Spicy hot) 🌶️",         "8-10h (On fire) 🔥",        "10-12h (Volcano) 🌋",      "12h+ (Literal sun) ☀️"]},
    {"q": "Study hours completed? ✅",                     "a": ["0h (Marked off) ❌",   "1-3h (Started) ⬜",         "3-6h (Yellow flag) 🟨",    "6-8h (Orange zone) 🟧",        "8-10h (Green light) 🟩",    "10-12h (Blue ribbon) 🟦",  "12h+ (Purple heart) 🟪"]},
    {"q": "Grind time today? ⚡",                          "a": ["0h (Battery rest) 🪫", "1-3h (Charging up) 🔋",    "3-6h (Plugged in) 🔌",     "6-8h (Electric) ⚡",            "8-10h (Lightning) 🌩️",     "10-12h (Thunderstorm) ⛈️","12h+ (Tornado force) 🌪️"]},
    {"q": "How many hours studied? 📚",                    "a": ["0h (Chill mode) 🌴",   "1-3h (Baby steps) 👶",     "3-6h (Growing strong) 🌿", "6-8h (Blooming) 🌸",           "8-10h (Full bloom) 🌺",     "10-12h (Garden master) 🌻","12h+ (Forest legend) 🌳"]},
    {"q": "Study duration check? 🎓",                      "a": ["0h (No cap) 🧢",       "1-3h (Rookie gains) 🏃‍♂️","3-6h (Pro moves) 🏋️‍♂️",  "6-8h (Expert level) 🥷",       "8-10h (Master class) 🧙",   "10-12h (Sensei status) 🥋","12h+ (Final boss) 👹"]},
    {"q": "Total grind hours? 💎",                         "a": ["0h (Stone) 🪨",        "1-3h (Bronze) 🥉",         "3-6h (Silver) 🥈",         "6-8h (Gold) 🥇",               "8-10h (Platinum) 💿",       "10-12h (Diamond) 💎",      "12h+ (Unranked legend) 👑"]}
]

def stop_poll(message_id):
    url = f"{BASE_URL}/stopPoll"
    payload = {"chat_id": CHAT_ID, "message_id": message_id}
    response = requests.post(url, json=payload)
    print("Stop poll response:", response.json())

def send_poll(template):
    url = f"{BASE_URL}/sendPoll"
    payload = {
        "chat_id": CHAT_ID,
        "question": template["q"],
        "options": template["a"],
        "is_anonymous": False  # Allow group members to see exactly who voted
    }
    response = requests.post(url, json=payload)
    res_json = response.json()
    print("Send poll response:", res_json)
    if res_json.get("ok"):
        return res_json["result"]["message_id"]
    return None

def pin_message(message_id):
    url = f"{BASE_URL}/pinChatMessage"
    payload = {
        "chat_id": CHAT_ID,
        "message_id": message_id,
        "disable_notification": False  # Pins and notifies all members
    }
    response = requests.post(url, json=payload)
    print("Pin message response:", response.json())

def delete_message(message_id):
    url = f"{BASE_URL}/deleteMessage"
    payload = {"chat_id": CHAT_ID, "message_id": message_id}
    response = requests.post(url, json=payload)
    print(f"Delete message {message_id} response:", response.json())

def main():
    if not TOKEN or not CHAT_ID:
        print("Error: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set in the environment.")
        return

    # Load state
    state_file = "state.json"
    if os.path.exists(state_file):
        with open(state_file, "r") as f:
            state = json.load(f)
    else:
        state = {"last_message_id": None, "poll_index": 0}

    last_msg_id = state.get("last_message_id")
    poll_idx = state.get("poll_index", 0)

    # 1. Stop previous poll
    if last_msg_id is not None:
        print(f"Stopping previous poll with message ID: {last_msg_id}")
        stop_poll(last_msg_id)

    # 2. Send new poll
    template = POLL_TEMPLATES[poll_idx]
    print(f"Sending new poll: {template['q']}")
    new_msg_id = send_poll(template)

    # 3. Pin new poll
    if new_msg_id:
        print(f"Pinning new poll with message ID: {new_msg_id}")
        pin_message(new_msg_id)

        # Telegram generates a "Bot pinned a message" service message.
        # It's highly likely to be the immediate next message ID.
        print(f"Attempting to delete the pin service message (ID: {new_msg_id + 1})")
        delete_message(new_msg_id + 1)

        # Update and save state configuration
        state["last_message_id"] = new_msg_id
        state["poll_index"] = (poll_idx + 1) % len(POLL_TEMPLATES)
        with open(state_file, "w") as f:
            json.dump(state, f, indent=4)
        print("State updated successfully.")
    else:
        print("Failed to send new poll.")

if __name__ == "__main__":
    main()
