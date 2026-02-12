# LangGraph x NextJs Chat App

This is a base code and an AI Chatbot App serve with LangGraph to Next.JS that enables you to chat with your PostgreSQL database. Feel Free to use this for the base of your Project. It supports latest version of LangGraph as well as Persistent Chat with PostgreSQL.

## 1. How to Install

### Prerequisites
Ensure you have the following installed:
- Python 3.11+
- Git
- npm

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/ZahrizhalAli/langgraph-nextjs-chatbot.git
   cd langgraph-nexts-chatbot
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

   or
   
   pip install -r requirements.txt

   npm install 
   ```
3. Run the application - Server :
   ```bash
   python server/server.py
   ```
4. Run the application - Client :
   ```bash
   npm run dev
   ```

## 4. Current Capabilities
LangGraph x Nextjs Chatbot currently supports the following features:

### Simple Chat Capabilities with memories
- Engages in basic text-based conversations with memories. 🆕
- Supports predefined responses and limited contextual awareness.

Future updates will introduce advanced reasoning, memory retention, and multi-modal interactions. Stay tuned!
