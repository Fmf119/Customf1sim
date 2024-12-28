import streamlit as st
import random

# Initialize session state to store the data
if 'teams' not in st.session_state:
    st.session_state.teams = []
if 'drivers' not in st.session_state:
    st.session_state.drivers = []
if 'hall_of_fame' not in st.session_state:
    st.session_state.hall_of_fame = []
if 'former_teams' not in st.session_state:
    st.session_state.former_teams = []

# Function to add teams
def add_team():
    team_name = st.text_input("Enter team name:")
    nationality = st.text_input("Enter team nationality:")
    if st.button("Add Team"):
        if team_name:
            st.session_state.teams.append({'name': team_name, 'nationality': nationality, 'drivers': [], 'bankrupt': False})
            st.success(f"Team {team_name} added!")

# Function to add drivers
def add_driver():
    driver_name = st.text_input("Enter driver name:")
    nationality = st.text_input("Enter driver's nationality:")
    age = st.number_input("Enter driver's age", min_value=18, max_value=100, value=18)
    racecraft = st.slider("Racecraft", 1, 100)
    overtaking = st.slider("Overtaking", 1, 100)
    iq = st.slider("IQ", 1, 100)
    focus = st.slider("Focus", 1, 100)
    potential = st.slider("Potential", 1, 100)
    
    team_name = st.selectbox("Choose a team", [team['name'] for team in st.session_state.teams if not team['bankrupt']])

    if st.button("Add Driver"):
        if driver_name and nationality and team_name:
            driver = {
                'name': driver_name,
                'nationality': nationality,
                'age': age,
                'stats': {'racecraft': racecraft, 'overtaking': overtaking, 'iq': iq, 'focus': focus, 'potential': potential},
                'team': team_name,
                'retired': False,
                'retirement_reason': None,
                'wdcs': 0,
                'constructor_championships': 0
            }
            # Add driver to team
            for team in st.session_state.teams:
                if team['name'] == team_name:
                    team['drivers'].append(driver)
            st.session_state.drivers.append(driver)
            st.success(f"Driver {driver_name} added to team {team_name}!")

# Show driver profile
def show_driver_profile():
    driver_name = st.selectbox("Select a driver to view profile", [driver['name'] for driver in st.session_state.drivers])
    for driver in st.session_state.drivers:
        if driver['name'] == driver_name:
            st.write(f"Name: {driver['name']}")
            st.write(f"Nationality: {driver['nationality']}")
            st.write(f"Age: {driver['age']}")
            st.write(f"Racecraft: {driver['stats']['racecraft']}")
            st.write(f"Overtaking: {driver['stats']['overtaking']}")
            st.write(f"IQ: {driver['stats']['iq']}")
            st.write(f"Focus: {driver['stats']['focus']}")
            st.write(f"Potential: {driver['stats']['potential']}")
            if driver['retired']:
                st.write(f"Retired: Yes, at age {driver['age']} due to {driver['retirement_reason']}")
            else:
                st.write(f"Retired: No")

# Retire a driver
def retire_driver():
    driver_name = st.selectbox("Select a driver to retire", [driver['name'] for driver in st.session_state.drivers if not driver['retired']])
    retirement_reason = st.text_input("Enter retirement reason:")
    
    if st.button("Retire Driver"):
        for driver in st.session_state.drivers:
            if driver['name'] == driver_name:
                driver['retired'] = True
                driver['retirement_reason'] = retirement_reason
                st.success(f"Driver {driver_name} has retired!")

# Add driver to hall of fame
def add_to_hall_of_fame():
    driver_name = st.selectbox("Select a driver to add to Hall of Fame", [driver['name'] for driver in st.session_state.drivers if not driver['retired']])
    
    if st.button("Add to Hall of Fame"):
        for driver in st.session_state.drivers:
            if driver['name'] == driver_name:
                st.session_state.hall_of_fame.append({
                    'name': driver['name'],
                    'wdcs': driver['wdcs'],
                    'constructor_championships': driver['constructor_championships'],
                    'retirement_age': driver['age']
                })
                st.success(f"Driver {driver_name} added to Hall of Fame!")

# Simulate a season
def simulate():
    # Increase drivers' ages
    for driver in st.session_state.drivers:
        if not driver['retired']:
            driver['age'] += 1
    
    # Simulate WDC and Constructors Championship
    winner_driver = random.choice(st.session_state.drivers)
    winner_team = next(team for team in st.session_state.teams if team['name'] == winner_driver['team'])

    winner_driver['wdcs'] += 1
    winner_team['constructor_championships'] += 1

    st.write(f"The WDC winner is {winner_driver['name']}!")
    st.write(f"The Constructors' Champion is {winner_team['name']}!")

# Force a team into bankruptcy
def bankrupt_team():
    team_name = st.selectbox("Select a team to bankrupt", [team['name'] for team in st.session_state.teams if not team['bankrupt']])
    
    if st.button("Force Bankruptcy"):
        for team in st.session_state.teams:
            if team['name'] == team_name:
                team['bankrupt'] = True
                st.session_state.former_teams.append(team)
                st.success(f"Team {team_name} has gone bankrupt!")

# Page layout
def main():
    menu = ["Add Teams", "Add Drivers", "Hall of Fame", "Team Championship Totals", "View Teams", "Former Teams", "Simulate"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Teams":
        add_team()
    elif choice == "Add Drivers":
        add_driver()
    elif choice == "Hall of Fame":
        if len(st.session_state.hall_of_fame) > 0:
            for member in st.session_state.hall_of_fame:
                st.write(f"Name: {member['name']}, WDCs: {member['wdcs']}, Constructor Championships: {member['constructor_championships']}, Retirement Age: {member['retirement_age']}")
        else:
            st.write("Hall of Fame is empty!")
    elif choice == "Team Championship Totals":
        for team in st.session_state.teams:
            st.write(f"Team {team['name']}: {len(team['drivers'])} drivers, Championships: {team['constructor_championships']}")
    elif choice == "View Teams":
        for team in st.session_state.teams:
            st.write(f"Team: {team['name']}, Nationality: {team['nationality']}")
            for driver in team['drivers']:
                st.write(f"  - {driver['name']}")
    elif choice == "Former Teams":
        for team in st.session_state.former_teams:
            st.write(f"Former Team: {team['name']}")
    elif choice == "Simulate":
        simulate()

    # Additional actions
    if choice == "Add Drivers":
        st.write("---")
        show_driver_profile()
        st.write("---")
        retire_driver()
        st.write("---")
        add_to_hall_of_fame()
        st.write("---")
        bankrupt_team()

if __name__ == '__main__':
    main()
