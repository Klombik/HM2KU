import subprocess
from src.exceptions import GraphVisualizationError
import os
from PIL import Image

class GraphVisualizer:
    def __init__(self, graphviz_path: str, output_path: str):
        self.graphviz_path = graphviz_path
        self.output_path = output_path
        
    def visualize_graph(self, mermaid_graph: str) -> None:
        """Визуализирует граф и сохраняет в файл png."""
        try:
            # Конвертируем Mermaid в DOT
            dot_graph = self.convert_mermaid_to_dot(mermaid_graph)
            
            # Используем Graphviz для рендеринга
            with open('temp.dot', 'w') as f:
                f.write(dot_graph)
            
            subprocess.run([self.graphviz_path, '-Tpng', 'temp.dot', '-o', self.output_path], check=True)
            
            os.remove('temp.dot')

        except Exception as e:
            raise GraphVisualizationError(f"Error visualizing graph: {e}") from e
        
    def convert_mermaid_to_dot(self, mermaid_graph: str) -> str:
        """Конвертирует Mermaid в DOT, добавляя кавычки."""
        dot_graph = "digraph G {\n"
        lines = mermaid_graph.split('\n')
        for line in lines:
            if line.startswith("graph LR"):
                continue
            elif ' --> ' in line:
                parts = line.split(' --> ')
                dot_graph += f'  "{parts[0].strip()}" -> "{parts[1].strip()}";\n'
        dot_graph += "}\n"
        return dot_graph