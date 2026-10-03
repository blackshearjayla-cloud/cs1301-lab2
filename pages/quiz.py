import os
import streamlit as st

st.set_page_config(page_title="CS Career Quiz", page_icon="💻")

# ---------------------------------------------------------------
# Helper: show an image if the file exists in your project folder
# (put your images in the same folder as this file or an images/ folder)
# ---------------------------------------------------------------
def show_image(path, caption):
    if os.path.exists(path):
        st.image(path, caption=caption, use_container_width=True)
    else:
        st.info(f"(Add an image named '{path}' to your project folder)")


st.title("💻 Which CS Career Path Fits You?")
show_image("Images/quiz_banner.png", "Let's find your path!")
st.write("Answer all 6 questions, then press **See my result**.")

# ---------------------------------------------------------------
# Questions
# ---------------------------------------------------------------

# Q1: multiple choice (single answer)
q1 = st.radio(  # NEW
    "1. What sounds like the best Saturday?",
    [
        "Designing a cool website",
        "Digging through a big dataset",
        "Solving a puzzle or CTF challenge",
        "Playing or building a game",
    ],
    index=None,
)

# Q2: dropdown
q2 = st.selectbox(  # NEW
    "2. What would you most like to build?",
    ["Choose one...", "A mobile app", "A prediction model", "An unhackable system", "A video game"],
)

# Q3: multi-select
q3 = st.multiselect(  # NEW
    "3. Which of these interest you? (pick all that apply)",
    ["Colors and layouts", "Statistics", "Encryption", "Storytelling", "Graphics and animation", "Patterns in data"],
)

# Q4: slider
q4 = st.slider(  # NEW
    "4. How much do you enjoy math? (0 = not at all, 10 = love it)",
    0, 10, 5,
)

# Q5: number input
q5 = st.number_input(  # NEW
    "5. How many hours would you debug before asking for help?",
    min_value=0, max_value=24, value=1, step=1,
)

# Q6: multiple choice (single answer)
q6 = st.radio(  # NEW
    "6. Pick a superpower:",
    ["Making things beautiful", "Seeing the future", "Invisibility", "Creating worlds"],
    index=None,
)

# ---------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------
RESULTS = {
    "Frontend Developer": {
        "image": "Images/frontend.png",
        "text": "You love making things look great and feel smooth. Look into web dev, UI/UX, and design systems.",
    },
    "Data Scientist": {
        "image": "Images/data.png",
        "text": "You find the story hiding in numbers. Look into machine learning, statistics, and data viz.",
    },
    "Cybersecurity Analyst": {
        "image": "Images/security.png",
        "text": "You like puzzles and protecting things. Look into security, networking, and cryptography.",
    },
    "Game Developer": {
        "image": "Images/game.png",
        "text": "You want to build whole worlds. Look into graphics, game engines, and interactive design.",
    },
}


BADGE_COLORS = {
    "Frontend Developer": "blue",
    "Data Scientist": "green",
    "Cybersecurity Analyst": "red",
    "Game Developer": "violet",
}

LEARNING_TIPS = {
    "Frontend Developer": ["Learn HTML, CSS and JavaScript", "Build a personal site", "Try a framework like React"],
    "Data Scientist": ["Practice with pandas and matplotlib", "Take a stats course", "Try a Kaggle dataset"],
    "Cybersecurity Analyst": ["Try beginner CTFs (picoCTF)", "Learn networking basics", "Study how encryption works"],
    "Game Developer": ["Try Unity or Godot", "Join a game jam", "Learn basic linear algebra for graphics"],
}


def calculate_result():
    scores = {name: 0 for name in RESULTS}

    # Q1
    q1_map = {
        "Designing a cool website": "Frontend Developer",
        "Digging through a big dataset": "Data Scientist",
        "Solving a puzzle or CTF challenge": "Cybersecurity Analyst",
        "Playing or building a game": "Game Developer",
    }
    if q1:
        scores[q1_map[q1]] += 2

    # Q2
    q2_map = {
        "A mobile app": "Frontend Developer",
        "A prediction model": "Data Scientist",
        "An unhackable system": "Cybersecurity Analyst",
        "A video game": "Game Developer",
    }
    if q2 in q2_map:
        scores[q2_map[q2]] += 2

    # Q3 (multi-select: 1 point per pick)
    q3_map = {
        "Colors and layouts": "Frontend Developer",
        "Statistics": "Data Scientist",
        "Patterns in data": "Data Scientist",
        "Encryption": "Cybersecurity Analyst",
        "Storytelling": "Game Developer",
        "Graphics and animation": "Game Developer",
    }
    for pick in q3:
        scores[q3_map[pick]] += 1

    # Q4 (slider)
    if q4 >= 7:
        scores["Data Scientist"] += 2
    elif q4 >= 4:
        scores["Cybersecurity Analyst"] += 1
    else:
        scores["Frontend Developer"] += 1

    # Q5 (number input)
    if q5 >= 5:
        scores["Cybersecurity Analyst"] += 2   # patient and persistent
    elif q5 >= 2:
        scores["Data Scientist"] += 1
    else:
        scores["Frontend Developer"] += 1
        scores["Game Developer"] += 1

    # Q6
    q6_map = {
        "Making things beautiful": "Frontend Developer",
        "Seeing the future": "Data Scientist",
        "Invisibility": "Cybersecurity Analyst",
        "Creating worlds": "Game Developer",
    }
    if q6:
        scores[q6_map[q6]] += 2

    return max(scores, key=scores.get), scores


# ---------------------------------------------------------------
# Submit + results
# ---------------------------------------------------------------
if st.button("See my result"):
    if q1 is None or q2 == "Choose one..." or q6 is None or len(q3) == 0:
        st.warning("Please answer every question first!")
    else:
        winner, scores = calculate_result()

        st.balloons()  # NEW
        st.toast(f"Result unlocked: {winner}!", icon="🎉")  # EXTRA CREDIT
        st.header(f"🎉 You're a {winner}!")
        st.badge(winner, icon="💻", color=BADGE_COLORS[winner])  # EXTRA CREDIT
        show_image(RESULTS[winner]["image"], winner)
        st.write(RESULTS[winner]["text"])

        with st.popover("Where to start learning"):  # EXTRA CREDIT
            for tip in LEARNING_TIPS[winner]:
                st.write(f"- {tip}")

        st.subheader("Your score breakdown")
        cols = st.columns(len(scores))
        for col, (name, score) in zip(cols, scores.items()):
            col.metric(label=name, value=score)  # NEW
