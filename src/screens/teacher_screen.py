import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.database.db import check_teacher_exists, create_teacher, teacher_login, get_teacher_subjects
from src.components.dialog_create_subject import create_subject_dialog
from src.components.subject_card import subject_card
from src.components.share_subject_dialog import share_subject_dialog


def teacher_screen():
    style_background_dashboard()
    style_base_layout()
    if 'teacher_data' in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type == 'login':
        teacher_screen_login()
    elif st.session_state.teacher_login_type == 'register':
        teacher_screen_register()


def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Logout!", type='secondary',
                     key='loginbackbtn', shortcut='control+backspace'):
            st.session_state['is_logged_in'] = False
            del st.session_state.teacher_data
            st.rerun()
    st.subheader(f"""Welcome, {teacher_data['name']}""")

    st.space()
    st.space()
    if 'current_teacher_tab' not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'
    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        type1 = 'primary' if st.session_state.current_teacher_tab == 'take_attendance' else 'tertiary'
        if st.button('Take Attendance', width='stretch', type=type1,
                     icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()

    with tab2:
        type2 = 'primary' if st.session_state.current_teacher_tab == 'manage_subjects' else 'tertiary'
        if st.button('Manage Subjects', width='stretch', type=type2,
                     icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()

    with tab3:
        type3 = 'primary' if st.session_state.current_teacher_tab == 'attendance_records' else 'tertiary'
        if st.button('Attendance Records', width='stretch', type=type3,
                     icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun()

    st.divider()

    if st.session_state.current_teacher_tab == 'take_attendance':
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab == 'manage_subjects':
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab == 'attendance_records':
        teacher_tab_attendance_records()

    footer_dashboard()


def teacher_tab_take_attendance():
    st.header("Take AI Attendance")


def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']
    col1, col2 = st.columns(2, vertical_alignment='center')
    with col1:
        st.header("Manage Subjects")
    with col2:
        if st.button("Create New Subject", width='stretch', ):
            create_subject_dialog(teacher_id)

    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ('🧑‍🤝‍🧑', 'Students', sub['total_students']),
                ('⏰', 'Classes', sub['total_classes'])
            ]

            def share_btn():
                if st.button(f'Share Code : {sub['name']}', key=f'share_{sub['subject_code']}', icon=':material/share:'):
                    share_subject_dialog(sub['name'], sub['subject_code'])
                st.space()
            subject_card(
                name=sub['name'], code=sub['subject_code'], section=sub['section'], stats=stats, footer_callback=share_btn)
    else:
        st.info('No Subject Found!. Create A new one')


def teacher_tab_attendance_records():
    st.header("Attendance Records")


def login_teacher(username, password):
    if not username or not password:
        return False

    teacher = teacher_login(username, password)

    if teacher:
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True

    return False


def teacher_screen_login():
    style_background_dashboard()
    style_base_layout()
    col1, col2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with col1:
        header_dashboard()

    with col2:
        if st.button('Go back to Home', type='secondary', key='loginbackbtn', shortcut='control+backspace'):
            st.session_state['login_type'] = None
            st.rerun()

    st.header("Login using password")
    st.space()
    st.space()
    teacher_username = st.text_input(
        "Enter username", placeholder='jaskaransingh')

    teacher_password = st.text_input(
        "Enter password", type='password', placeholder='Enter your password')

    st.divider()

    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button('Login', type='secondary', icon=':material/passkey:',
                     shortcut='control+enter', width='stretch'):
            if login_teacher(teacher_username, teacher_password):
                st.toast("Welcome Back", icon="👋🏻")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid Credentials")
    with btnc2:
        if st.button('Register Instead', type='primary',
                     icon=':material/passkey:', width='stretch'):
            st.session_state['teacher_login_type'] = 'register'
            st.rerun()
    footer_dashboard()


def register_teacher(teacher_username, teacher_name, teacher_password, teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_password or not teacher_pass_confirm:
        return False, 'All Fields are Required!'

    if check_teacher_exists(teacher_username):
        return False, 'Username already taken!'

    if teacher_password != teacher_pass_confirm:
        return False, 'Passwords does not match'

    try:
        create_teacher(username=teacher_username,
                       password=teacher_password, name=teacher_name)
        return True, 'Account Created Sucessfully! Login Now'

    except Exception as e:
        return False, 'Unexpected Error'


def teacher_screen_register():
    col1, col2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with col1:
        header_dashboard()

    with col2:
        if st.button('Go back to Home', type='secondary', key='loginbackbtn', shortcut='control+backspace'):
            st.session_state['login_type'] = None
            st.rerun()

    st.header("Register your Teacher Profile")
    st.space()
    st.space()
    teacher_username = st.text_input(
        "Enter username", placeholder='jaskaransingh')

    teacher_name = st.text_input(
        "Enter Name", placeholder='Jaskaran Singh')

    teacher_password = st.text_input(
        "Enter password", type='password', placeholder='Enter your password')

    teacher_pass_confirm = st.text_input(
        "Confirm your password", type='password', placeholder='Re-enter your password')

    st.divider()

    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button('Register Now', type='secondary', icon=':material/passkey:',
                     shortcut='control+enter', width='stretch'):

            success, message = register_teacher(
                teacher_username, teacher_name, teacher_password, teacher_pass_confirm)

            if success:
                st.success(message)
                import time
                time.sleep(1)
                st.session_state.teacher_login_type = 'login'
                st.rerun()
            else:
                st.error(message)
    with btnc2:
        if st.button('Login Instead', type='primary',
                     icon=':material/passkey:', width='stretch'):
            st.session_state.teacher_login_type = 'login'
            st.rerun()
    footer_dashboard()
