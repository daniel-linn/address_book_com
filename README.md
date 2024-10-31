# Address Book.com

This is a web application built as a practice project and also serves as the final project for CS50. Enjoy exploring the functionality!  
This project mainly uses Flask and SQLAlchemy, and some JavaScript to implement the AJAX querying.

## About Address Book.com

Address Book.com is an online address book where users can browse other users’ information in a single main page, similar to a real-world address book. Key features include:

- **User Profile Management**: Users can update their own information.
- **Instant Search**: Quickly query information without browsing page by page.
- **Mailbox System**: Receive messages from the admin directly on the platform.

### Management System

Admins have access to a management system with tools to:
- **Validate or Delete Users**: Ensures only recognized users can access the address book.
- **Send Messages**: Communicate updates or important information to all or specific users.

This structure supports the privacy and security of an address book typically meant for a private group, like a club or fraternity.

## Try It Out

Experience the demo at [Address Book.com](https://ha3269570.pythonanywhere.com/login) using:
- **Username**: `test01`
- **Password**: `test01`

This demo account showcases all functions and pages. After logging in, click the envelope symbol to read messages.

> **Note**: This GitHub version differs from the demo. The `test01` account with full access is exclusive to the demonstration, not in this repo version.

## Auto-Register Script

For testing, use the `auto_register_30.py` script, which registers 30 sample users with basic information. Customize it as needed to suit your testing requirements.

---

> **Important Security Note**: If deploying this app directly, change the default admin account password found in `config.py` immediately after setup.

