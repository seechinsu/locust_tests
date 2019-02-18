from locust import HttpLocust, TaskSet, task
from bs4 import BeautifulSoup
from random import randint

USER_CREDENTIALS = ["seechinsu" + str(x+1) + "@yahoo.com" for x in range(1000)]

# USER_CREDENTIALS = ["locust" + str(x+1) + "@yahoo.com" for x in range(2000)]


class UserBehavior(TaskSet):

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        if len(USER_CREDENTIALS) > 0:
            email = USER_CREDENTIALS.pop()
            # print(email)
            self.login(email)

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        # self.logout()

    def login(self, email):
        response = self.client.get("/login")
        soup = BeautifulSoup(response.content, 'html.parser')
        csrfToken = soup.find(attrs={"name": "_csrf_token"})['value']
        # print(csrfToken)
        self.client.post(
            "/sessions", {"user[email]": email, "user[password]": "sechien123", "_csrf_token": csrfToken}, headers={"X-CSRFToken": csrfToken})

    # @task(1)
    # def logout(self):
    #     self.client.get("/logout")

    @task(5)
    def index(self):
        self.client.get("/")

    @task(4)
    def profile(self):
        self.client.get("/profiles")

    @task(4)
    def project(self):
        self.client.get("/projects")

    @task(3)
    def contact_us(self):
        self.client.get("/contacts/new")

    @task(4)
    def profile_view(self):
        profile_id = randint(1, 200)
        self.client.get(f"/profiles/{profile_id}")

    @task(4)
    def project_view(self):
        project_id = randint(1, 200)
        self.client.get(f"/projects/{project_id}")

    @task(3)
    def newProject(self):
        response = self.client.get("/projects/new")
        # print(response.content)
        soup = BeautifulSoup(response.content, 'html.parser')
        csrfToken = soup.find(attrs={"name": "_csrf_token"})['value']
        self.client.post("/projects", {"project[title]": "test", "project[content]": "test",
                                       "project[github_link]": "https://github.com/seechinsu/elixir-phoenix"}, headers={"x-csrf-token": csrfToken})

    @task(3)
    def newProfile(self):
        response = self.client.get("/profiles/new")
        # print(response)
        soup = BeautifulSoup(response.content, 'html.parser')
        csrfToken = soup.find(attrs={"name": "_csrf_token"})['value']
        self.client.post("/profiles", {"profile[title]": "Locust", "profile[team]": "Elixir", "profile[pic_link]": "https://www.geek.com/wp-content/uploads/2017/08/squidward-anime-625x352.jpg", "profile[bio]": "Locust",
                                       "profile[github_link]": "https://github.com/seechinsu", "profile[linkedin_link]": "https://www.linkedin.com/in/se-chien-nick-hsu-b5723a37/", "profile[twitter_link]": "https://twitter.com/seechinsu"}, headers={"x-csrf-token": csrfToken})


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
