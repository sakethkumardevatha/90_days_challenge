import json
import os
import sys
import time

# --- CONFIG ---
ROADMAP_FILE = "roadmap.json"

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_data():
    if not os.path.exists(ROADMAP_FILE):
        return {}
    try:
        with open(ROADMAP_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {}

def save_data(data):
    with open(ROADMAP_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def main_menu():
    while True:
        data = load_data()
        clear_screen()
        print(f"{Colors.BOLD}🎓 AI CAREER AGENT (Active){Colors.ENDC}")
        
        sorted_keys = sorted(data.keys(), key=lambda x: int(x) if x.isdigit() else x)
        
        if not sorted_keys:
            print(f"\n{Colors.YELLOW}Roadmap is empty!{Colors.ENDC}")
            sys.exit()

        print(f"\n{Colors.HEADER}--- AVAILABLE SPRINTS ---{Colors.ENDC}")
        for day in sorted_keys:
            content = data[day]
            tasks = content['tasks']
            done = len([t for t in tasks if t['status'] == 'done'])
            total = len(tasks)
            status = "✅" if done == total else f"({done}/{total})"
            print(f"[{day}] {content['date']} - {content['focus']} {status}")

        print("\n[S] Manual Sync (Save)  [Q] Quit")
        choice = input("\nEnter Day ID to Work On: ").strip()

        if choice.lower() == 'q': sys.exit()
        if choice.lower() == 's':
            save_data(data)
            print("Progress Synced."); time.sleep(1); continue
        
        if choice in data:
            view_day(choice, data)

def view_day(day_id, data):
    while True:
        clear_screen()
        day_data = data[day_id]
        tasks = day_data['tasks']
        
        print(f"\n{Colors.HEADER}📅 {day_data['date']}: {day_data['focus']}{Colors.ENDC}")
        print("-" * 85)
        print(f"{'ID':<6} {'STATUS':<10} {'SUBJECT':<12} {'TASK'}")
        print("-" * 85)
        
        for t in tasks:
            status_color = Colors.GREEN if t['status'] == 'done' else Colors.FAIL
            status_text = "DONE" if t['status'] == 'done' else "TODO"
            
            sub_emoji = {"DSA": "🔴", "ML Theory": "🔵", "ML Math": "🟢", "Project": "🟣", "Tools": "🟠"}.get(t['subject'], "⚪")
            
            print(f"{t['id']:<6} {status_color}{status_text:<10}{Colors.ENDC} {sub_emoji} {t['subject']:<10} {t['topic']}")
        
        print("-" * 85)
        print("\n[1] Mark Task Done  [2] View Details  [3] Back to Menu")
        cmd = input("\nChoice: ")
        
        if cmd == '1':
            try:
                t_id = int(input("Enter Task ID: "))
                for t in tasks:
                    if t['id'] == t_id:
                        t['status'] = 'done'
                        save_data(data)
                        print(f"{Colors.GREEN}Progress Saved!{Colors.ENDC}"); time.sleep(0.5)
            except ValueError: pass
        elif cmd == '2':
            try:
                t_id = int(input("Enter Task ID: "))
                task = next((t for t in tasks if t['id'] == t_id), None)
                if task:
                    print(f"\n{Colors.BLUE}--- TASK DETAILS ---{Colors.ENDC}")
                    print(f"Action: {Colors.BOLD}{task['action']}{Colors.ENDC}")
                    input("\nPress Enter to return...")
            except ValueError: pass
        elif cmd == '3':
            break

if __name__ == "__main__":
    main_menu()