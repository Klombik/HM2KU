import unittest
from unittest.mock import patch, MagicMock
from src.visualizer import GraphVisualizer
from src.exceptions import GraphVisualizationError

class TestGraphVisualizer(unittest.TestCase):
    def setUp(self):
        self.graphviz_path = 'dot'
        self.output_path = 'output.png'
        self.visualizer = GraphVisualizer(self.graphviz_path, self.output_path)
    
    @patch('subprocess.run')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('os.remove')
    def test_visualize_graph(self, mock_remove, mock_open, mock_subprocess_run):
        dot_graph = 'digraph G {\n"node1" -> "node2";\n}'
        self.visualizer.visualize_graph(dot_graph)
        
        # Проверяем, что файл temp.dot был создан и записан
        mock_open.assert_called_with('temp.dot', 'w')
        mock_open().write.assert_called_with(dot_graph)
        
        # Проверяем, что subprocess.run был вызван с правильными аргументами
        mock_subprocess_run.assert_called_with(
            [self.graphviz_path, '-Tpng', 'temp.dot', '-o', self.output_path],
            check=True
        )
        
        # Проверяем, что temp.dot был удален
        mock_remove.assert_called_with('temp.dot')
    
    @patch('subprocess.run', side_effect=Exception('Subprocess error'))
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_visualize_graph_subprocess_error(self, mock_open, mock_subprocess_run):
        dot_graph = 'digraph G {\n"node1" -> "node2";\n}'
        with self.assertRaises(GraphVisualizationError) as context:
            self.visualizer.visualize_graph(dot_graph)
        self.assertIn('Error visualizing graph', str(context.exception))

if __name__ == '__main__':
    unittest.main()