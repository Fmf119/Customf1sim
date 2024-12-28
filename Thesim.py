import streamlit as st
import random
import pickle
import os

# File paths for saving data
DATA_FILES = {
    'teams': 'teams.pkl',
    'drivers': 'drivers.pkl',
    'hall_of_fame': 'hall_of_fame.pkl',
    'former_teams': 'former_teams.pkl',
    'tracks': 'tracks.pkl'
}

# Initialize session state to store the data
def init_data():
    for key in ['teams', 'drivers', 'hall_of_fame', 'former_teams', 'tracks']:
        if key not in st.session_state:
            st.session_state[key] = []

init_data()

# Save progress to files
def save_progress():
    for key, file_path in DATA_FILES.items():
        with open(file_path, 'wb') as f:
            pickle.dump(st.session_state[key], f)
    st.success("Progress saved!")

# Load progress from files
def load_progress():
    for key, file_path in DATA_FILES.items():
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                st.session_state[key] = pickle.load(f)
    st.success("Progress loaded!")

# Save progress locally
def save_to_device():
    for key in st.session_state:
        if key in DATA_FILES:
            st.download_button(
                label=f"Download {key.capitalize()} Data",
                data=pickle.dumps(st.session_state[key]),
                file_name=f"{key}.pkl",
                mime="application/octet-stream"
            )

# Load progress from local file
def load_from_device(file, key):
    if file is not None:
        st.session_state[key] = pickle.loads(file.read())
        st.success(f"{key.capitalize()} data loaded from file!")

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
            overall = (racecraft + overtaking + iq + focus + potential) / 5
            driver = {
                'name': driver_name,
                'nationality': nationality,
                'age': age,
                'stats': {'racecraft': racecraft, 'overtaking': overtaking, 'iq': iq, 'focus': focus, 'potential': potential, 'overall': overall},
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

# Transfer drivers between teams
def transfer_driver():
    driver_name = st.selectbox("Select a driver to transfer", [driver['name'] for driver in st.session_state.drivers if not driver['retired']])
    new_team = st.selectbox("Select new team", [team['name'] for team in st.session_state.teams if not team['bankrupt']])
    
    if st.button("Transfer Driver"):
        for driver in st.session_state.drivers:
            if driver['name'] == driver_name:
                old_team = driver['team']
                driver['team'] = new_team
                # Update teams
                for team in st.session_state.teams:
                    if team['name'] == old_team:
                        team['drivers'] = [d for d in team['drivers'] if d['name'] != driver_name]
                    if team['name'] == new_team:
                        team['drivers'].append(driver)
                st.success(f"Driver {driver_name} transferred to {new_team}!")

# Add race tracks
def add_track():
    track_name = st.text_input("Enter track name:")
    location = st.text_input("Enter track location:")
    if st.button("Add Track"):
        if track_name and location:
            st.session_state.tracks.append({'name': track_name, 'location': location})
            st.success(f"Track {track_name} in {location} added!")

# Hall of Fame
def hall_of_fame():
    if len(st.session_state.hall_of_fame) > 0:
        for member in st.session_state.hall_of_fame:
            st.write(f"Name: {member['name']}, WDCs: {member['wdcs']}, Constructor Championships: {member['constructor_championships']}, Retirement Age: {member['retirement_age']}, Reason: {member.get('retirement_reason', 'N/A')}")
    else:
        st.write("Hall of Fame is empty!")

# Simulate a season
def simulate():
    # Increase drivers' ages
    for driver in st.session_state.drivers:
        if not driver['retired']:
            driver['age'] += 1
    
    # Simulate WDC and Constructors Championship
    winner_driver = random.choice([d for d in st.session_state.drivers if not d['retired']])
    winner_team = next(team for team in st.session_state.teams if team['name'] == winner_driver['team'])

    winner_driver['wdcs'] += 1
    winner_team['constructor_championships'] = winner_team.get('constructor_championships', 0) + 1

    st.write(f"The WDC winner is {winner_driver['name']}!")
    st.write(f"The Constructors' Champion is {winner_team['name']}!")

# Page layout
def main():
    menu = ["Add Teams", "Add Drivers", "Hall of Fame", "Add Tracks", "Team Championship Totals", "View Teams", "Former Teams", "Transfer Drivers", "Simulate", "Save/Load Progress"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Teams":
        add_team()
    elif choice == "Add Drivers":
        add_driver()
    elif choice == "Transfer Drivers":
        transfer_driver()
    elif choice == "Add Tracks":
        add_track()
    elif choice == "Hall of Fame":
        hall_of_fame()
    elif choice == "Team Championship Totals":
        for team in st.session_state.teams:
            st.write(f"Team {team['name']}: {len(team['drivers'])} drivers, Championships: {team.get('constructor_championships', 0)}")
    elif choice == "View Teams":
        for team in st.session_state.teams:
            st.write(f"Team: {team['name']}, Nationality: {team['nationality']}")
            for driver in team['drivers']:
                st.write(f"  - {driver['name']}: {driver['stats']['overall']:.2f} Overall Rating")
    elif choice == "Former Teams":
        for team in st.session_state.former_teams:
            st.write(f"Former Team: {team['name']}")
    elif choice == "Simulate":
        simulate()
    elif choice == "Save/Load Progress":
        if st.button("Save Progress"):
            save_progress()
        if st.button("Load Progress"):
            load_progress()
        st.write("---")
        st.file_uploader("Load from Device", type=["pkl"], key="file")
        for key in DATA_FILES:
            load_from_device(st.session_state.get("file"), key)
        st.write("---")
        save_to_device()

if __name__ == '__main__':
    main()
