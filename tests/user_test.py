import logging

from app import db
from app.db.models import User, Song


def test_adding_user(application):
    log = logging.getLogger("myApp")
    with application.app_context():
        assert db.session.query(User).count() == 0
        assert db.session.query(Song).count() == 0
        # showing how to add a record
        # create a record
        user = User('clf9@njit.edu', 'testtest')
        # add it to get ready to be committed
        db.session.add(user)
        # call the commit
        # db.session.commit()
        # assert that we now have a new user
        # assert db.session.query(User).count() == 1
        # finding one user record by email
        user = User.query.filter_by(email='clf9@njit.edu').first()
        log.info(user)
        # asserting that the user retrieved is correct
        assert user.email == 'clf9@njit.edu'
        # this is how you get a related record ready for insert
        user.songs = [Song("test", "smap", "1900", "rock"), Song("test2", "te", "1900", "rock")]
        # commit is what saves the songs
        db.session.commit()
        assert db.session.query(Song).count() == 2
        song1 = Song.query.filter_by(title='test').first()
        assert song1.title == "test"
        # changing the title of the song
        song1.title = "SuperSongTitle"
        # saving the new title of the song
        db.session.commit()
        song2 = Song.query.filter_by(title='SuperSongTitle').first()
        assert song2.title == "SuperSongTitle"
        # checking cascade delete
        db.session.delete(user)
        assert db.session.query(User).count() == 0
        assert db.session.query(Song).count() == 0


def test_login_auth(application, client):
    with application.app_context():
        user = User('clf9@njit.edu', 'testtest')
        db.session.add(user)
        db.session.commit()
        res = client.post('/login', data=dict(email="clf9@njit.edu", password='testtest'), follow_redirects=True)
        assert res.status_code == 200
        db.session.delete(user)


def test_register_auth(client):
    with client:
        res = client.post('/register', data=dict(email="clf9@njit.edu", password='testtest'), follow_redirects=True)
        print(res.data)
        assert res.status_code == 200


def test_dashboard_access(application, client):
    with application.app_context():
        user = User('clf9@njit.edu', 'testtest')
        assert user.is_authenticated() == True


def test_dashboard_denial(application, client):
    with application.app_context():
        user = User('keith@webizly.com', 'testtest')
        db.session.add(user)
        db.session.commit()
        res2 = client.post('/dashboard')
        res = client.post('/login', data=dict(email="keith@webizly.com", password='testtest'), follow_redirects=True)
        assert res2.status_code == 405
        assert res.status_code == 200
        db.session.delete(user)
