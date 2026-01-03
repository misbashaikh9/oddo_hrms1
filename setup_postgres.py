#!/usr/bin/env python
"""
PostgreSQL Database Setup Script for HR Management System
Run this script to create the PostgreSQL database for the HR system.
"""

import psycopg2
from psycopg2 import sql

def create_database():
    """Create the PostgreSQL database for HR management system"""

    # Database connection parameters for creating database
    # Connect to default 'postgres' database first
    conn_params = {
        'database': 'postgres',
        'user': 'postgres',
        'password': 'Misba@123',  # Updated password
        'host': 'localhost',
        'port': '5432'
    }

    try:
        # Connect to PostgreSQL
        print("Connecting to PostgreSQL...")
        conn = psycopg2.connect(**conn_params)
        conn.autocommit = True  # Enable autocommit for database creation
        cursor = conn.cursor()

        # Create database if it doesn't exist
        db_name = 'hrms'
        print(f"Creating database '{db_name}'...")

        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (db_name,))
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            print(f"✅ Database '{db_name}' created successfully!")
        else:
            print(f"ℹ️  Database '{db_name}' already exists.")

        cursor.close()
        conn.close()

        # Test connection to the new database
        print("Testing connection to HRMS database...")
        test_conn_params = conn_params.copy()
        test_conn_params['database'] = db_name

        test_conn = psycopg2.connect(**test_conn_params)
        test_conn.close()
        print("✅ Database connection successful!")

        print("\n🎉 PostgreSQL setup complete!")
        print("\nNext steps:")
        print("1. Run: python manage.py migrate")
        print("2. Run: python manage.py runserver")
        print("3. Access the application at: http://127.0.0.1:8000")

    except psycopg2.Error as e:
        print(f"❌ PostgreSQL Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure PostgreSQL is installed and running")
        print("2. Check your PostgreSQL credentials in settings.py")
        print("3. Create a user in pgAdmin if needed")
        print("4. Make sure the PostgreSQL service is running")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    print("🚀 HR Management System - PostgreSQL Setup")
    print("=" * 50)
    create_database()
