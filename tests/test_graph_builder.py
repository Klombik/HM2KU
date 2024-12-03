import unittest
from unittest.mock import MagicMock
from git import Commit
from src.graph_builder import GraphBuilder
from src.git_analyzer import GitAnalyzer

class TestGraphBuilder(unittest.TestCase):
    def test_build_commit_graph(self):
        git_analyzer = MagicMock(spec=GitAnalyzer)
        commit1 = MagicMock(spec=Commit)
        commit2 = MagicMock(spec=Commit)
        
        commit1.hexsha = 'a1b2c3d4e5f6g7h8i9j0'
        commit2.hexsha = 'j0i9h8g7f6e5d4c3b2a1'
        
        git_analyzer.get_commit_info.side_effect = [
            ('2023-12-01', '12:34:56', 'John Doe'),
            ('2023-12-02', '13:45:00', 'Jane Smith'),
        ]
        
        git_analyzer.get_commit_parents.side_effect = [
            [commit2],  # commit1 has parent commit2
            []          # commit2 has no parents
        ]
        
        commits = [commit1, commit2]
        
        graph_builder = GraphBuilder(git_analyzer)
        dot_graph = graph_builder.build_commit_graph(commits)
        
        # Проверяем, что результат начинается с "digraph G {"
        self.assertTrue(dot_graph.strip().startswith("digraph G {"))
        
        # Проверяем, что содержимое графа корректно
        expected_lines = [
            '    "a1b2c3d" [label="2023-12-01 12:34:56\\nJohn Doe"];',
            '    "j0i9h8g" [label="2023-12-02 13:45:00\\nJane Smith"];',
            '    "j0i9h8g" -> "a1b2c3d";'
        ]
        
        for line in expected_lines:
            self.assertIn(line, dot_graph)
        
        # Проверяем, что граф завершается "}"
        self.assertTrue(dot_graph.strip().endswith("}"))

if __name__ == '__main__':
    unittest.main()