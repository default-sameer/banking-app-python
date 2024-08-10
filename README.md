## Banking System in Python

This project is a simple banking system implemented in Python. It includes functionalities for user management, session handling, and role-based access control. The system supports two types of users: superadmin and regular users.

### Features

- User management : Create users, change usernames, and passwords.
- Session handling : Manage user sessions with timeout functionality.
- Role-based access control : Superadmin can access all functionalities, while regular users can only view their account details and create customers accounts.

### Project Structure

```
.
├── README.md
├── app
│   ├── app_initialization.py
│   ├── customer_management.py
│   ├── session.py
│   ├── user_management.pyy
└── utils
    ├── constants.py
    ├── generators.py
    ├── helps.py
    ├── session_helpers.py
    ├── user_helpers.py
    ├── validation.py
├──  main.py
├── config.py

```

#### Visible Bugs

- Sometimes when the superuser logs out instead of going back to the login page, it shows the enter youy choice prompt again.
- Add Back button in the customer portal to go back to the main menu.
