#!/usr/bin/env python
"""
Database Switch Script for HR Management System
Switch between PostgreSQL and SQLite databases
"""

import os
import sys
from pathlib import Path

def switch_to_sqlite():
    """Switch Django settings to use SQLite instead of PostgreSQL"""

    settings_file = Path(__file__).parent / 'myproject' / 'settings.py'

    if not settings_file.exists():
        print("❌ settings.py file not found!")
        return

    # Read current settings
    with open(settings_file, 'r') as f:
        content = f.read()

    # Replace PostgreSQL config with SQLite
    old_config = '''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hrms',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'driver': 'pg8000',
        },
    }
}'''

    new_config = '''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}'''

    if old_config in content:
        content = content.replace(old_config, new_config)
        print("✅ Switched to SQLite database")

        # Write back to file
        with open(settings_file, 'w') as f:
            f.write(content)

        print("✅ Settings updated successfully!")
        print("\n📋 Next steps:")
        print("1. Run: python manage.py migrate")
        print("2. Run: python manage.py runserver")
        print("3. Your data will be stored in db.sqlite3 file")

    else:
        print("ℹ️  Already using SQLite or configuration not found")

def switch_to_postgresql():
    """Switch Django settings to use PostgreSQL instead of SQLite"""

    settings_file = Path(__file__).parent / 'myproject' / 'settings.py'

    if not settings_file.exists():
        print("❌ settings.py file not found!")
        return

    # Read current settings
    with open(settings_file, 'r') as f:
        content = f.read()

    # Replace SQLite config with PostgreSQL
    old_config = '''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}'''

    new_config = '''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hrms',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'driver': 'pg8000',
        },
    }
}'''

    if old_config in content:
        content = content.replace(old_config, new_config)
        print("✅ Switched to PostgreSQL database")

        # Write back to file
        with open(settings_file, 'w') as f:
            f.write(content)

        print("✅ Settings updated successfully!")
        print("\n📋 Make sure PostgreSQL is set up, then:")
        print("1. Run: python setup_postgres.py")
        print("2. Run: python manage.py migrate")
        print("3. Run: python manage.py runserver")

    else:
        print("ℹ️  Already using PostgreSQL or configuration not found")

def main():
    if len(sys.argv) != 2:
        print("Usage: python switch_to_sqlite.py [sqlite|postgres]")
        print("\nExamples:")
        print("  python switch_to_sqlite.py sqlite   # Switch to SQLite")
        print("  python switch_to_sqlite.py postgres # Switch to PostgreSQL")
        return

    choice = sys.argv[1].lower()

    if choice == 'sqlite':
        switch_to_sqlite()
    elif choice == 'postgres':
        switch_to_postgresql()
    else:
        print("❌ Invalid option. Use 'sqlite' or 'postgres'")

if __name__ == '__main__':
    main()
