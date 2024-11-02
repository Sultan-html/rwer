import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None 

    def open_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_name)
            self.connection.row_factory = sqlite3.Row

    def close_connection(self):
        if self.connection is not None:
            self.connection.close() 
            self.connection = None

    def search_user(self, username):
        self.open_connection()
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        self.close_connection()
        return user

    def execute_transaction(self, operations):
        self.open_connection() 
        try:
            cursor = self.connection.cursor()
            for operation in operations: 
                cursor.execute(operation) 
            self.connection.commit() 
        except Exception as e:
            self.connection.rollback()
            print(f"Transaction failed: {e}")
        finally:
            self.close_connection() 

class User:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_user(self, username, email):
        self.db_manager.open_connection()
        cursor = self.db_manager.connection.cursor() 
        cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", (username, email))
        self.db_manager.connection.commit()
        self.db_manager.close_connection()
        
          
    def get_user_by_id(self, user_id):
        self.db_manager.open_connection()  
        cursor = self.db_manager.connection.cursor() 
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone() 
        self.db_manager.close_connection()
        return user 

    def delete_user(self, user_id):
        self.db_manager.open_connection()
        cursor = self.db_manager.connection.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.db_manager.connection.commit()
        self.db_manager.close_connection()

user = User()
user.create.table()
