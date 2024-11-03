# Import necessary libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from welly import Project
import folium
from IPython.core.display import HTML
import time
import welly.quality as wq
from welly import Well
from IPython.display import HTML
from welly import Location
import pkg_resources

# Main function to run the app
# Caching function to load LAS file
@st.cache_data
def load_well_from_las(las_file_url):
    return Well.from_las(las_file_url)

# Caching function to load survey data from CSV
@st.cache_data
def load_survey_data(csv_file_url):
    return pd.read_csv(csv_file_url)

# Caching function to load multiple wells
@st.cache_resource
def load_multiple_wells(well_file_urls):
    return [Well.from_las(url) for url in well_file_urls]
def main():
    st.title("Horizontal Drilling Trajectory Visualization")

    # Sidebar for category selection
    category = st.sidebar.radio("Select Analysis Category", ("Single Well Location", "Multi Well Analysis"))

    # Set local file paths for LAS and CSV files for single well analysis
    las_file_url = 'https://raw.githubusercontent.com/Youssef1Rezk/well-trajectory/main/L05-15-Spliced.las'
    csv_file_url = 'https://raw.githubusercontent.com/Youssef1Rezk/well-trajectory/main/L05-15-Survey.csv'

    # Create an empty placeholder for category content
    content_placeholder = st.empty()

    if category == "Single Well Location":
        with content_placeholder.container():
            st.header("Single Well Location Analysis")
            time.sleep(0.5)  # Wait for half a second to simulate animation

            try:
                # Load LAS data using Welly
                well = Well.from_las(las_file_url)
                
                # Button to display LAS file data
                if st.button("Show well-logged floor"):
                    st.write("Loaded LAS file curves successfully.")
                    st.pyplot(well.plot(extents='curves'))

                # Load survey data from CSV file
                survey = pd.read_csv(csv_file_url)

                # Button to display survey data
                if st.button("Show Survey Data"):
                    st.write("Survey data:")
                    st.write(survey.head())

                # Extract and display relevant columns
                survey_subset = survey[['MD', 'INC', 'AZI']]
                well.location.add_deviation(survey_subset.values)

                # Retrieve position data
                x_loc = well.location.position[:, 0]
                y_loc = well.location.position[:, 1]
                z_loc = well.location.position[:, 2]

                # Button to plot 2D trajectory views
                if st.button("Show 2D Trajectory Plots"):
                    st.subheader("2D Trajectory Plots")
                    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

                    ax1.plot(x_loc, y_loc, lw=3)
                    ax1.set_title("X Location vs Y Location")

                    ax2.plot(x_loc, z_loc, lw=3)
                    ax2.set_title("X Location vs TVD")
                    ax2.invert_yaxis()

                    ax3.plot(y_loc, z_loc, lw=3)
                    ax3.set_title("Y Location vs TVD")
                    ax3.invert_yaxis()

                    st.pyplot(fig)

                # Button to plot 2D trajectory with start/end markers
                if st.button("Show 2D Trajectory with Start/End Markers"):
                    st.subheader("2D Trajectory with Start/End Markers")
                    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

                    ax1.plot(x_loc, y_loc, lw=3)
                    ax1.plot(x_loc[0], y_loc[0], marker='s', color='black', ms=8, label="Start")
                    ax1.plot(x_loc[-1], y_loc[-1], marker='*', color='red', ms=8, label="End")
                    ax1.set_title("X Location vs Y Location")
                    ax1.legend()

                    ax2.plot(x_loc, z_loc, lw=3)
                    ax2.plot(x_loc[0], z_loc[0], marker='s', color='black', ms=8)
                    ax2.plot(x_loc[-1], z_loc[-1], marker='*', color='red', ms=8)
                    ax2.set_title("X Location vs TVD")
                    ax2.invert_yaxis()

                    ax3.plot(y_loc, z_loc, lw=3)
                    ax3.plot(y_loc[0], z_loc[0], marker='s', color='black', ms=8)
                    ax3.plot(y_loc[-1], z_loc[-1], marker='*', color='red', ms=8)
                    ax3.set_title("Y Location vs TVD")
                    ax3.invert_yaxis()

                    st.pyplot(fig)

                # Button to compare calculated trajectory against original survey data
                if st.button("Compare Against Original Survey"):
                    st.subheader("Comparison Against Original Survey Data")
                    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

                    ax1.plot(x_loc, y_loc, lw=7, label="Calculated")
                    ax1.plot(x_loc[0], y_loc[0], marker='s', color='black', ms=8)
                    ax1.plot(survey['X-offset'], survey['Y-offset'], label="Original Survey")
                    ax1.plot(x_loc[-1], y_loc[-1], marker='*', color='red', ms=8)
                    ax1.set_title("X Location vs Y Location")
                    ax1.legend()

                    ax2.plot(x_loc, z_loc, lw=7, label="Calculated")
                    ax2.plot(x_loc[0], z_loc[0], marker='s', color='black', ms=8)
                    ax2.plot(survey['X-offset'], survey['TVD'], label="Original Survey")
                    ax2.plot(x_loc[-1], z_loc[-1], marker='*', color='red', ms=8)
                    ax2.invert_yaxis()
                    ax2.set_title("X Location vs TVD")
                    ax2.legend()

                    ax3.plot(y_loc, z_loc, lw=7, label="Calculated")
                    ax3.plot(y_loc[0], z_loc[0], marker='s', color='black', ms=8)
                    ax3.plot(survey['Y-offset'], survey['TVD'], label="Original Survey")
                    ax3.plot(y_loc[-1], z_loc[-1], marker='*', color='red', ms=8)
                    ax3.invert_yaxis()
                    ax3.set_title("Y Location vs TVD")
                    ax3.legend()

                    st.pyplot(fig)

                # Button to show 3D plot for the trajectory
                if st.button("Show 3D Trajectory Plot"):
                    st.subheader("3D Trajectory Plot")
                    fig = plt.figure(figsize=(8, 8))
                    ax = fig.add_subplot(111, projection='3d')
                    ax.plot3D(x_loc, y_loc, z_loc, lw=2, color="blue")
                    ax.set_xlabel("X Location")
                    ax.set_ylabel("Y Location")
                    ax.set_zlabel("TVD")
                    ax.set_zlim(3000, 0)
                    st.pyplot(fig)

            except FileNotFoundError:
                st.error("One or both of the required files were not found. Please ensure the paths are correct.")

   # Multi Well Analysis
    elif category == "Multi Well Analysis":
        with content_placeholder.container():
            st.header("Multi Well Analysis")
            time.sleep(0.5)  # Wait for half a second to simulate animation
            
            # List of well file URLs
            well_file_urls = [
            'https://raw.githubusercontent.com/Youssef1Rezk/well-trajectory/refs/heads/main/all%20wells%E2%80%9C/L0509_comp%20(1).las',
            'https://raw.githubusercontent.com/Youssef1Rezk/well-trajectory/refs/heads/main/all%20wells%E2%80%9C/NLOG_LIS_LAS_2048_8636_l0606_2004_comp.las',
            'https://raw.githubusercontent.com/Youssef1Rezk/well-trajectory/refs/heads/main/all%20wells%E2%80%9C/NLOG_LIS_LAS_2629_8971_l0607_2009_comp.las',
            'https://raw.githubusercontent.com/Youssef1Rezk/well-trajectory/refs/heads/main/all%20wells%E2%80%9C/NLOG_LIS_LAS_3164_7264_l0701_1971_comp.las'
         ]

            # Load wells using Project from URLs
            wells = [Well.from_las(url) for url in well_file_urls]
            st.write(f"Loaded {len(wells)} wells.")

            well_dict = {}
            for well in wells:
                well_dict[well.uwi] = {
                    'well name': well.name, 
                    'Latitude': well.location.latitude,  
                    'Longitude': well.location.longitude  
                }

            wells_df = pd.DataFrame.from_dict(well_dict, orient='index')
            wells_df.reset_index(inplace=True)
            wells_df.rename(columns={'index': 'UWI'}, inplace=True)

            # Plot all well locations on a single map
            mean_lat = wells_df['Latitude'].mean()
            mean_long = wells_df['Longitude'].mean()
            m = folium.Map(location=[mean_lat, mean_long], zoom_start=7)

            for index, well_location in wells_df.iterrows():
                folium.Marker(
                    [well_location['Latitude'], well_location['Longitude']],
                    popup=well_location['well name']
                ).add_to(m)

            st.subheader("Well Locations Map")
            st.components.v1.html(m._repr_html_(), height=500, scrolling=True)

        # Continue with plotting GR, RHOB, NPHI, and quality control tests as before...


            # Plot GR from all wells
            fig, axs = plt.subplots(figsize=(14, 10), ncols=len(wells))
            for i, (ax, well) in enumerate(zip(axs, wells)):
                gr = well.get_curve('GR')
                if gr is not None:
                    ax = gr.plot(ax=ax, c='green')
                ax.set_title(f"GR for\n{well.name}")

            st.pyplot(fig)

            # Plot RHOB from all wells
            fig, axs = plt.subplots(figsize=(14, 10), ncols=len(wells))
            curve_name = 'RHOB'
            for i, (ax, well) in enumerate(zip(axs, wells)):
                rhob = well.get_curve(curve_name)
                if rhob is not None:
                    ax = rhob.plot(ax=ax, c='blue')
                ax.set_title(f"RHOB for\n{well.name}")

            st.pyplot(fig)

            # Plot NPHI from all wells
            fig, axs = plt.subplots(figsize=(14, 10), ncols=len(wells))
            curve_name = 'NPHI'
            for i, (ax, well) in enumerate(zip(axs, wells)):
                nphi = well.get_curve(curve_name)
                if nphi is not None:
                    ax = nphi.plot(ax=ax, c='orange')
                ax.set_title(f"NPHI for\n{well.name}")

            st.pyplot(fig)

            # Quality control tests
            tests = {
                'Each': [wq.no_flat, wq.no_gaps, wq.not_empty],
                'GR': [
                    wq.all_positive,
                    wq.all_between(0, 250),
                    wq.check_units(['API', 'GAPI']),
                ],
                'RHOB': [
                    wq.all_positive,
                    wq.all_between(1.5, 3),
                    wq.check_units(['G/CC', 'g/cm3']),
                ]
            }

            # Create a quality control table for each well individually
            qc_dict = {}
            for well in wells:
                qc_table_html = well.qc_table_html(tests)
                qc_dict[well.name] = qc_table_html

            # Display Data Quality Control
            st.subheader("Data Quality Control")
            for well_name, qc_html in qc_dict.items():
                st.write(f"### {well_name}")
                st.write(HTML(qc_html), unsafe_allow_html=True)
if __name__ == "__main__":
    main()
