import streamlit as st

st.title("Ausschank Preisrechner")

class Counter:
    price = 0;
    name = "unknown"

    def __init__(self, name,  price):
        self.name = name
        self.price = price
        if(self.name not in st.session_state):
            st.session_state[self.name] = 0


    def inc(self):
        st.session_state[self.name] = st.session_state[self.name] + 1

    def count(self):
        return st.session_state[self.name]
        

    def sum(self):
        return self.count() * self.price
    
def reset():
    st.session_state.clear()
    
counters = [
     Counter("🫗 Pfandglas zurück", -2.00),
     Counter("🍺 Bier", 4.00),
     Counter("🥤 Cola", 2.00)
]


def inc(name):
    for counter in counters:
        if counter.name == name:
            counter.inc()
            return;
    st.write(f"Counter {name} not found")

st.subheader(f"Aktuelle Summe: **{sum(counter.sum() for counter in counters):.2f}€**")

st.button("❌ Reset", on_click=reset, use_container_width=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.header("Eingabe")
    st.button("🫗 Pfandglas zurück", type="primary" , use_container_width=True, on_click=lambda:inc("🫗 Pfandglas zurück"))
    st.button("🍺 Bier", type="primary", use_container_width=True, on_click=lambda:inc("🍺 Bier"))
    st.button("🥤 Cola", type="primary", use_container_width=True, on_click=lambda:inc("🥤 Cola"))

with col2:
    st.header("Zusammenfassung")

    for counter in counters:
        if(counter.count() > 0):
            st.write(f"{counter.name}: {counter.count()} x {counter.price:.2f}€ = {counter.sum():.2f}€")

    "---"

    st.markdown(f"Gesamt: **{sum(counter.sum() for counter in counters):.2f}€**")
    
