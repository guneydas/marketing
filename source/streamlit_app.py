import numpy as np
import pandas as pd
import altair as alt
import streamlit as st


st.set_page_config(
    page_title="Spend Diminishing Returns", 
    page_icon="chart_with_upwards_trend", 
    layout="centered"
)


def mmk(spend):
    vmax = 80000
    k = 20000
    return vmax * spend / (spend + k)

df = pd.DataFrame({'spend': [100*i for i in range(1, 801)]})
df['revenue'] = df.spend.apply(mmk)
df['revenue'] = df.revenue.astype('int')



#@st.cache_data(ttl=60 * 60 * 24)
def get_chart(data):
    hover = alt.selection_single(
        fields=["spend"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, height=500, title="Ad Spend vs Revenue")
        .mark_line()
        .encode(
            x=alt.X("spend", title="Spend"),
            y=alt.Y("revenue", title="Revenue"),
        )
    )

    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="spend",
            y="revenue",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("spend", title="Spend"),
                alt.Tooltip("revenue", title="Revenue"),
            ],
        )
        .add_selection(hover)
    )

    return (lines + points + tooltips).interactive()


st.title("Facebook Revenue by Spend")

st.write("See the relation between your Facebook Advertising Spend and the revenue it generates.")

target_roas = st.slider(
        "Choose target ROAS", min_value=0.8, max_value=10.0, step=0.1, value=2.0
    )


chart = get_chart(df)
st.altair_chart(chart.interactive(), use_container_width=True)


