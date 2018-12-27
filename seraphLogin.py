from locust import HttpLocust, TaskSet, task
from bs4 import BeautifulSoup

USER_CREDENTIALS = [
    ("gatling1@gmail.com", "sechien123"),
    ("gatling2@gmail.com", "sechien123"),
    ("gatling3@gmail.com", "sechien123"),
    ("gatling4@gmail.com", "sechien123"),
    ("gatling5@gmail.com", "sechien123"),
    ("gatling6@gmail.com", "sechien123"),
    ("gatling7@gmail.com", "sechien123"),
    ("gatling8@gmail.com", "sechien123"),
    ("gatling9@gmail.com", "sechien123"),
    ("gatling10@gmail.com", "sechien123")
]

class UserBehavior(TaskSet):

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        if len(USER_CREDENTIALS) > 0:
            email, passw = USER_CREDENTIALS.pop()
            self.login(email, passw)

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        self.logout()

    def login(self, email, passw):
        response = self.client.get("/login")
        soup = BeautifulSoup(response.content, 'html.parser')
        csrfToken = soup.find(attrs={"name":"_csrf_token"})['value']
        print(csrfToken)
        self.client.post("/sessions", {"user[email]":email, "user[password]":passw, "_csrf_token":csrfToken})

    @task(2)
    def logout(self):
        self.client.get("/logout")

    @task(2)
    def index(self):
        self.client.get("/")

    @task(3)
    def profile(self):
        self.client.get("/profiles")

    @task(2)
    def project(self):
        self.client.get("/projects")

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000