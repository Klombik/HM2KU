import unittest
import os
import json
from src.utils import load_config
from src.exceptions import ConfigError

class TestUtils(unittest.TestCase):

    def setUp(self):
        # Создаем временный файл конфигурации для тестирования
        self.config_path = "test_config.json"
        self.valid_config = {
            "graphviz_path": "C:\\Users\\smart\\KU\\Graphviz\\bin\\dot.exe",  # Настройте этот путь
            "repo_path": "C:\\Users\\smart\\KU\\graph_visualizer\\my_repo",  # Настройте этот путь
            "output_path": "test_output.png",
            "since_date": "2023-12-01"
        }
        with open(self.config_path, 'w') as f:
            json.dump(self.valid_config, f)

    def tearDown(self):
        # Удаляем временный файл конфигурации
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        if os.path.exists("test_output.png"):
            os.remove("test_output.png")

    def test_load_config_valid(self):
        # Тестируем загрузку корректной конфигурации
        config = load_config(self.config_path)
        self.assertEqual(config, self.valid_config)

    def test_load_config_file_not_found(self):
        # Тестируем случай, когда файл конфигурации не найден
        with self.assertRaises(ConfigError):
            load_config("nonexistent_config.json")

    def test_load_config_invalid_json(self):
        # Тестируем случай, когда файл конфигурации содержит некорректный JSON
        with open(self.config_path, 'w') as f:
            f.write("invalid json")
        with self.assertRaises(ConfigError):
            load_config(self.config_path)

    def test_load_config_missing_keys(self):
        # Тестируем случай, когда в конфигурации отсутствуют обязательные ключи
        invalid_config = {"repo_path": "some/path"}
        with open(self.config_path, 'w') as f:
            json.dump(invalid_config, f)
        with self.assertRaises(ConfigError):
            load_config(self.config_path)

    def test_load_config_repo_path_not_exist(self):
        # Тестируем случай, когда путь к репозиторию не существует
        invalid_config = self.valid_config.copy()
        invalid_config["repo_path"] = "nonexistent/path"
        with open(self.config_path, 'w') as f:
            json.dump(invalid_config, f)
        with self.assertRaises(ConfigError):
            load_config(self.config_path)

    def test_load_config_graphviz_path_not_exist(self):
        # Тестируем случай, когда путь к Graphviz не существует
        invalid_config = self.valid_config.copy()
        invalid_config["graphviz_path"] = "nonexistent/path"
        with open(self.config_path, 'w') as f:
            json.dump(invalid_config, f)
        with self.assertRaises(ConfigError):
            load_config(self.config_path)

    def test_load_config_invalid_date_format(self):
        # Тестируем случай, когда формат даты некорректен
        invalid_config = self.valid_config.copy()
        invalid_config["since_date"] = "invalid-date"
        with open(self.config_path, 'w') as f:
            json.dump(invalid_config, f)
        with self.assertRaises(ConfigError):
            load_config(self.config_path)