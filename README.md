> A simple URL shortening service built on FastAPI.

# SwiftBit

![Tech Stack Used](https://github-readme-tech-stack.vercel.app/api/cards?title=Tech+Stack+Used&lineCount=1&theme=hacker&bg=%230D1117&badge=%23161B22&border=%2321262D&titleColor=%2358A6FF&line1=fastapi%2Cfastapi%2C009688%3Bpydantic%2Cpydantic%2CE92063%3Bjsonwebtokens%2CJWT%2Cffffff%3Bsqlalchemy%2CSQLAlchemy%2CD71F00%3B)

## Overview & Logic

This service provides functionality to shorten long URLs into shorter, more manageable links. Users can create shortened URLs, retrieve them, and delete them as needed.

A random short **UUID** is generated for a request object. When the shortened URL is used in the browser, the API request is called to search for the requested URL. If found, the user is redirected to the original URL, otherwise a 404 response is returned.

## Base URL

The base URL for accessing the service endpoints is https://swiftbit.onrender.com .<br>

You can also access the **API Docs** on `/docs` powered by **SwaggerUI** or on `/redoc` powered by **ReDoc**.

## Authentication

Authentication is required for creating and managing urls to ensure the security of user data. Authentication tokens must be included in the request headers for these endpoints.

## Authentication Endpoints

- **URL:** `/user/register`
- **Method:** POST
- **Description:** Register your user to start using the service.
  <br>
  <br>
- **URL:** `/user/login`
- **Method:** POST
- **Description:** Login a user so that URLs can be managed.
  <br>
  <br>
- **URL:** `/user/edit-user`
- **Method:** PATCH
- **Description:** Edit the details of the logged in user.
  <br>
  <br>
- **URL:** `/user/delete-user`
- **Method:** DELETE
- **Description:** Deletes the logged in user from the database.

## Service Endpoints and Usage

### Get User URLs

- **URL:** `/url`
- **Method:** GET
- **Description:** Fetch all the shortened urls of the user who raised the request.
- **Response Body:**
  ```json
  [
    {
      "short_url": "https://swiftbit.onrender.com/df200df7",
      "url": "https://leetcode.com/MacWeTT/"
    },
    {
      "short_url": "https://swiftbit.onrender.com/175a872c",
      "url": "https://www.ign.com/wikis/red-dead-redemption-2/Walkthrough"
    }
  ]
  ```

### Create Short URL

- **URL:** `/url`
- **Method:** POST
- **Description:** Accepts a request url and returns a shortened URL..
- **Request Body:**
  ```json
  {
    "request_url": "string"
  }
  ```
- **Response Body:**
  ```json
  {
  "message": "Requested URL has been shortened.",
  "original_url": "https://www.ign.com/wikis/red-dead-redemption-2/Walkthrough",
  "shortened_url": "https://swiftbit.onrender.com/99d72426"
}
  ```

### Delete URL

- **URL:** `/url/{url_id}`
- **Method:** DELETE
- **Description:** Fetch all the shortened urls of the user who raised the request.
- **Request Body:**
  ```json
  {
    "url_id": "df200df7"
  }
  ```
- **Response Body:**
  ```json
  {
    "message": "Short URL has been deleted successfully."
  }
  ```

## Installation and Setup

### 1. Install Python

Ensure you have Python installed on your system. You can download it from the [official Python website](https://www.python.org/downloads/) and follow the installation instructions for your operating system.

### 2. Create a Virtual Environment (Optional but Recommended)

It's a good practice to work within a virtual environment to isolate your project dependencies. You can create a virtual environment using `venv` or `virtualenv`. For example:

```bash
# Using venv (Python 3.3+)
python3 -m venv myenv
source myenv/bin/activate

# Using virtualenv
virtualenv myenv
source myenv/bin/activate
```

Your console should look like this:

```bash
(env) macwett@MacWeTT-PC:~/SwiftBit$
```

If it doesn't, make sure you have installed and activated the virtual environment correctly.

### 3. Install Required Dependencies

Next, install the required dependencies by using this command. <br>
Make sure your virtual environment is activated before installing the dependencies.

```bash
pip install -r requirements.txt
```

### 4. Initialize Environment Variables

Next, create a **.env** file in the root directory and add the following keys to it:

```env
API_URL="http://localhost:8000"
ALGORITHM = "YOUR_JWT_ALGORITHM"
SECRET_KEY = "YOUR_SECRET_KEY"
```

If you don't have a secret key, you can generate one for yourself using a script provided with the application and input that here.

### 5. Run the application

Finally, run the application by using this command:

```bash
uvicorn main:app --reload
```

This will run the uvicorn server on port **8000**, given everything is set up flawlessly :)
