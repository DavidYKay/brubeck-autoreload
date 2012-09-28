import sys
import os
from datetime import datetime


from brubeck.request_handling import Brubeck
from brubeck.connections import Mongrel2Connection
from demo_minimal import DemoHandler

import autoreload

#lass Command(BaseCommand):
class Command:
    def __init__(self, *args, **options):
        self.stdout = sys.stdout

    def run(self, *args, **options):
        """
        Runs the server, using the autoreloader if needed
        """
        use_reloader = options.get('use_reloader')

        if use_reloader:
            autoreload.main(self.inner_run, args, options)
        else:
            self.inner_run(*args, **options)

    def inner_run(self, *args, **options):
        threading = options.get('use_threading')
        shutdown_message = options.get('shutdown_message', '')
        quit_command = (sys.platform == 'win32') and 'CTRL-BREAK' or 'CONTROL-C'

        #self.stdout.write("Validating models...\n\n")
        #self.validate(display_num_errors=True)
        #self.stdout.write((
        #    "%(started_at)s\n"
        #    "Brubeck version %(version)s,\n"
        #    "Development server is running at http://%(addr)s:%(port)s/\n"
        #    "Quit the server with %(quit_command)s.\n"
        #) % {
        #    "started_at": datetime.now().strftime('%B %d, %Y - %X'),
        #    "version": self.get_version(),
        #    #"settings": settings.SETTINGS_MODULE,
        #    "addr": self._raw_ipv6 and '[%s]' % self.addr or self.addr,
        #    "port": self.port,
        #    "quit_command": quit_command,
        #})

        try:
            """
              handler = self.get_handler(*args, **options)
              basehttp.run(self.addr, int(self.port), handler,
                           ipv6=self.use_ipv6, threading=threading)
            """
            config = {
                'msg_conn': Mongrel2Connection('tcp://127.0.0.1:9999',
                                               'tcp://127.0.0.1:9998'),
                'handler_tuples': [(r'^/brubeck', DemoHandler)],
            }
            app = Brubeck(**config)
            app.run()

        #except WSGIServerException as e:
        #    # Use helpful error messages instead of ugly tracebacks.
        #    ERRORS = {
        #        13: "You don't have permission to access that port.",
        #        98: "That port is already in use.",
        #        99: "That IP address can't be assigned-to.",
        #    }
        #    try:
        #        error_text = ERRORS[e.args[0].args[0]]
        #    except (AttributeError, KeyError):
        #        error_text = str(e)
        #    sys.stderr.write("Error: %s" % error_text)
        #    # Need to use an OS exit because sys.exit doesn't work in a thread
        #    os._exit(1)
        except KeyboardInterrupt:
            if shutdown_message:
                self.stdout.write(shutdown_message)
            sys.exit(0)

if __name__ == '__main__':
    Command().run(use_reloader=True)
