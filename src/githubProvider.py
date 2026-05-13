import os
from github import Github, Auth
from dotenv import load_dotenv

load_dotenv()

class GitHubProvider:
    def __init__(self):
        """
        Github client object 
        """
        token = os.getenv("GITHUB_PAT")
        if not token:
            raise ValueError("GITHUB_PAT not found. Check your .env file.")
        
        auth = Auth.Token(token)
        self.client = Github(auth=auth)

    def get_repo_contents(self, repo_full_name: str, path: str = "", ignore_dirs=None):
        """
        Fetches files with selective filtering.
        ignore_dirs: List of folders to skip (e.g., ['venv', 'tests'])
        """
        if ignore_dirs is None: 
            ignore_dirs = ['venv', '.git', 'node_modules', '__pycache__', 'dist', 'build']
        try:
            repo = self.client.get_repo(repo_full_name)
            contents = repo.get_contents(path)
            files = []

            while contents:
                file_content = contents.pop(0)
                
                # Selective Auditing: Skip ignored directories
                if file_content.type == "dir":
                    if file_content.name not in ignore_dirs:
                        contents.extend(repo.get_contents(file_content.path))
                else:
                    # Selective Auditing: Only process supported code files
                    if self._is_code_file(file_content.name):
                        files.append({
                            "name": file_content.name,
                            "path": file_content.path,
                            "content": file_content.decoded_content.decode("utf-8")
                        })
            return files
        
        except Exception as e:
            print(f"Error fetching GitHub data: {e}")
            return []

    def _is_code_file(self, filename: str) -> bool:
        """Filter for relevant file extensions to avoid binary/image bloat."""
        valid_extensions = ('.py', '.js', '.ts', '.go', '.sql', '.yml', '.yaml', '.dockerfile')
        return filename.lower().endswith(valid_extensions) or filename.lower() == "dockerfile"
