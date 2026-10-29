# Marg Web App - Web-Based Billing & Inventory Management System

A web-based billing and inventory management system modeled after Marg ERP 9+, built with Flask and MariaDB.

---

## What is the `.env` file and why do we use it?

Think of the `.env` file like a **personal settings card** for your computer.

When multiple developers work on the same project:
1. **Different Computers Have Different Settings**: One developer might run MariaDB on port `3306` with user `root`, while another runs it on port `3307` with user `atharvmscds`.
2. **Security**: Storing database passwords directly in code files is dangerous because anyone viewing the GitHub repository can see them.

Instead of changing the main Python files every time someone pushes code:
* All private settings (database username, password, port, secret keys) are kept in a local file called `.env`.
* The `.env` file stays **only on your computer** and is listed in `.gitignore` so Git ignores it.
* A file called `.env.example` is shared on Git as a template so new team members know what settings they need to create.

---

##  Project Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository_url>
cd marg-web-app