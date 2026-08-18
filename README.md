# 🏋️ AI Workout Plan Generator

An intelligent, Streamlit-based web application that acts as your personal AI trainer. It generates highly personalized weekly workout routines based on your specific goals, constraints, and available equipment using the Groq API.

## ✨ Features

- **Personalized Plans:** Tailors workouts based on your fitness goal, experience level, available days per week, and access to equipment.
- **Injury Awareness:** Takes injuries and physical limitations into account to provide conservative and safe exercise recommendations.
- **Robust Error Handling:** Gracefully handles missing inputs, API connection issues, rate limits, and even provides a "Friendly Fallback Plan" if the AI service becomes temporarily unavailable.
- **Downloadable:** Export your generated workout plan as a formatted Markdown file to keep on your devices.
- **Regenerate Variations:** Easily tweak or request a new variation of your plan with a single click.

## 🛠️ Prerequisites

- Python 3.8+
- A [Groq](https://groq.com/) API Key

## 🚀 Setup & Installation

1. **Navigate to the project directory:**
   ```bash
   cd workout-plan-generator-app
   ```

2. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your API Key:**
   Create a `.env` file in the root directory of the app and add your Groq API key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

## 🎮 Usage

Run the Streamlit application locally:

```bash
streamlit run app.py
```

The app will open automatically in your default web browser (typically at `http://localhost:8501`). Enter your details, click "Generate Plan", and get ready to sweat!

## 📁 Project Structure

- `app.py`: The main Streamlit web application containing the UI and state management.
- `llm_generator.py`: Contains the logic for constructing the prompt and communicating with the Groq API.
- `requirements.txt`: The Python dependencies (`streamlit`, `groq`, `python-dotenv`) required to run the project.
- `.env`: Environment variables file containing your sensitive API keys.

## Prompt Design Approach 

The prompt is designed to generate a personalized and practical workout plan instead of a generic response.

It specifically handles:

- **🎯 Fitness goal** — adapts the plan to the user's objective.
- **🏋️ Experience level** — adjusts exercise difficulty and workout intensity.
- **📅 Exact number of workout days** — generates exactly the number of days selected.
- **🏠 Available equipment** — uses only the equipment provided by the user.
- **⚠️ Injuries/limitations** — considers user limitations and avoids conflicting exercises.
- **📋 Structured Markdown output** — provides a clear day-by-day plan with exercises, sets, reps, and rest.
- **🛡️ Medical disclaimer** — avoids medical claims and includes a disclaimer when limitations are provided.
- **🚫 Constraint enforcement** — explicitly instructs the LLM to follow all user-provided constraints.

This approach combines structured inputs + explicit constraints + a defined output format to produce a reliable, personalized, and usable workout plan.

## Screenshots are available in the screenshots folder.