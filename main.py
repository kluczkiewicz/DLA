import streamlit as st
from dla import generate_dla, init_grid
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import streamlit.components.v1 as components

st.title('Diffusion-limited aggregation')

col1, col2, col3 = st.columns(3)
with col1:
    box_size = st.number_input('Box size:', value = 101)
with col2:
    n_iterations = st.number_input('Number of iterations:', value = 100000)
with col3:
    freq = st.number_input('Save frame every nth iterations:', value = 100)

if st.button('Generate new pattern'):
    with st.spinner('Generating...'):
        init_grid(box_size)
        images, n = generate_dla(n_iterations, freq)
        fig = plt.figure()
        im = plt.imshow(images[0], animated=True)
        def updatefig(frame):
            im.set_array(images[frame])
            return [im]
        ani = animation.FuncAnimation(fig, updatefig, frames = images.shape[0], blit=True)
        plot = ani.to_jshtml()

    st.write(f'Model converged  after {n} iterations!')
    components.html(plot, height=1000)