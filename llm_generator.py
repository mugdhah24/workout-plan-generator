from typing import List, Optional
from groq import Groq, GroqError, APIConnectionError, APIStatusError, RateLimitError, AuthenticationError

def generate_workout_plan(
    my_api_key: str,
    goal: str,
    experience: str,
    days: int,
    equipment: List[str],
    injuries: Optional[str] = None,
    model: str = "openai/gpt-oss-120b"
) -> Optional[str]:
    """
    Generates a personalized workout plan using the Groq API based on user inputs.

    Args:
        my_api_key: The Groq API key to use for authentication.
        goal: The user's fitness goal.
        experience: The user's experience level.
        days: Number of days available per week.
        equipment: List of available equipment.
        injuries: Optional string describing injuries or limitations.
        model: The Groq model to use.

    Returns:
        The generated markdown workout plan as a string, or None if the API call failed.
    """
    if not my_api_key:
        raise ValueError("API key is required.")
    
    if days < 1 or days > 7:
        raise ValueError("Days available must be between 1 and 7.")
    
    client = Groq(api_key=my_api_key)

    system_prompt = (
        "You are a world-class personal trainer. Your job is to create a realistic, "
        "structured, and highly personalized weekly workout plan based on the user's constraints.\n\n"
        "### STRICT RULES:\n"
        "1. DO NOT suggest exercises that require equipment the user does not have.\n"
        "2. If the user mentions injuries or limitations, you MUST strictly avoid any exercises that could aggravate them. Be extremely cautious.\n"
        "3. You are NOT a doctor. Do NOT give medical advice. If an injury is mentioned, keep the exercises extremely conservative.\n"
        f"4. The plan MUST consist of exactly {days} workout days per week.\n"
        "5. Output the plan in clean Markdown format with headers for each day (e.g., '### Day 1: Full Body').\n"
        "6. Structure the exercises clearly, including recommended Sets and Reps (e.g., using a markdown table or bullet points).\n"
        "7. Do NOT generate a wall of text. Use formatting (bolding, lists, tables) to make it easy to read.\n"
        "8. Keep the introduction brief and jump straight into the plan."
    )

    equipment_str = ", ".join(equipment) if equipment else "No equipment (bodyweight only)"
    injuries_str = injuries if injuries else "None"

    user_prompt = (
        f"Please create a {days}-day workout plan for me.\n"
        f"- Goal: {goal}\n"
        f"- Experience Level: {experience}\n"
        f"- Equipment Available: {equipment_str}\n"
        f"- Injuries/Limitations: {injuries_str}\n\n"
        "Make sure to specify sets, reps, and rest times for each exercise."
    )

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model=model,
            temperature=0.7,
            max_tokens=2048
        )
        
        content = chat_completion.choices[0].message.content
        if not content:
            raise ValueError("The model returned an empty response.")
            
        return content

    except AuthenticationError as e:
        raise Exception(f"Authentication failed. Please check your API key. ({str(e)})")
    except RateLimitError as e:
        raise Exception(f"Rate limit exceeded. Please try again later. ({str(e)})")
    except APIConnectionError as e:
        raise Exception(f"Failed to connect to the Groq API. Please check your internet connection. ({str(e)})")
    except APIStatusError as e:
        raise Exception(f"Groq API returned an error status. ({str(e)})")
    except GroqError as e:
        raise Exception(f"Groq API Error: {str(e)}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {str(e)}")
