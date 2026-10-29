from flask import Blueprint, request, jsonify
from backend.config import get_db_connection

members_bp = Blueprint('members', __name__)

# -----------------------------------------------------------------------------
# 1. Fetch All Members (Management Table)
# -----------------------------------------------------------------------------
@members_bp.route('', methods=['GET'])
def get_members():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, member_code, name, phone, email, tier, reward_points, status, created_at "
                "FROM members ORDER BY id DESC;"
            )
            members = cursor.fetchall()
        conn.close()
        return jsonify({'members': members}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# -----------------------------------------------------------------------------
# 2. Search Member by Phone or Code (Used in POS Billing Screen)
# -----------------------------------------------------------------------------
@members_bp.route('/search', methods=['GET'])
def search_member():
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify({'error': 'Search query parameter is required'}), 400

    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, member_code, name, phone, email, tier, reward_points, status "
                "FROM members "
                "WHERE (phone = %s OR member_code = %s) AND status = 'active';",
                (query, query)
            )
            member = cursor.fetchone()
        conn.close()

        if member:
            return jsonify({'member': member}), 200
        return jsonify({'error': 'Member not found or inactive'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# -----------------------------------------------------------------------------
# 3. Register New Member
# -----------------------------------------------------------------------------
@members_bp.route('', methods=['POST'])
def create_member():
    data = request.get_json() or {}
    member_code = data.get('member_code', '').strip()
    name = data.get('name', '').strip()
    phone = data.get('phone', '').strip()
    email = data.get('email', '').strip() or None
    tier = data.get('tier', 'Bronze')

    if not member_code or not name or not phone:
        return jsonify({'error': 'Member code, name, and phone number are required'}), 400

    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO members (member_code, name, phone, email, tier) "
                "VALUES (%s, %s, %s, %s, %s);",
                (member_code, name, phone, email, tier)
            )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Member registered successfully'}), 201
    except Exception as e:
        err_msg = str(e)
        if 'phone' in err_msg:
            return jsonify({'error': 'A member with this phone number already exists'}), 400
        if 'member_code' in err_msg:
            return jsonify({'error': 'Member code already exists'}), 400
        return jsonify({'error': err_msg}), 500


# -----------------------------------------------------------------------------
# 4. Update Member Details & Tier Level
# -----------------------------------------------------------------------------
@members_bp.route('/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    phone = data.get('phone', '').strip()
    email = data.get('email', '').strip() or None
    tier = data.get('tier', 'Bronze')
    status = data.get('status', 'active')

    if not name or not phone:
        return jsonify({'error': 'Name and phone are required'}), 400

    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE members SET name=%s, phone=%s, email=%s, tier=%s, status=%s WHERE id=%s;",
                (name, phone, email, tier, status, member_id)
            )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Member updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500