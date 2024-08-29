import streamlit as st
import mysql.connector

# Function to connect to the MySQL database
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="project"
    )

# Function to fetch data from the database
def fetch_data(query):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

# Functions to get distinct data for dropdowns
def get_route_names():
    query = "SELECT DISTINCT bus_route_name FROM project.bus_routes"
    return fetch_data(query)

def get_bus_names(route_name):
    query = f"SELECT DISTINCT bus_name FROM project.bus_routes WHERE bus_route_name='{route_name}'"
    return fetch_data(query)

def get_bus_types(route_name, busname):
    query = f"SELECT DISTINCT bus_type FROM project.bus_routes WHERE bus_route_name='{route_name}' AND bus_name='{busname}'"
    return fetch_data(query)

def get_departing_times(route_name, busname, bustype):
    query = f"""
    SELECT DISTINCT departing_time 
    FROM project.bus_routes 
    WHERE bus_route_name='{route_name}' 
    AND bus_name='{busname}' 
    AND bus_type='{bustype}'
    """
    return fetch_data(query)

# Fetch all information based on selections
def get_bus_info(route_name, busname, bustype, departing_time):
    query = f"""
    SELECT duration, reaching_time, star_rating, price, seat_availability
    FROM project.bus_routes 
    WHERE bus_route_name='{route_name}' 
    AND bus_name='{busname}' 
    AND bus_type='{bustype}'
    AND departing_time='{departing_time}'
    """
    return fetch_data(query)

# Streamlit Application UI
st.title(" GoBus Booking Application")

# Step 1: Select Bus Route
routes = get_route_names()
route_names = [route['bus_route_name'] for route in routes]
selected_route = st.selectbox("Select Bus Route", route_names)

# Step 2: Select Bus Name
if selected_route:
    buses = get_bus_names(selected_route)
    bus_names = [bus['bus_name'] for bus in buses]
    selected_bus = st.selectbox("Select Bus Name", bus_names)

# Step 3: Select Bus Type
if selected_bus:
    bus_types = get_bus_types(selected_route, selected_bus)
    bus_type_options = [bus_type['bus_type'] for bus_type in bus_types]
    selected_bus_type = st.selectbox("Select Bus Type", bus_type_options)

# Step 4: Select Departing Time
if selected_bus_type:
    departing_times = get_departing_times(selected_route, selected_bus, selected_bus_type)
    departing_time_options = [time['departing_time'] for time in departing_times]
    selected_departing_time = st.selectbox("Select Departing Time", departing_time_options)

# Step 5: Display Bus Information and Book
if selected_departing_time:
    bus_info = get_bus_info(selected_route, selected_bus, selected_bus_type, selected_departing_time)
    
    if bus_info:
        st.subheader("Bus Details")
        st.write("Duration:", bus_info[0]['duration'])
        st.write("Reaching Time:", bus_info[0]['reaching_time'])
        st.write("Star Rating:", bus_info[0]['star_rating'])
        st.write("Price: ₹", bus_info[0]['price'])
        st.write("Seats Available:", bus_info[0]['seat_availability'])
        
        # Step 6: Book Now Button
        if bus_info[0]['seat_availability'] > 0:
            if st.button("Book Now"):
                st.success(f"Booking successful for {selected_bus} on route {selected_route} at {selected_departing_time}!")
        else:
            st.error("No seats available for this bus.")
    else:
        st.write("No data available for the selected options.")
