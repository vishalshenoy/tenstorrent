import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

# Tenstorrent graphing tool
st.title('Tenstorrent Performance Graphs')
st.markdown("Create graphs for Tenstorrent model performance analysis.")

hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)


option = st.radio("Select Configuration:", ('Grayskull', 'Wormhole'))

core_count = 0
if option == 'Grayskull':
    core_count = 108
else:
    core_count = 64

st.write("")

# File uploader for multiple files
uploaded_files = st.file_uploader("Upload Excel or CSV performance sheets", type=["xlsx", "csv"], accept_multiple_files=True)

if uploaded_files:
    tab_names = []
    for file in uploaded_files:
        name_before_dot = (file.name).split('.')[0]
        tab_names.append(f"{name_before_dot}")

    tabs = st.tabs(tab_names)

    for i, uploaded_file in enumerate(uploaded_files):
        with tabs[i]:
            name = uploaded_file.name
            if ".xlsx" in name:
                df = pd.read_excel(uploaded_file)
            elif ".csv" in name:
                df = pd.read_csv(uploaded_file)

            # Calculate adjusted utilization for all on-device operations
            df['Adjusted Utilization'] = ((df['PM IDEAL [ns]'] / df['DEVICE KERNEL DURATION [ns]']) * (core_count / df['CORE COUNT']) * 100)
            df['Adjusted Utilization'] = df['Adjusted Utilization'].replace([np.inf, -np.inf], np.nan).fillna(0)
            df['Adjusted Utilization'] = df['Adjusted Utilization'].astype(float)


            matmul_df = df[(df['OP TYPE'] == 'tt_dnn_device') & (df['OP CODE'].str.contains('matmul', case=False, na=False))].reset_index(drop=True)
            conv_df = df[(df['OP TYPE'] == 'tt_dnn_device') & (df['OP CODE'].str.contains('conv', case=False, na=False))].reset_index(drop=True)
            other_ops_df = df[(df['OP TYPE'] == 'tt_dnn_device') & (~df['OP CODE'].str.contains('matmul|conv', case=False, na=False))].reset_index(drop=True)

            matmul_df['Operation Number'] = matmul_df.index + 1
            conv_df['Operation Number'] = conv_df.index + 1
            other_ops_df['Operation Number'] = other_ops_df.index + 1

            # Calculate and display average utilization for each set of operations
            avg_utilization_matmul = matmul_df['Adjusted Utilization'].mean()
            avg_utilization_conv = conv_df['Adjusted Utilization'].mean()
            avg_utilization_other = other_ops_df['Adjusted Utilization'].mean()

            st.subheader('Average Utilization')
            st.write(f"Average Utilization for MatMul Operations: {avg_utilization_matmul:.2f}%")
            st.write(f"Average Utilization for Conv Operations: {avg_utilization_conv:.2f}%")
            st.write(f"Average Utilization for Other Operations: {avg_utilization_other:.2f}%")
            st.divider()

            def add_download_button(fig, name, description):
                buf = BytesIO()
                fig.savefig(buf, format="png")
                buf.seek(0)
                st.download_button(
                    label=f"Download Graph Above",
                    data=buf,
                    file_name=f"{name}_{description.replace(' ', '_').lower()}.png",
                    mime="image/png"
                )

            # Plotting the graphs for MatMul operations
            st.subheader('MatMul Operations')

            # First graph: Operation Core Count + Utilization (MatMul)
            st.markdown("Operation Core Count + Utilization (MatMul)")
            fig1, ax1 = plt.subplots()
            ax2 = ax1.twinx()
            ax1.bar(matmul_df['Operation Number'], matmul_df['CORE COUNT'], color='b', alpha=0.6, label='Core Count')
            ax2.plot(matmul_df['Operation Number'], matmul_df['Adjusted Utilization'], color='r', label='Utilization')
            ax1.set_xlabel('Operation Number')
            ax1.set_ylabel('Core Count')
            ax2.set_ylabel('Utilization (%)')
            ax1.legend(loc='upper left')
            ax2.legend(loc='upper right')
            st.pyplot(fig1)
            add_download_button(fig1, name, "Operation Core Count + Utilization (MatMul)")

            # Second graph: Operation Device Kernel Duration + Utilization (MatMul)
            st.markdown("Operation Device Kernel Duration + Utilization (MatMul)")
            fig2, ax3 = plt.subplots()
            ax4 = ax3.twinx()
            ax3.bar(matmul_df['Operation Number'], matmul_df['DEVICE KERNEL DURATION [ns]'], color='g', alpha=0.6, label='Device Kernel Duration')
            ax4.plot(matmul_df['Operation Number'], matmul_df['Adjusted Utilization'], color='r', label='Utilization')
            ax3.set_xlabel('Operation Number')
            ax3.set_ylabel('Device Kernel Duration (ns)')
            ax4.set_ylabel('Utilization (%)')
            ax3.legend(loc='upper left')
            ax4.legend(loc='upper right')
            st.pyplot(fig2)
            add_download_button(fig2, name, "Operation Device Kernel Duration + Utilization (MatMul)")

            # Third graph: Device Kernel Duration vs Utilization (MatMul)
            st.markdown("Device Kernel Duration vs Utilization (MatMul)")
            fig3, ax5 = plt.subplots()
            ax5.scatter(matmul_df['DEVICE KERNEL DURATION [ns]'], matmul_df['Adjusted Utilization'], color='purple')
            ax5.set_xlabel('Device Kernel Duration (ns)')
            ax5.set_ylabel('Utilization (%)')
            st.pyplot(fig3)
            add_download_button(fig3, name, "Device Kernel Duration vs Utilization (MatMul)")
            st.divider()

            # Plotting the graphs for Conv operations
            st.subheader('Conv Operations')
            st.text("")

            # First graph: Operation Core Count + Utilization (Conv)
            st.markdown("Operation Core Count + Utilization (Conv)")
            fig4, ax6 = plt.subplots()
            ax7 = ax6.twinx()
            ax6.bar(conv_df['Operation Number'], conv_df['CORE COUNT'], color='b', alpha=0.6, label='Core Count')
            ax7.plot(conv_df['Operation Number'], conv_df['Adjusted Utilization'], color='r', label='Utilization')
            ax6.set_xlabel('Operation Number')
            ax6.set_ylabel('Core Count')
            ax7.set_ylabel('Utilization (%)')
            ax6.legend(loc='upper left')
            ax7.legend(loc='upper right')
            st.pyplot(fig4)
            add_download_button(fig4, name, "Operation Core Count + Utilization (Conv)")

            # Second graph: Operation Device Kernel Duration + Utilization (Conv)
            st.markdown("Operation Device Kernel Duration + Utilization (Conv)")
            fig5, ax8 = plt.subplots()
            ax9 = ax8.twinx()
            ax8.bar(conv_df['Operation Number'], conv_df['DEVICE KERNEL DURATION [ns]'], color='g', alpha=0.6, label='Device Kernel Duration')
            ax9.plot(conv_df['Operation Number'], conv_df['Adjusted Utilization'], color='r', label='Utilization')
            ax8.set_xlabel('Operation Number')
            ax8.set_ylabel('Device Kernel Duration (ns)')
            ax9.set_ylabel('Utilization (%)')
            ax8.legend(loc='upper left')
            ax9.legend(loc='upper right')
            st.pyplot(fig5)
            add_download_button(fig5, name, "Operation Device Kernel Duration + Utilization (Conv)")

            # Third graph: Device Kernel Duration vs Utilization (Conv)
            st.markdown("Device Kernel Duration vs Utilization (Conv)")
            fig6, ax10 = plt.subplots()
            ax10.scatter(conv_df['DEVICE KERNEL DURATION [ns]'], conv_df['Adjusted Utilization'], color='purple')
            ax10.set_xlabel('Device Kernel Duration (ns)')
            ax10.set_ylabel('Utilization (%)')
            st.pyplot(fig6)
            add_download_button(fig6, name, "Device Kernel Duration vs Utilization (Conv)")
            st.divider()
            
            # Plotting the graphs for other on-device operations
            st.subheader('Other On-Device Operations')
            st.text("")

            # First graph: Operation Core Count + Utilization (Other)
            st.markdown("Operation Core Count + Utilization (Other)")
            fig7, ax11 = plt.subplots()
            ax12 = ax11.twinx()
            ax11.bar(other_ops_df['Operation Number'], other_ops_df['CORE COUNT'], color='b', alpha=0.6, label='Core Count')
            ax12.plot(other_ops_df['Operation Number'], other_ops_df['Adjusted Utilization'], color='r', label='Utilization')
            ax11.set_xlabel('Operation Number')
            ax11.set_ylabel('Core Count')
            ax12.set_ylabel('Utilization (%)')
            ax11.legend(loc='upper left')
            ax12.legend(loc='upper right')
            st.pyplot(fig7)
            add_download_button(fig7, name, "Operation Core Count + Utilization (Other)")

            # Second graph: Operation Device Kernel Duration + Utilization (Other)
            st.markdown("Operation Device Kernel Duration + Utilization (Other)")
            fig8, ax13 = plt.subplots()
            ax14 = ax13.twinx()
            ax13.bar(other_ops_df['Operation Number'], other_ops_df['DEVICE KERNEL DURATION [ns]'], color='g', alpha=0.6, label='Device Kernel Duration')
            ax14.plot(other_ops_df['Operation Number'], other_ops_df['Adjusted Utilization'], color='r', label='Utilization')
            ax13.set_xlabel('Operation Number')
            ax13.set_ylabel('Device Kernel Duration (ns)')
            ax14.set_ylabel('Utilization (%)')
            ax13.legend(loc='upper left')
            ax14.legend(loc='upper right')
            st.pyplot(fig8)
            add_download_button(fig8, name, "Operation Device Kernel Duration + Utilization (Other)")

            # Third graph: Device Kernel Duration vs Utilization (Other)
            st.markdown("Device Kernel Duration vs Utilization (Other)")
            fig9, ax15 = plt.subplots()
            ax15.scatter(other_ops_df['DEVICE KERNEL DURATION [ns]'], other_ops_df['Adjusted Utilization'], color='purple')
            ax15.set_xlabel('Device Kernel Duration (ns)')
            ax15.set_ylabel('Utilization (%)')
            st.pyplot(fig9)
            add_download_button(fig9, name, "Device Kernel Duration vs Utilization (Other)")
            st.divider()

            # Pie Chart
            st.subheader('Operation Types Pie Chart')
            st.text("")

            # Op Types + Identifiers
            op_types = {
                'MatMul': 'MatMul',
                'Conv': 'Conv',
                'InterleavedToSharded': 'I2S',
                'MaxPool': 'MaxPool',
                'Move': 'Move',
                'Reduce': 'Reduce',
                'Reshard': 'Reshard',
                'Tile/Untile': 'Tile/Untile',
                'Binary': 'Binary',
                'Halo': 'Halo'
            }

            # Sum of kernel durations for ops
            op_sums = {op_name: df[df['OP CODE'].str.contains(identifier, case=False, na=False)]['DEVICE KERNEL DURATION [ns]'].sum() for identifier, op_name in op_types.items()}

            total_duration = sum(op_sums.values())
            op_percentages = {op_name: (duration / total_duration) * 100 for op_name, duration in op_sums.items()}

            # Pie chart
            fig_pie, ax_pie = plt.subplots()
            wedges, texts = ax_pie.pie(op_sums.values(), startangle=140)
            
            # Legend for Pie Chart
            legend_labels = [f'{op_name}: {op_percentages[op_name]:.1f}%' for op_name in op_sums.keys()]
            ax_pie.legend(wedges, legend_labels, title="Operation Types", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            
            ax_pie.axis('equal')
            st.pyplot(fig_pie)
            add_download_button(fig_pie, name, "Operation Types Pie Chart")

            # Download filtered data button
            st.divider()
            st.subheader('Download Graph Data')
            filtered_data = pd.concat([matmul_df, conv_df, other_ops_df])
            col1, col2 = st.columns(2)
            st.markdown("""
            <style>
                div[data-testid="column"] {
                    width: fit-content !important;
                    flex: unset;
                }
                div[data-testid="column"] * {
                    width: fit-content !important;
                }
            </style>
            """, unsafe_allow_html=True)
            
            # Select only the specified columns
            filtered_data = filtered_data[['OP CODE', 'OP TYPE', 'GLOBAL CALL COUNT', 'CORE COUNT', 'DEVICE KERNEL DURATION [ns]', 'Adjusted Utilization']]
            
            def convert_df_to_csv(df):
                return df.to_csv(index=False).encode('utf-8')

            csv_data = convert_df_to_csv(filtered_data)

            with col1:
                st.download_button(
                    label="Download Data (CSV)",
                    data=csv_data,
                    file_name=f'graph_data_{name}.csv',
                    mime='text/csv',
                    key=f'download-csv-{name}'
                )

            output_overall = BytesIO()
            with pd.ExcelWriter(output_overall, engine='xlsxwriter') as writer:
                filtered_data.to_excel(writer, index=False, sheet_name='Overall Data')
            overall_data = output_overall.getvalue()

            with col2:
                st.download_button(
                    label="Download Data (XLSX)",
                    data=overall_data,
                    file_name=f"graph_data_{name}.xlsx",
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    key=f'download-xlsx-{name}'
                )
