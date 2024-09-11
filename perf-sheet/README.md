# Performance Sheet Analysis Tool
### Intro
This is a web tool for easily analyzing Excel and CSV performance sheets. Primarily, it calculates FPS and Adjusted Utilization for each operation.

### Codebase
The tool is built using _Streamlit_ for the interface, with _Pandas_ and _NumPy_ for data manipulation and sheet formatting. The main file containing the web interface and data manipulation is `streamlit_app.py`. The dependencies are listed in `requirements.txt`, and the `.streamlit` file contains configurations for UI styling.

### Usage

#### How it Works
To utilize the tool, a user selects the `Grayskull` or `Wormhole` configuration, adjusting core count for calculations accordingly. Then, the user uploads a `.csv` or `.xlsx` performance sheet. The tool automatically starts the analysis process

<img width="500" alt="Screenshot 2024-09-05 at 12 17 33 PM" src="https://github.com/user-attachments/assets/de04b1a0-a88c-419e-a934-9ec1f9c253e1">

#### Results
After a few seconds, the tool displays FPS for All Operations, MatMul + Conv Operations only, and Other On-Device
Operations (excluding MatMul + Conv).  The user can download performance sheets filtered for any of these configurations.

<img width="500" alt="Screenshot 2024-09-05 at 12 17 50 PM" src="https://github.com/user-attachments/assets/fcf5fd5c-5342-4ef8-8405-1c990ba7cdf3">

#### Downloaded Spreadsheet
If downloaded, the modified spreadsheet appends an Adjusted Utilization column for each operation, and an FPS column for the configuration. It also shuffles the Core Count + Device Kernel Duration columns to the end for easy comparison.

<img width="500" alt="Screenshot 2024-09-10 at 10 50 10 AM" src="https://github.com/user-attachments/assets/72454ccc-60d5-462d-a1da-15b5f417e66b">

### Run Locally
To run the tool locally, install the requirements from requirements.txt using the command `pip install -r requirements.txt`. Then, within the directory, run the command `streamlit run streamlit_app.py`. The web tool will default to opening at http://localhost:8501/, unless port 8501 is already in use.