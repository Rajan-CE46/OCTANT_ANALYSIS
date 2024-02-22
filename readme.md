# Octant Analysis Web Application

## Overview

The Octant Analysis Web Application is a Streamlit-based tool designed to facilitate the analysis of particle trajectories in three-dimensional space. The application preprocesses time-series data containing particle coordinates and calculates various statistics to provide insights into particle behavior within different octants.

## Features

- **Data Preprocessing**: The application preprocesses input data by calculating average coordinates and normalizing particle coordinates based on these averages.
- **Octant Identification**: Using normalized coordinates, the application assigns octant IDs to particles based on their location in 3D space.
- **Real-Time Visualization**: Users can upload data files, specify mod values, and visualize octant analysis results in real-time through an intuitive user interface.
- **Statistical Analysis**: The application calculates various statistics, including total particle counts, predominant octants within specified mod ranges, octant transition counts, and the longest continuous durations spent in each octant.

## Technologies Used

- **Streamlit**: For building the user interface and data visualization components.
- **Pandas**: For data manipulation and analysis, particularly for handling tabular data structures.
- **NumPy**: For numerical computing in Python, providing support for large, multi-dimensional arrays and matrices.
- **Openpyxl**: For reading and writing Excel files, particularly for data preprocessing tasks.

## Installation

To install the required dependencies, run:

Once the application is running, navigate to the provided URL in your web browser to access the Octant Analysis Web Application.

## Contributing

Contributions are welcome! If you have any ideas for new features, improvements, or bug fixes, please submit a pull request or open an issue on GitHub.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- This project was inspired by the need for efficient particle trajectory analysis tools in the field of Physics.
