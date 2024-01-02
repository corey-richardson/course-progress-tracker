# Course Progress Tracker
#### [Video Demo](https://www.youtube.com/watch?v=7JPFLDDc1sU)
#### Description:

Course Progress Tracker is a Flask Web Application that allows the user to track their enrollments to online courses and university modules. The database is maintained by `sqlite3` in `courses.db`, consisting of tables `users` and `courses`.

```
sqlite> .schema
CREATE TABLE users (id INTEGER, username TEXT NOT NULL UNIQUE, hash TEXT NOT NULL, PRIMARY KEY(id));
CREATE TABLE courses (id INTEGER, user_id INTEGER NOT NULL, name TEXT NOT NULL UNIQUE, url TEXT, topics TEXT NOT NULL, desc TEXT NOT NULL, provider TEXT NOT NULL, is_complete BOOL NOT NULL, is_course BOOL NOT NULL, PRIMARY KEY(id));
```

```
+----+------------------+--------+
| id |     username     |  hash  |
+----+------------------+--------+
| 1  | corey-richardson | ...... |
| 2  | test-user        | ...... |
+----+------------------+--------+
```
```
+----+---------+-------+------+---------+----------------------------------+-------------------------+-------------+-----------+
| id | user_id | name  | url  | topics  |               desc               |        provider         | is_complete | is_course |
+----+---------+-------+------+---------+----------------------------------+-------------------------+-------------+-----------+
| 18 | 2       | CS101 | NULL | CompSci | A course about Computer Science. | University of Somewhere | 1           | 1         |
+----+---------+-------+------+---------+----------------------------------+-------------------------+-------------+-----------+
```

Route | Page Name | Description
---   | ---       | ---
`/`   | Homepage  | Displays all of the currently signed in users courses. If they have none, prompt them to add one via the `/add` route.
`/register` | Register | HTML form to allow the user to add a new account to the `users` table. Username must be unique. Password field must be typed twice and match.
`/login` | Log In | HTML form to allow the user to enter their username and password. This is compared with hashed data from the `users` table. All following routes require the user to be logged in to access them.
`/modules` | Homepage  | Displays all of the currently signed in users university. If they have none, prompt them to add one via the `/add` route.
`/add` | Add | HTML form to add a new course or module to the database.
`/update` | Update | HTML form to allow the user to modify the completition status of one of their courses or modules.
`/drop` | Drop | HTML form to allow the user to drop one of their enrollments from the database.

---

To pull changes into PythonAnywhere:
```
git checkout main
git pull origin main
```
