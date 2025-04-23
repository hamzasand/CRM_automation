from conversation_db import init_db
from check_inbox import check_and_respond

if __name__ == "__main__":
    print("📨 Starting AI email assistant...")
    init_db()
    check_and_respond()
