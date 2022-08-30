# Trivia App - Let"s Smack

Learning or playin? Both. That"s the concept of this Trivia App. A webpage where users can test their general knowledge and guess to questions related to many different categories and have fun finding their score in each set of play. Users can search for different questions and find their answers, can add and delete questions and also play a quiz game that renders a final score based on a set of correct answers from a set of questions.

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). 

## Colaborators Guidelines
At this stage, the project works as explained in the introduction, but of course, there are plenty of room to fulfill anyone"s dreams in terms of what can be added. In the future, users will want to find their rating and maybe have the opportunity to get a set of questions based on the difficulty level.

## Getting Started

### Getting the Project
You can fork and clone the project to your local directory from: (https://github.com/idelmac/Trivia.git).

### Pre-requisites
Developers using this project should already have Python, pip and node installed on their local machines.

## About the Stack
The project is designed with some key functional areas:

### Backend

#### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we"ll use to handle the lightweight SQL database. You"ll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we"ll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.


### Frontend

#### Getting Setup

> _tip_: this frontend is designed to work with [Flask-based Backend](../backend) so it will not load successfully if the backend is not working or not connected. We recommend that you **stand up the backend first**, and then the frontend should integrate smoothly.

#### Installing Dependencies

1. **Installing Node and NPM**
   This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

2. **Installing project dependencies**
   This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

> _tip_: `npm i`is shorthand for `npm install``

#### Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use `npm start`. You can change the script in the `package.json` file.

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.

```bash
npm start
```

#### Request Formatting

The frontend should be fairly straightforward and disgestible. You"ll primarily work within the `components` folder in order to understand, and if you so choose edit, the endpoints utilized by the components. While working on your backend request handling and response formatting, you can reference the frontend to view how it parses the responses.

After you complete your endpoints, ensure you return to the frontend to confirm your API handles requests and responses appropriately:

- Endpoints defined as expected by the frontend
- Response body provided as expected by the frontend

##### Optional: Updating Endpoints and API behavior

Would you rather the API had different behavior - different endpoints, return the response body in a different format? Go for it! Make the updates to your API and the corresponding updates to the frontend so it works with your API seamlessly.

##### Optional: Styling

In addition, you may want to customize and style the frontend by editing the CSS in the `stylesheets` folder.


## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 409: Resources conflict
- 422: Not Processable 


### Endpoints 
#### GET /categories
`GET "/api/v1.0/categories"`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

#### GET /questions
`GET "/questions?page=${integer}"`

- Fetches a paginated set of questions, a total number of questions, all categories and current category string
- Request Arguments: page - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string

```json
{
    "questions": [
        {
            "id": 1,
            "question": "This is a question",
            "answer": "This is an answer",
            "difficulty": 5,
            "category": 2
        },
    ],
    "totalQuestions": 100,
    "categories": { "1" : "Science",
    "2" : "Art",
    "3" : "Geography",
    "4" : "History",
    "5" : "Entertainment",
    "6" : "Sports" },
    "currentCategory": "History"
}
```

#### DELETE /questions
`DELETE "/questions/${id}"`
- Deletes a specified question using the id of the question
- Request Arguments: id - integer
- Returns: HTTP status code and the id of the question.

#### POST /questions
`POST "/questions"`
- Sends a post request in order to add a new question
- Request Body:
```json
{
    "question":  "Heres a new question string",
    "answer":  "Heres a new answer string",
    "difficulty": 1,
    "category": 3,
}
```
Returns: Does not return any new data

#### Search /questions
`POST "/questions"`
Sends a post request in order to search for a specific question by search term
Request Body:
```json
{
    "searchTerm": "this is the term the user is looking for"
}
```

Returns: any array of questions, a number of totalQuestions that met the search term and the current category string
```json
{
    "questions": [
        {
            "id": 1,
            "question": "This is a question",
            "answer": "This is an answer",
            "difficulty": 5,
            "category": 5
        },
    ],
    "totalQuestions": 100,
    "currentCategory": "Entertainment"
}
```

#### GET categories/${id}/questions
`GET "/categories/${id}/questions"`
Fetches questions for a cateogry specified by id request argument
Request Arguments: id - integer
Returns: An object with questions for the specified category, total questions, and current category string
```json
{
    "questions": [
        {
            "id": 1,
            "question": "This is a question",
            "answer": "This is an answer",
            "difficulty": 5,
            "category": 4
        },
    ],
    "totalQuestions": 100,
    "currentCategory": "History"
}
```

#### Post /quizzes
`POST "/quizzes"`
Sends a post request in order to get the next question
Request Body:
```json
{
    "previous_questions": [1, 4, 20, 15]
    "quiz_category": "current category"
}

```
Returns: a single new question object
```json
{
    "question": {
        "id": 1,
        "question": "This is a question",
        "answer": "This is an answer",
        "difficulty": 5,
        "category": 4
    }
}
```

## Deployment N/A

## Authors
Idelfonso Macingarrela 

## Acknowledgements 
Udacity. 