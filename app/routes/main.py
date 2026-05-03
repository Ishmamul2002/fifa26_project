from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from ..models import Match, Team, Cart, Ticket, Payment
from .. import db
from datetime import datetime
from flask_login import login_required, current_user
import qrcode
import os
from datetime import datetime, timedelta

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return redirect(url_for('auth.login'))


@main_bp.route('/upcoming-matches')
def upcoming_matches():
    search_query = request.args.get('search', '').strip()
    
    query = Match.query.filter(Match.date >= datetime.utcnow().date())
    
    if search_query:
        query = query.join(Team, (Match.team_a_id == Team.team_id) | 
                                 (Match.team_b_id == Team.team_id))\
                     .filter(Team.name.ilike(f'%{search_query}%'))
    
    matches = query.order_by(Match.date).limit(12).all()
    
    return render_template('public/upcoming_matches.html', 
                         matches=matches, 
                         search_query=search_query)


@main_bp.route('/book-ticket/<int:match_id>')
def book_ticket(match_id):
    match = Match.query.get_or_404(match_id)
    return render_template('public/book_ticket.html', match=match)


@main_bp.route('/cart')
def cart():
    return render_template('public/cart.html')


@main_bp.route('/buy-tickets')
def buy_tickets():
    matches = Match.query.filter(Match.date >= datetime.utcnow().date())\
                        .order_by(db.func.random()).limit(6).all()
    return render_template('public/buy_tickets.html', matches=matches)


# ================== NEW ROUTES ==================

@main_bp.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    try:
        data = request.get_json()
        
        new_item = Cart(
            user_id = current_user.user_id if current_user.is_authenticated else 3,
            item_type = data.get('category', 'Standard'),
            item_id = int(data.get('match_id')),
            quantity = int(data.get('quantity', 1)),
            price_per_ticket = float(data.get('price', 299)),
            total_price = float(data.get('price', 299)) * int(data.get('quantity', 1))
        )
        
        db.session.add(new_item)
        db.session.commit()
        
        print(f"✅ SUCCESS: Added {data.get('quantity')} × {data.get('category')} ticket")
        return jsonify({'success': True})
        
    except Exception as e:
        print(f"❌ Add to Cart Failed: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500
    


@main_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if request.method == 'POST':
        # Save tickets from cart to Ticket table
        cart_items = Cart.query.filter_by(user_id=current_user.user_id).all()
        
        for item in cart_items:
            ticket = Ticket(
                user_id = current_user.user_id,
                match_id = item.item_id,
                ticket_type = item.item_type or 'Standard',
                quantity = item.quantity,
                price = item.price_per_ticket or 299.0,
                status = 'active'
            )
            db.session.add(ticket)
            db.session.flush()
            
            # Generate QR
            import qrcode
            qr = qrcode.make(f"TICKET-{ticket.ticket_id}")
            qr_dir = "static/qrcodes"
            os.makedirs(qr_dir, exist_ok=True)
            qr_path = f"{qr_dir}/ticket_{ticket.ticket_id}.png"
            qr.save(qr_path)
            ticket.qr_code = f"qrcodes/ticket_{ticket.ticket_id}.png"
        
        # Clear cart
        Cart.query.filter_by(user_id=current_user.user_id).delete()
        db.session.commit()
        
        return redirect(url_for('main.my_tickets'))
    
    # GET request = Show payment page
    return render_template('public/checkout.html')


@main_bp.route('/user/tickets')
@login_required
def my_tickets():
    tickets = Ticket.query.filter_by(user_id=current_user.user_id).all()
    return render_template('user/my_tickets.html', tickets=tickets)


@main_bp.route('/api/cart')
def api_cart():
    cart_items = Cart.query.all()   # or filter by user later
    
    result = []
    for item in cart_items:
        match = Match.query.get(item.item_id)
        team_a = match.team_a.name if match and match.team_a else f"Team {item.item_id}"
        team_b = match.team_b.name if match and match.team_b else "Unknown"
        
        result.append({
            'cart_id': item.cart_id,
            'match_name': f"{team_a} vs {team_b}",
            'category': item.item_type,
            'quantity': item.quantity,
            'total_price': item.total_price or 299 * item.quantity
        })
    
    return jsonify({'cart': result})

@main_bp.route('/debug-cart')
def debug_cart():
    from sqlalchemy import text
    result = db.session.execute(text("SELECT COUNT(*) as count FROM cart")).scalar()
    items = Cart.query.all()
    
    output = f"""
    <h3>Database Check</h3>
    <p>Raw SQL Count: <b>{result}</b> items in cart table</p>
    <p>Model Count: <b>{len(items)}</b> items</p>
    <hr>
    """
    for item in items:
        output += f"<p>Cart ID {item.cart_id} | User {item.user_id} | Match {item.item_id} | Qty {item.quantity}</p>"
    
    return output


@main_bp.route('/debug-db')
def debug_db():
    from sqlalchemy import text
    try:
        result = db.session.execute(text("SELECT COUNT(*) FROM cart")).scalar()
        db_name = db.session.execute(text("SELECT DATABASE()")).scalar()
        return f"""
        <h3>Database Debug</h3>
        <p>Connected Database: <b>{db_name}</b></p>
        <p>Total rows in cart table: <b>{result}</b></p>
        """
    except Exception as e:
        return f"Error: {str(e)}"
    

@main_bp.route('/remove-from-cart/<int:cart_id>', methods=['POST'])
def remove_from_cart(cart_id):
    try:
        item = Cart.query.get(cart_id)
        if item:
            db.session.delete(item)
            db.session.commit()
            return jsonify({'success': True})
        return jsonify({'success': False, 'message': 'Item not found'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500