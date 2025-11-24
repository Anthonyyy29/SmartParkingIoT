import mysql.connector
from mysql.connector import Error
from config import settings

class DatabaseConnection:
    def __init__(self):
        self.connection = None
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                database=settings.DB_NAME
            )
            if self.connection.is_connected():
                print(f"✅ Connected to {settings.DB_NAME} database")
                return True
        except Error as e:
            print(f"❌ Connection error: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Connection closed")
    
    def execute_query(self, query, params=None):
        """Execute SELECT query and return results"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            print(f"❌ Query error: {e}")
            return None
    
    def execute_update(self, query, params=None):
        """Execute INSERT/UPDATE/DELETE query"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            last_id = cursor.lastrowid
            cursor.close()
            return last_id
        except Error as e:
            self.connection.rollback()
            print(f"❌ Update error: {e}")
            return None

# Global database connection
db = DatabaseConnection()
