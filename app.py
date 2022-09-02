## Import packages
import numpy as np
import pandas as pd
import pydeck as pdk
import geopandas as gpd
import streamlit as st
import json
import urllib
from urllib import request

st.set_page_config(layout="wide")


@st.cache(allow_output_mutation=True)
def load_data():
    # return pd.read_csv(r'C:\Users\David\django_project\streamlit_app\combined_df.csv')
    url = 'https://github.com/SH290596/test_small_area_streamlit_app/blob/main/data/small_area_data_v2.shp?raw=True'
    sf = urllib.request.urlretrieve(url, "small_area_data_v2.shp")
    shapefile = gpd.read_file(
        sf[0]
    )
    return shapefile


@st.cache(allow_output_mutation=True)
def load_json_data(map_df):
    test_json = json.loads(map_df.to_json())
    json_data = json.dumps(test_json)

    j = pd.read_json(json_data)
    # print(j)
    df = pd.DataFrame()
    df["coordinates"] = j["features"].apply(lambda row: row["geometry"]["coordinates"])
    df["ber_letter_rating"] = j["features"].apply(
        lambda row: row["properties"]["BER_Letter"]
    )
    df["Upgrade_Roof"] = j["features"].apply(
        lambda row: row["properties"]["Upgrade_Ro"]
    )
    df["Upgrade_Wall"] = j["features"].apply(
        lambda row: row["properties"]["Upgrade_Wa"]
    )
    df["Cavity_Wall_Count"] = j["features"].apply(
        lambda row: row["properties"]["Cavity_Wal"]
    )
    df["Wall_Count"] = j["features"].apply(lambda row: row["properties"]["Wall_Count"])
    df["Cavity_Wall_Check"] = j["features"].apply(
        lambda row: row["properties"]["Cavity_W_2"]
    )
    df["Open_Chimney_Count"] = j["features"].apply(
        lambda row: row["properties"]["Seal_Chimn"]
    )
    df["Chimney_Count"] = j["features"].apply(
        lambda row: row["properties"]["Chimney_Co"]
    )
    df["Open_Chimney_Check"] = j["features"].apply(
        lambda row: row["properties"]["Seal_Chi_2"]
    )
    df["SMALL_AREA"] = j["features"].apply(lambda row: row["properties"]["SMALL_AREA"])
    df["EDNAME"] = j["features"].apply(lambda row: row["properties"]["EDNAME"])
    df["Count_in_SA"] = j["features"].apply(lambda row: row["properties"]["Count_in_S"])

    ## Get color format for letter grades
    COLOR_RANGE = [
        [0, 88, 0],
        [7, 120, 6],
        [7, 153, 17],
        [75, 169, 62],
        [112, 185, 97],
        [145, 201, 131],
        [176, 217, 165],
        [197, 233, 132],
        [237, 243, 88],
        [246, 218, 50],
        [255, 192, 0],
        [255, 149, 0],
        [255, 102, 0],
        [235, 74, 34],
        [211, 47, 47],
    ]

    choices = [
        "A1",
        "A2",
        "A3",
        "B1",
        "B2",
        "B3",
        "C1",
        "C2",
        "C3",
        "D1",
        "D2",
        "E1",
        "E2",
        "F",
        "G",
    ]

    def color_scale(val):
        for i, b in enumerate(choices):
            if val == b:
                return COLOR_RANGE[i]
        return COLOR_RANGE[i]

    df["fill_color"] = df["ber_letter_rating"].apply(lambda row: color_scale(row))

    return df


# def load_data():
#     return pd.read_csv(r'C:\Users\David\django_project\streamlit_app\combined_df.csv')


def create_source(test_df, target_ber="", roof_insulation=""):
    test_df_interactive = test_df.copy()

    ## Always set inital value to no in order to not highlight
    test_df_interactive["highlight_field"] = "No"

    if (target_ber != "") & (roof_insulation == "Get Roof Insulated"):
        test_df_interactive["highlight_field"] = np.where(
            (test_df["ber_letter_rating"] == target_ber)
            & (test_df["Upgrade_Roof"] == "1"),
            "Yes",
            "No",
        )
    elif target_ber != "Current BER":
        test_df_interactive["highlight_field"] = np.where(
            (test_df["ber_letter_rating"] == target_ber), "Yes", "No"
        )
    elif roof_insulation == "Get Roof Insulated":
        test_df_interactive["highlight_field"] = np.where(
            (test_df["Upgrade_Roof"] == "1"),
            "Yes",
            test_df_interactive["highlight_field"],
        )
    else:
        pass

    test_df_interactive = test_df_interactive[
        test_df_interactive["highlight_field"] == "Yes"
    ]

    return test_df_interactive


def filter_based_on_current_ber(df, current_ber=""):
    test_df_interactive = df.copy()

    ## Always set inital value to no in order to not highlight
    test_df_interactive["highlight_field"] = "No"

    if current_ber != "Current BER":
        test_df_interactive["highlight_field"] = np.where(
            (df["ber_letter_rating"] == current_ber), "Yes", "No"
        )

        test_df_interactive = test_df_interactive[
            test_df_interactive["highlight_field"] == "Yes"
        ]

    else:
        pass

    return test_df_interactive


def filter_based_on_upgrade_roof(df, upgrade_roof=""):
    test_df_interactive = df.copy()

    if upgrade_roof != "No":
        test_df_interactive["highlight_field"] = np.where(
            (df["Upgrade_Roof"] == "1"), "Yes", "No"
        )

        test_df_interactive = test_df_interactive[
            test_df_interactive["highlight_field"] == "Yes"
        ]
    else:
        pass

    return test_df_interactive


def filter_based_on_upgrade_wall(df, upgrade_wall=""):
    test_df_interactive = df.copy()

    if upgrade_wall != "No":
        test_df_interactive["highlight_field"] = np.where(
            (df["Upgrade_Wall"] == "1"), "Yes", "No"
        )
        test_df_interactive = test_df_interactive[
            test_df_interactive["highlight_field"] == "Yes"
        ]
    else:
        pass

    return test_df_interactive


def filter_based_on_cavity_wall(df, cavity_wall=""):
    test_df_interactive = df.copy()

    if cavity_wall != "No":
        test_df_interactive["highlight_field"] = np.where(
            (df["Cavity_Wall_Check"] == "1"), "Yes", "No"
        )
    else:
        pass

    test_df_interactive = test_df_interactive[
        test_df_interactive["highlight_field"] == "Yes"
    ]
    return test_df_interactive


def filter_based_on_open_chimney(df, open_chimney=""):
    test_df_interactive = df.copy()

    if open_chimney != "No":
        test_df_interactive["highlight_field"] = np.where(
            (df["Open_Chimney_Check"] == "1"), "Yes", "No"
        )
    else:
        pass

    test_df_interactive = test_df_interactive[
        test_df_interactive["highlight_field"] == "Yes"
    ]
    return test_df_interactive


def app():

    bers = [
        "Current BER",
        "A1",
        "A2",
        "A3",
        "B1",
        "B2",
        "B3",
        "C1",
        "C2",
        "C3",
        "D1",
        "D2",
        "E1",
        "E2",
        "F",
        "G",
    ]

    target_bers = [
        "Target BER",
        "A1",
        "A2",
        "A3",
        "B1",
        "B2",
        "B3",
        "C1",
        "C2",
        "C3",
        "D1",
        "D2",
        "E1",
        "E2",
        "F",
        "G",
    ]

    upgrades = [
        "Upgrade Option",
        "Get Roof Insulated",
        "Get Walls Insulated",
        "Boiler Upgrade",
    ]

    df = load_json_data(load_data())
    # df_json = load_data()
    co_ords = df["coordinates"].to_list()
    corrupted_coords_index = [i for i, x in enumerate(co_ords) if len(x) > 1]
    df = df.drop(corrupted_coords_index)

    st.markdown(
        "<h1 style='text-align: center; color: Black;'>Interactive BER Dashboard</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        """<p style='text-align: center;'><strong>Introduction: </strong>This interactive dashboard is designed for identifying the small area codes in Ireland 
        which would be good candidates for energy uprades.</p>,
    """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([2, 4, 4])

    with col1:
        st.subheader("Input Data")

        dropdown_option = ["No", "Yes"]

        target_ber = st.selectbox("Small Area code average BER", bers)
        # upgrade_option = st.selectbox("Upgrades Needed", upgrades)
        filter_for_roof = st.selectbox(
            "Majority of homes need their Roof Insulated", dropdown_option
        )
        filter_for_wall = st.selectbox(
            "Majority of homes need their Walls Insulated", dropdown_option
        )
        filter_for_cavity_wall = st.selectbox(
            "Majority of homes have cavity walls", dropdown_option
        )
        filter_for_chimney = st.selectbox(
            "Majority of homes have open chimney", dropdown_option
        )
        sa_targer_ber = st.selectbox("Target BER for Small Area code", target_bers)

    ## Filter Dataframe
    df["highlight_field"] = "No"
    # df_fil = create_source(df, target_ber, upgrade_option)
    df_fil = filter_based_on_current_ber(df, target_ber)
    df_fil = filter_based_on_upgrade_roof(df_fil, filter_for_roof)
    df_fil = filter_based_on_upgrade_wall(df_fil, filter_for_wall)
    df_fil = filter_based_on_cavity_wall(df_fil, filter_for_cavity_wall)
    df_fil = filter_based_on_open_chimney(df_fil, filter_for_chimney)

    best_retrofit_df = df_fil[
        [
            "EDNAME",
            "Cavity_Wall_Count",
            "Open_Chimney_Count",
            "Count_in_SA",
            "ber_letter_rating",
        ]
    ].sort_values(by=["Count_in_SA"], ascending=False)

    best_retrofit_df.rename(
        columns={
            "EDNAME": "Location",
            "Cavity_Wall_Count": "# Homes - Cavity Walls",
            "Open_Chimney_Count": "# Homes - Open Chimney",
            "Count_in_SA": "# Homes - Area",
            "ber_letter_rating": "Average BER",
        },
        inplace=True,
    )

    initial_view_state = pdk.ViewState(
        latitude=53.574449758314195,
        longitude=-6.106089702889869,
        zoom=5,
        max_zoom=16,
        pitch=0,
        bearing=0,
        height=600,
        width=None,
    )

    polygon_layer = pdk.Layer(
        "PolygonLayer",
        df_fil,
        get_polygon="coordinates",
        filled=True,
        get_fill_color=[225, 225, 0],
        auto_highlight=True,
        pickable=True,
        get_line_color=[0, 0, 0],
        get_line_width=2,
        line_width_min_pixels=1,
    )

    tooltip = {
        "html": """<b>SA Code:</b> {SMALL_AREA} <br /> 
                    <b>Location:</b> {EDNAME} <br/>
                    <b>BER:</b> {ber_letter_rating} <br />
                    <b>Upgrade Roof:</b> {Upgrade_Roof} <br/>
                    <b>Upgrade Walls:</b> {Upgrade_Wall} <br/>
                    <b># Homes that have cavity walls:</b> {Cavity_Wall_Count} <br/>
                    <b># Homes that have an open chimney:</b> {Open_Chimney_Count} <br/>
                    <b># Homes:</b> {Count_in_SA} <br/>"""
    }

    layers = [polygon_layer]

    r = pdk.Deck(
        layers=layers,
        initial_view_state=initial_view_state,
        map_style="light",
        tooltip=tooltip,
    )

    with col2:
        st.subheader("Interactive Map")
        st.pydeck_chart(r)

    with col3:
        st.subheader("Best Small Areas for Retrofit")

        # CSS to inject contained in a string
        hide_dataframe_row_index = """
                    <style>
                    .row_heading.level0 {display:none}
                    .blank {display:none}
                    </style>
                    """

        # Inject CSS with Markdown
        st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)

        best_retrofit_df["# Homes - Area"] = best_retrofit_df["# Homes - Area"].astype(
            int
        )

        best_retrofit_df["# Homes - Cavity Walls"] = best_retrofit_df[
            "# Homes - Cavity Walls"
        ].astype(int)
        best_retrofit_df["# Homes - Open Chimney"] = best_retrofit_df[
            "# Homes - Open Chimney"
        ].astype(int)

        st.dataframe(best_retrofit_df.head(10).round(0))

        st.markdown(
            """
        #### Number of SA that match critera is: <span>{temp1}</span>   
        """.format(
                temp1=len(df_fil)
            ),
            unsafe_allow_html=True,
        )

    st.markdown(
        """<h4 style='text-align: center;'>Map of Ireland Showing the distribution of BER ratings across Small Area Codes</h4>,
    """,
        unsafe_allow_html=True,
    )

    colored_map = df.dropna()

    polygon_layer_2 = pdk.Layer(
        "PolygonLayer",
        colored_map,
        get_polygon="coordinates",
        filled=True,
        get_fill_color="fill_color",
        auto_highlight=True,
        pickable=True,
        get_line_color=[0, 0, 0],
        get_line_width=2,
        line_width_min_pixels=1,
    )

    layers_2 = [polygon_layer_2]

    r_2 = pdk.Deck(
        layers=layers_2,
        initial_view_state=initial_view_state,
        map_style="light",
        tooltip=tooltip,
    )

    col4, col5, col6 = st.columns([2, 4, 4])

    with col5:
        st.pydeck_chart(r_2)


app()
