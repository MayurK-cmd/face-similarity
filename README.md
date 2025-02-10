//BACKEND//

--through python(3.10.1)
1. python -m venv venv
2. venv\Scripts\Activate
3. pip install -r requirements.txt
4. uvicorn app:app --reload


--through docker
1. docker build -t python-backend .
2. docker run -p 8000:8000 python-backend{hosted on 8000}


//FRONTEND//

--through node.js
1. npm i
2. npm run dev

--through docker
1. docker build -t react-frontend .
2. docker run -p 5173:5173 react-frontend{hosted on 5173}
