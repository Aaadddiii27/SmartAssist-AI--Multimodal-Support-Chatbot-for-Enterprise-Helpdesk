import streamlit as st

from backend.database import (
    get_total_chats
)

from backend.ticket import (
    get_tickets,
    get_open_ticket_count
)

st.title(
    "📊 SmartAssist Dashboard"
)

st.metric(
    "Total Chats",
    get_total_chats()
)

st.metric(
    "Open Tickets",
    get_open_ticket_count()
)

st.subheader(
    "Recent Tickets"
)

tickets = get_tickets()

for ticket in tickets[:20]:

    st.write(
        f"Ticket #{ticket[0]}"
    )

    st.write(
        ticket[1]
    )

    st.write(
        ticket[2]
    )

    st.divider()