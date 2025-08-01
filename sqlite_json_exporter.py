import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Any

class SQLiteToJSONExporter:
    def __init__(self, db_path: str):
        """
        Initialize the exporter with the database path.
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path
        self.connection = None
    
    def connect(self):
        """Establish connection to the SQLite database."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Enable column access by name
            print(f"Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise
    
    def disconnect(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            print("Database connection closed.")
    
    def get_table_names(self) -> List[str]:
        """Get all table names from the database."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        return tables
    
    def export_table_to_dict(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Export a single table to a list of dictionaries.
        
        Args:
            table_name (str): Name of the table to export
            
        Returns:
            List[Dict[str, Any]]: List of rows as dictionaries
        """
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        
        rows = cursor.fetchall()
        result = []
        
        for row in rows:
            # Convert sqlite3.Row to dictionary
            row_dict = dict(row)
            result.append(row_dict)
        
        print(f"Exported {len(result)} rows from table '{table_name}'")
        return result
    
    def export_all_tables(self, output_file: str = None, table_names: List[str] = None):
        """
        Export all tables or specified tables to JSON.
        
        Args:
            output_file (str, optional): Output JSON file path. If None, uses database name.
            table_names (List[str], optional): Specific table names to export. If None, exports all tables.
        """
        try:
            self.connect()
            
            # Get table names to export
            if table_names is None:
                available_tables = self.get_table_names()
                tables_to_export = available_tables
            else:
                tables_to_export = table_names
            
            print(f"Tables to export: {tables_to_export}")
            
            # Export data
            exported_data = {}
            for table_name in tables_to_export:
                try:
                    exported_data[table_name] = self.export_table_to_dict(table_name)
                except sqlite3.Error as e:
                    print(f"Error exporting table '{table_name}': {e}")
                    continue
            
            # Generate output filename if not provided
            if output_file is None:
                db_name = os.path.splitext(os.path.basename(self.db_path))[0]
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"{db_name}_export_{timestamp}.json"
            
            # Write to JSON file
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(exported_data, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"\nExport completed successfully!")
            print(f"Output file: {output_file}")
            print(f"Total tables exported: {len(exported_data)}")
            
            # Print summary
            for table_name, data in exported_data.items():
                print(f"  - {table_name}: {len(data)} rows")
        
        except Exception as e:
            print(f"Export failed: {e}")
            raise
        finally:
            self.disconnect()
    
    def export_specific_tables(self, table_names: List[str], output_file: str = None):
        """
        Export only the specified tables to JSON.
        
        Args:
            table_names (List[str]): List of table names to export
            output_file (str, optional): Output JSON file path
        """
        self.export_all_tables(output_file, table_names)


def main():
    """Example usage of the SQLiteToJSONExporter."""
    
    # Configuration
    DATABASE_PATH = "example.db"  # Change this to your database path
    OUTPUT_FILE = "database_export.json"  # Optional: specify output file
    
    # Option 1: Export all tables
    exporter = SQLiteToJSONExporter(DATABASE_PATH)
    
    try:
        # Export all tables
        exporter.export_all_tables(OUTPUT_FILE)
        
        # Option 2: Export only specific tables (uncomment to use)
        # specific_tables = ["users", "products", "orders", "categories"]
        # exporter.export_specific_tables(specific_tables, "specific_tables_export.json")
        
    except FileNotFoundError:
        print(f"Database file '{DATABASE_PATH}' not found.")
        print("Please update the DATABASE_PATH variable with the correct path to your SQLite database.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
