import numpy as np
import pandas as pd
import altair as alt
import streamlit as st


vmax = 80000
k = 20000

def mmk(spend):
    return vmax * spend / (spend + k)

def mmk_inverse(revenue):
    return revenue * k / (vmax - revenue)

def mmk_roas_to_spend(roas):
    return vmax / roas - k


df = pd.DataFrame({'Spend': [100*i for i in range(1, 801)]})
df['Revenue'] = df.Spend.apply(mmk).astype('int')
df['ROAS'] = df.Revenue / df.Spend

new_rows = []
for roas in np.arange(0.8, 3.91, 0.01):
    spend =  mmk_roas_to_spend(roas)
    revenue = mmk(spend)
    if (spend not in df.Spend.values) and (roas not in df.ROAS.values):
        new_rows.append({
            'ROAS': round(roas, 2),
            'Spend': round(spend),
            "Revenue": round(revenue),
        })

df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True).sort_values('Spend').reset_index(drop=True)


st.set_page_config(
    page_title="Spend Diminishing Returns", 
    page_icon="chart_with_upwards_trend", 
    layout="centered"
)


st.title("Facebook Revenue by Spend")

st.write("See the relation between your Facebook Advertising Spend and the revenue it generates.")

col1, col2, col3 = st.columns(3)
with col1:
    target_roas = st.slider(
            "Choose target ROAS", min_value=1., max_value=3.9, step=0.01, value=2.0
        )


line = alt.Chart(df).mark_line().encode(
    alt.X('Spend', title="Spend (weekly)"),
    alt.Y('Revenue'),
    tooltip = [
        alt.Tooltip('Spend'),
        alt.Tooltip('Revenue'),
    ],
)

target_point = alt.Chart(df[df.ROAS == target_roas]).mark_point(
    color='orange',
    size=100,
    opacity=0.8,
).encode(
    alt.X('Spend'),
    alt.Y('Revenue'),
)


current_point = alt.Chart(df[df.Spend == 14000]).mark_point(
    color='red',
    size=100,
    opacity=0.5,
).encode(
    alt.X('Spend'),
    alt.Y('Revenue'),
)


annotation_layer = (
    alt.Chart(df[df.ROAS == target_roas])
    .mark_text(size=12, text='Target', color='orange', dy=-10, dx=-15, opacity=0.8)
    .encode(
        x='Spend',
        y='Revenue'
    ) +
    alt.Chart(df[df.Spend == 14000])
    .mark_text(size=12, text='Current', color='red', dy=10, dx=15, opacity=0.5)
    .encode(
        x='Spend',
        y='Revenue'
    )
)




st.altair_chart((
    line + target_point + annotation_layer + current_point
), use_container_width=True)


# https://discuss.streamlit.io/t/remove-made-with-streamlit-from-bottom-of-app/1370/16
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

