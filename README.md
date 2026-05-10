# Medical Portal - Cyber Security Project I

This is a Django-based web application developed for the Cybersecurity MOOC at the University of Helsinki. It replicates a patient medical records portal and contains intentional security vulnerabilities from the OWASP Top 10 (2021 list), along with their fixes (commented out in the code).

The project contains 5 intentional security flaws from the OWASP Top 10 (2021 list) : 

1. SQL Injection 
2. XSS Injection 
3. Insecure Direct Object Reference (IDOR)
4. Sensitive Data Exposure
5. Cross-Site Request Forgery (CSRF)


# Installation

```bash
# 1. Clone the repository
git clone https://github.com/adnan-faize/cybersecurity-mooc_project.git
cd cybersecurity-mooc_project

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the virtual environment
venv/Scripts/activate    # for Windows
source venv/bin/activate # for Linux / MacOS

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run migrations
python manage.py migrate

# 6. Populate sample data
python populate_data.py

# 7. Start the server
python manage.py runserver

# 8. Access the application visiting http://localhost:8000 in your browser
```
