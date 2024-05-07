import streamlit as st
from msal_streamlit_t2 import msal_authentication



login_token = msal_authentication(
        auth={
            "clientId": "b41588cc-a34a-4324-8327-1c1412300bc4",
            "authority": "https://login.microsoftonline.com/76431109-ff89-42c2-8781-a07ca07a2d57",
            "redirectUri": "/",
            "postLogoutRedirectUri": "/",
        },  # Corresponds to the 'auth' configuration for an MSAL Instance
        cache={
            "cacheLocation": 'localStorage',
            "storeAuthStateInCookie": True,
            "allowRedirectInIframe": True,
        },  # Corresponds to the 'cache' configuration for an MSAL Instance
        login_request={
            "scopes": [f"""{"b41588cc-a34a-4324-8327-1c1412300bc4"}/data.read"""],
        },  # Optional
        logout_request={},  # Optional
        class_name="css_button_class_selector",  # Optional, defaults to None. Corresponds to HTML class.
        html_id="html_id_for_button",  # Optional, defaults to None. Corresponds to HTML id.
        key="yo",  # Optional if only a single instance is needed
    )


st.write(login_token)

