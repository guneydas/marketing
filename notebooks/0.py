# %%
import numpy as np
import scipy as sp
import pandas as pd

import matplotlib.pylab as plt

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
df['revenue'] = df.spend.apply(mmk)

# %%
df

# %%



