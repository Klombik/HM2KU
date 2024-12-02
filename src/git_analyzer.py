import git
from datetime import datetime
from typing import List, Dict, Tuple
from src.exceptions import GitError

class GitAnalyzer:
    def __init__(self, repo_path: str):
        try:
           self.repo = git.Repo(repo_path)
        except git.InvalidGitRepositoryError as e:
            raise GitError(f"Invalid Git repository: {repo_path}") from e

    def get_commits_after_date(self, since_date: datetime) -> List[git.objects.commit.Commit]:
        """Возвращает список коммитов после заданной даты."""
        commits = []
        try:
            for commit in self.repo.iter_commits('HEAD', reverse=True):
                 if commit.authored_datetime.replace(tzinfo=None) > since_date:
                     commits.append(commit)
        except git.GitCommandError as e:
            raise GitError(f"Error during git command: {e}") from e

        return commits
    

    def get_commit_parents(self, commit: git.objects.commit.Commit) -> List[git.objects.commit.Commit]:
        """Возвращает список родительских коммитов."""
        return list(commit.parents)
    
    def get_commit_info(self, commit: git.objects.commit.Commit) -> Tuple[str, str, str]:
        """Возвращает дату, время и автора коммита."""
        date_str = commit.authored_datetime.strftime("%Y-%m-%d")
        time_str = commit.authored_datetime.strftime("%H:%M:%S")
        author_str = commit.author.name
        return date_str, time_str, author_str