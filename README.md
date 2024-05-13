# Socket Demo: Enhanced Chat Application

#### Introduction
This project showcases an advanced chat application that integrates third-party AI chat interfaces for conversations. The system supports long-lasting connections for stream-like dialogues and incorporates sophisticated data structures to store conversational history and context. This guide details the setup required to get the project running.

#### Features
- **Third-Party AI Chat Integration**: Utilizes a third-party AI to facilitate real-time, block-style dialogues.
- **Long Connection Communication**: Implements long-lasting connection techniques to ensure continuous and fluid dialogues.
- **Context Management**: Algorithms are employed to handle and process contextual information, making conversations more coherent and context-aware.
- **Interactive Front-End**: A user-friendly interface that allows users to engage in dialogues, which interact with the backend's long connection communication technologies.
- **Extended UI Capabilities**: Supports storing multiple dialogue histories simultaneously, enhancing user interaction.
- **Backend Logic for Multiple Dialogues**: Adjusted backend logic to associate and switch between multiple dialogues effectively.
- **Integration with Drawing API**: Integrates a third-party drawing API, modifies backend logic to recognize and handle drawing tasks, and saves the drawing results as image files on the local server.
- **Result Presentation**: Returns drawing results to users as image files.

#### Technical Stack
- **Flask**: A lightweight and flexible micro-framework for web development in Python, used for handling backend logic and routing.
- **Bootstrap**: A front-end framework used for creating modern and responsive layouts, ensuring the application is aesthetically pleasing and functional across different devices.
- **Server-Sent Events (SSE)**: Used for handling real-time bidirectional communication between clients and servers, which is crucial for maintaining long connections for live chat sessions.
- **ChatGPT**: Integrated as the AI engine to drive conversational capabilities, enabling sophisticated dialogues based on context and prior interactions.
- **DALL-E**: A third-party API utilized for generating images based on textual descriptions within chats, enhancing the interactive experience by providing visual feedback.

#### Installation and Setup Guide

To successfully install and run this project, please follow these steps:

1. **Install Dependencies**:
   First, ensure to install all the dependencies listed in `requirements.txt`. Open your terminal or command prompt, navigate to the project root directory, and run the following command:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure the Database**:
   Next, execute the `data.sql` script to set up the database schema. This script will create the necessary tables and initial data. After that, modify the database settings in `routes.__init__.py` according to your database configuration.

3. **Set Up Environment Variables**:
   Finally, create a `.env` file in the project root directory that contains a key environmental variable for storing your OpenAI API key. The content should look like this:
   ```
   OPENAI_API_KEY=your_api_key
   ACCESS_KEY_ID=your_aliyun_id
   ACCESS_KEY_SECRET=your_aliyun_secret
   ```

After completing the setup steps, you should be able to run the project and begin testing its socket communication and AI-integrated chat features. For any issues, ensure each step has been properly configured and executed.