from matplotlib import pyplot as plt
import mnist
import numpy as np

train_images = mnist.train_images()

image = train_images[0]
image = np.where(image < (255/2), 0, 255)

plt.imshow(image, cmap='gray')
plt.show()



