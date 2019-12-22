import os, sys, subprocess, argparse
#Payload is a file path to a switch payload
fusee_path = "fusee-launcher.py"

class fusee_object:
    def __init__(self, print_function = print, result_function = None):
        self.running = False
        self.print_function = print_function
        self.result_function = result_function
        self.cwd = os.path.dirname(os.path.abspath(__file__))

    def inject(self, payload):
        self.running = True
        if payload:
            p = subprocess.Popen([sys.executable, '-u', os.path.join(self.cwd, fusee_path), payload],
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, 
                bufsize=1,
            )

            with p.stdout:
                for line in iter(p.stdout.readline, b''):
                    self.do_print_function(line)
            p.wait()
        else:
            print("Payload is nonetype")
        self.running = False

    def do_print_function(self, string):
        if self.print_function:
            self.print_function(string)

if __name__ == "__main__":
    def create_arg_parser():
        """"Creates and returns the ArgumentParser object."""
        parser = argparse.ArgumentParser(description='Pass file path of payload to inject')
        parser.add_argument('payload',
                        help='Path to fusee payload')
        return parser

    arg_parser = create_arg_parser()
    parsed_args = arg_parser.parse_args(sys.argv[1:])
    payload = parsed_args.payload

    fusee = fusee_object(print)
    fusee.inject(payload)
else:
    injector = fusee_object()
