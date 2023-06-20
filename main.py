import streamlit as st
from dla import generate_dla, init_grid, calculate_dim, power_law
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import streamlit.components.v1 as components
import numpy as np

st.set_page_config(layout="wide")
st.title('Diffusion-limited aggregation')
#st.write('Wprowadzenie do fizyki złożoności. Fizyka statystyczna sieci złożonych - final project made by Kamil Łuczkiewicz')

col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1.2, 2, 1, 1])
with col1:
    box_size = st.number_input('Box size:', value = 101)
with col2:
    n_iterations = st.number_input('Number of iterations:', value = 100000)
with col3:
    freq = st.number_input('Save frame every nth iterations:', value = 100)
with col4:
    edges = st.multiselect(
    'Select edges to start random walk:',
    ['right', 'left', 'up', 'down'],
    ['right', 'left', 'up', 'down'])
with col5:
    start_point = st.selectbox(
    'Cluster starting point:',
    ('center', 'right', 'left', 'up', 'down'))
with col6:
    disable_checkbox = True
    if start_point != 'center':
        disable_checkbox = False
    st.write('Fill full edge:')
    full_edge = st.checkbox('Yes', disabled = disable_checkbox)

if st.button('Generate new pattern'):
    with st.spinner('Generating...'):
        cx, cy = init_grid(box_size, start_point, full_edge)
        images, n = generate_dla(n_iterations, freq, edges)

        indices = np.indices(images[0].shape)
        distances = np.sqrt((indices[0]-cx)**2 + (indices[1]-cy)**2)

        N_values_list = []
        popt_list = []

        R_values = np.arange(1, min(images[0].shape) // 2, 2)
        for grid in images:
            N_values, popt, _ = calculate_dim(grid, R_values, distances)
            N_values_list.append(N_values)
            popt_list.append(popt)

        # fig = plt.figure()
        # im = plt.imshow(images[0], animated=True)
        # def updatefig(frame):
        #     im.set_array(images[frame])
        #     return [im]
        # ani = animation.FuncAnimation(fig, updatefig, frames = images.shape[0], blit=True)
        # plot_grids = ani.to_jshtml()

        # fig, ax = plt.subplots()
        # ax.set_xlabel('R')
        # ax.set_ylabel('N(R)')
        # ax.set_title('N(R) for each iteration')

        # def update(num):
        #     ax.clear()
        #     ax.loglog(R_values, N_values_list[num], 'ko', label="Data")
        #     ax.loglog(R_values, power_law(R_values, *popt_list[num]), 'r-', label="Fit: A = %5.3f, alpha = %5.3f" % tuple(popt_list[num]))
        #     ax.legend()

        # ani = animation.FuncAnimation(fig, update, frames=range(len(N_values_list)), repeat=False)
        # plot_dim = ani.to_jshtml()

        # Plotting the animation
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

        # For the aggregate plot
        im = ax1.imshow(images[0], cmap='Greys')

        # For the N(R) plot
        line1, = ax2.loglog(R_values, N_values_list[0], 'ko', label="Data")
        line2, = ax2.loglog(R_values, power_law(R_values, *popt_list[0]), 'r-', label="Fit: A = %5.3f, alpha = %5.3f" % tuple(popt_list[0]))
        ax2.set_xlabel('R')
        ax2.set_ylabel('N(R)')
        ax2.set_title('N(R) for each iteration')
        ax2.legend()

        plt.tight_layout()

        def update(num):
            # Update the aggregate plot
            im.set_array(images[num])
            ax1.set_title('Step: {}'.format(num * freq))
            
            # Update the N(R) plot
            ax2.clear()
            ax2.loglog(R_values, N_values_list[num], 'ko', label="Data")
            ax2.loglog(R_values, power_law(R_values, *popt_list[num]), 'r-', label="Fit: A = %5.3f, alpha = %5.3f" % tuple(popt_list[num]))
            ax2.legend()

        ani = animation.FuncAnimation(fig, update, frames=range(len(N_values_list)), repeat=False)
        subplot = ani.to_jshtml()

    col21, col22= st.columns([1, 10])
    with col21:
        st.write(' ')
    with col22:
        st.write(f'Model converged  after {n} iterations!')
        components.html(subplot, height=1000)
