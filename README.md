# Exam Registration App

This is a Django application for managing exam registrations. It provides a portal for students to register for exams and an administration interface for faculty to manage exam sessions.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8+
- pip

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd exam-registration-app
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install django
    ```
    *(Note: In the provided environment, Django is already installed.)*

3.  **Set up the database:**
    The project uses SQLite, so no special database setup is needed. Just run the migrations:
    ```bash
    python exam_registration/manage.py migrate
    ```

### Running the Application

1.  **Start the development server:**
    ```bash
    python exam_registration/manage.py runserver
    ```
    The application will be available at `http://127.0.0.1:8000/`.

## User and Role Management

The application uses a role-based system with two main roles: **Faculty** and **Students**.

### 1. Create a Superuser

First, create a superuser account to access the admin site:
```bash
python exam_registration/manage.py createsuperuser
```
Follow the prompts to set a username, email, and password.

### 2. Set Up Groups (Roles)

1.  Start the development server and go to the admin site: `http://127.0.0.1:8000/admin/`.
2.  Log in with your superuser account.
3.  On the admin dashboard, find the **AUTHENTICATION AND AUTHORIZATION** section.
4.  Click on **Groups** and then click **ADD GROUP**.
5.  Create a group named `Faculty`.
6.  Create another group named `Students`.

### 3. Create a Faculty User

1.  In the admin site, go to **Users** and click **ADD USER**.
2.  Enter a username and password.
3.  Under the **Permissions** section, check the **Staff status** box. This allows the user to log in to the admin site.
4.  Under the **Groups** section, select the `Faculty` group and move it to the "Chosen groups" box.
5.  Save the user.

Faculty users can now log in to the admin site to create and manage `Exam Sessions`.

### 4. Create a Student User

1.  In the admin site, go to **Users** and click **ADD USER**.
2.  Enter a username, email, and password.
3.  **Important:** Make sure the **Staff status** box is **not** checked.
4.  Under the **Groups** section, select the `Students` group and move it to the "Chosen groups" box.
5.  Save the user.

Student users can now log in through the main site to register for exams.

## How to Use the App

-   **Faculty:**
    -   Log in to the admin site (`/admin/`).
    -   Create new `Exam Sessions` with details like title, description, start/end times, and capacity.
    -   View and manage existing registrations.
-   **Students:**
    -   Go to the home page (`/`).
    -   Log in with a student account.
    -   View the list of available exam sessions.
    -   Click "Register" to sign up for a session.
    -   View your registrations on the "My Registrations" page.