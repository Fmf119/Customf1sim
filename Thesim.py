import streamlit as st
import pickle
import os

# File path for saving all data
SAVE_FILE = "f1_simulation_data.pkl"

# Initialize session state to store the data
def init_data():
    if 'data' not in st.session_state:
        st.session_state['data'] = {
            'teams': [],
            'drivers': [],
            'hall_of_fame': [],
            'former_teams': [],
            'tracks': [],
            'team_champions': []
        }

init_data()

# Save progress to a single file
def save_progress():
    with open(SAVE_FILE, 'wb') as f:
        pickle.dump(st.session_state['data'], f)
    st.success("Progress saved to device!")

# Load progress from a single file
def load_progress():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'rb') as f:
            st.session_state['data'] = pickle.load(f)
        st.success("Progress loaded!")
    else:
        st.warning("No save file found!")

# Save progress locally for download
def save_to_device():
    data = pickle.dumps(st.session_state['data'])
    st.download_button(
        label="Download Save File",
        data=data,
        file_name="f1_simulation_data.pkl",
        mime="application/octet-stream"
    )

# Load progress from a local file
def load_from_device(file):
    if file is not None:
        st.session_state['data'] = pickle.loads(file.read())
        st.success("Progress loaded from file!")

# Function to add teams
def add_team():
    team_name = st.text_input("Enter team name:")
    nationality = st.text_input("Enter team nationality:")
    if st.button("Add Team"):
        if team_name:
            st.session_state['data']['teams'].append({'name': team_name, 'nationality': nationality, 'drivers': [], 'bankrupt': False, 'championships': 0})
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
    
    team_name = st.selectbox("Choose a team", [team['name'] for team in st.session_state['data']['teams'] if not team['bankrupt']])

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
            for team in st.session_state['data']['teams']:
                if team['name'] == team_name:
                    team['drivers'].append(driver)
            st.session_state['data']['drivers'].append(driver)
            st.success(f"Driver {driver_name} added to team {team_name}!")

# Simulate a season
def simulate():
    # Increase drivers' ages
    for driver in st.session_state['data']['drivers']:
        if not driver['retired']:
            driver['age'] += 1
    
    # Simulate WDC and Constructors Championship
    active_drivers = [d for d in st.session_state['data']['drivers'] if not d['retired']]
    if not active_drivers:
        st.error("No active drivers to simulate!")
        return
    
    winner_driver = random.choice(active_drivers)
    winner_team = next(team for team in st.session_state['data']['teams'] if team['name'] == winner_driver['team'])

    winner_driver['wdcs'] += 1
    winner_team['championships'] += 1

    st.session_state['data']['team_champions'].append({
        'year': len(st.session_state['data']['team_champions']) + 1,
        'team': winner_team['name'],
        'driver': winner_driver['name']
    })

    st.success(f"The WDC winner is {winner_driver['name']}!")
    st.success(f"The Constructors' Champion is {winner_team['name']}!")

# Page layout
def main():
    menu = ["Add Teams", "Add Drivers", "Hall of Fame", "Simulate", "Save/Load Progress"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Teams":
        add_team()
    elif choice == "Add Drivers":
        add_driver()
    elif choice == "Hall of Fame":
        for member in st.session_state['data']['hall_of_fame']:
            st.write(f"Name: {member['name']}, WDCs: {member['wdcs']}, Constructor Championships: {member['constructor_championships']}, Retirement Age: {member['retirement_age']}, Reason: {member.get('retirement_reason', 'N/A')}")
    elif choice == "Simulate":
        simulate()
    elif choice == "Save/Load Progress":
        if st.button("Save Progress"):
            save_progress()
        if st.button("Load Progress"):
            load_progress()
        st.write("---")
        file = st.file_uploader("Load from Device", type=["pkl"])
        if file:
            load_from_device(file)
        st.write("---")
        save_to_device()

if __name__ == '__main__':
    main()
