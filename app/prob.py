from bokeh.embed import components
from bokeh.plotting import figure, gridplot
import numpy as np
from scipy.ndimage.filters import uniform_filter


def window_stdev(arr, window):
    c1 = uniform_filter(arr, window, mode='constant', origin=0)
    c2 = uniform_filter(arr * arr, window, mode='constant', origin=0)
    return ((c2 - c1 * c1)**.5)[:]


def plot_chamber():
    x = np.arange(0, 10 * np.pi, 0.1)
    y = np.sin(x) * 5 + (np.random.rand(x.shape[0]) - 0.5) * 2 + 55
    temp_plot = make_figure(x,
                            y,
                            target_high=60,
                            target_low=50,
                            window_size=30,
                            y_max_lower_bound=70,
                            y_min_upper_bound=40,
                            plot_width=500,
                            plot_height=300,
                            title="Temperature",
                            y_axis_label="Temperature (F)",
                            x_axis_label="Time",
                            measurement_name="Temp.")

    x = np.arange(0, 10 * np.pi, 0.1)
    y = np.sin(x) * 10 + (np.random.rand(x.shape[0]) - 0.5) * 2 + 70

    humid_plot = make_figure(x,
                             y,
                             target_high=80,
                             target_low=60,
                             window_size=30,
                             x_range=temp_plot.x_range,
                             y_max_lower_bound=100,
                             y_min_upper_bound=40,
                             plot_width=500,
                             plot_height=300,
                             title="Humidity",
                             y_axis_label="Humidity (% RH)",
                             x_axis_label="Time",
                             measurement_name="Humidity.")

    p = gridplot([[temp_plot, humid_plot]])
    # render template
    script, div = components(p)
    return script, div


def plot_ambient():
    x = np.arange(0, 10 * np.pi, 0.1)
    y = (np.random.rand(x.shape[0]) - 0.5) * 4 + 72
    temp_plot = make_figure(x,
                            y,
                            target_high=None,
                            target_low=None,
                            window_size=30,
                            y_max_lower_bound=80,
                            y_min_upper_bound=60,
                            plot_width=500,
                            plot_height=300,
                            title="Temperature",
                            y_axis_label="Temperature (F)",
                            x_axis_label="Time",
                            measurement_name="Temp.")

    x = np.arange(0, 10 * np.pi, 0.1)
    y = (np.random.rand(x.shape[0]) - 0.5) * 10 + 30

    humid_plot = make_figure(x,
                             y,
                             target_high=None,
                             target_low=None,
                             window_size=30,
                             x_range=temp_plot.x_range,
                             y_max_lower_bound=50,
                             y_min_upper_bound=0,
                             plot_width=500,
                             plot_height=300,
                             title="Humidity",
                             y_axis_label="Humidity (% RH)",
                             x_axis_label="Time",
                             measurement_name="Humidity.")

    p = gridplot([[temp_plot, humid_plot]])
    # render template
    script, div = components(p)
    return script, div


def make_figure(x,
                y,
                target_high=60,
                target_low=50,
                window_size=30,
                x_range=None,
                y_max_lower_bound=70,
                y_min_upper_bound=70,
                plot_width=400,
                plot_height=150,
                title="Temperature",
                y_axis_label="Temperature (F)",
                x_axis_label="Time",
                measurement_name="Temp."):
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
                  x_axis_type="datetime")
    if target_high and target_low:
        plot.varea(x=x,
                   y1=np.ones(x.shape) * 1e5,
                   y2=np.ones(x.shape) * target_high,
                   alpha=0.2,
                   color='red')
        plot.varea(x=x,
                   y1=np.ones(x.shape) * target_low,
                   y2=-np.ones(x.shape) * 1e5,
                   alpha=0.2,
                   color='red')
        plot.varea(x=x,
                   y1=np.ones(x.shape) * target_high,
                   y2=np.ones(x.shape) * target_low,
                   alpha=0.2,
                   color='green',
                   legend_label='Target range')
    plot.line(x, y, legend_label=measurement_name, color='darkblue')
    plot.varea(x=x[window_size // 2:-window_size // 2],
               y1=y_avg[window_size // 2:-window_size // 2] +
               y_std[window_size // 2:-window_size // 2],
               y2=y_avg[window_size // 2:-window_size // 2] -
               y_std[window_size // 2:-window_size // 2],
               alpha=0.6,
               color='darkgray',
               legend_label='Std. ' + measurement_name)
    plot.line(x[window_size // 2:-window_size // 2],
              y_avg[window_size // 2:-window_size // 2],
              color='black',
              legend_label='Avg. ' + measurement_name)
    plot.legend.orientation = "horizontal"
    return plot