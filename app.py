from provider import Provider
from time import sleep

class App(Provider):

    """
    App initialization. Sets up the socket used for the app.

    Important!
    Modify this function with care.
    """
    def __init__(self):
        Provider.__init__(self)

    """
    Implementation of add function as defined in the manifest. Replace this function and the
    functions below with the functions for your app. Note that the name of the function must match
    the function as it is defined in your manifest (case-sensitive).
    """
    def add(self, a, b, progress, fail):
        return a + b

    """
    Implementation of add_with_progress function as defined in the manifest. This demonstrates the
    ability to update the progress of a calculation. The `progress` function has the signature:
        progress(progress, message="")
    where the `progress` parameter is a float and the `message` parameter is an optional string.
    """
    def add_with_progress(self, a, b, progress, fail):
        progress(0.25)
        sleep(1)
        progress(0.5, "Halfway done")
        sleep(1)
        progress(0.75)
        sleep(1)
        return a + b

    """
    Implementation of add_with_failure function as defined in the manifest. This demonstrates the
    ability to fail a calculation. The `fail` function has the signature:
        fail(code, message)
    where the `code` parameter is a string and the `message` parameter is also a string.
    """
    def add_with_failure(self, a, b, progress, fail):
        fail("my_error", "This is a test of the error functionality")

    """
    Implementation of get_blob_length function as defined in the manifest. This demonstrates how
    MessagePack binary values are automatically deserialized to bytearrays.
    """
    def get_blob_length(self, a, progress, fail):
        return len(a)

    """
    Implementation of get_hour function as defined in the manifest. This demonstrates how the
    MessagePack extension type for a datetime is automatically deserialized to a python datetime.
    """
    def get_hours(self, a, progress, fail):
        return a.hour


if __name__ == "__main__":

    app = App()
    app.run()