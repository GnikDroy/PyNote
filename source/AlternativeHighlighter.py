import multiprocessing
from pygments import lexers
from pygments import token,styles
import pygments

class Highlighter:

    def __init__(self, textwidget):
        self.textwidget = textwidget
        self.config()
        self.pygmentizer = PygmentizerProcess()
        self.textwidget.bind("<KeyRelease>",self.highlight_all,add="+")
        #self.textwidget.after(50, self._do_highlights)
    
    def config(self):
        def _list_all_token_types(tokentype):
            yield tokentype
            for sub in map(_list_all_token_types, tokentype.subtypes):
                for x in sub: yield x
        self._fonts = {}
        for bold in (True, False):
            for italic in (True, False):
                # the fonts will be updated later, see _on_config_changed()
                self._fonts[(bold, italic)] = tkFont.Font(
                    weight=('normal' if bold else 'normal'),
                    slant=('roman' if italic else 'roman'))
        self._ALL_TAGS = set(map(str, _list_all_token_types(token.Token)))
        style = styles.get_style_by_name("default")
        
        for tokentype, infodict in style:
            # this doesn't use underline and border
            # i don't like random underlines in my code and i don't know
            # how to implement the border with tkinter
            key = (infodict['bold'], infodict['italic'])   # pep8 line length
            kwargs = {'font': self._fonts[key]}
            if infodict['color'] is None:
                kwargs['foreground'] = ''    # reset it
            else:
                kwargs['foreground'] = '#' + infodict['color']
            if infodict['bgcolor'] is None:
                kwargs['background'] = ''
            else:
                kwargs['background'] = '#' + infodict['bgcolor']

            self.textwidget.tag_config(str(tokentype), **kwargs)
            self.textwidget.tag_lower(str(tokentype), 'sel')
            
    def on_destroy(self, junk=None):
        self.pygmentizer.process.terminate()

    # handle things from the highlighting process
    def _do_highlights(self,event=None):
        # this check is actually unnecessary; turns out that destroying
        # the text widget stops this timeout because the text widget's
        # after method was used, but i don't feel like relying on it
        if not self.pygmentizer.process.is_alive():
            return

        # if the pygmentizer process has put multiple result dicts to
        # the queue, only use the last one
        tags2add = None
        try:
            while True:
                tags2add = self.pygmentizer.out_queue.get(block=False)
        except:
            pass
        
        if tags2add is not None:
            # print("_do_highlights: got something")
            for tag in self._ALL_TAGS:
                self.textwidget.tag_remove(tag, '0.0', 'end')
            for tag, places in tags2add.items():
                self.textwidget.tag_add(tag, *places)

        # 50 milliseconds doesn't seem too bad, bigger timeouts tend to
        # make things laggy
        #self.textwidget.after(50, self._do_highlights)

    def highlight_all(self, junk=None):
        code = self.textwidget.get('1.0', 'end - 1 char')
        self.pygmentizer.in_queue.put(["python", code])
        self._do_highlights()

# CPython) so it's done in another process
class PygmentizerProcess:

    def __init__(self):
        self.in_queue = multiprocessing.Queue()   # contains strings
        self.out_queue = multiprocessing.Queue()  # dicts from _pygmentize()
        self.process = multiprocessing.Process(target=self._run)
        self.process.start()

    # returns {str(tokentype): [start1, end1, start2, end2, ...]}
    def _pygmentize(self, language, code):
        # pygments doesn't include any info about where the tokens are
        # so we need to do it manually :(
        lineno = 1
        column = 0
        ##########################################################################
        lexer=lexers.Python3Lexer()
        result = {}
        for tokentype, string in lexer.get_tokens(code):
            start = '%d.%d' % (lineno, column)
            if '\n' in string:
                lineno += string.count('\n')
                column = len(string.rsplit('\n', 1)[1])
            else:
                column += len(string)
            end = '%d.%d' % (lineno, column)
            result.setdefault(str(tokentype), []).extend([start, end])

        return result

    def _run(self):
        while True:
            # if multiple codes were queued while this thing was doing
            # the previous code, just do the last one and ignore the rest
            args = self.in_queue.get(block=True)
            try:
                while True:
                    args = self.in_queue.get(block=False)
                    # print("_run: ignoring a code")
            except:
                pass

            result = self._pygmentize(*args)
            self.out_queue.put(result)

