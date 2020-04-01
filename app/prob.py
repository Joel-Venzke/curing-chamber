from bokeh.embed import components
from bokeh.plotting import figure, gridplot
import numpy as np
from scipy.ndimage.filters import uniform_filter
from bokeh.models.annotations import BoxAnnotation
import Adafruit_DHT as dht


class Prob:
    def __init__(self, prop_pin, sensor_type=dht.DHT22):
        self.prop_pin = prop_pin
        self.sensor_type = sensor_type
        self.temp = None
        self.humid = None
        self.update_reading()

    def update_reading(self):
        # read from sensor
        self.humid, self.temp = Adafruit_DHT.read_retry(self.sensor_type,
                                                        self.prop_pin,
                                                        delay_seconds=0)
        self.temp_c_to_f()

    def temp_c_to_f(self):
        self.temp = (self.temp * 9. / 5.) + 32


def window_stdev(arr, window):
    c1 = uniform_filter(arr, window, mode='constant', origin=0)
    c2 = uniform_filter(arr * arr, window, mode='constant', origin=0)
    return ((c2 - c1 * c1)**.5)[:]


def plot_data():
    x = np.arange(0, 10 * np.pi, 0.1)
    y = np.sin(x) * 5 + (np.random.rand(x.shape[0]) - 0.5) * 4 + 55
    chamber_temp_plot = make_figure(x,
                                    y,
                                    target_high=60,
                                    target_low=50,
                                    window_size=50,
                                    y_max_lower_bound=70,
                                    y_min_upper_bound=40,
                                    plot_width=500,
                                    plot_height=300,
                                    title="Chamber Temperature",
                                    y_axis_label="Temperature (F)",
                                    x_axis_label="Time",
                                    measurement_name="Temp.")

    x = np.arange(0, 10 * np.pi, 0.1)
    y = np.sin(x) * 10 + (np.random.rand(x.shape[0]) - 0.5) * 2 + 70

    chamber_humid_plot = make_figure(x,
                                     y,
                                     target_high=80,
                                     target_low=60,
                                     window_size=50,
                                     x_range=chamber_temp_plot.x_range,
                                     y_max_lower_bound=100,
                                     y_min_upper_bound=40,
                                     plot_width=500,
                                     plot_height=300,
                                     title="Chamber Humidity",
                                     y_axis_label="Humidity (% RH)",
                                     x_axis_label="Time",
                                     measurement_name="Humidity")
    x = np.arange(0, 10 * np.pi, 0.1)
    y = (np.random.rand(x.shape[0]) - 0.5) * 4 + 72
    ambient_temp_plot = make_figure(x,
                                    y,
                                    target_high=None,
                                    target_low=None,
                                    window_size=50,
                                    x_range=chamber_temp_plot.x_range,
                                    y_max_lower_bound=80,
                                    y_min_upper_bound=60,
                                    plot_width=500,
                                    plot_height=300,
                                    title="Ambient Temperature",
                                    y_axis_label="Temperature (F)",
                                    x_axis_label="Time",
                                    measurement_name="Temp.")

    x = np.arange(0, 10 * np.pi, 0.1)
    y = (np.random.rand(x.shape[0]) - 0.5) * 10 + 30

    ambient_humid_plot = make_figure(x,
                                     y,
                                     target_high=None,
                                     target_low=None,
                                     window_size=50,
                                     x_range=chamber_temp_plot.x_range,
                                     y_max_lower_bound=50,
                                     y_min_upper_bound=0,
                                     plot_width=500,
                                     plot_height=300,
                                     title="Ambient Humidity",
                                     y_axis_label="Humidity (% RH)",
                                     x_axis_label="Time",
                                     measurement_name="Humidity")

    p = gridplot([[chamber_temp_plot, chamber_humid_plot],
                  [ambient_temp_plot, ambient_humid_plot]])
    # render template
    script, div = components(p)
    return script, div


def make_figure(
        x,
        y,
        target_high=60,
        target_low=50,
        window_size=50,
        x_range=None,
        y_max_lower_bound=70,
        y_min_upper_bound=70,
        plot_width=400,
        plot_height=150,
        title="Temperature",
        y_axis_label="Temperature (F)",
        x_axis_label="Time",
        measurement_name="Temp.",
        tools="pan,crosshair,hover,box_select,lasso_select,save,reset,help"):
    window = np.ones(window_size) / float(window_size)
    y_avg = np.convolve(y, window, 'same')
    y_std = window_stdev(y, window_size) / 2

    y_max = max(y.max(), y_max_lower_bound)
    y_min = min(y.min(), y_min_upper_bound)

    if x_range == None:
        x_range = (x.max(), x.min())

    plot = figure(plot_width=plot_width,
                  plot_height=plot_height,
                  x_range=x_range,
                  y_range=(y_min, y_max),
                  title=title,
                  x_axis_label=x_axis_label,
                  y_axis_label=y_axis_label,
                  x_axis_type="datetime",
                  tools=tools)
    if target_high and target_low:
        upper = BoxAnnotation(bottom=target_high,
                              fill_alpha=0.2,
                              fill_color='red')
        plot.add_layout(upper)
        lower = BoxAnnotation(top=target_low, fill_alpha=0.2, fill_color='red')
        plot.add_layout(lower)
        target = BoxAnnotation(bottom=target_low,
                               top=target_high,
                               fill_alpha=0.2,
                               fill_color='green')
        plot.add_layout(target)
    plot.varea(x=x[window_size // 2:-window_size // 2],
               y1=y_avg[window_size // 2:-window_size // 2] +
               y_std[window_size // 2:-window_size // 2],
               y2=y_avg[window_size // 2:-window_size // 2] -
               y_std[window_size // 2:-window_size // 2],
               alpha=0.6,
               color='darkgray',
               legend_label='Std. ' + measurement_name)
    plot.line(x, y, legend_label=measurement_name, color='darkblue')
    plot.line(x[window_size // 2:-window_size // 2],
              y_avg[window_size // 2:-window_size // 2],
              color='black',
              legend_label='Avg. ' + measurement_name,
              line_dash=[2])
    plot.legend.orientation = "horizontal"
    return plot