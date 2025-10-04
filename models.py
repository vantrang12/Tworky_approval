# models.py
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

class User:
    @staticmethod
    def get_by_username(username):
        response = supabase.table('users').select('*').eq('username', username).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def get_by_id(user_id):
        response = supabase.table('users').select('*').eq('id', user_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def get_all():
        response = supabase.table('users').select('*, organizations(name)').execute()
        return response.data
    
    @staticmethod
    def create(username, password, fullname, description, organization_id, role, role_approve):
        data = {
            'username': username,
            'password': password,
            'fullname': fullname,
            'description': description,
            'organization_id': organization_id,
            'role': role,
            'role_approve': role_approve
        }
        response = supabase.table('users').insert(data).execute()
        return response.data
    
    @staticmethod
    def update(user_id, username, password, fullname, description, organization_id, role, role_approve):
        data = {
            'username': username,
            'password': password,
            'fullname': fullname,
            'description': description,
            'organization_id': organization_id,
            'role': role,
            'role_approve': role_approve
        }
        response = supabase.table('users').update(data).eq('id', user_id).execute()
        return response.data
    
    @staticmethod
    def delete(user_id):
        response = supabase.table('users').delete().eq('id', user_id).execute()
        return response.data

class Organization:
    @staticmethod
    def get_all():
        response = supabase.table('organizations').select('*').execute()
        return response.data
    
    @staticmethod
    def get_by_id(org_id):
        response = supabase.table('organizations').select('*').eq('id', org_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def create(name):
        data = {'name': name}
        response = supabase.table('organizations').insert(data).execute()
        return response.data
    
    @staticmethod
    def update(org_id, name):
        data = {'name': name}
        response = supabase.table('organizations').update(data).eq('id', org_id).execute()
        return response.data
    
    @staticmethod
    def delete(org_id):
        response = supabase.table('organizations').delete().eq('id', org_id).execute()
        return response.data

class Submission:
    @staticmethod
    def get_by_user(user_id, organization_id):
        # Lấy phiếu do user tạo hoặc phiếu gửi đến organization của user
        response = supabase.table('submissions').select('*, organizations(name), users(fullname)').or_(f'created_by_id.eq.{user_id},organization_id.eq.{organization_id}').order('created_at', desc=True).execute()
        return response.data
    
    @staticmethod
    def get_by_id(submission_id):
        response = supabase.table('submissions').select('*, organizations(name), users(fullname)').eq('id', submission_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def create(organization_id, content, created_by_id):
        data = {
            'organization_id': organization_id,
            'content': content,
            'status': 'Chờ phê duyệt',
            'created_by_id': created_by_id
        }
        response = supabase.table('submissions').insert(data).execute()
        return response.data
    
    @staticmethod
    def update_status(submission_id, status):
        data = {'status': status}
        response = supabase.table('submissions').update(data).eq('id', submission_id).execute()
        return response.data