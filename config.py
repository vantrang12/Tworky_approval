# config.py
import os

# Lấy thông tin từ biến môi trường (cho Render) hoặc giá trị mặc định (cho local)
SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://sglmtibibkqvqqdtlxkv.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNnbG10aWJpYmtxdnFxZHRseGt2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk1ODA0MjAsImV4cCI6MjA3NTE1NjQyMH0.Yelo9-XCs5uzThvh8l7mz5ONq3nS8ugyjl5EXN-hc90')
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-thiss')