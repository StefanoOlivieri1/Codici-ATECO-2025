import os
import subprocess

def run_git_commands():
    github_token = os.getenv('GITHUB_TOKEN')
    repo_url = f"https://{github_token}@github.com/StefanoOlivieri1/Codici-ATECO-2025.git"
    
    commands = [
        ['git', 'config', '--global', 'user.name', 'StefanoOlivieri1'],
        ['git', 'config', '--global', 'user.email', 'stefano.olivieri@example.com'],
        ['git', 'remote', 'remove', 'origin'],
        ['git', 'remote', 'add', 'origin', repo_url],
        ['git', 'push', '-u', 'origin', 'main']
    ]
    
    for cmd in commands:
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"Executed: {' '.join(cmd[:-1] if 'token' in cmd[-1] else cmd)}")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error executing {' '.join(cmd[:-1] if 'token' in cmd[-1] else cmd)}")
            print(f"Error: {e.stderr}")
            return False
    return True

if __name__ == "__main__":
    success = run_git_commands()
    if success:
        print("Successfully pushed to GitHub!")
    else:
        print("Failed to push to GitHub.")
