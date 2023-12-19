# MyFinance
#### Video Demo:  https://youtu.be/uYH8Vbz4hLM
#### Description:

MyFinance is a Flask web application that enables users to manage their finances by registering income and expense transactions. This README file provides an in-depth explanation of the project, including the purpose of each file and design choices made during development.

## Project Files

### `app.py`

`app.py` serves as the main application file for MyFinance. It contains the Flask web application and handles routing and user interactions. Some of the key functionalities include:

- **User Registration**: Users can create an account by providing a username and password. Passwords are securely hashed before being stored in the database for enhanced security.

- **User Login**: Registered users can log in by providing their username and password. The application verifies user credentials by comparing hashed passwords.

- **User Logout**: Users can log out of their accounts by clearing their session.

- **Transaction Management**: The main functionality allows users to input and view their financial transactions, categorizing them as either income or expense. The user's available cash is updated based on the transactions.

- **Transaction History**: Users can view their transaction history, which is categorized by month and year.

### `util.py`

`util.py` contains utility functions used within the application. These functions include:

- **`apology`**: This function renders an apology message with an HTTP status code, allowing the application to communicate errors to the user.

- **`login_required`**: A decorator function that ensures a user is logged in before accessing certain routes.

- **`usd`**: A filter function that formats numerical values as USD currency.

### `myfinance.db`

`myfinance.db` is an SQLite database file used to store user and transaction data. It contains two tables:

- **`transactions`**: This table records individual financial transactions, including the user ID, value, date, type (income or expense), and a name for the transaction. Transactions are also associated with a specific day and month-year.

- **`users`**: This table stores user information, including the username, hashed password, and available cash balance.

### `templates/`

This directory contains HTML templates used to render various views of the application, ensuring a user-friendly interface. The templates include:

- **`layout.html`**: A base template that defines the overall structure of the web pages, including navigation bars, styles, and headers. It also contains links to Bootstrap and the application's favicon.

- **`index.html`**: The template for the main page where users can input and view their transactions. It includes a form for entering transaction details and a table to display transaction history.

- **`login.html`**: The template for the login page, which allows registered users to log in by providing their credentials.

- **`register.html`**: The template for the registration page, where users can create an account by choosing a username and password.

- **`history.html`**: The template for the transaction history page, which displays a summary of transactions categorized by month and year.

- **`apology.html`**: A template used to render apology messages with customizable text and images.

### `static/styles.css`

The CSS file `styles.css` is used to customize the application's appearance. It includes styling for the navigation bar, background colors, fonts, and other visual elements.

## Design Choices

1. **Password Security**: Passwords are securely hashed before being stored in the database, enhancing user data security.

2. **Session Management**: The application uses Flask's session management to keep track of user authentication and data between requests.

3. **Transaction History**: Transactions are categorized by month and year, providing users with a clear summary of their financial history.

4. **Usability**: The user interface is designed to be user-friendly, allowing users to easily input and view their financial transactions.

5. **Currency Formatting**: The application uses the `usd` filter to format currency values in a user-friendly manner.

By documenting these design choices and explaining the purpose of each file, this README file provides a comprehensive understanding of the project's structure and functionality, facilitating collaboration and maintenance.
