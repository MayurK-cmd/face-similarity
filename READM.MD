//BACKEND//

through python(3.10.1)
python -m venv venv
pip install -r requirements.txt
uvicorn app:app --reload


through docker
docker build -t python-backend .
docker run -p 8000:8000 python-backend{hosted on 8000}


//FRONTEND//

through node.js
npm i
npm run dev

through docker
docker build -t react-frontend .
docker run -p 5173:5173 react-frontend{hosted on 5173}