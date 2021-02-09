For starting project: clone project to your pc, build images, and run the project in docker.
```
git clone https://github.com/CHESTERFIELD/url-shorter-jooble-test.git
cd url-shorter-jooble-test     
docker-compose up --build
```
For testing, paste in the working container with flask application command -
```
docker exec -it url-shorter-jooble-test-project_web_1 bash
cd src/ && python -m unittest tests.test_api
```
We have one API endpoint to working with other programs by http://127.0.0.1:8000/api/v1/url: 
- required method:
  * POST
- params:
  * required full_url -> str
  * optional life_period -> int from 1 to 365
