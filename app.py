from flask import Flask, render_template, redirect, url_for, flash, request
from forms import LoginForm, RegistrationForm, IncomeForm, ExpenseForm
from models import db, User, Expenses, Income
from extensions import db, bcrypt, login_manager
from flask_login import login_user, current_user, logout_user, login_required


app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

first_request = True


@app.before_request
def create_tables():
    global first_request
    if first_request:
        db.create_all()
        first_request = False


@app.route('/')
@login_required
def home():
    user_expenses = Expenses.query.filter_by(user_id=current_user.id).all()
    user_income = Income.query.filter_by(user_id=current_user.id).all()

    total_expense = sum(expense.amount for expense in user_expenses)
    total_income = sum(income.amount for income in user_income)

    balance = total_income - total_expense

    transactions = sorted(user_expenses + user_income,
                          key=lambda x: x.date, reverse=True)[:5]

    return render_template('index.html', expenses=total_expense, income=total_income, balance=balance, current_user=current_user, transactions=transactions)


@app.route('/transaction')
@login_required
def transaction():
    user_expenses = Expenses.query.filter_by(user_id=current_user.id).all()
    user_income = Income.query.filter_by(user_id=current_user.id).all()

    transactions = sorted(user_expenses + user_income,
                          key=lambda x: x.date, reverse=True)

    return render_template('transaction.html', transactions=transactions)


@app.route('/add_income', methods=['GET', 'POST'])
@login_required
def add_income():
    form = IncomeForm()
    if form.validate_on_submit():
        amount = form.amount.data
        source = form.source.data
        income = Income(amount=amount, source=source,
                        user_id=current_user.id)
        db.session.add(income)
        db.session.commit()
        flash('Income added successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('add_transaction.html', title='Add Income', form=form, endpoint='add_income')


@app.route('/add_expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        amount = form.amount.data
        description = form.description.data
        expense = Expenses(
            amount=amount, description=description, user_id=current_user.id)
        db.session.add(expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('add_transaction.html', title='Add Expense', form=form, endpoint='add_expense')


@app.route('/edit_transaction/<int:transaction_id>', methods=['POST', 'GET'])
@login_required
def edit_transaction(transaction_id):
    transaction = Expenses.query.get(
        transaction_id) or Income.query.get(transaction_id)

    if transaction is None:
        flash('Transaction not found.', 'danger')
        return redirect(url_for('home'))

    if isinstance(transaction, Expenses):
        form = ExpenseForm()
    else:
        form = IncomeForm()

    if request.method == 'GET':
        form.amount.data = transaction.amount
        if isinstance(transaction, Expenses):
            form.description.data = transaction.description
        else:
            form.source.data = transaction.source

    if form.validate_on_submit():
        transaction.amount = form.amount.data
        if isinstance(transaction, Expenses):
            transaction.description = form.description.data
        else:
            transaction.source = form.source.data
        db.session.commit()
        flash('Transaction has been updated!', 'success')
        return redirect(url_for('home'))

    return render_template('edit_transaction.html', title='Edit Transaction', transaction=transaction, form=form)


@app.route('/delete_transaction/<int:transaction_id>')
@login_required
def delete_transaction(transaction_id):
    transaction = Expenses.query.get(transaction_id)
    if transaction:
        db.session.delete(transaction)
    else:
        transaction = Income.query.get(transaction_id)
        if transaction:
            db.session.delete(transaction)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
