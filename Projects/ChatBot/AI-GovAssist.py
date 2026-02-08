import streamlit as st
import uuid
import random

# - Page Setup 

st.set_page_config(page_title="E-Governance Chatbot", page_icon="🤖")
st.title("🤖 E-Governance Chatbot")
st.caption("AI-based Citizen Support System")

# -Session State 

if "messages" not in st.session_state:
    st.session_state.messages = []

if "complaints" not in st.session_state:
    st.session_state.complaints = {}

if "identity" not in st.session_state:
    st.session_state.identity = {}

if "documents" not in st.session_state:
    st.session_state.documents = {}

# -Sidebar Menu 

menu = st.sidebar.radio("Choose Service", [
    "Chat Assistant",
    "Register Digital Identity",
    "Upload Documents",
    "View My Profile"
])

# - Register Digital Identity -

if menu == "Register Digital Identity":

    st.subheader("🆔 Digital Identity Registration")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Mobile Number")

    if st.button("Register"):

        if name.strip() == "" or email.strip() == "" or phone.strip() == "":
            st.warning("⚠ Please fill all details")

        else:
            did = str(uuid.uuid4())[:8]

            st.session_state.identity = {
                "DID": did,
                "Name": name,
                "Email": email,
                "Phone": phone
            }

            st.success("✅ Digital Identity Created Successfully")
            st.write("Your Digital ID:", did)

# - Upload Documents 

if menu == "Upload Documents":

    st.subheader("📄 Document Upload & Verification")

    if not st.session_state.identity:
        st.warning("⚠ Please register your digital identity first.")
    else:
        doc_type = st.selectbox("Select Document Type", [
            "Aadhaar Card",
            "PAN Card",
            "Driving License",
            "Passport"
        ])

        uploaded_file = st.file_uploader("Upload Document", type=["jpg","png","pdf"])

        if st.button("Submit Document"):

            if uploaded_file is None:
                st.warning("⚠ Please upload a document")
            else:
                trust_score = random.randint(55, 98)

                if trust_score >= 80:
                    status = "Verified"
                elif trust_score >= 50:
                    status = "Partially Verified"
                else:
                    status = "Rejected"

                st.session_state.documents[doc_type] = {
                    "filename": uploaded_file.name,
                    "status": status,
                    "trust_score": trust_score
                }

                st.success("✅ Document Uploaded Successfully")
                st.write("Verification Status:", status)
                st.write("Trust Score:", trust_score)

# - View Profile 

if menu == "View My Profile":

    st.subheader("👤 My Profile")

    if st.session_state.identity:
        st.json(st.session_state.identity)

        if st.session_state.documents:
            st.subheader("📑 Uploaded Documents")
            st.json(st.session_state.documents)
        else:
            st.info("No documents uploaded yet")

    else:
        st.warning("No digital identity found")

# - Chat Assistant

if menu == "Chat Assistant":

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    user_input = st.chat_input("Type your problem or question...")

    if user_input:

        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)

        text = user_input.lower()
        reply = ""

        # -Track Complaint 

        if "track" in text or "status" in text:

            cid = text[-6:].upper()

            if cid in st.session_state.complaints:
                data = st.session_state.complaints[cid]
                reply = f"""📌 Complaint ID: **{cid}**

📍 Status: **{data['status']}**
⚡ Priority: **{data['priority']}**
"""
            else:
                reply = "❌ Invalid Complaint ID"

        # - Register Complaint 

        elif any(word in text for word in
                 ["problem","issue","complaint","leak","broken","not working",
                  "delay","garbage","danger","accident","gas","fire","shock","emergency"]):

            cid = str(uuid.uuid4())[:6].upper()

            if any(word in text for word in ["danger","accident","electric","gas","fire","shock","emergency"]):
                priority = "High"
            elif any(word in text for word in ["leak","overflow","sewage","broken","not working"]):
                priority = "Medium"
            else:
                priority = "Low"

            st.session_state.complaints[cid] = {
                "status": "Registered",
                "priority": priority
            }

            reply = f"""✅ Complaint Registered Successfully

🆔 Complaint ID: **{cid}**
📍 Status: **Registered**
⚡ Priority: **{priority}**

Use:
Track {cid}
"""

        # - Document Help -

        elif "upload document" in text or "document upload" in text:

            reply = """📄 How to Upload Documents:

1. Go to left sidebar.
2. Select **Upload Documents**.
3. Choose document type.
4. Upload JPG / PNG / PDF.
5. Click **Submit Document**.

Your document will be verified and trust score will be generated.
"""

        elif "trust score" in text:

            reply = """🔐 Trust Score Meaning:

80–100 : Fully Verified  
50–79  : Partially Verified  
Below 50 : Rejected
"""

        # - Digital Identity Help 

        elif "register digital identity" in text or "create digital identity" in text:

            reply = """🆔 How to Register Digital Identity:

1. Open sidebar menu.
2. Select **Register Digital Identity**.
3. Enter Name, Email, Mobile.
4. Click Register.
"""

        # - FAQ 

        elif "document" in text:
            reply = "Required documents: Aadhaar, PAN, Driving License, Passport."

        elif "verification" in text:
            reply = "Verification usually takes 24–72 hours."

        elif "digital identity" in text:
            reply = "Digital identity provides secure access to online government services."

        else:
            reply = "Please describe your problem clearly or ask for help."

        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)
