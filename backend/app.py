import os
from flask import Flask, render_template, send_from_directory, jsonify
from backend.config import Config, get_db_connection

# Import API Blueprints
from backend.auth import auth_bp
from backend.products import products_bp
from backend.purchases import purchases_bp
from backend.billing import billing_bp
from backend.members import members_bp
from backend.reports import reports_bp


def create_app():
    # Resolve relative paths pointing to frontend pages and static assets
    base_dir = os.path.abspath(os.path.dirname(__file__))
    frontend_dir = os.path.join(base_dir, '..', 'frontend')
    pages_dir = os.path.join(frontend_dir, 'pages')

    app = Flask(
        __name__,
        template_folder=pages_dir,
        static_folder=frontend_dir,
        static_url_path=''
    )
    
    app.config.from_object(Config)

    # Register API Blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(purchases_bp, url_prefix='/api/purchases')
    app.register_blueprint(billing_bp, url_prefix='/api/billing')
    app.register_blueprint(members_bp, url_prefix='/api/members')
    app.register_blueprint(reports_bp, url_prefix='/api/reports')

    # -------------------------------------------------------------------------
    # HTML Page Routes
    # -------------------------------------------------------------------------
    @app.route('/')
    def index():
        return render_template('login.html')

    @app.route('/login')
    def login_page():
        return render_template('login.html')

    @app.route('/pos')
    def pos_page():
        return render_template('pos.html')

    @app.route('/products')
    def products_page():
        return render_template('products.html')

    @app.route('/purchases')
    def purchases_page():
        return render_template('purchases.html')

    @app.route('/members')
    def members_page():
        return render_template('members.html')

    @app.route('/history')
    def history_page():
        return render_template('history.html')

    @app.route('/reports')
    def reports_page():
        return render_template('reports.html')

    # -------------------------------------------------------------------------
    # Static Assets Handler
    # -------------------------------------------------------------------------
    @app.route('/css/<path:filename>')
    def serve_css(filename):
        return send_from_directory(os.path.join(frontend_dir, 'css'), filename)

    @app.route('/js/<path:filename>')
    def serve_js(filename):
        return send_from_directory(os.path.join(frontend_dir, 'js'), filename)

    # -------------------------------------------------------------------------
    # System Health Check
    # -------------------------------------------------------------------------
    @app.route('/api/health', methods=['GET'])
    def health_check():
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1 AS status;")
                result = cursor.fetchone()
            conn.close()
            return jsonify({'status': 'healthy', 'database': 'connected', 'data': result}), 200
        except Exception as e:
            return jsonify({'status': 'unhealthy', 'database_error': str(e)}), 500

    # -------------------------------------------------------------------------
    # Error Handlers
    # -------------------------------------------------------------------------
    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({'error': 'Resource or Page Not Found'}), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify({'error': 'Internal Server Error'}), 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)