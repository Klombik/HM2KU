import unittest
from datetime import datetime, timedelta
from src.git_analyzer import GitAnalyzer
from src.exceptions import GitError
import git
import os

class TestGitAnalyzer(unittest.TestCase):

    def setUp(self):
        self.repo_path = "C:\\Users\\smart\\KU\\graph_visualizer\\my_repo"  # Настройте этот путь
        try:
            self.git_analyzer = GitAnalyzer(self.repo_path)  # Инициализируем анализатор Git
        except GitError:
            self.skipTest("Тест требует наличия корректного Git репозитория по указанному пути.") # Пропускаем, если репозиторий не найден

    def test_get_commits_after_date(self):
        # Тестируем получение коммитов после определенной даты
        since_date = datetime.now() - timedelta(days=1)  # Дата - 1 день назад
        commits = self.git_analyzer.get_commits_after_date(since_date)
        self.assertIsInstance(commits, list) # Проверяем, что возвращается список
        for commit in commits:
            self.assertIsInstance(commit, git.Commit) # Проверяем, что каждый элемент - объект Commit
            self.assertGreaterEqual(commit.authored_datetime.replace(tzinfo=None), since_date) # Проверяем, что дата коммита позже since_date

    def test_get_commit_parents(self):
        # Тестируем получение родительских коммитов
        commits = self.git_analyzer.get_commits_after_date(datetime(1970, 1, 1))  # Получаем все коммиты
        if commits: # Если коммиты есть
            parents = self.git_analyzer.get_commit_parents(commits[0]) # Берем первый коммит и получаем его родителей
            self.assertIsInstance(parents, list) # Проверяем, что возвращается список
            for parent in parents:
                self.assertIsInstance(parent, git.Commit) # Проверяем, что каждый родитель - Commit

    def test_get_commit_info(self):
        # Тестируем получение информации о коммите
        commits = self.git_analyzer.get_commits_after_date(datetime(1970, 1, 1)) # Получаем все коммиты
        if commits: # Если коммиты есть
            date, time, author = self.git_analyzer.get_commit_info(commits[0]) # Получаем инфо о 1м коммите
            self.assertIsInstance(date, str) # дата - строка
            self.assertIsInstance(time, str) # время - строка
            self.assertIsInstance(author, str) # автор - строка

    def test_invalid_repo_path(self):
        with self.assertRaises(git.exc.NoSuchPathError):  # Ловим конкретное исключение
            GitAnalyzer("nonexistent/path")