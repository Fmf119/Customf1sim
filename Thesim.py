import streamlit as st
import pandas as pd
import random
import pickle
import os

# Initial Setup for data storage
if 'teams' not in st.session_state:
    st.session_state.teams = {}
if 'drivers' not in st.session_state:
    st.session_state.drivers = {}
if 'hall_of_fame' not in st.session_state:
    st.session_state.hall_of_fame = []
if 'former_teams' not in st.session_state:
    st.session_state.former_teams = []

# Define a driver class for stats management
class Driver:
    def __init__(self, name, nationality, age, stats=None):
        self.name = name
        self.nationality = nationality
        self.age = age
        self.stats = stats or {'overall': 0, 'racecraft': 0, 'overtaking': 0, 'iq': 0, 'focus': 0, 'potential': 0}
        self.retired = False
        self.retirement_reason = None
        self.wdc_count = 0
        self.constructor_champs = 0

    def update_stats(self, stats):
        self.stats.update(stats)

    def retire(self, reason):
        self.retired = True
        self.retirement_reason = reason

    def add_to_hall_of_fame(self):
        st.session_state.hall_of_fame.append({
            'name': self.name,
            'wdc_count': self.wdc_count,
            'constructor_champs': self.constructor_champs,
            'age_retired': self.age
        })

# Function to simulate a race and award WDC and Constructor's Championship
def simulate_race():
    wdc_winner = random.choice(list(st.session_state.drivers.values()))
    constructor_winner = random.choice(list(st.session_state.teams.values()))
    wdc_winner.wdc_count += 1
    return wdc_winner, constructor_winner

# UI to add teams
def add_team():
    team_name = st.text_input('Enter team name')
    nationality = st.text_input('Enter team nationality')
    if st.button('Add Team'):
        st.session_state.teams[team_name] = {'name': team_name, 'nationality': nationality, 'drivers': []}
        st.success(f'Team {team_name} added!')

# UI to add drivers
def add_driver():
    driver_name = st.text_input('Enter driver name')
    nationality = st.text_input('Enter driver nationality')
    age = st.number_input('Enter driver age', min_value=18, max_value=100)
    if st.button('Add Driver'):
        new_driver = Driver(driver_name, nationality, age)
        st.session_state.drivers[driver_name] = new_driver
        st.success(f'Driver {driver_name} added!')

# UI to assign driver to team
def assign_driver_to_team():
    driver_name = st.selectbox('Select Driver', list(st.session_state.drivers.keys()))
    team_name = st.selectbox('Select Team', list(st.session_state.teams.keys()))
    if st.button('Assign Driver to Team'):
        st.session_state.teams[team_name]['drivers'].append(st.session_state.drivers[driver_name])
        st.success(f'{driver_name} assigned to {team_name}!')

# View driver profile
def view_driver_profile():
    driver_name = st.selectbox('Select Driver to View Profile', list(st.session_state.drivers.keys()))
    driver = st.session_state.drivers[driver_name]
    st.write(f"Name: {driver.name}")
    st.write(f"Age: {driver.age}")
    st.write(f"Nationality: {driver.nationality}")
    st.write(f"Overall Rating: {driver.stats['overall']}")
    st.write(f"Racecraft: {driver.stats['racecraft']}")
    st.write(f"Overtaking: {driver.stats['overtaking']}")
    st.write(f"IQ: {driver.stats['iq']}")
    st.write(f"Focus: {driver.stats['focus']}")
    st.write(f"Potential: {driver.stats['potential']}")
    st.write(f"Retired: {driver.retired}")
    if driver.retired:
        st.write(f"Retirement Reason: {driver.retirement_reason}")
    update_stats = st.checkbox('Update Stats')
    if update_stats:
        stats = {
            'overall': st.slider('Overall', 0, 100, driver.stats['overall']),
            'racecraft': st.slider('Racecraft', 0, 100, driver.stats['racecraft']),
            'overtaking': st.slider('Overtaking', 0, 100, driver.stats['overtaking']),
            'iq': st.slider('IQ', 0, 100, driver.stats['iq']),
            'focus': st.slider('Focus', 0, 100, driver.stats['focus']),
            'potential': st.slider('Potential', 0, 100, driver.stats['potential']),
        }
        if st.button('Save Stats'):
            driver.update_stats(stats)
            st.success('Stats updated successfully!')
    
    if st.button('Retire Driver'):
        reason = st.text_input('Reason for Retirement')
        driver.retire(reason)
        st.success(f'{driver_name} has retired for the following reason: {reason}')

# UI for Hall of Fame
def hall_of_fame():
    st.write("Hall of Fame")
    if st.session_state.hall_of_fame:
        for driver in st.session_state.hall_of_fame:
            st.write(f"Name: {driver['name']}, WDCs: {driver['wdc_count']}, Constructor Championships: {driver['constructor_champs']}, Retired Age: {driver['age_retired']}")
    else:
        st.write("No drivers in Hall of Fame yet.")

# UI for Team Championship totals
def team_championship_totals():
    st.write("Team Championship Totals")
    for team in st.session_state.teams.values():
        st.write(f"Team: {team['name']} - Drivers: {len(team['drivers'])}")

# View and interact with teams
def view_teams():
    st.write("View Teams")
    for team in st.session_state.teams.values():
        st.write(f"Team: {team['name']}, Nationality: {team['nationality']}")
        for driver in team['drivers']:
            st.write(f"  Driver: {driver.name}, Nationality: {driver.nationality}")

# View Former Teams
def former_teams():
    st.write("Former Teams")
    for team in st.session_state.former_teams:
        st.write(f"Team: {team['name']}, Nationality: {team['nationality']}")

# Simulate a race
def simulate():
    st.write("Simulating Race...")
    wdc_winner, constructor_winner = simulate_race()
    st.write(f"WDC Winner: {wdc_winner.name}!")
    st.write(f"Constructor's Champion: {constructor_winner['name']}!")

# Save data locally
def save_data():
    data = {
        'teams': st.session_state.teams,
        'drivers': st.session_state.drivers,
        'hall_of_fame': st.session_state.hall_of_fame,
        'former_teams': st.session_state.former_teams
    }
    file_path = 'f1_simulation_data.pkl'
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)
    with open(file_path, "rb") as file:
        st.download_button(label="Download F1 Simulation Data", data=file, file_name="f1_simulation_data.pkl", mime="application/octet-stream")
    st.success("Data saved!")

# Load data from a file
def load_data():
    uploaded_file = st.file_uploader("Upload saved F1 simulation data", type=["pkl"])
    if uploaded_file is not None:
        with open("f1_simulation_data.pkl", "wb") as f:
            f.write(uploaded_file.read())
        with open("f1_simulation_data.pkl", "rb") as f:
            data = pickle.load(f)
            st.session_state.teams = data['teams']
            st.session_state.drivers = data['drivers']
            st.session_state.hall_of_fame = data['hall_of_fame']
            st.session_state.former_teams = data['former_teams']
        st.success("Data loaded successfully!")

# Main menu for navigation
def main_menu():
    menu = ['Add Teams', 'Add Drivers', 'Hall of Fame', 'Team Championship Totals', 'View Teams', 'Former Teams', 'Simulate', 'Save Data', 'Load Data']
    choice = st.sidebar.selectbox("Select an Option", menu)

    if choice == 'Add Teams':
        add_team()
    elif choice == 'Add Drivers':
        add_driver()
    elif choice == 'Hall of Fame':
        hall_of_fame()
    elif choice == 'Team Championship Totals':
        team_championship_totals()
    elif choice == 'View Teams':
        view_teams()
    elif choice == 'Former Teams':
        former_teams()
    elif choice == 'Simulate':
        simulate()
    elif choice == 'Save Data':
        save_data()
    elif choice == 'Load Data':
        load_data()

if __name__ == "__main__":
    main_menu()
