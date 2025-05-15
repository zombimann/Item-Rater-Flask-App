# Item Rater Flask App

## Overview
This is a simple Flask web application that allows users to rate single-word items on a scale from -10 (very evil) to 10 (very good). Users can navigate between items, add new items, and see the average rating for each item. User ratings are persisted using HTTP cookies.

## Features
- Rate items with buttons from -10 to 10.
- View average rating for each item.
- Navigate to previous and next items.
- Add new single-word items.
- User ratings are saved in cookies and highlighted on revisit.
- Data is stored persistently in a SQLite database (development).
- Designed to be production-ready with PostgreSQL.

## Technology Stack
- Python 3
- Flask
- Flask-SQLAlchemy
- SQLite (development)
- Jinja2 templates
- Minimal CSS for styling

## Setup Instructions

1. Clone the repository or copy the files.

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the Flask app:
   ```
   flask run
   ```

5. Open your browser and go to:
   ```
   http://127.0.0.1:5000/
   ```

## Code Structure

- `app.py`: Main Flask application with routes and logic.
- `models.py`: Database models for Items and Ratings.
- `templates/`: HTML templates for item rating and adding items.
- `requirements.txt`: Python dependencies.

## Extending the App

- To switch to PostgreSQL for production, update the `SQLALCHEMY_DATABASE_URI` in `app.py`.
- Add user authentication if needed.
- Implement outlier exclusion in average rating calculation.
- Enhance UI with JavaScript for better user experience.
- Add pagination or search for items.

## Testing

- Manually test all routes:
  - `/` redirects to first item or add item page.
  - `/item/<id>` displays item and ratings.
  - `/rate/<id>` accepts rating submissions.
  - `/add_item` allows adding new items with validation.

## Notes

- Ratings cookie is set with HttpOnly flag; set Secure flag in production.
- Input validation prevents SQL injection and XSS.
- The app is designed for simplicity, scalability, and user-friendliness.

---
