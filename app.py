import streamlit as st
from packing_engine import size_split, packing_engine
import pandas as pd
import os

# ------------------------------------------------
# PAGE SETTINGS
# ------------------------------------------------

st.set_page_config(
    page_title="Menology Packing Planner",
    layout="wide"
)

# ------------------------------------------------
# MEN OLOGY STYLE
# ------------------------------------------------

st.markdown("""
<style>

body {
    background-color:#f4f6fa;
}

h1 {
    color:#154c79;
}

h2,h3 {
    color:#154c79;
}

.stButton>button {
    background-color:#154c79;
    color:white;
    border-radius:8px;
    height:45px;
    width:240px;
    font-size:16px;
    border:none;
}

.stButton>button:hover {
    background-color:#0e3554;
}

.block-container {
    padding-top:1.5rem;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# HEADER
# ------------------------------------------------

col1, col2 = st.columns([6,1])

with col1:
    st.markdown("<h1>Menology Packing Planning System</h1>", unsafe_allow_html=True)

with col2:
    logo_path = os.path.join(os.getcwd(), "logo.webp")
    st.image(logo_path, width=200)

st.divider()

# ------------------------------------------------
# ORDER INPUT
# ------------------------------------------------

order_id = st.text_input("Order ID / Style Number")

st.markdown("## Input Data")

# ------------------------------------------------
# COLOR INPUT
# ------------------------------------------------

with st.expander("Color Quantities", expanded=True):

    num_colors = st.number_input("Number of Colors", min_value=1, step=1)

    colors = []
    pieces = []

    for i in range(num_colors):

        c1, c2 = st.columns(2)

        color = c1.text_input(f"Color {i+1}", key=f"color{i}")
        piece = c2.number_input(f"Pieces {i+1}", min_value=0, key=f"piece{i}")

        colors.append(color)
        pieces.append(piece)

# ------------------------------------------------
# SIZE INPUT
# ------------------------------------------------

with st.expander("Size Ratios", expanded=True):

    num_sizes = st.number_input("Number of Sizes", min_value=1, step=1)

    sizes = []
    ratios = []

    for i in range(num_sizes):

        c1, c2 = st.columns(2)

        size = c1.text_input(f"Size {i+1}", key=f"size{i}")

        ratio = c2.number_input(
            f"Ratio {i+1}",
            min_value=0.1,
            step=0.1,
            format="%.2f",
            key=f"ratio{i}"
        )

        sizes.append(size)
        ratios.append(ratio)

st.divider()

# ------------------------------------------------
# GENERATE PACKING PLAN
# ------------------------------------------------

if st.button("Generate Packing Plan"):

    split_data = size_split(colors, pieces, sizes, ratios)

    results = packing_engine(split_data)

    st.markdown(f"## Packing Plan - Order {order_id}")

    # ------------------------------------------------
    # SIZE SPLIT MATRIX
    # ------------------------------------------------

    st.markdown("### Size Split Matrix")

    table_data = []

    for color in colors:

        row = {"Color": color}

        for size in sizes:
            row[size] = split_data[color][size]

        table_data.append(row)

    df = pd.DataFrame(table_data)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ------------------------------------------------
    # PACKING RESULTS
    # ------------------------------------------------

    st.markdown("### Packing Instructions")

    excel_rows = []

    for r in results:

        st.markdown(
            f"""
            <div style="
            background-color:white;
            padding:20px;
            border-radius:10px;
            border-left:6px solid #154c79;
            margin-bottom:15px;
            ">

            <h3>Size {r['size'].upper()}</h3>

            <b>True Combo</b><br>
            Boxes: {r['true_boxes']}<br>
            Structure: {r['true_structure']}

            </div>
            """,
            unsafe_allow_html=True
        )

        excel_rows.append({
            "Order ID": order_id,
            "Size": r["size"],
            "Type": "True Combo",
            "Boxes": r["true_boxes"],
            "Structure": r["true_structure"]
        })

        if r["secondary"]:

            st.warning("Secondary Combination")

            for s in r["secondary"]:

                st.write(f"Boxes: {s['boxes']}")
                st.write(f"Structure: {s['structure']}")

                excel_rows.append({
                    "Order ID": order_id,
                    "Size": r["size"],
                    "Type": "Secondary",
                    "Boxes": s["boxes"],
                    "Structure": s["structure"]
                })

        st.markdown("**Remaining Pieces**")

        for color, qty in r["remaining"].items():
            st.write(f"{color}: {qty}")

        st.divider()

    # ------------------------------------------------
    # EXPORT TO EXCEL
    # ------------------------------------------------

    excel_df = pd.DataFrame(excel_rows)

    file_name = f"Packing_Plan_{order_id}.xlsx"

    excel_df.to_excel(file_name, index=False)

    with open(file_name, "rb") as f:

        st.download_button(
            label="Download Packing Plan (Excel)",
            data=f,
            file_name=file_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# ------------------------------------------------
# FOOTER
# ------------------------------------------------

st.markdown("---")
st.markdown("Menology Packing Planning System")