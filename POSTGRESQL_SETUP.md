# PostgreSQL Setup Guide for HR Management System

## 📋 Prerequisites
1. **Install PostgreSQL**: Download from https://www.postgresql.org/download/
2. **Install pgAdmin**: Download from https://www.pgadmin.org/download/

## 🛠️ Step-by-Step Setup

### 1. Start PostgreSQL Service
- **Windows**: Open Services (services.msc) and start "postgresql-x64-XX"
- **Linux/Mac**: Use `sudo systemctl start postgresql` or `brew services start postgresql`

### 2. Set PostgreSQL Password
Open Command Prompt as Administrator and run:
```bash
psql -U postgres
```
In the PostgreSQL shell:
```sql
ALTER USER postgres PASSWORD 'password';
\q
```

### 3. Create Database in pgAdmin
1. Open pgAdmin
2. Connect to your PostgreSQL server
3. Right-click on "Databases" → "Create" → "Database"
4. Name: `hr_management`
5. Owner: `postgres`
6. Click "Save"

### 4. Alternative: Use the Setup Script
After setting up PostgreSQL with the correct password, run:
```bash
python setup_postgres.py
```

### 5. Run Django Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Start the Server
```bash
python manage.py runserver
```

## 🔧 Troubleshooting

### Connection Issues
- **"password authentication failed"**: Set PostgreSQL password as shown above
- **"could not connect to server"**: Make sure PostgreSQL service is running
- **Port issues**: Default port is 5432, make sure it's not blocked

### pgAdmin Issues
- **Can't connect**: Check PostgreSQL service is running
- **Authentication failed**: Verify username/password in pgAdmin connection

## ⚙️ Database Configuration

The current settings in `myproject/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hr_management',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'driver': 'pg8000',
        },
    }
}
```

**Modify these values** if your PostgreSQL setup is different:
- `NAME`: Your database name
- `USER`: Your PostgreSQL username
- `PASSWORD`: Your PostgreSQL password
- `HOST`: Usually 'localhost' or '127.0.0.1'
- `PORT`: Usually '5432'

## 🔄 Fallback to SQLite

If PostgreSQL setup is too complex, you can use SQLite instead:

1. Comment out the PostgreSQL DATABASES config
2. Uncomment the SQLite DATABASES config in `settings.py`
3. Run: `python manage.py migrate`

SQLite will work fine for development and testing!

## ✅ Verification

After setup, verify everything works:
1. Visit: http://127.0.0.1:8000
2. Check admin panel: http://127.0.0.1:8000/admin/
3. Data should now be saved to PostgreSQL database

## 📞 Need Help?

If you encounter issues:
1. Check PostgreSQL service is running
2. Verify credentials in `settings.py`
3. Test connection using pgAdmin
4. Try the SQLite fallback option
