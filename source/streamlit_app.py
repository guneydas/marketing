import numpy as np
import pandas as pd
import altair as alt
import streamlit as st


platform_details = {
    'Facebook': {
        'parent': 'Meta',
        'Vmax': 80000,
        'k': 20000,
        'current': 15000,
    },
    'Instagram': {
        'parent': 'Meta',
        'Vmax': 80000,
        'k': 30000,
        'current': 20000,
    },
    'Audience Network': {
        'parent': 'Meta',
        'Vmax': 40000,
        'k': 30000,
        'current': 10000,
    },
    'Google Search': {
        'parent': 'Google',
        'Vmax': 90000,
        'k': 5000,
        'current': 15000,
    },
    'Youtube': {
        'parent': 'Google',
        'Vmax': 40000,
        'k': 10000,
        'current': 15000,
    },
    'Google Display Network': {
        'parent': 'Google',
        'Vmax': 30000,
        'k': 20000,
        'current': 10000,
    },
    'Bing Search': {
        'parent': 'Microsoft',
        'Vmax': 10000,
        'k': 2000,
        'current': 10000,
    },
}


def mmk(spend, vmax, k):
    return vmax * spend / (spend + k)

def mmk_inverse(revenue, vmax, k):
    return revenue * k / (vmax - revenue)

def mmk_roas_to_spend(roas, vmax, k):
    return vmax / roas - k


rows = []
target_roas_rows = []
current_rows = []
for platform, details in platform_details.items():
    # calculate values for every 100s of spend and
    for i in range(1, max(details['Vmax'], details['current']) // 100 + 1):
        spend = 100 * i
        revenue = round(mmk(spend, details['Vmax'], details["k"]))
        rows.append({
            'Spend': spend,
            'Revenue': revenue,
            'ROAS': revenue / spend,
            'Platform': platform,
            'Parent': details['parent'],
        })
    # calculate values for every 0.01s of roas
    min_roas = round(revenue / spend, 2)  # last calculated roas (for highest spend)
    max_roas = round(mmk(100, details['Vmax'], details["k"]) / 100, 2)  # for min spend
    for roas in np.arange(min_roas, max_roas + 0.01, 0.01):
        spend = mmk_roas_to_spend(roas, details['Vmax'], details["k"])
        revenue = mmk(spend, details['Vmax'], details["k"])
        row = {
            'Spend': round(spend),
            'Revenue': round(revenue),
            'ROAS': round(100 * roas),
            'Platform': platform,
            'Parent': details['parent'],
        }
        target_roas_rows.append(row)
        #if spend % 100 != 0:
        #    rows.append(row)
    # calculate values for current spend
    spend = round(details['current'])
    revenue = round(mmk(spend, details['Vmax'], details["k"]))
    row = {
        'Spend': spend,
        'Revenue': revenue,
        'ROAS': revenue / spend,
        'Platform': platform,
        'Parent': details['parent'],
    }
    if spend % 100 != 0:
        rows.append(row)
    current_rows.append(row)

df_base = pd.DataFrame(rows).sort_values(['Parent', 'Platform', 'Spend']).reset_index(drop=True)
del rows

df_target_roas = pd.DataFrame(target_roas_rows).sort_values(['Parent', 'Platform', 'Spend']).reset_index(drop=True)
del target_roas_rows

df_current = pd.DataFrame(current_rows).sort_values(['Parent', 'Platform', 'Spend']).reset_index(drop=True)
del current_rows

 
st.set_page_config(
    page_title="Spend vs Revenue", 
    page_icon="chart_with_upwards_trend", 
    layout="centered"
)


st.title("Ad Spend - Revenue relation")
st.write("See the relation between your Ad Spend and the Revenue it generates for each platform.")


df = df_base

col1, col2, col3 = st.columns(3)
with col1:
    st.text("\u25CB: Current Spend")
    st.text("\u25A1: Target Spend")
with col2:
    target_roas = st.slider(
        "Choose target ROAS", min_value=1., max_value=4., step=0.01, value=2.0
    )

line = alt.Chart(df).mark_line(
).encode(
    alt.X('Spend', title="Spend (weekly)"),
    alt.Y('Revenue'),
    color = 'Platform',
    tooltip = [
        alt.Tooltip('Platform'),
        alt.Tooltip('Spend'),
        alt.Tooltip('Revenue'),
    ],
)
target_point = alt.Chart(
    df_target_roas[df_target_roas.ROAS == round(100*target_roas)]
).mark_square(
    size=100,
    opacity=0.8,
).encode(
    alt.X('Spend'),
    alt.Y('Revenue'),
    color = 'Platform',
)
current_point = alt.Chart(
    df_current
).mark_circle(
    size=100,
    opacity=0.5,
).encode(
    alt.X('Spend'),
    alt.Y('Revenue'),
    color = 'Platform',
)
st.altair_chart((
    line + target_point  + current_point
), use_container_width=True)




# https://discuss.streamlit.io/t/remove-made-with-streamlit-from-bottom-of-app/1370/16
hide_streamlit_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
