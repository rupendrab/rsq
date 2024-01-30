import time
import numpy as np
import streamlit as st
import pandas as pd
from datetime import datetime

def get_date_parts(dt: datetime):
    day = dt.day
    month = dt.month
    year_str = str(dt.year)
    year_first_two = year_str[:2]
    year_last_two = year_str[2:]    
    return day, month, int(year_first_two), int(year_last_two)

def create_ra_matrix(dt: datetime):
    r1 = list(get_date_parts(dt))
    r2 = [r1[3] + 1, r1[2] -1, r1[1] - 3, r1[0] + 3]
    r3 = [r1[1] - 2, r1[0] + 2, r1[3] + 2, r1[2] - 2]
    r4 = [r1[2] + 1, r1[3] - 1, r1[0] + 1, r1[1] - 1]
    return np.matrix([r1, r2, r3, r4]).reshape(4, 4)

styles = [
    "<style>",
    "td.highlight {background-color: blue; color: white}",  
    "</style>"
]
css = "\n".join(styles)

def to_html(df: pd.DataFrame, highlight_cells = None):
    table_str = '<table border="1" class="dataframe">\n'
    table_str += '<tbody>\n'
    l = df.values.tolist()
    for rowind, row in enumerate(l):
        table_str += '<tr style="text-align: right;">\n'
        for colind, val in enumerate(row):
            if highlight_cells is not None and (rowind, colind) in highlight_cells:
                table_str += f'<td class="highlight">{val}</td>'
            else:
                table_str += f'<td>{val}</td>'
        table_str += '</tr>\n'
    table_str += '</tbody>\n'
    table_str += '</table>\n'
    return css + table_str

# Set a default date
default_date = datetime.today()

st.set_page_config(page_title="Ramanujan's Magic Square")
st.header("Ramanujan's Magic Square")
st.subheader('Create a magic square for any date')
st.markdown("*Use Ramanujan's birthdate 1887/12/22 to get his original magic square...*")

# Create a date input widget
min_date = datetime(1800, 1, 1)
selected_date = st.date_input("Enter a date", None, min_value=min_date)

sleep_time = 0.5

default_col_count = 1
col_count = st.radio("Choose number of columns for output", [1,2,3,4], index=default_col_count-1)

if selected_date is not None:
    matrix = create_ra_matrix(selected_date)

    # Create sample matrix
    matrix1 = np.arange(16).reshape(4,4)

    # Convert to DataFrame
    df = pd.DataFrame(matrix)

    # df = df.rename(columns = {0:" ", 1:"  ", 2: "   ", 3: "    "})
    # html = df.to_html(index=False, header=False)

    # Initialize state
    if 'highlight_cells' not in st.session_state:
        st.session_state['highlight_cells'] = None

    def get_sum(highlight_cells):
        sum = 0
        for row, col in highlight_cells:
            sum += matrix[row, col]
        return sum

    cols = st.columns(col_count)
    curcol = 0

    def next_col(curcol):
        curcol += 1
        if curcol >= len(cols):
            curcol = 0
        return curcol
    
    def display_data(col, highlight_cells, curcol):
        html = to_html(df, highlight_cells=highlight_cells)
        col.markdown(html, unsafe_allow_html=True)
        sum_val = get_sum(highlight_cells)
        col.markdown(f"**Sum = {sum_val}**")
        time.sleep(sleep_time)
        curcol = next_col(curcol)
        return curcol

    for rownum in range(0, 4):
        col = cols[curcol]
        highlight_cells = [(rownum, i) for i in range(4)]
        curcol = display_data(col, highlight_cells, curcol)

    for colnum in range(0, 4):
        col = cols[curcol]
        highlight_cells = [(i, colnum) for i in range(4)]
        curcol = display_data(col, highlight_cells, curcol)

    col = cols[curcol]
    highlight_cells = [(i, i) for i in range(4)]
    curcol = display_data(col, highlight_cells, curcol)

    col = cols[curcol]
    highlight_cells = [(i, 4-i-1) for i in range(4)]
    curcol = display_data(col, highlight_cells, curcol)

    col = cols[curcol]
    highlight_cells = [(0, 0), (0, 3), (3, 0), (3, 3)]
    curcol = display_data(col, highlight_cells, curcol)

    col = cols[curcol]
    highlight_cells = [(0, 1), (0, 2), (3, 1), (3, 2)]
    curcol = display_data(col, highlight_cells, curcol)

    col = cols[curcol]
    highlight_cells = [(1, 0), (1, 3), (2, 0), (2, 3)]
    curcol = display_data(col, highlight_cells, curcol)

    col = cols[curcol]
    highlight_cells = [(0, 1), (1, 0), (2, 3), (3, 2)]
    curcol = display_data(col, highlight_cells, curcol)

    col = cols[curcol]
    highlight_cells = [(0, 2), (1, 3), (2, 0), (3, 1)]
    curcol = display_data(col, highlight_cells, curcol)

    col = cols[curcol]
    highlight_cells = [(1, 1), (1, 2), (2, 1), (2, 2)]
    curcol = display_data(col, highlight_cells, curcol)

    for r in [0, 2]:
        for c in [0, 2]:
            col = cols[curcol]
            highlight_cells = [(r, c), (r, c+1), (r+1, c), (r+1, c+1)]
            curcol = display_data(col, highlight_cells, curcol)

    for r, c in [(1, 0), (1, 2)]:
        col = cols[curcol]
        highlight_cells = [(r, c), (r, c+1), (r+1, c), (r+1, c+1)]
        curcol = display_data(col, highlight_cells, curcol)

def highlight_row(rownum):
    st.session_state['highlight_cells'] = [(rownum, i) for i in range(4)]

def highlight_rows():
    for rownum in range(0, 4):
        highlight_row(rownum)
        time.sleep(1)

# st.button(label="Rows", on_click=highlight_rows)

# Footer
footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Developed by <a style='display: block; text-align: center;' href="https://www.linkedin.com/in/rupendra/" target="_blank">Rupendra Bandyopadhyay</a></p>
</div>
"""

st.markdown(footer,unsafe_allow_html=True)
