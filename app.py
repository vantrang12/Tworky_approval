# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import User, Organization, Submission
from config import SECRET_KEY
import os

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Decorator kiểm tra đăng nhập
def login_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# Decorator kiểm tra quyền admin
def admin_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user = User.get_by_id(session['user_id'])
        if user['role'] != 'admin':
            flash('Bạn không có quyền truy cập trang này', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.get_by_username(username)
        
        if user and user['password'] == password:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            session['role_approve'] = user['role_approve']
            session['organization_id'] = user['organization_id']
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Tên đăng nhập hoặc mật khẩu không đúng', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Đã đăng xuất', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    user = User.get_by_id(session['user_id'])
    return render_template('dashboard.html', user=user)

# ============ QUẢN LÝ NGƯỜI DÙNG ============
@app.route('/users')
@admin_required
def users():
    all_users = User.get_all()
    return render_template('users.html', users=all_users)

@app.route('/users/add', methods=['GET', 'POST'])
@admin_required
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        fullname = request.form['fullname']
        description = request.form['description']
        organization_id = request.form['organization_id'] if request.form['organization_id'] else None
        role = request.form['role']
        role_approve = request.form['role_approve']
        
        User.create(username, password, fullname, description, organization_id, role, role_approve)
        flash('Thêm người dùng thành công', 'success')
        return redirect(url_for('users'))
    
    organizations = Organization.get_all()
    return render_template('user_detail.html', user=None, organizations=organizations, action='add')

@app.route('/users/<int:user_id>')
@admin_required
def user_detail(user_id):
    user = User.get_by_id(user_id)
    organizations = Organization.get_all()
    return render_template('user_detail.html', user=user, organizations=organizations, action='view')

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        fullname = request.form['fullname']
        description = request.form['description']
        organization_id = request.form['organization_id'] if request.form['organization_id'] else None
        role = request.form['role']
        role_approve = request.form['role_approve']
        
        User.update(user_id, username, password, fullname, description, organization_id, role, role_approve)
        flash('Cập nhật người dùng thành công', 'success')
        return redirect(url_for('users'))
    
    user = User.get_by_id(user_id)
    organizations = Organization.get_all()
    return render_template('user_detail.html', user=user, organizations=organizations, action='edit')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    User.delete(user_id)
    flash('Xóa người dùng thành công', 'success')
    return redirect(url_for('users'))

# ============ QUẢN LÝ PHÒNG/BAN ============
@app.route('/organizations')
@admin_required
def organizations():
    all_orgs = Organization.get_all()
    return render_template('organizations.html', organizations=all_orgs)

@app.route('/organizations/add', methods=['POST'])
@admin_required
def add_organization():
    name = request.form['name']
    Organization.create(name)
    flash('Thêm phòng/ban thành công', 'success')
    return redirect(url_for('organizations'))

@app.route('/organizations/<int:org_id>/edit', methods=['POST'])
@admin_required
def edit_organization(org_id):
    name = request.form['name']
    Organization.update(org_id, name)
    flash('Cập nhật phòng/ban thành công', 'success')
    return redirect(url_for('organizations'))

@app.route('/organizations/<int:org_id>/delete', methods=['POST'])
@admin_required
def delete_organization(org_id):
    Organization.delete(org_id)
    flash('Xóa phòng/ban thành công', 'success')
    return redirect(url_for('organizations'))

# ============ QUẢN LÝ PHIẾU ĐỀ XUẤT ============
@app.route('/submissions')
@login_required
def submissions():
    user_id = session['user_id']
    organization_id = session['organization_id']
    all_submissions = Submission.get_by_user(user_id, organization_id)
    return render_template('submissions.html', submissions=all_submissions)

@app.route('/submissions/add', methods=['GET', 'POST'])
@login_required
def add_submission():
    if request.method == 'POST':
        organization_id = request.form['organization_id']
        content = request.form['content']
        created_by_id = session['user_id']
        
        Submission.create(organization_id, content, created_by_id)
        flash('Tạo phiếu đề xuất thành công', 'success')
        return redirect(url_for('submissions'))
    
    organizations = Organization.get_all()
    return render_template('submission_detail.html', submission=None, organizations=organizations, action='add')

@app.route('/submissions/<int:submission_id>')
@login_required
def submission_detail(submission_id):
    submission = Submission.get_by_id(submission_id)
    organizations = Organization.get_all()
    return render_template('submission_detail.html', submission=submission, organizations=organizations, action='view')

@app.route('/submissions/<int:submission_id>/approve', methods=['POST'])
@login_required
def approve_submission(submission_id):
    if session['role_approve'] != 'approver':
        flash('Bạn không có quyền phê duyệt', 'error')
        return redirect(url_for('submissions'))
    
    Submission.update_status(submission_id, 'Đã phê duyệt')
    flash('Đã phê duyệt phiếu đề xuất', 'success')
    return redirect(url_for('submissions'))

@app.route('/submissions/<int:submission_id>/reject', methods=['POST'])
@login_required
def reject_submission(submission_id):
    if session['role_approve'] != 'approver':
        flash('Bạn không có quyền từ chối', 'error')
        return redirect(url_for('submissions'))
    
    Submission.update_status(submission_id, 'Đã từ chối')
    flash('Đã từ chối phiếu đề xuất', 'success')
    return redirect(url_for('submissions'))

if __name__ == '__main__':
    # Lấy port từ biến môi trường (cho Render) hoặc dùng 5000 (cho local)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)