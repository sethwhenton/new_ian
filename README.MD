# Group 5

| Name | Email | FIM ID |
| ---- | ----- | ------ |
|  Ian Tayebwa    |  tayebw01@ads.uni-passau.de  |    tayebwa    |
|  Whenton Seth   |  whento01@ads.uni-passau.de  |    Whenton    |
|  Jack Grant Dagogo  |  dagogo01@ads.uni-passau.de  |    dagogojack    |

# Run API with Development Server (runs with MYSQL server based Databse):  

```
OBJ_DETECT_ENV=dev OBJ_DETECT_MYSQL_USER=obj_detect_dev OBJ_DETECT_MYSQL_PWD=obj_detect_dev_pwd OBJ_DETECT_MYSQL_HOST=127.0.0.1 OBJ_DETECT_MYSQL_DB=obj_detect_dev_db python3 -m src.app
```
# Running unit tests (runs with SQL Lite Database):  
```
OBJ_DETECT_ENV=test OBJ_DETECT_MYSQL_DB=obj_detect_test_db python3 -m unittestst
```