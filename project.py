"""
Name: Nicklas Widodo
CS230: Section 6
Data: Cannabis Registry
URL:

Description:
    This program is used to locate the different types of Cannabis Retailers and Cannabis establishments in Boston.
    Throughout the program it shows the locations of dispenseries and the users are able to find locations using their zip code, license or name.
    Lastly this program also outputs the types of Dispenseries and the total data analytics of Dispensaries in Boston.
"""

import matplotlib.pyplot as plt
import pandas as pd
import pydeck as pdk
import streamlit as st

st.title("Massachusetts Cannabis Licenses")
pd.set_option("display.max_rows", None, "display.max_columns", None, 'display.width', None, 'max_colwidth', None)

license_type = {'Retail', 'Cultivate', 'Manufact', 'Operator', 'Co-Located', 'Courier', 'TestLab', 'Transport',
                'Medical'}

# Function to load data
def load_data():
    df_cannabis = pd.read_csv('/Users/nicklasw69/Desktop/CS230 - Python/project/cannabis_registry.csv')
    return df_cannabis

#Find Dispensary Near You Page
def find_dispen():
    st.title("Find a Dispensary Near You")

    # Select search method using a dropdown
    search_method = st.radio("Select search method:", ["Zip Code", "License Number", "Dispensary Name"])
    #Slider for map zoom
    zoom_level = st.sidebar.slider("Please select the zoom level", 0.0, 15.0, 10.0)

    license_list = list(license_type)
    selected_license = st.selectbox("Select License:", ["All"] + license_list)

    if search_method == "Zip Code":
        user_input = st.text_input("Enter your Zip Code:")

        if st.button("Search"):
            if user_input:
                df_cannabis = load_data()
                # Filter by selected license if one is chosen
                if selected_license != "All":
                    df_near_you = df_cannabis[(df_cannabis['facility_zip_code'] == float(user_input)) & (df_cannabis['app_license_category'] == selected_license)][
                        ["app_license_category", "app_business_name", "facility_address", "latitude", "longitude"]]
                else:
                    df_near_you = df_cannabis[df_cannabis['facility_zip_code'] == float(user_input)][
                        ["app_license_category", "app_business_name", "facility_address", "latitude", "longitude"]]

                st.dataframe(df_near_you)
                # Show Scatterplot map based on the search results
                show_scatter_map(df_near_you,zoom_level)

            else:
                st.text("Please enter a Zip Code.")

    elif search_method == "License Number":
        user_input = st.text_input("Enter license number:")

        if st.button("Search"):
            if user_input:

                df_cannabis = load_data()

                if selected_license != "All":
                    df_near_you = df_cannabis[(df_cannabis['app_license_no'] == str(user_input)) & (df_cannabis['app_license_category'] == selected_license)][
                        ["app_license_category", "app_business_name", "facility_address", "latitude", "longitude"]]
                else:
                    df_near_you = df_cannabis[df_cannabis['app_license_no'] == str(user_input)][
                        ["app_license_category", "app_business_name", "facility_address", "latitude", "longitude"]]

                st.dataframe(df_near_you)
                # Show Scatterplot map based on the search results
                show_scatter_map(df_near_you,zoom_level)

            else:
                st.text("Please enter a License Number.")

    elif search_method == "Dispensary Name":
        user_input = st.text_input("Enter a Dispensary name:")

        if st.button("Search"):
            if user_input:
                df_cannabis = load_data()

                if selected_license != "All":
                    df_near_you = df_cannabis[(df_cannabis['app_business_name'].str.lower().str.contains(user_input.lower(), na=False)) & (df_cannabis['app_license_category'] == selected_license)][
                        ["app_license_category", "app_business_name", "facility_address", "latitude", "longitude"]]
                else:
                    df_near_you = df_cannabis[df_cannabis['app_business_name'].str.lower().str.contains(user_input.lower(), na=False)][
                        ["app_license_category", "app_business_name", "facility_address", "latitude", "longitude"]]

                st.dataframe(df_near_you)

                show_scatter_map(df_near_you,zoom_level)

            else:
                st.text("Please enter a Dispensary Name.")

def show_scatter_map(df_cannabis, zoom_level):
    st.subheader("Scatterplot map")

    # Create custom icons
    ICON_URL = "https://upload.wikimedia.org/wikipedia/commons/4/44/Cannabis_leaf_2.svg"


    # Format your icon
    icon_data = {
        "url": ICON_URL,
        "width": 100,
        "height": 100,
        "anchorY": 1
    }

    # Add icons to your dataframe
    df_cannabis["icon_data"] = [icon_data for i in df_cannabis.index]

    # Create a layer with your custom icon
    icon_layer = pdk.Layer(type="IconLayer",
                           data=df_cannabis,
                           get_icon="icon_data",
                           get_position=['longitude','latitude'],
                           get_size=3,
                           size_scale=10,
                           pickable=True)

    view_state = pdk.ViewState(
        latitude=df_cannabis['latitude'].mean(),
        longitude=df_cannabis['longitude'].mean(),
        zoom=zoom_level,
        pitch=0
    )


    # stylish tool tip: https://pydeck.gl/tooltip.html?highlight=tooltip
    tool_tip = {"html": "Dispensary Address <br/> <b>{facility_address}</b> <br/> <b>{app_business_name}",
                "style": {"backgroundColor": "dark green",
                          "color": "white"}
                }

    icon_map = pdk.Deck(
        map_style='mapbox://styles/mapbox/navigation-day-v1',
        layers=[icon_layer],
        initial_view_state=view_state,
        tooltip=tool_tip
    )

    st.pydeck_chart(icon_map)



#Types of Dispensaries Page
def type_dispen():
    st.set_option('deprecation.showPyplotGlobalUse', False)

    st.title("Types of Dispensaries")
# first parameter and question to user
    st.subheader("What type of licensed Dispensary are you looking for?")
    st.write("\n**Retail:** Refers to businesses involved in the sale of cannabis products directly to consumers.\n"
         "\n**Cultivate:** Involves the cultivation or growing of cannabis plants, typically for later processing and distribution.\n"
         "\n**Manufact:** Pertains to establishments engaged in the manufacturing or processing of cannabis products.\n"
         "\n**Operator:** Describes entities or individuals involved in operating and managing cannabis-related facilities or businesses.\n"
         "\n**Co-Located:** Indicates establishments that house multiple types of cannabis-related operations or businesses in a shared space.\n"
         "\n**Courier:** Involves delivery services that transport cannabis products from suppliers to consumers.\n"
         "\n**TestLab:** Represents laboratories responsible for testing and analyzing cannabis products for quality, safety, and compliance.\n"
         "\n**Transport:** Refers to companies engaged in the transportation of cannabis products between different locations.\n"
         "\n**Medical:** Pertains to facilities and services specifically focused on the medical use of cannabis for therapeutic purposes.")
def selected_license_type():
    selected_license = st.selectbox("Select the type of cannabis license", license_type)
    zoom_level = st.sidebar.slider("Please select the zoom level", 0.0, 15.0, 10.0)

    df_cannabis = load_data()

    df1 = df_cannabis[df_cannabis.app_license_category == selected_license][["app_license_category","app_business_name","facility_address","latitude","longitude"]]

    st.dataframe(df1)

    st.subheader("User Inputed Data")
    show_scatter_map(df1, zoom_level=zoom_level)
    show_bar_graph_based_on_town(df1)


def extract_town(facility_address):
    if pd.notna(facility_address):  # Check if the address is not NaN
        parts = facility_address.split(', ')
        if len(parts) > 1:
            return parts[-1]
    return None

# Function to show bar graph based on the town
def show_bar_graph_based_on_town(df1):
    # Add a new column for the town
    df1['Town'] = df1['facility_address'].apply(extract_town)

    # Count occurrences of each town in the DataFrame
    town_counts = df1['Town'].value_counts()

    # Plotting the bar graph
    plt.figure()
    town_counts.plot(kind='bar', color=["springgreen", "blue"])
    plt.xlabel('Town')
    plt.ylabel('Count')
    plt.title('Counts of Addresses by Town')
    st.pyplot()


#Total Dispensary Data Page
def bar_chart():
    df_sales = pd.read_csv("/Users/nicklasw69/Desktop/CS230 - Python/project/cannabis_registry.csv")
    df_sales = df_sales[df_sales['app_license_no'] != 'CAN538045']

    # Count occurrences of each app license category
    license_type_counts = df_sales['app_license_category'].value_counts()
    license_type_counts = license_type_counts.sort_values()

    # Plotting the horizontal bar chart
    license_type_counts.plot(kind="barh", color=["lime", "forestgreen"])
    plt.xlabel('Number of Stores')
    plt.ylabel('App License Category')
    plt.title('Number of Stores by App License Category')

    st.pyplot()

def pie_chart():
    df_pie = pd.read_csv("/Users/nicklasw69/Desktop/CS230 - Python/project/cannabis_registry.csv")
    df_pie = df_pie[df_pie['app_license_no'] != 'CAN538045']
    # Count of each app license category
    license_type_counts = df_pie['app_license_category'].value_counts()

    # Plotting the ring pie chart
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(license_type_counts, autopct="%1.1f%%", textprops=dict(color="white"), pctdistance=0.85,wedgeprops=dict(width=0.4), labels=None)

    # Create legend with percentages
    legend_labels = [f"{label} ({percent:.1f}%) " for label, percent in zip(license_type_counts.index, license_type_counts / license_type_counts.sum() * 100)]
    ax.legend(wedges, legend_labels, title='License Categories', bbox_to_anchor=(1, 0.5), loc="center left")

    # Set equal aspect ratio for a circle
    ax.axis('equal')

    plt.title('Distribution of App License Categories')

    st.pyplot()



# Main function
def main():

    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Go to", ["Home","Types of Dispensaries", "Find a Dispensary Near You","Total Dispensaries in Boston"])

    if page == "Home":
        st.subheader("Legalized Cannabis in MA")

        # Embed the YouTube video from youtube
        st.markdown(f'<iframe width="560" height="315" src="https://www.youtube.com/embed/X-9EGfJu5rM?si=Kz9a0H3HAVnuTI2T" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>',
                    unsafe_allow_html=True)
        st.image('/Users/nicklasw69/Desktop/CS230 - Python/project/cs230_image.jpeg',caption='Dispensary Store Front')

    elif page == "Find a Dispensary Near You":
        find_dispen()

    elif page == "Types of Dispensaries":
        type_dispen()
        selected_license_type()

    elif page == "Total Dispensaries in Boston":
        st.subheader("Data for All Boston Dispensaries")
        bar_chart()
        pie_chart()

if __name__ == "__main__":
    main()

