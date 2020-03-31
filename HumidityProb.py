import matplotlib.pyplot as plt
import numpy as np
import io

def plot_data():
    values = np.arange(0,2*np.pi,0.1)
    plt.plot(values,np.sin(values))
    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format='png')
    bytes_image.seek(0)
    return bytes_image
