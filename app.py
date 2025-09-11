from enum import Enum
import streamlit as st

st.set_page_config(page_title="Ausschank Preisrechner", page_icon="🍺", layout="wide")


class CounterCatergory(Enum):
    DRINKS = "Getränke 🥤🧃"


class Counter:
    price = 0;
    name = "unknown"
    category = None

    def __init__(self, name, price):
        self.name = name
        self.price = price
        if (self.name not in st.session_state):
            st.session_state[self.name] = 0

    def inc(self):
        st.session_state[self.name] = st.session_state[self.name] + 1

    def dec(self):
        st.session_state[self.name] = st.session_state[self.name] - 1

    def count(self):
        return st.session_state[self.name]

    def sum(self):
        return self.count() * self.price


def reset():
    st.session_state.clear()


counters_by_category = {

    CounterCatergory.DRINKS: [
        Counter("Großes Pfandglas zurück", -2.00),
        Counter("Kleines Pfandglas zurück", -0.50),
        Counter("Cola/Fanta/Sprite", 2.00),
        Counter("Wasser/Saft", 2.00),
        Counter("Apfelschorle", 2.00),
        Counter("Rote Brause", 2.50),
        Counter("Bier/Radler/Diesel", 5.50),
        Counter("Glas Wein", 2.50),
        Counter("Sekt", 3.00),
        Counter("Bowle", 3.00),
    ],
}

all_counters = [counter for category in CounterCatergory for counter in counters_by_category[category]]

tc, rc = st.columns(2, gap="small")
st.divider()

for category in CounterCatergory:
    category_counters = [counter for counter in counters_by_category[category]]
    category_cols = st.columns(2)
    for i in range(len(category_counters)):
        with category_cols[i % 2]:
            product_container = st.container()
            button_cols = st.columns([0.25, 0.6, 0.25], gap=None, vertical_alignment="center", border=False)
            with product_container:
                st.markdown("""
                    <style>
                    div.stButton > button {
                        border: none;                 /* remove border */
                        outline: none !important;     /* remove focus outline */
                    }
                        div.stButton > button:focus {
                            border: none;
                            outline: none !important;
                        }
                        div.stButton > button:active {
                            border: none;
                            outline: none !important;
                        }
                    div.stButton > button[kind="primary"] { 
                        background-color: #00C853; 
                        color: white;
                    }
                    div.stButton > button[kind="secondary"] { 
                        background-color: #D50000; 
                        color: white;
                    }
                    </style>
                """, unsafe_allow_html=True)
                with button_cols[0]:
                    btn = st.button(
                        "➕",
                        key=f"{category_counters[i].name}_inc",
                        width="stretch",
                        type="primary"
                    )
                    if (btn):
                        category_counters[i].inc()

                with button_cols[2]:
                    dec_btn = st.button(
                        "➖",
                        key=f"{category_counters[i].name}_dec",
                        width="stretch",
                        type="secondary"
                    )
                    if (dec_btn):
                        if (category_counters[i]>=1):
                            category_counters[i].dec()
                with button_cols[1]:

                    counter_product_container = st.container(horizontal=True, gap=None, horizontal_alignment="center")
                    with counter_product_container:
                        counter_cols = st.columns([1,6], gap=None, border=False)

                        with counter_cols[0]:
                            if (category_counters[i].count() > 0):
                                st.markdown(
                                    f"<p style='text-align: center; color: #00B0FF ; font-weight: bold; font-size: 30px'>{category_counters[i].count()}</p>",
                                    unsafe_allow_html=True
                                )

                        with counter_cols[1]:
                            name = category_counters[i].name
                            price = category_counters[i].price
                            st.markdown(
                            f"<p style='text-align: center'>{name}({price:.2f}€)</p>",
                            unsafe_allow_html=True
                            )

with tc:
    st.subheader(f"Gesamt: **{sum(counter.sum() for counter in all_counters):.2f}€**")

with rc:
    st.button("❌ Reset", on_click=reset, use_container_width=True)
