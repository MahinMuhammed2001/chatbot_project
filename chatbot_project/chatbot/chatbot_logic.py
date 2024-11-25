import os
import spacy
import mysql.connector
from google.cloud import dialogflow_v2 as dialogflow

# Configure the path to your Dialogflow credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"D:\Chatbot_Project\chatbot_project\dialogflow-calvichatbot.json"

# Load spaCy's language model
try:
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    print(f"Error loading spaCy model: {e}")
    nlp = None

# Database connection details
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MySQL",
    database="electronica_data"
)

# Synonyms dictionary
synonyms = {
    "semiconductors": ["semiconductor", "chips", "electronics"],
    "microcontrollers": ["mcu", "microcontroller", "32-bit microcontroller", "8-bit processors", "embedded systems"],
    "germany": ["germany", "deutschland", "german", "germans", "berlin"]
}

# Fetch companies data from the MySQL database
def fetch_companies_from_db():
    try:
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM companies;")
        companies_data = cursor.fetchall()
        cursor.close()
        return companies_data
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return []

# Dialogflow integration
def detect_intent_texts(project_id, session_id, texts, language_code="en"):
    """
    Detect intent from user messages using Dialogflow.
    """
    try:
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(project_id, session_id)

        print(f"Session path: {session}\n")

        for text in texts:
            text_input = dialogflow.TextInput(text=text, language_code=language_code)
            query_input = dialogflow.QueryInput(text=text_input)

            response = session_client.detect_intent(
                request={"session": session, "query_input": query_input}
            )

            # Debug: Print the Dialogflow response
            print("Dialogflow Response:", response.query_result)

            return {
                "query_text": response.query_result.query_text,
                "intent": response.query_result.intent.display_name,
                "confidence": response.query_result.intent_detection_confidence,
                "fulfillment_text": response.query_result.fulfillment_text,
            }
    except Exception as e:
        print(f"Dialogflow API error: {e}")
        return {
            "query_text": "",
            "intent": None,
            "confidence": 0,
            "fulfillment_text": "Sorry, there was an issue connecting to Dialogflow.",
        }

# Main chatbot handler
def handle_query(user_message):
    """
    Processes the user message to understand and respond based on Dialogflow or spaCy logic.
    """
    companies_data = fetch_companies_from_db()
    if not companies_data:
        return "Sorry, I'm unable to fetch company data at the moment."

    project_id = "cavlichatbot"  # Replace with your Dialogflow project ID
    session_id = "user_session"  # Unique session ID for each user
    dialogflow_response = detect_intent_texts(project_id, session_id, [user_message])

    # Check if Dialogflow detected an intent
    if dialogflow_response["intent"]:
        return dialogflow_response["fulfillment_text"]

    # Fallback to spaCy logic if no intent detected or confidence is low
    if dialogflow_response["confidence"] < 0.7 and nlp:
        # Process the user input with spaCy
        doc = nlp(user_message.lower())

        # Extract named entities (locations, companies, etc.) from the user input
        entities = [entity.text for entity in doc.ents]

        # Check for 'germany' in entities and return relevant company information
        if any(entity in synonyms["germany"] for entity in entities):
            companies_info = [
                f"Company Name: {company['company_name']}\n"
                f"Address: {company['address']}\n"
                f"Email: {company['email']}\n"
                f"Phone: {company['phone']}\n"
                f"Website: {company['website']}\n"
                f"{'-'*40}"
                for company in companies_data
                if any(syn in company["address"].lower() for syn in synonyms["germany"])
            ]
            return "\n".join(companies_info) if companies_info else "No companies found in Germany."

        # Check for 'semiconductors' in the message and return the count of companies in the industry
        if any(syn in user_message.lower() for syn in synonyms["semiconductors"]):
            count = sum(
                1 for company in companies_data
                if any(syn in company["industry_category"].lower() or syn in company["products_services"].lower() for syn in synonyms["semiconductors"])
            )
            return f"There are {count} companies in the 'Semiconductors' industry." if count else "No companies found in the 'Semiconductors' industry."

        # Check for 'microcontrollers' and return companies that manufacture them
        if any(syn in user_message.lower() for syn in synonyms["microcontrollers"]):
            companies = [
                company["company_name"]
                for company in companies_data
                if any(syn in company["products_services"].lower() for syn in synonyms["microcontrollers"])
            ]
            return f"Companies manufacturing 'Microcontrollers': {', '.join(companies)}" if companies else "No companies found manufacturing Microcontrollers."

    # Default response if no matching intent or fallback logic
    return "I'm not sure how to answer that. Can you rephrase?"

# Example user query
if __name__ == "__main__":
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        bot_response = handle_query(user_input)
        print(f"Bot: {bot_response}")
