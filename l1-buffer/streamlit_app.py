import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(layout="wide")

def plot_buffers(sqlite_file, x_range_option):
    conn = sqlite3.connect(sqlite_file)
    
    query = """
    SELECT buffers.operation_id, operations.name as operation_name, buffers.address, buffers.max_size_per_bank
    FROM buffers
    JOIN operations ON buffers.operation_id = operations.operation_id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    # This line filters out rows where the address exceeds 2,000,000
    df = df[df['address'] <= 2_000_000]

    df['end_address'] = df['address'] + df['max_size_per_bank']
    
    df = df.sort_values(by='address')
    df = df.sort_values(by='operation_id', ascending=False)

    fig, ax = plt.subplots(figsize=(12, 200), dpi=60)

    for _, row in df.iterrows():
        ax.barh(row['operation_id'], row['max_size_per_bank'], left=row['address'], height=0.8, label=row['operation_name'])
    
    st.write(f"Operation buffers address range: {df['address'].min()} to {df['end_address'].max()}")
    st.write(f"Operations with buffers ID range: {df['operation_id'].min()} to {df['operation_id'].max()}")
    
    ax.set_xlabel('Address')
    ax.set_ylabel('Operation ID')
    ax.set_title('L1 Buffer Utilization')

    ax.grid(True, axis='x')

    min_op_id = df['operation_id'].min()
    max_op_id = df['operation_id'].max()
    ax.set_ylim(min_op_id - 1, max_op_id + 1)
    ax.invert_yaxis()

    minTick = 0
    max_range = 1_500_000

    if x_range_option == "Half":
        max_range = 1_000_000
    elif x_range_option == "Full":
        max_range = 1_500_000
    else:  # Optimized
        minTick = df['address'].min() - 100000
        max_range = df['end_address'].max()
    
    x_ticks = range(minTick, max_range + 1, 100000)
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([f'{(x // 1000)}k' for x in x_ticks])

    secax_top = ax.secondary_xaxis('top')
    secax_top.set_xticks(x_ticks)
    secax_top.set_xticklabels([f'{(x // 1000)}k' for x in x_ticks])
    secax_top.set_xlabel('Address')

    secax = ax.secondary_yaxis('right')
    secax.set_yticks(df['operation_id'])
    secax.set_yticklabels(df['operation_id'])

    st.pyplot(fig)
    
    df_sorted = df.sort_values(by='operation_id', ascending=True)
    st.dataframe(df_sorted[['operation_id', 'operation_name', 'address', 'max_size_per_bank']], use_container_width=True)


def main():
    hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
    '''
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

    st.title("Tenstorrent L1 Utilization Graph")

    x_range_option = st.selectbox("Select Address Range", ["Half", "Full", "Optimized"])

    uploaded_file = st.file_uploader("Choose a SQLite file", type="sqlite")

    if uploaded_file is not None:
        with open("temp_sqlite_file.sqlite", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        plot_buffers("temp_sqlite_file.sqlite", x_range_option)

if __name__ == "__main__":
    main()
