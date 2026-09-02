from locust import HttpUser, task, between


class PerformanceValidatorUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def analyze_performance(self):
        self.client.post(
            "/analyze/",
            json={
                "current_value": 105
            },
            name="/analyze/"
        )