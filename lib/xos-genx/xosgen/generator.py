import plyproto.parser as plyproto
import jinja2
import os
from xos2jinja import XOS2Jinja
from proto2xproto import Proto2XProto
import jinja2_extensions

loader = jinja2.PackageLoader(__name__, 'templates')
env = jinja2.Environment(loader=loader)

class XOSGenerator:
    def __init__(self, args):
        self.context = {}
        self.args = args
        # TODO validate args (see xosgen.py for options)

    def _read_input_files(self, files):
        input = ""
        for fname in files:
            with open(fname) as infile:
                input += infile.read()
        return input

    def _attach_parser(self):
        if hasattr(self.args, 'rev') and self.args.rev:
            v = Proto2XProto()
            self.ast.accept(v)
        else:
            v = XOS2Jinja()
            self.ast.accept(v)
        return v

    def _get_template(self, target):
        if not os.path.isabs(target):
            return os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + '/targets/' + target)
        return target

    def _file_exists(self):
        # NOTE this method can be used in the jinja template
        def file_exists2(name):
            try:
                path = self.args.attic + '/' + name
            except Exception:
                path = name
            return (os.path.exists(path))

        return file_exists2

    def _include_file(self):
        # NOTE this method can be used in the jinja template
        def include_file2(name):
            try:
                path = self.args.attic + '/' + name
            except Exception:
                path = name
            return open(path).read()
        return include_file2
        # FIXME: Support templates in the future
        #return jinja2.Markup(loader.get_source(env, name)[0])

    def _load_jinja2_extensions(self):
        # NOTE why those cannot be in jinja2_extensions?
        self.os_template_env.globals['include_file'] = self._include_file()  # Generates a function
        self.os_template_env.globals['file_exists'] = self._file_exists()  # Generates a function

        for f in dir(jinja2_extensions):
            if f.startswith('xproto'):
                self.os_template_env.globals[f] = getattr(jinja2_extensions, f)

    def _add_context(self,):
        if not hasattr(self.args, 'kv') or not self.args.kv:
            return
        try:
            context = {}
            for s in self.args.kv.split(','):
                k, val = s.split(':')
                context[k] = val
            return context
        except Exception, e:
            print e.message

    def _write_file(self, content, dir):

        if not os.path.isabs(dir):
            raise Exception("[XosGenX] The output dir must be an absolute path!")

        if not os.path.isdir(dir):
            raise Exception("[XosGenX] The output dir must be a directory!")

        lines = content.splitlines()
        current_buffer = []
        for l in lines:
            if (l.startswith('+++')):

                if self.args.output:
                    path = self.args.output + '/' + l[4:]

                fil = open(path, 'w')
                buf = '\n'.join(current_buffer)

                obuf = buf

                fil.write(obuf)
                fil.close()

                if hasattr(self.args, 'quiet') and self.args.quiet == False:
                    print "Save file to: %s" % path

                current_buffer = []
            else:
                current_buffer.append(l)


    def generate(self):
        self.parser = plyproto.ProtobufAnalyzer()
        self.input = self._read_input_files(self.args.inputs)
        self.ast = self.parser.parse_string(self.input, debug=0)
        v = self._attach_parser()
        self.template_name = self._get_template(self.args.target)
        os_template_loader = jinja2.FileSystemLoader(searchpath=[os.path.split(self.template_name)[0]])
        self.os_template_env = jinja2.Environment(loader=os_template_loader)
        self._load_jinja2_extensions()
        self.template = self.os_template_env.get_template(os.path.split(self.template_name)[1])
        self.context = self._add_context()

        rendered = self.template.render(
            {"proto":
                {
                    'message_table': v.models,
                    'messages': v.messages,
                    'message_names': [m['name'] for m in v.messages]
                },
                "context": self.context,
                "options": v.options
            }
        )

        if hasattr(self.args, 'output'):
            self._write_file(rendered, self.args.output)

        return rendered
