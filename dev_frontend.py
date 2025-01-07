import streamlit as st
import requests
import json
from datetime import datetime
import time
import uuid

# Constants
DEFAULT_ERROR_MESSAGE = "An error occurred while communicating with the API"
RETRY_ATTEMPTS = 3
RETRY_DELAY = 1  # seconds

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.sender_id = str(uuid.uuid4())  # Generate a unique sender ID for this session
    
    def test_connection(self) -> bool:
        """Test the API connection with retry logic"""
        for attempt in range(RETRY_ATTEMPTS):
            try:
                response = requests.get(
                    f"{self.base_url}/test",
                    timeout=5
                )
                return response.status_code == 200
            except requests.exceptions.RequestException:
                if attempt < RETRY_ATTEMPTS - 1:
                    time.sleep(RETRY_DELAY)
                continue
        return False
    
    def send_message(self, message: str, customer_info: dict = {}) -> dict:
        """Send a message to the API with retry logic"""
        for attempt in range(RETRY_ATTEMPTS):
            try:
                # Convert customer_info dict to JSON string
                customer_info_json = json.dumps(customer_info)
                
                # Updated to use the new endpoint structure
                params = {
                    "query": message,
                    "senderId": self.sender_id,
                    "customer_info": customer_info_json  # Send as JSON string
                }
                
                response = requests.get(
                    f"{self.base_url}/response",
                    params=params,
                    timeout=30
                )
                response.raise_for_status()
                response_data = response.json()
                
                # Extract the result field from the response
                if "result" in response_data:
                    return {"response": response_data["result"]}
                else:
                    return {"error": "Invalid response format from API"}
                
            except requests.exceptions.RequestException as e:
                if attempt < RETRY_ATTEMPTS - 1:
                    time.sleep(RETRY_DELAY)
                continue
            except Exception as e:
                return {"error": f"Error: {str(e)}"}
        return {"error": DEFAULT_ERROR_MESSAGE}

def init_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'api_url' not in st.session_state:
        st.session_state.api_url = ''
    if 'api_status' not in st.session_state:
        st.session_state.api_status = False
    if 'api_client' not in st.session_state:
        st.session_state.api_client = None
    if 'customer_info' not in st.session_state:
        st.session_state.customer_info = {}

def apply_custom_css():
    """Apply custom CSS styles"""
    st.markdown("""
        <style>
        .stChat {
            padding: 20px;
        }
        .chat-message {
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
            max-width: 80%;
        }
        .user-message {
            background-color: #e9ecef;
            margin-left: auto;
        }
        .assistant-message {
            background-color: #f8f9fa;
            margin-right: auto;
        }
        .timestamp {
            font-size: 0.8rem;
            color: #6c757d;
            margin-top: 0.5rem;
        }
        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 5px;
        }
        .status-connected {
            background-color: #28a745;
        }
        .status-disconnected {
            background-color: #dc3545;
        }
        .sender-id {
            font-size: 0.8rem;
            color: #6c757d;
            margin-top: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)

def display_chat_message(message: dict):
    """Display a single chat message with styling"""
    role = message["role"]
    content = message["content"]
    timestamp = message["timestamp"]
    
    with st.chat_message(role):
        st.markdown(content)
        st.markdown(f"<div class='timestamp'>{timestamp}</div>", unsafe_allow_html=True)

def clear_chat_history():
    """Clear the chat history"""
    st.session_state.messages = []
    st.rerun()

def main():
    st.set_page_config(
        page_title="Developer Chat Interface",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    init_session_state()
    apply_custom_css()

    # Sidebar configuration
    with st.sidebar:
        st.title("Chat Settings")
        
        # API Configuration
        st.subheader("API Configuration")
        new_api_url = st.text_input(
            "API URL",
            value=st.session_state.api_url,
            placeholder="https://your-ngrok-url.ngrok.io",
            help="Enter the base URL for your API endpoint"
        )
        
        # Update API client if URL changes
        if new_api_url != st.session_state.api_url:
            st.session_state.api_url = new_api_url
            if new_api_url:
                st.session_state.api_client = APIClient(new_api_url)
                st.session_state.api_status = st.session_state.api_client.test_connection()
        
        # Display Sender ID
        if st.session_state.api_client:
            st.markdown(f"<div class='sender-id'>Sender ID: {st.session_state.api_client.sender_id}</div>", 
                       unsafe_allow_html=True)
        
        # Connection status and test button
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.session_state.api_status:
                st.markdown("""
                    <div>
                        <span class="status-indicator status-connected"></span>
                        Connected
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div>
                        <span class="status-indicator status-disconnected"></span>
                        Disconnected
                    </div>
                """, unsafe_allow_html=True)
        
        with col2:
            if st.button("Test"):
                if st.session_state.api_client:
                    with st.spinner("Testing connection..."):
                        st.session_state.api_status = st.session_state.api_client.test_connection()
                else:
                    st.warning("Please enter an API URL first")
        
        # Chat controls
        st.subheader("Chat Controls")
        if st.button("Clear Chat History"):
            clear_chat_history()

    # Main chat interface
    st.title("Developer Chat Interface")

    # Chat messages container
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            display_chat_message(message)

    # Chat input
    if prompt := st.chat_input(
        "Type your message here...",
        disabled=not st.session_state.api_status,
        key="chat_input"
    ):
        # Add user message
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "timestamp": timestamp
        })

        # Get assistant response
        if st.session_state.api_status:
            with st.spinner("Getting response..."):
                response = st.session_state.api_client.send_message(
                    prompt,
                    st.session_state.customer_info
                )
                
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if "error" in response:
                    content = f"🚫 {response['error']}"
                else:
                    content = response.get("response", "No response received")
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": content,
                    "timestamp": timestamp
                })
                
                st.rerun()

if __name__ == "__main__":
    main()