import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

nd = np.random.randint(0, 100, size=100)
s = pd.Series(nd)
# bins默认值是10
s.hist(bins=10).plot()
plt.show()
