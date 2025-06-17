__author__ = 'naras_mg'
# libraries
from flask import Flask, jsonify, abort, make_response, request, send_file
from flask_cors import cross_origin # CORS,
import os, logging, zlib, base64  #,json,
import argparse
import socket
from contextlib import closing
import threading
import secrets
import sys
from datetime import datetime, timedelta
import hashlib
# from datetime import datetime
import tempfile
import shutil

# Add the project root to Python path
from pathlib import Path
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from Source.Model import BaseModel as bm, HideRevealRoutines as hrr

# User management
class User:
    def __init__(self, username: str, password_hash: str, is_admin: bool = False):
        self.username = username
        self.password_hash = password_hash
        self.is_admin = is_admin
        self.grids = set()  # Grids owned by this user
        self.session_token = None
        self.session_expiry = None

    def can_access_grid(self, grid_name: str) -> bool:
        return self.is_admin or grid_name in self.grids
    def can_create_grid(self) -> bool:
        return True  # All users can create grids
    def can_remove_grid(self, grid_name: str) -> bool:
        return self.is_admin or grid_name in self.grids
    def can_perform_operation(self, operation: str) -> bool:
        # Define which operations are allowed for regular users
        allowed_operations = {'hide', 'reveal', 'display', 'noisefill', 'it_fits_in'}
        return self.is_admin or operation in allowed_operations

    def create_session(self) -> str:
        """Create a new session for the user"""
        self.session_token = secrets.token_urlsafe(32)
        self.session_expiry = datetime.now() + timedelta(hours=24)  # 24 hour session
        return self.session_token
    def validate_session(self, token: str) -> bool:
        """Validate the session token"""
        if not self.session_token or not self.session_expiry: return False
        if datetime.now() > self.session_expiry: return False
        return self.session_token == token

    def logout(self):
        """Invalidate the session"""
        self.session_token = None
        self.session_expiry = None

    def verify_password(self, password: str) -> bool:
        """Verify the password"""
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

def hash_password(password: str) -> str:
    """Hash a password for storing"""
    return hashlib.sha256(password.encode()).hexdigest()

# Initialize users dictionary with admin
admin_password = 'admin123$%^' # secrets.token_urlsafe(16)  # Generate a random admin password
users = {'admin': User('admin', hash_password(admin_password), is_admin=True)}
print(f"\nAdmin credentials:")
print(f"Username: admin")
print(f"Password: {admin_password}")
print(f"Please login as admin before performing any operations\n")

# Session management
def get_current_user() -> User:
    """Get the current user from the session token"""
    token = request.headers.get('X-Session-Token')
    if not token: return None  # No session token provided
    
    # Check all users for valid session
    for user in users.values():
        if user.validate_session(token): return user
    return None  # No valid session found

def require_auth():
    """Decorator to require authentication"""
    def decorator(f):
        def wrapped(*args, **kwargs):
            user = get_current_user()
            if not user:
                return make_response(jsonify({'error': 'Authentication required'}), 401)
            return f(*args, **kwargs)
        wrapped.__name__ = f.__name__
        return wrapped
    return decorator

def find_free_port(start_port=5000, max_port=65535):
    """
    Find the next available port starting from start_port.
    Returns None if no port is available.
    """
    for port in range(start_port, max_port + 1):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            try:
                sock.bind(('', port))
                return port
            except OSError:
                continue
    return None
def parse_args():
    parser = argparse.ArgumentParser(description='Run the Ancient Indian Encryption Systems REST server')
    parser.add_argument('--port', type=int, help='Port to run the server on')
    parser.add_argument('--auto-port', action='store_true', help='Automatically find next available port')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind the server to')
    return parser.parse_args()

logging.basicConfig(filename='../../CryptologyJournal.log',format='%(asctime)s %(message)s',level=logging.DEBUG)
global grids
grids = {}  # Will store {grid_name: {'grid': CellGrid, 'owner': username}}

app = Flask(__name__)
endpoint_prefix = '/Cryptology/api/v1.0/'

# Generate a random shutdown token
# shutdown_token = secrets.token_urlsafe(32)
# print(f"Server shutdown token: {shutdown_token}")

def shutdown_server(shutdown_func=None):
    """Shutdown the Flask server gracefully"""
    try:
        # Use the captured shutdown function if available
        if shutdown_func is not None: shutdown_func()

        # Give the server a moment to shutdown gracefully
        threading.Timer(1.0, lambda: os._exit(0)).start()
    except Exception as e:
        # If anything goes wrong, force quit after a short delay
        print(f"Error during graceful shutdown: {e}")
        threading.Timer(1.0, lambda: os._exit(0)).start()

@app.route(endpoint_prefix + 'shutdown')
@cross_origin()
@require_auth()
def shutdown():
    """Endpoint to shutdown the server"""
    user = get_current_user()
    if not user.is_admin: return make_response(jsonify({'error': 'Only administrators can shutdown the server'}), 403)
    # token = request.args.get('token')
    # if token != shutdown_token: return make_response(jsonify({'error': 'Invalid shutdown token'}), 403)
    try:
        # Capture the shutdown function before starting the thread
        shutdown_func = request.environ.get('werkzeug.server.shutdown')
        # Start shutdown in a separate thread to allow response to be sent
        threading.Thread(target=shutdown_server, args=(shutdown_func,)).start()
        return jsonify({'message': 'Server is shutting down...'})
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

# User management endpoints
@app.route(endpoint_prefix + 'login', methods=['POST'])
@cross_origin()
def login():
    """Login endpoint to create a session"""
    try:
        if not request.is_json: return make_response(jsonify({'error': 'Content-Type must be application/json'}), 415)
        data = request.get_json()
        if not data: return make_response(jsonify({'error': 'No JSON data provided'}), 400)
        username = data.get('username')
        password = data.get('password')
        if not username or not password: return make_response(jsonify({'error': 'Username and password are required'}), 400)
        if username not in users: return make_response(jsonify({'error': 'Invalid username or password'}), 401)
        user = users[username]
        if not user.verify_password(password): return make_response(jsonify({'error': 'Invalid username or password'}), 401)
        
        token = user.create_session()
        return jsonify({
            'message': f'Login successful for {username}',
            'token': token,
            'expires': user.session_expiry.isoformat()
        })
    except Exception as e:
        return make_response(jsonify({'error': f'Exception: {str(e)}'}), 500)
@app.route(endpoint_prefix + 'logout', methods=['POST'])
@cross_origin()
@require_auth()
def logout():
    """Logout endpoint to invalidate the session"""
    try:
        token = request.headers.get('X-Session-Token')
        if not token:
            return make_response(jsonify({'error': 'No session token provided'}), 400)
        
        # Find user with this token and logout
        for user in users.values():
            if user.validate_session(token):
                user.logout()
                return jsonify({'message': f'Logout successful for {user.username}'})
        
        return make_response(jsonify({'error': 'Invalid session token'}), 401)
    except Exception as e:
        return make_response(jsonify({'error': f'Exception: {str(e)}'}), 500)

@app.route(endpoint_prefix + 'users/create', methods=['POST'])
@cross_origin()
@require_auth()
def create_user():
    """Create a new user"""
    user = get_current_user()
    # print(f'DEBUG: Current user: {user.username}, is_admin: {user.is_admin}, type: {type(user.is_admin)}')
    
    # More explicit admin check with debug
    is_admin = bool(user.is_admin)  # Force boolean conversion
    # print(f'DEBUG: Admin check - is_admin value: {is_admin}, type: {type(is_admin)}')
    
    if not is_admin:
        # print(f'DEBUG: Access denied - User {user.username} is not admin')
        return make_response(jsonify({'error': 'Only administrators can create users'}), 403)
    
    try:
        if not request.is_json: return make_response(jsonify({'error': 'Content-Type must be application/json'}), 415)
        data = request.get_json()
        if not data: return make_response(jsonify({'error': 'No JSON data provided'}), 400)
        
        username = data.get('username')
        password = data.get('password')
        
        # Validate is_admin is a boolean
        is_admin = data.get('is_admin')
        if is_admin is not None and not isinstance(is_admin, bool):
            return make_response(jsonify({
                'error': 'is_admin must be a boolean value (true/false), not a string',
                'received_type': str(type(is_admin)),
                'received_value': str(is_admin)
            }), 400)
        
        # Default to False if not provided
        is_admin = bool(is_admin) if is_admin is not None else False
        
        # print(f'DEBUG: Creating user {username} with admin={is_admin} (type: {type(is_admin)})')
        
        if not username or not password: return make_response(jsonify({'error': 'Username and password are required'}), 400)
        if username in users: return make_response(jsonify({'error': 'User already exists'}), 409)
        
        users[username] = User(username, hash_password(password), is_admin)
        # print(f'DEBUG: User {username} created successfully')
        return jsonify({'message': f'User {username} created successfully'})
    except Exception as e:
        # print(f'DEBUG: Error creating user: {str(e)}')
        return make_response(jsonify({'error': f'Exception: {str(e)}'}), 500)

@app.route(endpoint_prefix + 'users/delete/<username>', methods=['DELETE'])
@cross_origin()
@require_auth()
def delete_user(username):
    """Delete a user"""
    user = get_current_user()
    # print(f'DEBUG: Current user: {user.username}, is_admin: {user.is_admin}, type: {type(user.is_admin)}')
    
    # More explicit admin check with debug
    is_admin = bool(user.is_admin)  # Force boolean conversion
    # print(f'DEBUG: Admin check - is_admin value: {is_admin}, type: {type(is_admin)}')
    
    if not is_admin:
        # print(f'DEBUG: Access denied - User {user.username} is not admin')
        return make_response(jsonify({'error': 'Only administrators can delete users'}), 403)
    
    if username == 'admin': return make_response(jsonify({'error': 'Cannot delete admin user'}), 403)
    if username not in users: return make_response(jsonify({'error': 'User does not exist'}), 404)
    
    # print(f'DEBUG: Deleting user {username}')
    del users[username]
    # print(f'DEBUG: User {username} deleted successfully')
    return jsonify({'message': f'User {username} deleted successfully'})

@app.route(endpoint_prefix + 'users/list', methods=['GET'])
@cross_origin()
@require_auth()
def list_users():
    """List all users (admin only)"""
    user = get_current_user()
    if not user.is_admin:
        return make_response(jsonify({'error': 'Only administrators can list users'}), 403)
    
    try:
        # Create a list of user info, excluding sensitive data
        user_list = []
        for username, user_obj in users.items():
            user_info = {
                'username': username,
                'is_admin': user_obj.is_admin,
                'grids': list(user_obj.grids),
                'has_active_session': user_obj.session_token is not None,
                'session_expires': user_obj.session_expiry.isoformat() if user_obj.session_expiry else None
            }
            user_list.append(user_info)
        
        return jsonify({
            'message': 'User list retrieved successfully',
            'users': user_list,
            'total_users': len(user_list)
        })
    except Exception as e:
        return make_response(jsonify({'error': f'Exception: {str(e)}'}), 500)

# Helper function to check grid ownership
def check_grid_ownership(grid_name: str) -> bool:
    """Check if the current user owns the grid"""
    user = get_current_user()
    if not user: return False
    if user.is_admin: return True  # Admins can access all grids
    return grid_name in grids and grids[grid_name]['owner'] == user.username

@app.route(endpoint_prefix + 'createGrid')
@cross_origin()
@require_auth()
def gridCreate():
    user = get_current_user()
    # print(f'DEBUG: Creating grid for user {user.username}')
    if not user.can_create_grid(): return make_response(jsonify({'error': 'User not authorized to create grids'}), 403)
    r = request.args.get('rows', None)
    c = request.args.get('cols', None)
    name = request.args.get('name', 'Untitled')
    
    if name in grids:
        r, c = grids[name]['grid'].size().getx(), grids[name]['grid'].size().gety()
        return make_response(jsonify({f'result: grid already exists': {"name": name, 'rows':r, 'cols':c}}), 409)
    else:
        grid = bm.CellGrid(int(r), int(c))
        grids[name] = {
            'grid': grid,
            'owner': user.username
        }
        user.grids.add(name)  # Add grid to user's owned grids
        return jsonify({f'result: grid created by {user.username}': {"name": name, 'rows':r, 'cols':c}})

@app.route(endpoint_prefix + 'removeGrid')
@cross_origin()
@require_auth()
def gridRemove():
    user = get_current_user()
    name = request.args.get('name', 'Untitled')
    
    if not check_grid_ownership(name):
        return make_response(jsonify({'error': 'User not authorized to remove this grid'}), 403)
    
    if name in grids:
        grid = grids[name]['grid']
        r, c = grid.size().getx(), grid.size().gety()
        del grids[name]
        user.grids.discard(name)  # Remove grid from user's owned grids
        return jsonify({f'result: grid removed': {"name": name, 'rows':r, 'cols':c}})
    else: 
        return make_response(jsonify({f'result: grid does not exist': {"name": name}}), 404)

@app.route(endpoint_prefix + 'display')
@cross_origin()
@require_auth()
def grid_display():
    name = request.args.get('name', 'Untitled')
    if not check_grid_ownership(name):
        return make_response(jsonify({'error': 'User not authorized to access this grid'}), 403)
    
    if name in grids:
        grid = grids[name]['grid']
        text = str(hrr.show(grid, False))
        compressed = zlib.compress(text.encode('utf-8'))
        encoded = base64.b64encode(compressed).decode('utf-8')
        return jsonify({
            'result:': {
                'compressed': True,
                'data': encoded
            }
        })
    else: 
        return make_response(jsonify({f'result: grid does not exist': {"name": name}}), 404)

@app.route(endpoint_prefix + 'bandhaLiterals')
@cross_origin()
@require_auth()
def grid_bandhaLiterals():
    name = request.args.get('name', 'Untitled')
    if not check_grid_ownership(name):
        return make_response(jsonify({'error': 'User not authorized to access this grid'}), 403)
    
    if name in grids:
        grid = grids[name]['grid']
        return jsonify({'result': {'bandhas':grid.bandhaLiterals()}})
    else: 
        return make_response(jsonify({f'result: grid does not exist': {"name": name}}), 404)

@app.route(endpoint_prefix + 'bandhas')
@cross_origin()
@require_auth()
def grid_bandhas():
    name = request.args.get('name', 'Untitled')
    if not check_grid_ownership(name):
        return make_response(jsonify({'error': 'User not authorized to access this grid'}), 403)
    
    if name in grids:
        grid = grids[name]['grid']
        return jsonify({'result:': {'bandhas':str(grid.bandhas(bm.xy(0, 0)))}})
    else: 
        return make_response(jsonify({f'result: grid does not exist': {"name": name}}), 404)

@app.route(endpoint_prefix + 'it_fits_in')
@cross_origin()
@require_auth()
def grid_it_fits_in():
    name = request.args.get('name', 'Untitled')
    if not check_grid_ownership(name):
        return make_response(jsonify({'error': 'User not authorized to access this grid'}), 403)
    
    bandha = request.args.get('bandha', None)
    text = request.args.get('text', None)
    x, y = request.args.get('x', 0), request.args.get('y', 0)
    
    if name in grids:
        grid = grids[name]['grid']
        bandhaObject = grid.bandhas((bm.xy(int(x), int(y))))
        return jsonify({'result:': hrr.it_fits_in(grid, bandhaObject[bandha], text)})
    else: 
        return make_response(jsonify({f'result: grid does not exist': {"name": name}}), 404)

@app.route(endpoint_prefix + 'hide')
@cross_origin()
@require_auth()
def grid_hide():
    name = request.args.get('name', 'Untitled')
    if not check_grid_ownership(name):
        return make_response(jsonify({'error': 'User not authorized to access this grid'}), 403)
    
    bandha = request.args.get('bandha', None)
    text = request.args.get('text', None)
    x, y = request.args.get('x', 0), request.args.get('y', 0)
    
    if name in grids:
        grid = grids[name]['grid']
        bandhaObject = grid.bandhas((bm.xy(int(x), int(y))))
        return jsonify({'result:': hrr.hide_inplace(grid, bandhaObject[bandha], text)})
    else: 
        return make_response(jsonify({f'result: grid does not exist': {"name": name}}), 404)

@app.route(endpoint_prefix + 'reveal')
@cross_origin()
@require_auth()
def grid_reveal():
    name = request.args.get('name', 'Untitled')
    if not check_grid_ownership(name):
        return make_response(jsonify({'error': 'User not authorized to access this grid'}), 403)
    
    bandha = request.args.get('bandha', None)
    x, y, l = request.args.get('x', 0), request.args.get('y', 0), request.args.get('l', 25)
    
    if name in grids:
        grid = grids[name]['grid']
        bandhaObject = grid.bandhas((bm.xy(int(x), int(y))))
        return jsonify({'result:': hrr.reveal(grid, bandhaObject[bandha], int(l))})
    else: 
        return make_response(jsonify({f'result: grid does not exist': {"name": name}}), 404)

@app.route(endpoint_prefix + 'noisefill')
@cross_origin()
@require_auth()
def grid_noisefill():
    name = request.args.get('name', 'Untitled')
    if not check_grid_ownership(name):
        return make_response(jsonify({'error': 'User not authorized to access this grid'}), 403)
    
    if name in grids:
        grid = grids[name]['grid']
        text = str(hrr.export(grid))
        compressed = zlib.compress(text.encode('utf-8'))
        encoded = base64.b64encode(compressed).decode('utf-8')
        return jsonify({
            'result:': {
                'compressed': True,
                'data': encoded
            }
        })
    else: 
        return make_response(jsonify({f'result: grid does not exist': {"name": name}}), 404)

# Create a temporary directory for file operations
TEMP_DIR = os.path.join(tempfile.gettempdir(), 'ancient_indian_encryption')
os.makedirs(TEMP_DIR, exist_ok=True)

@app.route(endpoint_prefix + 'export')
@cross_origin()
@require_auth()
def grid_export():
    """Export grid to a downloadable file"""
    name = request.args.get('name', 'Untitled')
    if not check_grid_ownership(name):
        return make_response(jsonify({'error': 'User not authorized to access this grid'}), 403)
    
    if name in grids:
        grid = grids[name]['grid']
        # Create a temporary file
        temp_file = os.path.join(TEMP_DIR, f'{name}.txt')
        try:
            # Export the grid to the temporary file
            hrr.exportTofile(grid, temp_file, True)
            # Send the file to the client
            return send_file(
                temp_file,
                as_attachment=True,
                download_name=f'{name}.txt',
                mimetype='text/plain'
            )
        except Exception as e:
            return make_response(jsonify({'error': f'Failed to export grid: {str(e)}'}), 500)
        finally:
            # Clean up the temporary file
            try:
                os.remove(temp_file)
            except:
                pass
    else: 
        return make_response(jsonify({f'result: grid does not exist': {"name": name}}), 404)

@app.route(endpoint_prefix + 'import', methods=['POST'])
@cross_origin()
@require_auth()
def grid_import():
    """Import grid from an uploaded file"""
    user = get_current_user()
    name = request.args.get('name', 'Untitled')
    # if not check_grid_ownership(name): return make_response(jsonify({'error': 'User not authorized to access this grid'}), 403)
    if 'file' not in request.files: return make_response(jsonify({'error': 'No file provided'}), 400)
    file = request.files['file']
    if file.filename == '': return make_response(jsonify({'error': 'No file selected'}), 400)
    if not file.filename.endswith('.txt'): return make_response(jsonify({'error': 'Only .txt files are supported'}), 400)

    # Create a temporary file
    temp_file = os.path.join(TEMP_DIR, file.filename)
    try:
        # Save the uploaded file
        file.save(temp_file)
        if name not in grids:
            grid = hrr.importFromfile(temp_file)
            if grid:
                grids[name] = {
                    'grid': grid,
                    'owner': user.username
                }
                user.grids.add(name)
                return jsonify({'result:': {'imported': str(name)}})
            else:
                return make_response(jsonify({'error': 'Failed to import grid: Invalid file format'}), 400)
        else:
            return make_response(jsonify({f'result: grid exists': {"name": name}}), 409)
    except Exception as e:
        return make_response(jsonify({'error': f'Failed to import grid: {str(e)}'}), 500)
    finally:
        # Clean up the temporary file
        try:
            os.remove(temp_file)
        except:
            pass

@app.route(endpoint_prefix + 'gridlist')
@cross_origin()
@require_auth()
def grid_list():
    user = get_current_user()
    if user.is_admin:
        # Admin can see all grids
        grid_list = [f'name: {k} size:{v["grid"].size()} owner:{v["owner"]}' for k, v in grids.items()]
    else:
        # Regular users can only see their grids
        grid_list = [f'name: {k} size:{v["grid"].size()}' for k, v in grids.items() if v["owner"] == user.username]
    
    return jsonify({'result:': grid_list})

@app.route(endpoint_prefix + 'clear')
@cross_origin()
@require_auth()
def gridClear():
    name = request.args.get('name', 'Untitled')
    if not check_grid_ownership(name):
        return make_response(jsonify({'error': 'User not authorized to access this grid'}), 403)
    
    if name in grids:
        grid = grids[name]['grid']
        grid.clearAll()
        return jsonify({'message': f'Grid {name} cleared successfully'})
    else:
        return make_response(jsonify({f'result: grid does not exist': {"name": name}}), 404)

@app.route(endpoint_prefix + 'users/change-password', methods=['POST'])
@cross_origin()
@require_auth()
def change_password():
    """Change user's password"""
    user = get_current_user()
    try:
        if not request.is_json: return make_response(jsonify({'error': 'Content-Type must be application/json'}), 415)
        data = request.get_json()
        if not data: return make_response(jsonify({'error': 'No JSON data provided'}), 400)
        
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return make_response(jsonify({'error': 'Current password and new password are required'}), 400)
        
        if not user.verify_password(current_password):
            return make_response(jsonify({'error': 'Current password is incorrect'}), 401)
        
        user.password_hash = hash_password(new_password)
        return jsonify({'message': 'Password changed successfully'})
    except Exception as e:
        return make_response(jsonify({'error': f'Exception: {str(e)}'}), 500)

if __name__ == '__main__':
    args = parse_args()
    
    if args.auto_port:
        port = find_free_port()
        if port is None:
            print("Error: No available ports found")
            exit(1)
        print(f"Using automatically found port: {port}")
    else:
        port = args.port or 5001
    
    print(f"Starting server on {args.host}:{port}")
    app.run(debug=True, host=args.host, port=port)