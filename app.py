import requests
import pandas as pd
import streamlit as st

st.title("Drug Side-Effect Explorer")
st.caption("Reports show that a side effect was noticed, not that the drug caused it.")

drug = st.text_input("Type a drug's generic name", "ibuprofen")


@st.cache_data(ttl=86400)  # remember answers for 24 hours
def top_side_effects(drug_name):
    url = "https://api.fda.gov/drug/event.json"
    params = {
        "search": f'patient.drug.openfda.generic_name:"{drug_name}"',
        "count": "patient.reaction.reactionmeddrapt.exact",
        "limit": 10,
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None  # openFDA found nothing (or had a problem)
    return pd.DataFrame(response.json()["results"])  # columns: term, count


if drug:
    data = top_side_effects(drug.strip().lower())
    if data is None:
        st.error(f"No reports found for '{drug}'. Check the spelling or try the generic name.")
    else:
        st.subheader(f"Top 10 reported side effects: {drug}")
        st.bar_chart(data, x="term", y="count")
