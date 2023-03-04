import unittest
from unittest.mock import patch
import random
import string
from app import app, db, Task




class TestBoard(unittest.TestCase):

    def setUp(self):
        """
        Executed before each test
        """
        with app.app_context():
            app.config['TESTING'] = True
            app.config['DEBUG'] = False
            self.app = app.test_client()
            db.create_all()


    def tearDown(self):
        """
        Executed after each test
        """
        with app.app_context():
            db.session.remove()
            db.drop_all()


    def test_add_samename_task(self):
        """
        Test assing a simple task.
        Basic add test to teh database
        """
        with app.app_context():
            new = Task(id = 1, title = 'test', status = 'todo')
            self.app.post('/', data=dict(title='test'), follow_redirects=True)
            task = Task.query.filter_by(title='test').first()
            if task.id == 2:
                return True
            else:
                return False

    def test_add_random_task(self):
        """
        Checks the imput of tasks with random names

        Appends multiple random tasks to the database
        to check if the names are valid 
        """
        with app.app_context():
            test = []
            for i in range(10):
                num = random.randint(1, 200)
                characters = string.ascii_letters + string.digits + string.punctuation
                newt  = str(''.join(random.choice(characters) for i in range(num)))
                self.app.post('/', data=dict(title= newt), follow_redirects=True)
                task = Task.query.filter_by(title= newt).first()
                if task.id == i+1:
                    test.append(True)
            if False not in test:
                return True

    def test_delete_task(self):
        """
        Checks that tasks are deleted

        Uses the title, assuming the creation of a new db
        """
        with app.app_context():
            self.app.post('/', data=dict(title='test'), follow_redirects=True)
            task = Task.query.filter_by(title='test').first()
            self.app.post('/delete', data=dict(id=task.id), follow_redirects=True)
            task = Task.query.filter_by(title='test').first()
            self.assertIsNone(task)
    

    def test_delete_self_name_task(self):
        """
        Checks that only the specified it's delated and not others with teh same name
        Checks with asserting id's and lenght of the final query


        """
        with app.app_context():
            self.app.post('/', data=dict(title='test'), follow_redirects=True)
            task1 = Task.query.filter_by(title='test').first()
            self.app.post('/', data=dict(title='test'), follow_redirects=True)
            task2 = Task.query.filter_by(title='test').first()
            if task1.id != task2.id:
                return True
            self.app.post('/delete',  data=dict(id=task1.id), follow_redirects=True)
            after = Task.query.filter_by(title='test').all()
            #Becasue task1 was deleted task2 should be the only one with the name test
            task2 = Task.query.filter_by(title='test').first()
            self.assertEqual(len(after), len([1]))
            self.assertEqual(task1.id, 1)
            self.assertEqual(task2.id, 2)


    def test_update_task_next(self):
        """
        Checks if the task was updated to the next columns
        """
        with app.app_context():
            self.app.post('/', data=dict(title='test'), follow_redirects=True)
            task = Task.query.filter_by(title='test').first()
            self.app.post('/update_next', data=dict(id=task.id), follow_redirects=True)
            task = Task.query.filter_by(title='test').first()
            self.assertEqual(task.status, 'inprogress')
        
    def test_update_task_pre(self):
        """
        Check if the task was updated to the previous column
        """
        with app.app_context():
            self.app.post('/', data=dict(title='test'), follow_redirects=True)
            task = Task.query.filter_by(title='test').first()
            self.app.post('/update_pre', data=dict(id=task.id), follow_redirects=True)
            task = Task.query.filter_by(title='test').first()
            self.assertEqual(task.status, 'todo')

    def test_wrong_method_update(self):
        """
        Test that the page dosen't charsh if the wrong url is called
        """
        with app.app_context():
            response = self.app.get('/update_next', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            response = self.app.get('/update_pre', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_wrong_method_delete(self):
        """
        Test that the page dosen't charsh if the wrong url is called
        """
        with app.app_context():
            response = self.app.get('/delete', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_wrong_method_add(self):
        """
        Test that the page dosen't charsh if the wrong url is called
        """
        with app.app_context():
            response = self.app.get('/add', follow_redirects=True)
            self.assertEqual(response.status_code, 404)



if __name__ == "__main__":
    unittest.main()


