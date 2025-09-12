from enum import Enum
import streamlit as st

st.set_page_config(page_title="Ausschank Preisrechner", page_icon="🍺", layout="wide")

class CounterCatergory(Enum):
    TOP = "Header"
    NON_ALCOHOL = "Alkoholfreie Getränke 🥤🧃"
    ALCOHOL = "Getränke ab 16 Jahre 🍺🍷🥂"

class Counter:
    price = 0
    name = "unknown"
    category = None

    def __init__(self, name, price):
        self.name = name
        self.price = price
        if (self.name not in st.session_state):
            st.session_state[self.name] = 0


    def inc(self):
        st.session_state[self.name] = st.session_state[self.name] + 1

    def count(self):
        return st.session_state[self.name]
        

    def sum(self):
        return self.count() * self.price

def reset():
    st.session_state.clear()

counters_by_category = {
    CounterCatergory.TOP: [
        Counter("Großes Pfandglas zurück", -2.00),
        Counter("Kleines Pfandglas zurück", -0.50),
    ],
    CounterCatergory.NON_ALCOHOL: [
        Counter("Cola/Fanta/Sprite", 2.00),
        Counter("Wasser/Saft", 2.00),
        Counter("Apfelschorle", 2.00),
        Counter("Rote Brause", 2.50),
    ],
    CounterCatergory.ALCOHOL: [
        Counter("Bier/Radler/Diesel", 5.50),
        Counter("Glas Wein", 2.50),
        Counter("Sekt", 3.00),
        Counter("Bowle", 3.00),
    ]
}

all_counters = [counter for category in CounterCatergory for counter in counters_by_category[category]]

tc, rc = st.columns(2, gap="small")

col1, col2 = st.tabs(["✏️ Eingabe", "💸 Zusammenfassung"])

with col1:
    top_counters = [counter for counter in counters_by_category[CounterCatergory.TOP]]
    top_cols = st.columns(len(top_counters))
    for i in range(len(top_counters)):
        with top_cols[i]:
            btn = st.button(f"{top_counters[i].name} ({top_counters[i].price:.2f}€)", type="primary" , use_container_width=True)
            if (btn):
                top_counters[i].inc()

    for category in CounterCatergory:
        if category == CounterCatergory.TOP: continue

        st.subheader(category.value)
        category_counters = [counter for counter in counters_by_category[category]]
        category_cols = st.columns(2)
        for i in range(len(category_counters)):
            with category_cols[i%2]:
                btn = st.button(f"{category_counters[i].name} ({category_counters[i].price:.2f}€)", type="secondary" , use_container_width=True)
                if (btn):
                    category_counters[i].inc()

with col2:
    data = []

    for counter in all_counters:
        if(counter.count() > 0):
            data.append({"Posten": counter.name, "Anzahl": counter.count(), "Preis": f"{counter.price:.2f}€", "PostenSumme": f"{counter.sum():.2f}€"})

    if(len(data) > 0):
        st.dataframe(data, use_container_width=True)
        st.subheader(f"Gesamt: **{sum(counter.sum() for counter in all_counters):.2f}€**")
    else:
        st.subheader("Keine Daten")

with tc:
    st.subheader(f"Gesamt: **{sum(counter.sum() for counter in all_counters):.2f}€**") 

with rc:
    st.button("❌ Reset", on_click=reset, use_container_width=True)
