import unittest
from datetime import datetime, timedelta
from src.git_analyzer import GitAnalyzer
from src.graph_builder import GraphBuilder
from src.exceptions import GitError

class TestGraphBuilder(unittest.TestCase):

    def setUp(self):
        self.repo_path = "C:\\Users\\smart\\KU\\graph_visualizer\\my_repo"  # Настройте этот путь
        try:
            self.git_analyzer = GitAnalyzer(self.repo_path)
        except GitError:
            self.skipTest("Тест требует наличия корректного Git репозитория по указанному пути.")
        self.graph_builder = GraphBuilder(self.git_analyzer)

    def test_build_commit_graph(self):
        # Тестируем построение графа коммитов
        since_date = datetime.now() - timedelta(days=365)  # Коммиты за последний год
        commits = self.git_analyzer.get_commits_after_date(since_date)
        mermaid_graph = self.graph_builder.build_commit_graph(commits)
        self.assertIsInstance(mermaid_graph, str) # Граф - строка
        self.assertTrue(mermaid_graph.startswith("graph LR")) # Начинается с "graph LR"
        self.assertIn("-->", mermaid_graph)  # Содержит стрелки "-->"
