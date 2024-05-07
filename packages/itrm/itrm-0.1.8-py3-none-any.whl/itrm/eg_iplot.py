import numpy as np
import itrm

# Constants
K = 200000
J = 5

# x axis
x = np.linspace(0, 1, K)

# y axis data
Y = np.zeros((J, len(x)))
for j in range(J):
    Y[j] = np.cos(2*np.pi*2*x + (j/J)*np.pi)

# plot
#itrm.config.uni = False
itrm.plot(x, -Y, "Test")
itrm.plot(x, Y, "Multiple curves", overlay=True)
