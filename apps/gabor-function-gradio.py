import numpy as np
import matplotlib.pyplot as plt
import gradio as gr


def gabor(x, y, x0, y0, theta, beta_x, beta_y, alpha, f, phi):
    xp = (x - x0) * np.cos(theta) + (y - y0) * np.sin(theta)
    yp = -(x - x0) * np.sin(theta) + (y - y0) * np.cos(theta)
    envelope = alpha * np.exp(-0.5 * (beta_x * xp ** 2 + beta_y * yp ** 2))
    carrier = np.cos(2 * np.pi * f * xp + phi)
    return envelope * carrier

def draw_sigma(x0, y0, beta_x, beta_y, theta):
    sigma_x = 1 / np.sqrt(beta_x)
    sigma_y = 1 / np.sqrt(beta_y)

    # Calculate end points along rotated axes
    end_x_x = x0 + sigma_x * np.cos(theta)
    end_y_x = y0 + sigma_x * np.sin(theta)
    end_x_y = x0 - sigma_y * np.sin(theta)
    end_y_y = y0 + sigma_y * np.cos(theta)

    draw_labelled_arrow(x0, y0, end_x_x, end_y_x, r'$\sigma_x$')
    draw_labelled_arrow(x0, y0, end_x_y, end_y_y, r'$\sigma_y$')

def draw_labelled_arrow(x0, y0, x, y, label):
    plt.arrow(x0, y0, x - x0, y - y0, head_width=0.2, head_length=0.3, fc='white', ec='white',
              length_includes_head=True)
    delta = 0.3
    plt.text(x, y + delta, label, fontsize=12, color='white', horizontalalignment='center')

def plot_gabor(x0=0, y0=0, theta=0, beta_x=1, beta_y=1, alpha=1, f=0.5, phi=0, draw_parameters=False):
    x = np.linspace(-10, 10, 500)
    y = np.linspace(-10, 10, 500)
    X, Y = np.meshgrid(x, y)
    G = gabor(X, Y, x0, y0, theta, beta_x, beta_y, alpha, f, phi)

    fig = plt.figure(figsize=(6, 6))
    plt.imshow(G, extent=(-10, 10, -10, 10), origin='lower')
    plt.colorbar()

    if draw_parameters:
        draw_sigma(x0, y0, beta_x, beta_y, theta)

    return fig


iface = gr.Interface(fn=plot_gabor,
                     inputs=[gr.Slider(-10, 10, step=0.5, value=0, label="x0"),
                             gr.Slider(-10, 10, step=0.5, value=0, label="y0"),
                             gr.Slider(0, np.pi, step=np.pi / 16, value=2, label="theta"),
                             gr.Slider(0.001, 1, step=0.001, value=0.1, label="beta_x"),
                             gr.Slider(0.001, 1, step=0.001, value=0.03, label="beta_y"),
                             gr.Slider(0.1, 10, step=0.1, value=3, label="alpha"),
                             gr.Slider(0.01, 2, step=0.05, value=0.15, label="f"),
                             gr.Slider(0, 2 * np.pi, step=np.pi / 16, value=0, label="phi"),
                             gr.Checkbox(value=False, label="Draw sigma")],
                     outputs="plot",
                     title="Gabor Filter Visualization",
                     description="Adjust the parameters to see changes in the Gabor filter visualization.",
                     live=True,
                     allow_flagging='never')
iface.launch()
