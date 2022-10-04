# Social media API service

### Small social media like app with CRUD functionality built utilizing FastAPI and SQLAlchemy

API endpoints:
1) http://0.0.0.0:8000/posts - API for posting and viewing posts
2) http://0.0.0.0:8000/users - API for creating new user
3) http://0.0.0.0:8000/login - API for authentication
4) http://0.0.0.0:8000/vote - API for voing
5) http://0.0.0.0:8000/docs - Swagger documentation

To start the app you need to execute the following command:
```
uvicorn app.main:app --reload
```