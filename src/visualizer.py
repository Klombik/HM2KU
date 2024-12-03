import subprocess
from src.exceptions import GraphVisualizationError
import os

class GraphVisualizer:
    def __init__(self, graphviz_path: str, output_path: str):
        self.graphviz_path = graphviz_path
        self.output_path = output_path
        
    def visualize_graph(self, dot_graph: str) -> None:
        """Визуализирует DOT граф и сохраняет в файл PNG."""
        try:
            with open('temp.dot', 'w') as f:
                f.write(dot_graph)
            subprocess.run([self.graphviz_path, '-Tpng', 'temp.dot', '-o', self.output_path], check=True)
            os.remove('temp.dot')
        except Exception as e:
            raise GraphVisualizationError(f"Error visualizing graph: {e}") from e