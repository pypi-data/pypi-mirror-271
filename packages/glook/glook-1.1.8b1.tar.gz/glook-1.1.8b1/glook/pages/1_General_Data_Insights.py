import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import StringIO
st.set_page_config(page_title="GLook", layout="wide")
st.write("Session State:->", st.session_state["shared"])


if "df" in st.session_state and st.session_state.df is not None:
	df = st.session_state.df
	# Get number of rows
	num_rows = df.shape[0]

	# Get number of columns
	num_columns = df.shape[1]

	# Check for duplicates
	num_duplicates = df.duplicated().sum()

	# Get memory usage
	memory_usage = df.memory_usage(deep=True).sum() / (1024 * 1024)  # Convert bytes to MB
	# Calculate total memory usage in bytes
	# memory_usage = df.memory_usage(deep=True).sum()

	# Convert bytes to megabytes
	# memory_usage = memory_usage / (1024 ** 2)
	# Get number of features
	num_features = len(df.columns)

	# Get number of categorical features
	num_categorical = len(df.select_dtypes(include=['object']).columns)

	# Get number of numerical features
	num_numerical = len(df.select_dtypes(include=['number']).columns)

	
	# st.dataframe(df)
	# Exclude non-numeric columns
	numeric_df = df.select_dtypes(include='number')

	# Convert non-numeric values to NaN
	numeric_df = numeric_df.apply(pd.to_numeric, errors='coerce')
	st.header("Correlation Coefficient :green[Heatmap]")
	# Calculate the correlation matrix
	correlation_matrix = numeric_df.corr()
	# Define the list of colorscales
	# colorscales = ['aggrnyl', 'agsunset', 'algae', 'amp', 'armyrose', 'balance', 'blackbody', 'bluered', 'blues', 'blugrn', 'bluyl', 'brbg', 'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'curl', 'darkmint', 'deep', 'delta', 'dense', 'earth', 'edge', 'electric', 'emrld', 'fall', 'geyser', 'gnbu', 'gray', 'greens', 'greys', 'haline', 'hot', 'hsv', 'ice', 'icefire', 'inferno', 'jet', 'magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges', 'orrd', 'oryel', 'oxy', 'peach', 'phase', 'picnic', 'pinkyl', 'piyg', 'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn', 'puor', 'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu', 'rdgy', 'rdpu', 'rdylbu', 'rdylgn', 'redor', 'reds', 'solar', 'spectral', 'speed', 'sunset', 'sunsetdark', 'teal', 'tealgrn', 'tealrose', 'tempo', 'temps', 'thermal', 'tropic', 'turbid', 'turbo', 'twilight', 'viridis', 'ylgn', 'ylgnbu', 'ylorbr', 'ylorrd']
	# Number input for selecting the colorscale index
	# colorscale_index = st.number_input('Select a colorscale index:', min_value=0, max_value=len(colorscales)-1, value=0)
	# st.write(colorscales[colorscale_index])
	# Create the heatmap plot

	fig = go.Figure(data=go.Heatmap(
		z=correlation_matrix.values,
		x=correlation_matrix.columns,
		y=correlation_matrix.index,
		# colorscale=colorscales[colorscale_index],  # You can choose any colorscale
		colorscale='aggrnyl',
		text=correlation_matrix.values,  # Values to display
		texttemplate='%{text:.2f}',  # Format for displaying values
		showscale=True  # Display the color scale on the side
	))

	# Add title and axis labels
	fig.update_layout(
		title='Correlation Coefficient Heatmap',
		xaxis=dict(title='Columns'),
		yaxis=dict(title='Columns'),
		width=700,  # Adjust width
		height=700,  # Adjust height

	)

	# Show the plot
	st.plotly_chart(fig)

	st.header(":green[Edit Data] to Suit Your Needs:")
	df = st.data_editor(df)


	# Capture the output of df.info()
	info_buffer = StringIO()
	df.info(buf=info_buffer)
	info_str = info_buffer.getvalue()

	# Display the info in Streamlit
	st.subheader("DataFrame :green[Info:]")
	st.code(info_str, language="neon")


	try:
		st.header("Numerical :green[Data Overview]")
		# df_info = df.describe().T
		# styled_df_info = df_info.style.highlight_max(axis=0).highlight_min(axis=0).format("{:.2f}")
		df_info = (
			df.describe().T.style.set_table_styles(
				[
					{'selector': 'th', 'props': 'background-color: lightgreen; color: black;'},  # Table headers
					{'selector': 'td', 'props': 'background-color: lightblue; border: 1px solid black;'},  # Table cells
					{'selector': 'tr', 'props': 'border: 1px solid black;'}  # Table rows
				]
			)
			.highlight_max(axis=0, props='background-color: darkgreen; color: white;')  # Highlight max values with specific color
			.highlight_min(axis=0, props='background-color: yellowgreen; color: black;')  # Highlight min values with another color
			.format("{:.2f}")
		)
		st.dataframe(df_info)
	except ValueError:
		st.dataframe()

	try:
		st.header("Categorical :green[Data Overview]")

		df_info1 = df.select_dtypes(include=['object']).describe().T

		# Style to highlight the most frequent category
		styled_df_info1 = (
		df_info1.style.set_table_styles(
				[
					{'selector': 'th', 'props': 'background-color: lightgreen; color: black;'},  # Table headers
					{'selector': 'td', 'props': 'background-color: lightblue; border: 1px solid black;'},  # Table cells
					{'selector': 'tr', 'props': 'border: 1px solid black;'}  # Table rows
				]
			)
			.highlight_max(axis=0, props='background-color: darkgreen; color: white;')  # Highlight max values with specific color
			.highlight_min(axis=0, props='background-color: yellowgreen; color: black;')  # Highlight min values with another color
			# .format("{:.2f}")
		)

		st.dataframe(styled_df_info1)
	except ValueError:
		st.dataframe()
	# Display the insights
	st.subheader(f"Data dimensions: :green[{num_rows} rows, {num_columns} columns]")
	st.subheader(f"Number of rows: :green[{num_rows}]")
	st.subheader(f"Number of duplicates: :green[{num_duplicates}]")
	st.subheader(f"Deep Memory usage: :green[{memory_usage:.3f} MB]")
	st.subheader(f"Number of features: :green[{num_features}]")
	st.subheader(f"Number of categorical features: :green[{num_categorical}]")
	st.subheader(f"Number of numerical features: :green[{num_numerical}]")
	


else:
	st.write("DataFrame not yet uploaded.")
# if st.sidebar.button("Univariate Analysis"):
	# st.switch_page("pages/2_Univariate_Analysis.py")

if st.button("Univariate_Analysis", use_container_width=True):
	st.switch_page("pages/2_Univariate_Analysis.py")