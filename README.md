# Streamlit Chat Interface

A developer-friendly chat interface built with Streamlit for testing and interacting with chat APIs. This interface provides a clean, intuitive way to test chat endpoints with features like connection status monitoring, chat history management, and error handling.

## Features

- 🚀 Real-time chat interface
- 💫 Persistent session management
- 🔌 API connection status monitoring
- 📝 Chat history with timestamps
- 🆔 Unique sender ID generation
- 🎨 Clean, modern UI with custom styling
- ⚡ Automatic retry mechanism for failed requests
- 🧹 Chat history clearing functionality

## Test Your Chatbot API here :
- Deployed Application at:
```bash
https://app-interface-api-testing-mm8a3q85yhqbz4w8rtrntz.streamlit.app/
``` 

## API Endpoint Requirements

The chat interface expects the API to have the following endpoint:

```python
GET /response
Parameters:
- query: str           # The user's message
- senderId: str        # Unique identifier for the session
- customer_info: str   # JSON string containing additional customer information (optional)

Response format:
{
    "result": "Bot's response message"
}
```

## Configuration

The interface includes several configurable constants:

```python
DEFAULT_ERROR_MESSAGE = "An error occurred while communicating with the API"
RETRY_ATTEMPTS = 3
RETRY_DELAY = 1  # seconds
```

## Features in Detail

### API Client
- Handles all communication with the chat API
- Implements retry logic for failed requests
- Manages sender ID generation and persistence
- Converts parameters to appropriate formats

### Session Management
- Maintains chat history during the session
- Preserves API configuration
- Keeps track of connection status
- Stores customer information

### User Interface
- Clean, modern design with custom CSS
- Real-time connection status indicator
- Timestamps for all messages
- Clear chat history functionality
- Visible sender ID for debugging

### Error Handling
- Automatic retry for failed requests
- Clear error messages
- Connection status monitoring
- Invalid response format detection

## Customization

### Styling
The interface comes with built-in CSS styling that can be modified in the `apply_custom_css()` function. Key style elements include:

- Chat message containers
- Status indicators
- Timestamps
- Layout and spacing

### Error Messages
Custom error messages can be configured by modifying the constants at the top of the file.

### Retry Logic
The retry mechanism can be adjusted by modifying:
- `RETRY_ATTEMPTS`: Number of retry attempts
- `RETRY_DELAY`: Delay between retries in seconds

## Troubleshooting

1. Connection Issues:
   - Verify the API URL is correct
   - Check if the API server is running
   - Ensure network connectivity
   - Check the API endpoint format matches the expected structure

2. Response Format Issues:
   - Verify the API returns responses in the expected JSON format
   - Check if the "result" field is present in the response

3. Parameter Issues:
   - Ensure customer_info is properly formatted as a JSON string
   - Verify the senderId is being generated and sent correctly

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.