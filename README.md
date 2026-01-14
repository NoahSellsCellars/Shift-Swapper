# Shift Swapper

Shift Swapper is a Flask-based web application designed to streamline schedule management for teams. It allows employees to view their upcoming shifts, post shifts they cannot work for trade, and pick up available shifts from coworkers.

## Features

* **User Authentication:** Secure Sign Up, Log In, and Log Out functionality using Flask-Login.
* **Shift Dashboard:** A central hub where users can view all available shifts posted by colleagues.
* **Personal Schedule:** A dedicated "My Shifts" page to view and manage your specific work hours.
* **Trade Workflow:**
    * **Post:** Users can mark their own shifts as "Up for Trade."
    * **Take:** Other users can claim available shifts, which instantly updates the schedule.
    * **Keep:** Users can reclaim a shift they previously posted if they change their mind.
* **Responsive Design:** Built with Bootstrap 5 to look great on desktop and mobile.

## Tech Stack

* **Backend:** Python, Flask
* **Database:** SQLite, SQLAlchemy
* **Frontend:** HTML5, CSS, Bootstrap 5
* **Authentication:** Flask-Login

## Getting Started

Follow these instructions to get a copy of the project running on your local machine.

### Prerequisites

* Python 3.x installed on your machine.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/shift-swapper.git](https://github.com/YOUR_USERNAME/shift-swapper.git)
    cd shift-swapper
    ```

2.  **Set up a virtual environment (Recommended):**
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install flask flask-sqlalchemy flask-login
    ```

4.  **Run the Application:**
    ```bash
    python app.py
    ```

5.  **Access the App:**
    Open your web browser and go to `http://127.0.0.1:5000/`.

*Note: The application is set up to automatically create the SQLite database (`instance/shifts.db`) the first time you run `app.py`.*

## Usage

1.  **Sign Up:** Create a new account.
2.  **My Shifts:** (For testing purposes) You may need to manually add shifts to the database via the Python shell, or implement an Admin "Create Shift" page (see Future Improvements).
3.  **Post a Shift:** Go to "My Shifts" and click "Post for Trade" on any shift you own.
4.  **Take a Shift:** Go to the Home Dashboard to see shifts others have posted. Click "Take Shift" to claim one.

## Future Improvements

* **Admin Dashboard:** Functionality for admin users to create, edit, and delete shifts directly from the UI.
* **Email Notifications:** Notify users when their shift is taken.
* **Calendar View:** Visual representation of the monthly schedule.

## License

This project is open source.
