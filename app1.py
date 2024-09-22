import random
import streamlit as st

# Word list for the game
WORD_LIST = ["babu"]

# Choose a random word from the list
if "target_word" not in st.session_state:
    st.session_state.target_word = random.choice(WORD_LIST)

target_word = st.session_state.target_word

# Function to check the guess
def check_guess(guess, target):
    result = []
    for i, letter in enumerate(guess):
        if letter == target[i]:
            result.append(('green', letter))  # Correct letter in correct position
        elif letter in target:
            result.append(('yellow', letter))  # Correct letter in wrong position
        else:
            result.append(('gray', letter))  # Incorrect letter
    return result

# CSS for Wordle-like styling
st.markdown("""
    <style>
    .guess-box {
        display: flex;
        justify-content: center;
        gap: 5px;
    }
    .letter-box {
        width: 50px;
        height: 50px;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 20px;
        font-weight: bold;
        color: white;
        border: 2px solid #ccc;
        background-color: #333;
    }
    .letter-box.green {
        background-color: #6aaa64;
    }
    .letter-box.yellow {
        background-color: #c9b458;
    }
    .letter-box.gray {
        background-color: #787c7e;
    }
    </style>
    """, unsafe_allow_html=True)

# Streamlit app
def main():
    st.title("OUR Wordle Game")

    # Display instructions
    st.write("Hello Love")
    st.write("Guess the 4-letter word. The game will tell you:")
    st.write("- Green: Letter is correct and in the right position")
    st.write("- Yellow: Letter is correct but in the wrong position")
    st.write("- Gray: Letter is not in the word")

    # Store guesses in the session state
    if "guesses" not in st.session_state:
        st.session_state.guesses = []

    # Check if the user has made 6 guesses or guessed the correct word
    game_over = len(st.session_state.guesses) >= 6 or (st.session_state.guesses and st.session_state.guesses[-1] == target_word)

    if not game_over:
        # Input for guessing
        guess = st.text_input("Enter your 4-letter guess:", max_chars=4).lower()

        # Button to submit the guess
        if st.button("Submit Guess"):
            if len(guess) == 4 and guess.isalpha():
                st.session_state.guesses.append(guess)
            else:
                st.warning("Shi Shi saiba you guessed wrong")
    else:
        if st.session_state.guesses[-1] != target_word:
            st.error(f"Sorry, you've used all your guesses. The correct word was {target_word.upper()}.")

    # Display the 6-row Wordle grid
    for i in range(6):
        if i < len(st.session_state.guesses):
            guess = st.session_state.guesses[i]
            result = check_guess(guess, target_word)
        else:
            guess = "    "  # Empty guess
            result = [('gray', letter) for letter in guess]

        # Display the guess result as a row of letter boxes
        guess_html = '<div class="guess-box">'
        for color, letter in result:
            guess_html += f'<div class="letter-box {color}">{letter.upper()}</div>'
        guess_html += '</div>'
        st.markdown(guess_html, unsafe_allow_html=True)

    # Check if the player won
    if st.session_state.guesses and st.session_state.guesses[-1] == target_word:
        st.success(f"Congratulations! You guessed the word correctly: {target_word.upper()}!")
        st.balloons()

    # Allow the user to restart the game
    if st.button("Restart Game"):
        st.session_state.guesses = []
        st.session_state.target_word = random.choice(WORD_LIST)
        st.experimental_rerun()

if __name__ == "__main__":
    main()
