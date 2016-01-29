from provider import Provider

class App(Provider):

    """
    App initialization. Sets up the socket used for the app.

    Important!
    Modify this function with care.
    """
    def __init__(self):
        Provider.__init__(self)

    """
    Implementation of add function as defined in the manifest. Replace this function with the
    functions for your app. Note that the name of the function must match the function as it is
    defined in your manifest (case-sensitive).
    """
    def add(self, a, b, progress, fail):
        return a + b


if __name__ == "__main__":

    app = App()
    app.run()