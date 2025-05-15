import json
from flask import Flask, render_template, request, redirect, url_for, make_response, abort
from sqlalchemy import func
from models import db, Item, Rating

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

def get_ratings_cookie():
    ratings_cookie = request.cookies.get('ratings', '{}')
    try:
        ratings = json.loads(ratings_cookie)
        if not isinstance(ratings, dict):
            ratings = {}
    except Exception:
        ratings = {}
    return ratings

def set_ratings_cookie(response, ratings):
    response.set_cookie('ratings', json.dumps(ratings), httponly=True, secure=False)  # Set secure=True in production

@app.route('/')
def index():
    first_item = Item.query.order_by(Item.id.asc()).first()
    if first_item:
        return redirect(url_for('item_page', item_id=first_item.id))
    else:
        return redirect(url_for('add_item'))

@app.route('/item/<int:item_id>')
def item_page(item_id):
    item = Item.query.get(item_id)
    if not item:
        abort(404, description="Item not found")

    # Calculate average rating
    avg = db.session.query(func.avg(Rating.value)).filter(Rating.item_id == item_id).scalar()
    average = f"{avg:.2f}" if avg is not None else "No ratings yet."

    # Get user rating from cookie
    ratings = get_ratings_cookie()
    user_rating = ratings.get(str(item_id))

    # Navigation: previous and next item ids
    prev_item = Item.query.filter(Item.id < item_id).order_by(Item.id.desc()).first()
    next_item = Item.query.filter(Item.id > item_id).order_by(Item.id.asc()).first()

    if not prev_item:
        prev_item = Item.query.order_by(Item.id.desc()).first()
    if not next_item:
        next_item = Item.query.order_by(Item.id.asc()).first()

    return render_template('item.html',
                           item=item,
                           average=average,
                           user_rating=user_rating,
                           prev_id=prev_item.id,
                           next_id=next_item.id)

@app.route('/rate/<int:item_id>', methods=['POST'])
def rate_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        abort(404, description="Item not found")

    try:
        rating_value = int(request.form.get('rating'))
    except (TypeError, ValueError):
        abort(400, description="Invalid rating value")

    if rating_value < -10 or rating_value > 10:
        abort(400, description="Rating must be between -10 and 10")

    # Insert new rating
    new_rating = Rating(item_id=item_id, value=rating_value)
    db.session.add(new_rating)
    db.session.commit()

    # Update cookie
    ratings = get_ratings_cookie()
    ratings[str(item_id)] = str(rating_value)

    response = make_response(redirect(url_for('item_page', item_id=item_id)))
    set_ratings_cookie(response, ratings)
    return response

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    error = None
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if not name:
            error = "Item name cannot be empty."
        elif ' ' in name:
            error = "Item name must be a single word without spaces."
        else:
            # Check if item exists (case-sensitive)
            existing = Item.query.filter_by(name=name).first()
            if existing:
                error = "Item already exists."
        if error:
            return render_template('add_item.html', error=error)
        # Add new item
        new_item = Item(name=name)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('item_page', item_id=new_item.id))
    return render_template('add_item.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
