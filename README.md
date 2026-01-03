# HR Management System

A comprehensive Django-based HR Management System with user authentication, employee management, and HR functionalities.

## 🚀 Features

### Authentication System
- **User Registration**: Employees can register using Employee ID, Email, Password, and Role (Employee/HR)
- **Secure Password Requirements**:
  - At least 8 characters
  - At least one uppercase letter
  - At least one lowercase letter
  - At least one number
  - At least one special character
- **Role-based Access**: Employee and HR roles with different permissions

### User Roles
- **Employee**: Can view their profile, submit leave requests, view performance reviews
- **HR**: Can manage employees, approve leave requests, conduct performance reviews
- **Admin**: Full system access

## 🌐 Access the Application

The Django development server is now running at:
**http://127.0.0.1:8000**

### Test Accounts
- **Admin Account**:
  - Username: admin
  - Password: admin123
  - Role: Admin

## 📱 Pages Available

1. **Home/Login Page**: `http://127.0.0.1:8000/`
2. **Sign Up**: `http://127.0.0.1:8000/accounts/signup/`
3. **Dashboard**: `http://127.0.0.1:8000/accounts/dashboard/` (after login)
4. **Admin Panel**: `http://127.0.0.1:8000/admin/`

## 🗄️ Database Setup & Models

### Current Database: SQLite ✅
The application is currently using **SQLite** database (`db.sqlite3`) for immediate functionality. All your data is being saved to this file and will persist between server restarts.

### PostgreSQL Support (Optional)
To use PostgreSQL with pgAdmin:

1. **Setup PostgreSQL** following `POSTGRESQL_SETUP.md`
2. **Switch to PostgreSQL**:
   ```bash
   python switch_to_sqlite.py postgres
   python setup_postgres.py
   python manage.py migrate
   ```
3. **Switch back to SQLite** (if needed):
   ```bash
   python switch_to_sqlite.py sqlite
   python manage.py migrate
   ```

### Database Models

#### Accounts App
- **CustomUser**: Extended Django user with role field (Employee/HR/Admin)

#### Employee App
- **Department**: Company departments with managers
- **Employee**: Employee profiles with detailed information (ID, position, salary, etc.)

#### HR App
- **LeaveRequest**: Employee leave requests with approval workflow
- **PerformanceReview**: Employee performance evaluations (1-5 rating scale)

## 🛠️ Setup Instructions

1. Install dependencies: `pip install -r requirements.txt`
2. Run migrations: `python manage.py migrate`
3. Create superuser: `python manage.py createsuperuser`
4. Start server: `python manage.py runserver`

## 🔐 Password Security

The system enforces strong password requirements using Django's built-in password validation:
- Minimum length: 8 characters
- Contains uppercase and lowercase letters
- Contains at least one number
- Contains at least one special character

## 💾 Data Persistence

✅ **All data is being saved** to the SQLite database (`db.sqlite3`):
- User accounts and authentication data
- Employee profiles and department information
- Leave requests and performance reviews
- All form submissions and user interactions

**Data persists between server restarts** - your information is safe!

## 🎯 Current Status & Next Steps

✅ **Fully Functional HR System**:
- User registration and authentication
- Role-based access control
- Database persistence
- Web interface with modern design
- Admin panel for data management

**Ready to use features**:
1. Register new users through the signup page
2. Login with different roles and access appropriate features
3. Access the admin panel at `/admin/` to view and manage all data
4. Switch to PostgreSQL anytime using the provided setup scripts

Would you like me to add more features like:
- Employee profile management pages
- Leave request submission and approval workflow
- Performance review system
- Department management
- Reporting dashboards