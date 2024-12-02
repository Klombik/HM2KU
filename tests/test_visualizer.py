import unittest
from src.visualizer import GraphVisualizer
from src.exceptions import GraphVisualizationError
import os
from unittest.mock import patch, Mock, call
import subprocess

class TestGraphVisualizer(unittest.TestCase):

    def setUp(self):
        self.graphviz_path = "C:\\Users\\smart\\KU\\Graphviz\\bin\\dot.exe"  # Настройте этот путь
        self.output_path = "test_output.png"
        self.visualizer = GraphVisualizer(self.graphviz_path, self.output_path)

    def tearDown(self):
        if os.path.exists(self.output_path):
            os.remove(self.output_path)
        if os.path.exists("temp.dot"):
             os.remove("temp.dot")

    @patch('subprocess.run')
    def test_visualize_graph(self, mock_run):
        # Тестируем визуализацию графа (без ошибок)
        mermaid_graph = "graph LR\nA-->B"
        self.visualizer.visualize_graph(mermaid_graph)
        mock_run.assert_called_once_with([self.graphviz_path, '-Tpng', 'temp.dot', '-o', self.output_path], check=True)
       # self.assertTrue(os.path.exists(self.output_path))  # Проверяем создание файла

    @patch('subprocess.run')
    def test_visualize_graph_subprocess_error(self, mock_run):
        # Тестируем обработку ошибок subprocess
        mock_run.side_effect = subprocess.CalledProcessError(returncode=1, cmd="dot")  # Эмулируем ошибку
        mermaid_graph = "graph LR\nA-->B"
        with self.assertRaises(GraphVisualizationError):
            self.visualizer.visualize_graph(mermaid_graph) # Ошибка должна быть перехвачена

    def test_convert_mermaid_to_dot(self):
        mermaid_graph = "graph LR\nA --> B\nC --> D"
        expected_dot_graph = 'digraph G {\n  "A" -> "B";\n  "C" -> "D";\n}\n'
        actual_dot_graph = self.visualizer.convert_mermaid_to_dot(mermaid_graph)
        self.assertEqual(expected_dot_graph, actual_dot_graph)