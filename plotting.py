# fetch the data frame from motion_detector
from motion_detector import df

# import plotting interface of bokeh
from bokeh.plotting import figure, show, output_file

# bokeh tool for hover functionality
from bokeh.models import HoverTool, ColumnDataSource
# ColumnDataSource is a standardized way to provide data to a bokeh plot

# convert the start to strings datatypes with the format YYMMDD and HMS
df["Start_string"] = df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
# convert the start to strings datatypes with the format YYMMDD and HMS
df["End_string"] = df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

# convert df to column data source object
cds = ColumnDataSource(df)

# figure object
p = figure(x_axis_type = 'datetime', height = 100, width = 500, responsive = True, title = "Motion Graph")
# remove the stickers
p.yaxis.minor_tick_line_color = None
# remove the grid
p.ygrid[0].ticker.desired_num_ticks = 1


# Hover object - Start and end column from the dataframe when hovered over a quadrant
hover = HoverTool(tooltips = [("Start", "@Start_string"), ("End", "@End_string")])
# adding the hover tool to the tool menu
p.add_tools(hover)
# plot a glyph and Modify the quad method using the cds
q = p.quad(left = "Start", right = "End", bottom = 0, top = 1, color = "Green", source = cds)

# outputing the file
output_file("Graph2.html")
show(p)