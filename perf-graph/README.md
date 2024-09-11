# Performance Graph Visualizer Tool
### Intro
This is a web tool visualize TT-NN operations. 

### Codebase
The tool is built using _Streamlit_ for the interface, along with _Pandas_, _NumPy_, and _MatPlotLib_ for data manipulation and graphing. The main file containing the web interface and data manipulation is `streamlit_app.py`. The dependencies are listed in `requirements.txt`, and the `.streamlit` file contains configurations for UI styling.

#### How it Works
To utilize the tool, a user selects the `Grayskull` or `Wormhole` configuration, adjusting core count for calculations accordingly. Then, the user uploads a `.csv` or `.xlsx` performance sheet. The tool automatically starts the graphing process

<img width="500" alt="Screenshot 2024-09-10 at 11 20 29 AM" src="https://github.com/user-attachments/assets/d3bcf3e9-9130-46ab-8892-fd5d91daa89c">

#### Results
After a few seconds, the tool displays multiple graphs for the categories of All Operations, MatMul + Conv Operations only, and Other On-Device Operations (excluding MatMul + Conv). Each category has graphs for Core Count + Utilization, Device Kernel Duration + Utilization, and Device Kernel Duration vs Utilization.

<img width="500" alt="Screenshot 2024-09-10 at 11 19 46 AM" src="https://github.com/user-attachments/assets/ec3e72fd-eb77-4663-832a-e58256b61e22">

<img width="500" alt="Screenshot 2024-09-10 at 11 21 20 AM" src="https://github.com/user-attachments/assets/233f5cd7-65e9-4e32-b979-1e4dd295bba4">


There is also a Pie Chart to show the breakdown of Operation Types in the data.

<img width="500" alt="Screenshot 2024-09-10 at 11 19 35 AM" src="https://github.com/user-attachments/assets/39b07ec3-641f-4acf-a1e7-8700f9746019">

#### Downloaded Spreadsheet
Graphs and data are downloadable via buttons below each graph and a Download Data section at the bottom of the tool.

### Run Locally
To run the tool locally, install the requirements from requirements.txt using the command `pip install -r requirements.txt`. Then, within the directory, run the command `streamlit run streamlit_app.py`. The web tool will default to opening at http://localhost:8501/, unless port 8501 is already in use.