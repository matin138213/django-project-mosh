from celery.app import task


@task
def say_hello(self):
    self.client.get('playground/hello/')
