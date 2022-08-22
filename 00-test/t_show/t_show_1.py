import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
# ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot()
x = np.random.rand(11).cumsum()
y = np.random.rand(11).cumsum()

print(x)

# ax1.plot(x, y, 'c*-', label='ax1', linewidth=2)
ax2.plot(x, y, 'm.-.', label='ax2', linewidth=1)

# ax1.legend()
# ax1.set_title('hahaha')
ax2.legend()
ax2.set_title('xixixi')
ax2.set_xlabel('hengzhou')
ax2.set_ylabel('zongzhou')

plt.show()