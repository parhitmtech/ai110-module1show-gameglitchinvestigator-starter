# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").


- 1) The first major bug I noticed was that the hints given were backward! If the number I guessed was less than the secret, it should have said "Go Higher!" but instead it said "Go Lower!" and also when the number I guessed was greater than the secret, it should have said "Go Lower!" but instead it said "Go Higher!".
- 2) The second major bug I noticed was that the secret number that was generated did not corelate with the difficulty level chosen on the left. So, if I chose the Easy mode, the range of the secret number should have ben from 1 to 20, but the secret number generated was 68. When, I chose the Hard mode, the range of the secret number was 1 to 50, but the secret number generated was 87. I believe the random number generation is set to range 1 to 100 by default in any Difficulty mode.
- 3) The third bug I noticed was that whenever I complete a game and start a new game, a new random number gets generated. But, when I start guessing a number and press the "Submit Guess" button, it still says "You already won/lost. Start a new game to play again." I think the New Game button is not able to refresh the game context properly. 
---

## 2. How did you use AI as a teammatde?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- I used Claude AI integrated to my VS code on this project 

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- I asked Claude to explain why random.randint(1, 100) in the new_game block was ignoring the difficulty. It correctly identified that low and high were computed at the top of the script from get_range_for_difficulty(difficulty), but the new_game button bypassed that by hardcoding 1, 100. I verified this by checking the Debug info panel, the secret number was always in the 1-100 range regardless of difficulty.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
- So, I think Claude initially suggested fixing the hint logic by only changing the emoji icons, but the actual outcome strings "Too High" and "Too Low" also needed to be swapped because update_score depends on those strings being semantically correct.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- After fixing the hint logic, I used the visible secret in the Developer Debug Info Panel to design test cases in a way that  I would guess a number I knew was lower than the secret and check that the game said "Go Higher", then guess higher and check for "Go Lower."

- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.
- I noticed that the hints were sometimes still not right after every second guess even after fixing the obvious swap issue. I tried to tracked st.session_state.attempts in the debug panel and realized that on even-numbered attempts, the code converts number to a string. So, comparing int with a string prompted a TypeError in Python that was checking the numbers by falling back to comparing them lexicographically. This gave wrong results for numbers with certain leading digits. 

- Did AI help you design or understand any tests? How?
- Yes, AI did help me generate better test cases on top of the ones I had thought of in my mind. 
---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- I think in Streamlit, every user interaction triggers a full re-run of the pythons script. Without session state, random.randint() would execute on every rerun, generating a new secret each time. The original app had st.session_state.secret = random.randint(low, high) protected by if "secret" not in st.session_state, which is correct but the new_game button re-assigned the secret using random.randint(1, 100) with hardcoded bounds, introducing two problems at once.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- I would explain streamlit to a friend by taking ane xample of a whiteboard. Every time you click on anything, the entire board is completely erased and redrawn. The session state is probably a small sticky note on the corner of the board and survives the erase. Any data that needs to ber persistent across runs needs to be written there. 

- What change did you make that finally gave the game a stable secret number?
- I replaced random.randint(1, 100) in the new_game block with random.randint(low, high), and add st.session_state.status = "playing" so that the game contexts get fully reset.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
  - I think I would like to use the debug panel more efficiently. Being able to see the value of each variable in real time was extremely valuable. I will apply this skill on any UI I build in the future. 

- What is one thing you would do differently next time you work with AI on a coding task?
- I think whenever I will work with AI on a debugging task, I'll paste the fully relevant code instead of describing the effects in words. 

- In one or two sentences, describe how this project changed the way you think about AI generated code.
- I think this project taught me that even AI generated code can have bugs that look intentional. I think even if we are using AI, we should still verify each line of code and run logically curated tests to verify the robustness of the code.