import streamlit as st
import os
from dotenv import load_dotenv
from llm_generator import generate_workout_plan

load_dotenv()

st.set_page_config(page_title="Workout Plan Generator", page_icon="🏋️", layout="centered")

def main():
    st.title("🏋️ AI Workout Plan Generator")
    st.markdown("Generate a highly personalized weekly workout routine based on your goals, constraints, and available equipment.")

    # We load the API key directly from the environment variables (.env file)
    my_api_key = os.environ.get("GROQ_API_KEY", "")

    if "form_key" not in st.session_state:
        st.session_state.form_key = 0

    def reset_app():
        st.session_state.form_key = st.session_state.get("form_key", 0) + 1
        keys_to_clear = [key for key in st.session_state.keys() if key != "form_key"]
        for key in keys_to_clear:
            del st.session_state[key]

    # Session State Initialization
    if "workout_plan" not in st.session_state:
        st.session_state.workout_plan = None
    if "has_injuries" not in st.session_state:
        st.session_state.has_injuries = False

    # Main Form
    with st.form(f"workout_form_{st.session_state.form_key}"):
        col1, col2 = st.columns(2)
        
        with col1:
            goal = st.selectbox(
                "Fitness Goal",
                ["Build muscle", "Lose fat", "General fitness", "Improve endurance"],
                key=f"goal_{st.session_state.form_key}"
            )
            experience = st.selectbox(
                "Experience Level",
                ["Beginner", "Intermediate", "Advanced"],
                key=f"experience_{st.session_state.form_key}"
            )
            
        with col2:
            days = st.slider("Days available per week", min_value=1, max_value=7, value=3, key=f"days_{st.session_state.form_key}")
            
        equipment = st.multiselect(
            "Equipment Access",
            ["No equipment (Bodyweight)", "Home dumbbells", "Resistance bands", "Pull-up bar", "Full gym"],
            default=["No equipment (Bodyweight)"],
            key=f"equipment_{st.session_state.form_key}"
        )
        
        injuries = st.text_area(
            "Injuries or Limitations (Optional)", 
            placeholder="e.g., 'bad knees', 'no overhead pressing', 'recovering from shoulder surgery'",
            key=f"injuries_{st.session_state.form_key}"
        )

        _, submit_col, reset_col, _ = st.columns([2, 1.5, 1.5, 2])
        with submit_col:
            submit_button = st.form_submit_button("Generate Plan", type="primary", use_container_width=True)
        with reset_col:
            st.form_submit_button("Reset", on_click=reset_app, type="primary", use_container_width=True)

    # Generate Plan Logic
    if submit_button:
        # Validate inputs
        if days < 1:
            st.warning("👋 It looks like you haven't selected any days. Please select at least 1 day for your workout plan.")
        elif not equipment:
            st.warning("👋 Please select at least one equipment option so we know what you're working with!")
        elif not my_api_key:
            st.warning("🔑 We need a Groq API key to generate your plan. Please check your .env file or environment variables.")
        else:
            with st.spinner("Consulting AI Personal Trainer..."):
                try:
                    plan = generate_workout_plan(
                        my_api_key,
                        goal=goal,
                        experience=experience,
                        days=days,
                        equipment=equipment,
                        injuries=injuries.strip()
                    )
                    
                    if plan:
                        st.session_state.workout_plan = plan
                        st.session_state.has_injuries = bool(injuries.strip())
                        st.success("🎉 Plan generated successfully!")
                        
                except ValueError as e:
                    if "empty response" in str(e).lower():
                        st.warning("🤖 The AI had a little brain freeze! But don't worry, here is a basic fallback plan to get you started:")
                        st.session_state.workout_plan = "### Friendly Fallback Plan\n\n**Day 1: Full Body**\n- Squats: 3 sets of 10-15 reps\n- Push-ups: 3 sets to failure\n- Bodyweight Rows: 3 sets of 10-15 reps\n\n**Day 2: Active Recovery**\n- 30 minutes of light cardio or yoga\n\n**Day 3: Core & Mobility**\n- Planks: 3 sets of 30-60 seconds\n- Lunges: 3 sets of 12 reps per leg\n- Stretching routine"
                        st.session_state.has_injuries = False
                    else:
                        st.warning(f"🤔 Hmm, something's not quite right: {str(e)}")
                except Exception as e:
                    st.error(f"🔌 Oops! We ran into a connection or API issue:\n\n{str(e)}\n\nPlease try again in a moment.")

    # Display Plan and Stretch Goals
    if st.session_state.workout_plan:
        st.divider()
        st.header("📋 Your Personalized Workout Plan")
        
        if st.session_state.has_injuries:
            st.warning("🩺 **Medical Disclaimer:** You mentioned an injury or physical limitation. This plan is AI-generated and does not constitute medical advice. Please consult a physician or physical therapist before starting this routine.")

        # Display the generated plan
        st.markdown(st.session_state.workout_plan)
        
        st.divider()
        col_down, col_regen = st.columns(2)
        
        with col_down:
            st.download_button(
                label="📥 Download Plan as Markdown",
                data=st.session_state.workout_plan,
                file_name="my_workout_plan.md",
                mime="text/markdown",
                type="primary"
            )
            
        with col_regen:
            if st.button("🔄 Regenerate Variation", type="primary"):
                with st.spinner("Generating a new variation..."):
                    try:
                        plan = generate_workout_plan(
                            my_api_key,
                            goal=goal,
                            experience=experience,
                            days=days,
                            equipment=equipment,
                            injuries=injuries.strip()
                        )
                        if plan:
                            st.session_state.workout_plan = plan
                            st.rerun()
                    except ValueError as e:
                        if "empty response" in str(e).lower():
                            st.warning("🤖 The AI had a little brain freeze! Please try regenerating.")
                        else:
                            st.warning(f"🤔 Hmm: {str(e)}")
                    except Exception as e:
                        st.error(f"🔌 Oops! We ran into a connection or API issue:\n\n{str(e)}\n\nPlease try again.")

if __name__ == "__main__":
    main()
