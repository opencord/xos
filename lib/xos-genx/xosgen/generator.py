import plyproto.model as m
import pdb
import plyproto.parser as plyproto
import traceback
import sys
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
        # TODO test me!
        if hasattr(self.args, 'rev') and self.args.rev:
            v = Proto2XProto()
            self.ast.accept(v)
        else:
            v = XOS2Jinja()
            self.ast.accept(v)
        return v

    def _get_template(self, target):
        if not os.path.isabs(target):
            return os.path.abspath(target)
        return target

    def _file_exists(self):
        # NOTE this method can be used in the jinja template
        def file_exists2(name):
            try:
                path = self.args.attic + '/' + name
            except TypeError:
                path = name
            return (os.path.exists(path))
        return file_exists2

    def _include_file(self):
        # NOTE this method can be used in the jinja template
        def include_file2(name):
            try:
                path = self.args.attic + '/' + name
            except TypeError:
                path = name
            return open(path).read()
        return include_file2
        # FIXME: Support templates in the future
        #return jinja2.Markup(loader.get_source(env, name)[0])

    def _load_jinja2_extensions(self):
        # NOTE why those cannot be in jinja2_extensions?
        self.os_template_env.globals['include_file'] = self.include_file()  # Generates a function
        self.os_template_env.globals['file_exists'] = self.file_exists()  # Generates a function

        for f in dir(jinja2_extensions):
            if f.startswith('xproto'):
                self.os_template_env.globals[f] = getattr(jinja2_extensions, f)

    def _add_context(self,):
        if not hasattr(self.args, 'kv'):
            return
        try:
            context = {}
            for s in self.args.kv.split(','):
                k, val = s.split(':')
                context[k] = val
            return context
        except Exception, e:
            print e.message

    def _write_file(self, content, file):

        # TODO add the ability to print multiple files!

        if not os.path.isabs(file):
            raise Exception("[XosGenX] The output file must be an absolute path!")

        fil = open(file, 'w')
        fil.write(content)
        fil.close()


    def generate(self):
        self.parser = plyproto.ProtobufAnalyzer()
        self.input = self._read_input_files(self.args.inputs)
        self.ast = self.parser.parse_string(self.input, debug=0)
        v = self._attach_parser()
        self.template_name = self._get_template(self.args.target)
        os_template_loader = jinja2.FileSystemLoader(searchpath=[os.path.split(self.template_name)[0]])
        self.os_template_env = jinja2.Environment(loader=os_template_loader)
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


class XOSGenerator_bk:
    def __init__(self, args):
        self.args = args

    def file_exists(self):
        def file_exists2(name):
            try:
                path = self.args.attic+'/'+name
            except TypeError:
                path = name
            return (os.path.exists(path))
        return file_exists2

    def include_file(self):
        def include_file2(name):
            try:
                path = self.args.attic+'/'+name
            except TypeError:
                path = name
            return open(path).read()
        return include_file2
        # FIXME: Support templates in the future
        #return jinja2.Markup(loader.get_source(env, name)[0])

    def generate(self):
        try:
            parser = plyproto.ProtobufAnalyzer()
            # NOTE why not passing this as input to the method and use `parse.add_argument` in xosgen.py?
            input = self.input

            ast = parser.parse_string(input, debug=0)

            if (self.args.rev):
                v = Proto2XProto()
                ast.accept(v)
            
            v = XOS2Jinja()
            ast.accept(v)
            
            try:
                template_name = self.args.template_dir + '/' + self.args.target
            except AttributeError:
                template_name = os.path.abspath(self.args.target)

            os_template_loader = jinja2.FileSystemLoader( searchpath=[os.path.split(template_name)[0]])
            os_template_env = jinja2.Environment(loader=os_template_loader)

            os_template_env.globals['include_file'] = self.include_file() # Generates a function
            os_template_env.globals['file_exists'] = self.file_exists() # Generates a function

            for f in dir(jinja2_extensions):
                if f.startswith('xproto'):
                    os_template_env.globals[f] = getattr(jinja2_extensions, f)

            template = os_template_env.get_template(os.path.split(template_name)[1])
            context = {}

            try:
                for s in self.args.kv.split(','):
                    k,val=s.split(':')
                    context[k]=val
            except Exception, e:
                print e.message
                pass

            rendered = template.render({"proto": {'message_table':v.models, 'messages':v.messages, 'message_names':[m['name'] for m in v.messages]},"context":context,"options":v.options})

            lines = rendered.splitlines()
            current_buffer = []
            for l in lines:
                if (l.startswith('+++')):

                    # NOTE why not:
                    if self.args.output:
                        path = self.args.output + '/' + l[4:]

                    # prefix = ''
                    # prefixes = self.args.output.rsplit('/',1)
                    # if (len(prefixes)>1):
                    #     path = prefix+'/'+l[4:]
                    #     direc = prefix
                    #     if (direc):
                    #         os.system('mkdir -p %s'%direc)
                    # else:
                    #     path = l[4:]
                    
                    fil = open(path,'w')
                    buf = '\n'.join(current_buffer)

                    obuf = buf

                    """
                    for d in options.dict:
                        df = open(d).read()
                        d = json.loads(df)

                        pattern = re.compile(r'\b(' + '|'.join(d.keys()) + r')\b')
                        obuf = pattern.sub(lambda x: d[x.group()], buf)
                    """

                    fil.write(obuf)
                    fil.close()

                    try:
                        quiet = self.args.quiet
                    except:
                        quiet = False
                    if (not quiet):
                        print 'Written to file %s'%path

                    current_buffer = []
                else:
                    current_buffer.append(l)

            if (current_buffer):
                print '\n'.join(current_buffer)
                return current_buffer

        except Exception as e:
            print "    Error occurred! file[%s]" % (self.args.inputs), e
            print '-'*60
            traceback.print_exc(file=sys.stdout)
            print '-'*60
            exit(1)
    
def main():
    generator = XOSGenerator(args)
    generator.generate()

if __name__=='__main__':
    main()
