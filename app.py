import streamlit as st
import os
from backend.rag import search_documents
from backend.chatbot import get_chat_response
from backend.database import (
    initialize_database,
    save_chat,
    get_chat_history
)
from backend.rag import (search_documents_with_scores)
from backend.rag import (
    create_vector_store,
    search_documents
)
from backend.ticket import (
    create_ticket,
    get_tickets
)
from backend.image_analysis import (
    analyze_image,
    analyze_and_search
)
from backend.database import (get_total_chats)

from backend.ticket import (get_open_ticket_count)
# Initialize database
initialize_database()

def load_css():

    with open(
        "assets/css/style.css"
    ) as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )
def get_confidence_badge(confidence):

    confidence = confidence.lower()

    if confidence == "high":

        return """
        <span class='conf-high'>
        HIGH
        </span>
        """

    elif confidence == "medium":

        return """
        <span class='conf-medium'>
        MEDIUM
        </span>
        """

    return """
    <span class='conf-low'>
    LOW
    </span>
    """
# Session state for current chat
if "messages" not in st.session_state:
    st.session_state.messages = []
total_chats = get_total_chats()

open_tickets = get_open_ticket_count()

pdf_count = len(
    [
        f
        for f in os.listdir("data/pdfs")
        if f.endswith(".pdf")
    ]
)
st.set_page_config(
    page_title="SmartAssist AI",
    page_icon="🤖",
    layout="wide"
)
load_css()
st.markdown(
    f"""
    <div class='glass-card'>

    <h1>🤖 SmartAssist AI</h1>

    <h3>
    Enterprise Helpdesk Support Platform
    </h3>

    <br>

    <h4>
    💬 {total_chats} Chats
    &nbsp;&nbsp;&nbsp;

    🎫 {open_tickets} Tickets
    &nbsp;&nbsp;&nbsp;

    📄 {pdf_count} PDFs
    </h4>

    <br>

    <p>
    AI-Powered Support • RAG Search • Ticket Escalation • Screenshot Analysis
    </p>

    </div>
    """,
    unsafe_allow_html=True
)

st.subheader("Enterprise Helpdesk Support Chat Bot")

with st.sidebar:

    if st.button("🗑 Clear Current Chat"):
        st.session_state.messages = []
        st.rerun()

    st.header("📊 SmartAssist")

    st.metric(
        "Messages This Session",
        len(st.session_state.messages)
    )

    st.divider()
    st.subheader("📊 Analytics")

    total_chats = get_total_chats()

    open_tickets = get_open_ticket_count()

    pdf_count = len(
    [
        file
        for file in os.listdir(
            "data/pdfs"
        )
        if file.endswith(".pdf")
    ]
)

    st.markdown(
    f"""
    <div class='glass-card'>
    <h3>💬 Chats</h3>
    <h1>{total_chats}</h1>
    </div>
    """,
    unsafe_allow_html=True
)

    st.markdown(
    f"""
    <div class='glass-card'>
    <h3>🎫 Tickets</h3>
    <h1>{open_tickets}</h1>
    </div>
    """,
    unsafe_allow_html=True
)

    st.markdown(
    f"""
    <div class='glass-card'>
    <h3>📄 PDFs</h3>
    <h1>{pdf_count}</h1>
    </div>
    """,
    unsafe_allow_html=True
)

    st.divider()
    

    st.subheader("🎫 Tickets")

    tickets = get_tickets()

    for ticket in tickets[:10]:

        with st.expander(
        f"🎫 Ticket #{ticket[0]}"
    ):

            st.write(
            f"Status: {ticket[2]}"
        )

            st.write(
            f"Issue: {ticket[1]}"
        )

            st.write(
            f"Created: {ticket[3]}"
        )

    
    
    st.subheader(
    "🖼 Screenshot Analysis"
)
    uploaded_image = st.file_uploader(
    "Upload Screenshot",
    type=[
        "png",
        "jpg",
        "jpeg"
    ]
)
    if uploaded_image:
        image_path = (
        f"uploads/{uploaded_image.name}"
    )
        with open(
        image_path,
        "wb"
    ) as f:
            f.write(
            uploaded_image.getbuffer()
        )
        st.image(
        image_path,
        caption="Uploaded Screenshot"
    )
        if st.button(
        "🔍 Analyze Screenshot"
    ):
            with st.spinner(
            "Analyzing..."
        ):
                image_result = analyze_and_search(
                image_path
            )
            st.session_state.messages.append({
            "role": "user",
            "content":
            "[Uploaded Screenshot]"
        })

            st.session_state.messages.append({
            "role": "assistant",
            "content": image_result
        })

            st.rerun()

    st.subheader("📄 Upload PDFs")

    uploaded_files = st.file_uploader(
        "Knowledge Base PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )
    
    if uploaded_files:

        for file in uploaded_files:

            save_path = (
                f"data/pdfs/{file.name}"
            )

            with open(
                save_path,
                "wb"
            ) as f:

                f.write(
                    file.getbuffer()
                )

        st.success(
            "PDFs Uploaded"
        )

    if st.button(
        "⚡ Build Knowledge Base"
    ):

        with st.spinner(
            "Processing PDFs..."
        ):

            count = create_vector_store()

        st.success(
            f"{count} chunks indexed."
        )

    st.divider()

    st.header("📜 Recent Chats")

    history = get_chat_history()

    for chat in history:

        user_msg = chat[0]
        timestamp = chat[2]

        st.write(
            f"🕒 {timestamp}"
        )

        st.caption(
            user_msg[:50]
        )

        st.divider()
    st.divider()

    st.subheader(
    "📖 Retrieved Context"
)

    docs = st.session_state.get(
    "last_docs",
    []
)

    for doc in docs:

        with st.expander(
         doc["source"]
    ):

            st.write(
                doc["text"]
        )

            st.caption(
            f"Page: {doc['page']}"
        )

# Display current session messages
for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class='user-bubble'>
            {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class='assistant-bubble'>

            <strong>🤖 SmartAssist</strong>

            </div>

            
            """,
            unsafe_allow_html=True
    )
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input(
    "Ask me anything..."
)

# Handle messages
if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    retrieved_chunks = []

    try:

        retrieved_chunks = search_documents(
            user_input
        )

    except:

        pass
    retrieved_docs = (
        search_documents_with_scores(
            user_input
    )
)

    st.session_state.last_docs = (
        retrieved_docs
)
    with st.chat_message("user"):
        st.markdown(user_input)

        

    with st.chat_message("assistant"):

        if retrieved_chunks:

            with st.expander(
    "Retrieved Knowledge"
):

                for chunk in retrieved_chunks:

                    st.markdown(
                         f"**Source:** {chunk['source']} "
                         f"(Page {chunk['page']})")

                    st.write(
            chunk["text"][:500]
        )

                    st.divider()

    with st.spinner("Thinking..."):
        
        response = get_chat_response(
            user_input
        )
        if (
    "could not find" in response.lower()
):
            ticket_id = create_ticket(
                 user_input
             )

            response += (
                f"\n\n🎫 Ticket Created: "
                 f"#{ticket_id}"
                 )

        st.markdown(response)
        sources = []

        docs = st.session_state.get(
    "last_docs",
    []
)
        for doc in docs:
            if doc["source"] not in sources:

                sources.append(
                    doc["source"]
        )
        chips_html = ""
        for source in sources:
            clean_name = source.replace(
        ".pdf",
        ""
    )
            chips_html += f"""
            <span class='source-chip'>
            {clean_name}
            </span>
            """
        st.markdown(
        chips_html,
        unsafe_allow_html=True
)
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
    save_chat(
        user_input,
        response
    )
    st.rerun()

