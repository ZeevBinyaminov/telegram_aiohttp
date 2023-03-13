import psycopg2


class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            database='postgres', user='postgres',
            password='', host='localhost',
            port='5432'
        )
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS tasks "
            "(themes VARCHAR(256), "
            "solutions_number INT, "
            "title VARCHAR(128), "
            "difficulty INT, "
            "is_chosen INT DEFAULT 0)"
        )
        self.connection.commit()

    def get_task_info(self, title):
        self.cursor.execute(
            "SELECT themes, solutions_number, title, difficulty "
            "FROM tasks "
            "WHERE title = %s",
            (title,)
        )
        return self.cursor.fetchone()

    def exists(self, task):
        self.cursor.execute(
            "SELECT title "
            "FROM tasks "
            "WHERE title = %s",
            (task.title,)
        )
        return self.cursor.fetchone()

    def add_task(self, task):
        self.cursor.execute(
            "INSERT INTO tasks "
            "(themes, solutions_number, title, difficulty) "
            "VALUES (%s, %s, %s, %s);",
            (task.themes, task.solutions_number, task.title, task.difficulty)
        )

    def get_all_themes(self):
        self.cursor.execute(
            "SELECT DISTINCT themes "
            "FROM tasks"
        )
        themes = self.cursor.fetchall()
        themes_set = set()
        for theme in themes:
            themes_set.update(theme[0].split(', '))
        themes_set.remove('')
        return sorted(themes_set)

    def get_contest(self, theme, difficulty):
        self.cursor.execute(
            "SELECT themes, solutions_number, title, difficulty "
            "FROM tasks "
            "WHERE is_chosen = 0 AND "
            "themes LIKE %s AND difficulty = %s "
            "LIMIT 10",
            ('%' + theme + '%', difficulty,)
        )
        contest = self.cursor.fetchall()

        for task in contest:
            self.cursor.execute(
                "UPDATE tasks "
                "SET is_chosen = 1 "
                "WHERE title = %s",
                (task[2],)
            )
            self.connection.commit()
        return contest


db = Database()
db.create_table()
