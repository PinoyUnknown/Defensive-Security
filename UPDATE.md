# Update Instructions for Enterprise Defensive Security Toolkit

## Automatic Updates from Git Repository

### Prerequisites

- Git installed on your system
- Your project initialized as a Git repository
- Internet connection for fetching updates

### Update Commands

#### 1. **Update Toolkit (Full Update)**

Pull the latest version and update all files:

```bash
python main.py update
```

**What this command does:**
- ✅ Fetches latest changes from GitHub repository
- ✅ Checks for uncommitted local changes
- ✅ Pulls all updated files
- ✅ Updates Python dependencies if requirements.txt changed
- ✅ Updates version tracking

#### 2. **Check for Available Updates**

Check if updates are available without installing them:

```bash
python main.py check-updates
```

**Output includes:**
- ✅ Whether updates are available
- ✅ Latest commits in repository
- ✅ Current version
- ✅ Current branch

#### 3. **Status Check**

Check current toolkit status:

```bash
python main.py status
```

---

## Update Process Details

### Step 1: Check Git Repository
The update command verifies that:
- Git is installed and accessible
- Your directory is a Git repository
- You have valid repository configuration

### Step 2: Fetch Latest Changes
The toolkit fetches updates from the remote repository:
```bash
git fetch origin
```

### Step 3: Handle Uncommitted Changes
If you have local modifications:
- The toolkit will ask if you want to stash changes
- Stashing temporarily saves your changes
- After update, you can retrieve stashed changes:
  ```bash
  git stash pop
  ```

### Step 4: Pull Updates
The latest files are merged into your local copy:
```bash
git pull origin [current-branch]
```

### Step 5: Update Dependencies (Optional)
If `requirements.txt` was modified:
- The toolkit asks if you want to update Python packages
- Recommended to keep dependencies synchronized
- Updates are performed safely via pip

---

## Update Scenarios

### Scenario 1: First-Time Setup (Clone Repository)

```bash
# Clone the repository
git clone https://github.com/PinoyUnknown/Defensive-Security.git
cd Defensive-Security

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run the toolkit
python main.py start
```

### Scenario 2: Regular Updates

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Check for updates
python main.py check-updates

# If updates available, update
python main.py update

# Restart toolkit with latest version
python main.py start
```

### Scenario 3: Update with Local Changes

If you modified files and want to keep your changes:

```bash
# Stage and commit your changes first
git add .
git commit -m "My local customizations"

# Then update (will merge cleanly)
python main.py update
```

### Scenario 4: Discard Local Changes and Update

If you want to discard all local modifications:

```bash
# Reset to remote version
git reset --hard origin/[branch-name]

# Then update
python main.py update
```

---

## Troubleshooting Updates

### Error: "Git is not installed"

**Solution:** Install Git from https://git-scm.com/download

### Error: "Not a Git repository"

**Solution:** Clone the repository:
```bash
git clone https://github.com/PinoyUnknown/Defensive-Security.git
cd Defensive-Security
```

### Error: "Merge conflict"

**Solution:** Update command will notify you. To resolve:
```bash
# View conflicts
git status

# Resolve conflicts manually in conflicted files
# Then complete the merge
git add .
git commit -m "Resolved merge conflicts"
```

### Error: "Permission denied"

**Linux/macOS Solution:**
```bash
chmod +x main.py
python main.py update
```

### Error: "pip dependency error"

**Solution:** Manually update requirements:
```bash
pip install --upgrade -r requirements.txt
```

---

## Version Tracking

The toolkit maintains a `.version` file containing:
- Current version number
- Last update timestamp
- Platform information
- Developer information

This file is automatically updated after each successful update.

---

## Git Branch Management

### View available branches:
```bash
git branch -a
```

### Switch to different branch:
```bash
git checkout [branch-name]
```

### Update specific branch:
```bash
python main.py check-updates
python main.py update
```

---

## Automated Update Schedule

To check for updates regularly, you can create a scheduled task:

### Linux/macOS (cron)
```bash
# Edit crontab
crontab -e

# Add this line to check updates daily at 8 AM
0 8 * * * cd /path/to/Defensive-Security && python main.py check-updates
```

### Windows (Task Scheduler)
```batch
# Run Task Scheduler and create new task
# Set to run: python main.py check-updates
# Trigger: Daily at 8:00 AM
```

---

## Best Practices

✅ **Do:**
- Check for updates regularly: `python main.py check-updates`
- Backup important configurations before updating
- Test updates in a development environment first
- Keep your version of the toolkit updated
- Review update logs

❌ **Don't:**
- Force push if you don't understand Git
- Delete .git folder
- Modify core system files unless necessary
- Run update while toolkit is running

---

## Support

For update issues:
- GitHub Issues: https://github.com/PinoyUnknown/Defensive-Security/issues
- Check Git documentation: https://git-scm.com/doc
- Contact: PinoyUnknown

---

**Developed by: White Hat - PinoyUnknown**  
GitHub: https://github.com/PinoyUnknown  
Instagram: https://instagram.com/pinoyunknown
