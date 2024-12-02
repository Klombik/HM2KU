from typing import Dict, List, Tuple
from git.objects.commit import Commit
from src.git_analyzer import GitAnalyzer

class GraphBuilder:
    def __init__(self, git_analyzer: GitAnalyzer):
        self.git_analyzer = git_analyzer

    def build_commit_graph(self, commits: List[Commit]) -> str:
        """Строит mermaid граф зависимостей коммитов."""
        mermaid_str = "graph LR\n"
        
        commit_info_map = {} # Сохраняем информацию о коммитах, чтобы не повторять get_commit_info
        for commit in commits:
            date, time, author = self.git_analyzer.get_commit_info(commit)
            commit_id = str(commit.hexsha[:7])
            commit_label = f"{date} {time}\\n{author}"
            commit_info_map[commit.hexsha] = (commit_id, commit_label)

        for commit in commits:
            commit_id, commit_label = commit_info_map[commit.hexsha]
            mermaid_str += f"    {commit_id}[\"{commit_label}\"]\n"
            
            for parent in self.git_analyzer.get_commit_parents(commit):
                if parent.hexsha in commit_info_map:
                     parent_id, _ = commit_info_map[parent.hexsha]
                     mermaid_str += f"    {parent_id} --> {commit_id}\n"

        return mermaid_str