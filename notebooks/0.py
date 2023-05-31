# %%
import numpy as np
import scipy as sp
import pandas as pd

import matplotlib.pylab as plt
import altair as alt

# %%


# %%
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

# %%
def mmk(spend, vmax, k):
    return vmax * spend / (spend + k)

def mmk_inverse(revenue, vmax, k):
    return revenue * k / (vmax - revenue)

def mmk_roas_to_spend(roas, vmax, k):
    return vmax / roas - k

# %%
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

# %%
df_current

# %%
df_base

# %%
df_base[df_base.Platform == 'Facebook']

# %%
df_target_roas[df_target_roas.Platform == 'Facebook']

# %%
df_base.isnull().sum()

# %%
np.arange(0.8, 3.91, 0.01)

# %%
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

# %%
df

# %%
df[df.Spend % 100 != 0]

# %%
df_base[(df_base.Platform == 'Facebook') & df_base.Spend % 100 != 0]

# %%
len(np.arange(0.8, 3.91, 0.01))

# %%
df_base[(df_base.Platform == 'Facebook') & (df_base.ROAS.isin(np.arange(0.8, 3.91, 0.01)))]

# %%
df[df.ROAS.isin(np.arange(0.8, 3.91, 0.01))]

# %%



