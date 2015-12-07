from thinksocket import ThinkSocket

class App(object):

    """
    App initialization. Sets up the socket used for the app.

    Important!
    Modify this function with care.
    """
    def __init__(self, sock):
        self.sock = sock

    """
    Runs the app.
    1. Connects to the calculation supervisor.
    2. Registers itself as a calculation provider.
    3. Waits for the function.
    4. Computes the function.
    5. Sends result.

    Important!
    Modify this function with care.
    """
    def _run(self):
        self.sock.connect()
        self.sock.register()
        header = self.sock.receive_header()
        action = header["action"]
        if action == "function":
            request = self.sock.receive_request(header["length"])
            name = request["name"]
            args = request["args"]
            try:
                result = getattr(self, name)(*args)
                self.sock.send_result(result)
            except AttributeError as e:
                raise NotImplemented("Method `" + name + "` not implemented")
        else:
            raise TypeError("Expected action type to be `function` but got `" + action + "`")

    """
    Implementation of add function as defined in the manifest. Replace this function with the
    functions for your app. Note that the name of the function must match the function as it is
    defined in your manifest (case-sensitive).
    """
    def add(self, a, b):
        return a + b


if __name__ == "__main__":

    with ThinkSocket() as sock:
        app = App(sock)
        app._run()