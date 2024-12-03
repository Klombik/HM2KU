from typing import List
from git import Commit
from src.git_analyzer import GitAnalyzer

class GraphBuilder:
    def __init__(self, git_analyzer: GitAnalyzer):
        self.git_analyzer = git_analyzer

    def build_commit_graph(self, commits: List[Commit]) -> str:
        """Строит DOT граф зависимостей коммитов."""
        dot_graph = "digraph G {\n"
        dot_graph += "    rankdir=LR;\n"
        dot_graph += "    node [shape=box];\n"

        commit_info_map = {}  # Сохраняем информацию о коммитах
        for commit in commits:
            date, time, author = self.git_analyzer.get_commit_info(commit)
            commit_id = str(commit.hexsha[:7])
            commit_label = f"{date} {time}\\n{author}"
            commit_info_map[commit.hexsha] = (commit_id, commit_label)
            dot_graph += f'    "{commit_id}" [label="{commit_label}"];\n'

        for commit in commits:
            commit_id, _ = commit_info_map[commit.hexsha]
            for parent in self.git_analyzer.get_commit_parents(commit):
                if parent.hexsha in commit_info_map:
                    parent_id, _ = commit_info_map[parent.hexsha]
                    dot_graph += f'    "{parent_id}" -> "{commit_id}";\n'
        dot_graph += "}\n"
        return dot_graph