# %%
import numpy as np
import scipy as sp
import pandas as pd

import matplotlib.pylab as plt
import altair as alt

# %%
def mmk(spend):
    vmax = 80000
    k = 20000
    return vmax * spend / (spend + k)

# %%
for s in [10000, 20000, 30000]:
    print(s, mmk(s))

# %%
xs = [0]
last = 0
while last < 80000:
    xs += [last + x * (2*i+1) for x in range(1, 100)]
    last = xs[-1]


# %%
print(len(xs), xs[-1])

# %%
plt.plot(xs, [mmk(x) for x in xs])
plt.plot(xs, [270*np.sqrt(x) for x in xs])
plt.plot(xs, [2000*np.power(x, 0.3) for x in xs])

# %%


# %%
def mmk(spend):
    vmax = 80000
    k = 20000
    return vmax * spend / (spend + k)

df = pd.DataFrame({'spend': [100*i for i in range(1, 801)]})
df['revenue'] = df.spend.apply(mmk).astype('int')

# %%
df

# %%
alt.Chart(df).mark_line().encode(x='spend', y='revenue').interactive()

# %%
alt.Chart(df).mark_line().encode(
    alt.X('spend', title='Spend'),
    alt.Y('revenue', title='Revenue'),
)

# %%
def mmk(spend):
    vmax = 80000
    k = 20000
    return vmax * spend / (spend + k)

df = pd.DataFrame({'Spend': [100*i for i in range(1, 801)]})
df['Revenue'] = df.Spend.apply(mmk).astype('int')

# %%
alt.Chart(df).mark_line().encode(
    alt.X('Spend'),
    alt.Y('Revenue'),
    tooltip = [
        alt.Tooltip('Spend'),
        alt.Tooltip('Revenue'),
    ],
)

# %%
df['ROAS'] = df.Revenue / df.Spend
df.ROAS.hist(bins=100)

# %%
df.head()

# %%
df.tail()

# %%
df[df.Spend >= 19900]

# %%
np.arange(0.8, 4, 0.1)

# %%
vmax = 80000
k = 20000

def mmk(spend):
    return vmax * spend / (spend + k)

def mmk_inverse(revenue):
    return revenue * k / (vmax - revenue)

def mmk_roas_to_spend(roas):
    return vmax / roas - k

# %%
mmk(20000), mmk_inverse(mmk(20000))

# %%
mmk(100000), mmk_inverse(mmk(100000))

# %%
mmk_roas_to_spend(3)

# %%
df[df.Spend == 6700]

# %%
df = pd.DataFrame({'Spend': [100*i for i in range(1, 801)]})
df['Revenue'] = df.Spend.apply(mmk).astype('int')
df['ROAS'] = df.Revenue / df.Spend

new_rows = []
for roas in np.arange(0.8, 4, 0.1):
    spend =  mmk_roas_to_spend(roas)
    revenue = mmk(spend)
    if (spend not in df.Spend.values) and (roas not in df.ROAS.values):
        new_rows.append({
            'ROAS': round(roas, 1),
            'Spend': round(spend),
            "Revenue": round(revenue),
        })

df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True).sort_values('Spend').reset_index(drop=True)

# %%
df.head(15)

# %%
df.tail()

# %%
2000/513

# %%
new_rows

# %%


# %%


# %%
slider = alt.binding_range(min=0.8, max=3.9, step=-0.1, name='ROAS:')
roas_var = alt.Parameter('roas', value=2.0, bind=slider)

highlight = alt.Chart(df[df.ROAS == roas_var]).mark_point(color='orange', size=10).encode(
    alt.X('Spend'),
    alt.Y('Revenue'),
)

highlight

# %%
alt.__version__

# %%


# %%
slider = alt.binding_range(min=0.8, max=3.9, step=-0.1, name='ROAS:')
highlight = alt.Chart(df[df.ROAS == slider]).mark_circle(color='orange').encode(
    alt.X('Spend'),
    alt.Y('Revenue'),
)

main_chart = alt.Chart(df).mark_line().add_selection(highlight).encode(
    alt.X('Spend', title="Spend (weekly)"),
    alt.Y('Revenue'),
    tooltip = [
        alt.Tooltip('Spend'),
        alt.Tooltip('Revenue'),
    ],
)

main_chart

# %%



