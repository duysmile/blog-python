# Blog Api

### Installation
- Initialize:
```bash
export FLASK_APP=index.py
export FLASK_CONFIG=development
```
- Migrate DB:
```bash
flask db init
flask db migrate
flask db upgrade
```
- Create `.env` from `.env.example` and fill all information
- Run application
```
flask run
```