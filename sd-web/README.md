# Stable Diffusion Web Demo

## Introduction
Stable Diffusion is a latent text-to-image diffusion model capable of generating photo-realistic images given any text input. These instructions pertain to running Stable Diffusion with an interactive web interface on the TT-Wormhole machine.

## How to Run

> [!NOTE]
>
> If you are using Wormhole, you must set the `WH_ARCH_YAML` environment variable.
>
> ```
> export WH_ARCH_YAML=wormhole_b0_80_arch_eth_dispatch.yaml
> ```

To run the demo, make sure to build the project, activate the environment, and set the appropriate environment variables.
For more information, refer [installation and build guide](https://github.com/tenstorrent/tt-metal/blob/main/INSTALLING.md).

The interface of this project is built with [Streamlit](https://streamlit.io). Use `pip install streamlit` to install the Streamlit dependencies on your machine. 

The web demo utilizes a [Flask](https://flask.palletsprojects.com/en/3.0.x/) server. Use `pip install Flask` to install the Flask dependencies on your machine.

Use `python models/demos/wormhole/stable_diffusion/demo/web_demo/demo.py` to run the web demo. It should automatically pop-up at this [address](http://localhost:8501) (localhost:8501).