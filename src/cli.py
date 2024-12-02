import sys
import os

# Добавляем путь к пакету src в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils import load_config
from src.git_analyzer import GitAnalyzer
from src.graph_builder import GraphBuilder
from src.visualizer import GraphVisualizer
from src.exceptions import ConfigError, GitError, GraphVisualizationError

import argparse
import sys
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="Visualize Git commit dependencies.")
    parser.add_argument(
        "config_path",
        help="Path to the configuration file.",
    )
    args = parser.parse_args()

    try:
        config = load_config(args.config_path)
        repo_path = config["repo_path"]
        graphviz_path = config["graphviz_path"]
        output_path = config["output_path"]
        since_date = datetime.fromisoformat(config["since_date"])

        git_analyzer = GitAnalyzer(repo_path)
        commits = git_analyzer.get_commits_after_date(since_date)

        graph_builder = GraphBuilder(git_analyzer)
        mermaid_graph = graph_builder.build_commit_graph(commits)
        
        visualizer = GraphVisualizer(graphviz_path, output_path)
        visualizer.visualize_graph(mermaid_graph)

        print(f"Successfully visualized graph and saved to {output_path}")

    except (ConfigError, GitError, GraphVisualizationError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()