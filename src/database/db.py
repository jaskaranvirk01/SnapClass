from src.database.config import supabase
import bcrypt


def hash_pass(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_pass(incoming_pass, existing_pass):
    return bcrypt.checkpw(incoming_pass.encode(), existing_pass.encode())


def check_teacher_exists(username):
    response = supabase.table('teachers').select(
        'username').eq('username', username).execute()

    return len(response.data) > 0


def create_teacher(username, password, name):
    data = {
        'username': username,
        'password': hash_pass(password),
        'name': name
    }
    response = supabase.table('teachers').insert(data).execute()
    return response.data


def teacher_login(username, password):
    response = supabase.table('teachers').select(
        '*').eq('username', username).execute()

    if response.data:
        teacher = response.data[0]
        if check_pass(password, teacher['password']):
            return teacher

    return None


def get_all_students():
    response = supabase.table("students").select("*").execute()
    return response.data


def create_student(new_name, face_emb=None, voice_emb=None):
    data = {
        "name": new_name,
        'face_embedding': face_emb,
        'voice_embedding': voice_emb
    }

    response = supabase.table("students").insert(data).execute()

    return response.data
