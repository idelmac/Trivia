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
> View the [Backend README](./backend/README.md) for more details.

### Frontend
> View the [Backend README](./frontend/README.md) for more details.

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

### Expected success response
For every success return, it is appended a success statement and status code 200, as shown below :
```
{
    "success": True, 
    "status": 200,
    "data": {any object}
}
```

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