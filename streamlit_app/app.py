import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Product Manager", layout="centered")

if 'token' not in st.session_state:
    st.session_state['token'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None

# --- Authentication ---
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        response = requests.post(f"{API_URL}/token", data={"username": username, "password": password})
        if response.status_code == 200:
            token = response.json()["access_token"]
            st.session_state['token'] = token
            st.session_state['username'] = username
            st.success("Logged in!")
            st.session_state['menu'] = "Products"
            st.rerun()
        else:
            st.error("Login failed. Check your credentials.")

# --- Register ---
def register():
    st.title("Register")
    username = st.text_input("New Username")
    password = st.text_input("New Password", type="password")
    if st.button("Register"):
        response = requests.post(f"{API_URL}/register", json={"username": username, "password": password})
        if response.status_code == 200:
            st.success("Registration successful! Please log in.")
        else:
            st.error(response.json().get("detail", "Registration failed."))

# --- Product CRUD ---
def product_crud():
    st.title("Product Manager")
    token = st.session_state['token']
    headers = {"Authorization": f"Bearer {token}"}

    # List products
    st.header("Your Products")
    resp = requests.get(f"{API_URL}/products/", headers=headers)
    if resp.status_code == 200:
        products = resp.json()
        for prod in products:
            with st.expander(prod['name']):
                st.write(f"Description: {prod['description']}")
                st.write(f"Image URL: {prod.get('image_url', '')}")
                if st.button("Delete", key=f"del_{prod['id']}"):
                    del_resp = requests.delete(f"{API_URL}/products/{prod['id']}", headers=headers)
                    if del_resp.status_code == 200:
                        st.success("Deleted!")
                        st.rerun()
                    else:
                        st.error("Delete failed.")
                if st.button("Edit", key=f"edit_{prod['id']}"):
                    st.session_state['edit_id'] = prod['id']
                    st.session_state['edit_name'] = prod['name']
                    st.session_state['edit_desc'] = prod['description']
                    st.session_state['edit_img'] = prod.get('image_url', '')
                    st.rerun()
    else:
        st.error("Failed to fetch products.")

    # Add product
    st.header("Add Product")
    name = st.text_input("Product Name")
    description = st.text_area("Description")
    image_url = st.text_input("Image URL")
    if st.button("Add Product"):
        data = {"name": name, "description": description, "image_url": image_url}
        resp = requests.post(f"{API_URL}/products/", json=data, headers=headers)
        if resp.status_code == 200:
            st.success("Product added!")
            st.rerun()
        else:
            st.error("Failed to add product.")

    # Edit product
    if 'edit_id' in st.session_state:
        st.header(f"Edit Product {st.session_state['edit_id']}")
        new_name = st.text_input("Edit Name", value=st.session_state['edit_name'])
        new_desc = st.text_area("Edit Description", value=st.session_state['edit_desc'])
        new_img = st.text_input("Edit Image URL", value=st.session_state['edit_img'])
        if st.button("Update Product"):
            data = {"name": new_name, "description": new_desc, "image_url": new_img}
            resp = requests.put(f"{API_URL}/products/{st.session_state['edit_id']}", json=data, headers=headers)
            if resp.status_code == 200:
                st.success("Product updated!")
                del st.session_state['edit_id']
                st.rerun()
            else:
                st.error("Failed to update product.")
        if st.button("Cancel Edit"):
            del st.session_state['edit_id']
            st.rerun()

# --- Main App Logic ---
menu = ["Login", "Register", "Products"]
if 'menu' not in st.session_state:
    st.session_state['menu'] = menu[0]
choice = st.sidebar.selectbox("Menu", menu, index=menu.index(st.session_state['menu']))
st.session_state['menu'] = choice

if choice == "Login":
    login()
elif choice == "Register":
    register()
elif choice == "Products":
    if st.session_state['token']:
        product_crud()
    else:
        st.warning("Please log in first.")
        login() 