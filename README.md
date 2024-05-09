# socket_demo

#### Introduction
This is a sample project demonstrating basic socket communication features.

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
   ```

After following these steps, you should be able to smoothly run the project and start testing the socket communication features. If you encounter any issues during the process, please check that each step has been configured correctly.
```