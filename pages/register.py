import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

st.title("Register New User")

with open('D:\KULS\SEMESTER 7\KEAMANAN PEMROGRAMAN LANJUTAN\st\config.yml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

try:
    if authenticator.register_user('Register user', preauthorization=False):
        with open('D:\KULS\SEMESTER 7\KEAMANAN PEMROGRAMAN LANJUTAN\st\config.yml', 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
            st.success('User registered successfully')
except Exception as e:
    st.error(e)