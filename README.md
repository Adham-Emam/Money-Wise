# Personal Finance App

This is a personal finance application built using Flask. The app allows users to track their income and expenses, providing a clear financial summary and insights.

## Features

- User Registration and Login
- Add, Edit, and Delete Income and Expenses
- Financial Summary Dashboard
- Recent Transactions
- Income vs Expenses Chart

## Installation

1. Clone the repository:

   ```bash

   ```

2. Create a virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```

## Configuration

Configure the application settings in `config.py`. Here is an example configuration:

```python
class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

## Running the Application

1. Run the Flask application:

   ```bash
   flask run
   ```

2. Open your browser and navigate to `http://127.0.0.1:5000`.

## Project Structure

```
Money-Wise/
│
│── models.py
│── forms.py
│── templates/
│   ├── layout.html
│   ├── login.html
│   ├── register.html
│   ├── index.html
│   ├── transaction.html
│   ├── add_transaction.html
│   ├── edit_transaction.html
│── static/
│   ├── images/
│   ├── css/
│   │   ├── global.css
│
├── config.py
├── extensions.py
├── requirements.txt
├── Procfile
├── app.py
```

## Routes

- `/` - Home page (requires login)
- `/login` - User login
- `/register` - User registration
- `/add_income` - Add new income
- `/add_expense` - Add new expense
- `/edit_transaction/<int:transaction_id>` - Edit an existing transaction
- `/delete_transaction/<int:transaction_id>` - delete an existing transaction
- `/logout` - User logout

## Forms

- **LoginForm**: Handles user login
- **RegistrationForm**: Handles user registration
- **ExpenseForm**: Handles adding and editing expenses
- **IncomeForm**: Handles adding and editing income

## Models

- **User**: User model for storing user credentials and associated tasks
- **Income**: Model for storing income transactions
- **Expenses**: Model for storing expense transactions

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any bugs or improvements.
