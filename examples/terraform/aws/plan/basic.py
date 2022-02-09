import time

from locust import task, FastHttpUser

# from locust import run_single_user, HttpUser
# import logging
# logging.info("this log message will go wherever the other locust log messages go")


tenant = "edujourneys-s.gazt.gov.sa"
sign_up_headers = {
    "x-tenant": tenant,
    "Content-Type": "application/json",
    "authorization": "3fb5deef-cde3-4e47-ab6a-769d401a5924"
}


class FullJourney(FastHttpUser):
    host = "https://stg-api.elhamsol.com"

    @task
    def on_start(self):
        sign_up = self.client.post(
            "/api/external_system/auth/anonymous/",
            json={"API-KEY": "3fb5deef-cde3-4e47-ab6a-769d401a5924"},
            headers=sign_up_headers)
        if sign_up.status_code == 201:
            user_key = sign_up.json().get('user_key')
            login = self.client.post(
                '/api/v1/auth_key/login-external-user/?format=json',
                json={"AUTH_KEY": f"{user_key}", "user_key": f"{user_key}"},
                headers=sign_up_headers)
            if login.status_code == 200:
                token = login.json().get('key')
                headers = {
                    "x-tenant": tenant,
                    "Content-Type": "application/json",
                    "accept-language": "ar",
                    "Authorization": f"Token {token}",
                    "Accept": "application/json"
                }
                self.client.get('/api/v1/cache/courses/?limit=150&type=public', headers=headers)
                self.client.get('/api/v1/cache/courses/279/?type=public', headers=headers)
                self.client.get('/api/v1/customers/attributes/', headers=headers)
                self.client.get('/api/v1/users/current-user-details/', headers=headers)
                self.client.get('/api/v1/user_certificates/', headers=headers)
                self.client.get('/api/v1/courses/user_progress/', headers=headers)
                self.client.get('/api/v1/courses/279/current_user_position/', headers=headers)
                self.client.get('/api/v1/user_badge/', headers=headers)
                self.client.get('/api/v1/users/current_user_statistics/', headers=headers)
                self.client.get('/api/v1/visited_containers/?course=279', headers=headers)
                time.sleep(10)
                for i in range(3041, 3046):
                    self.client.post(
                        '/api/v1/time_logs/?format=json',
                        json={"container": i, "start_time": "2020-05-11T20:52:00+0200",
                              "end_time": "2020-05-11T20:53:35+0200", "earn_percentage": "1"}
                        , headers=headers)
                    time.sleep(120)

# if __name__ == "__main__":
#     run_single_user(FullJourney)
