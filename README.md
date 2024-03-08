Chatbot Template using LLMs for QA Retrieval

Steps to run:

1. Create a virtual environment\
   (Ensure you are using python 3.11)\
   `python --version` should output 3.11\
  a. To create a virtual environment\
   `pip install virtualenv`\
   `virtualenv env`\
  b. Activate the environemnt using\
   `env\bin\activate`
2. Install the required dependencies
  `pip insall -r requirements.txt`
3. Add your api token in `.env` file
4. Add the placeholder values in `scrapper.py` and `app.py` files
5. Start the webserver using
  `streamlit run app.py`
