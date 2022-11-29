from os import system as sys
from os import get_terminal_size as gts
'''
class Cellule:

    def __init__(self, var: object, next: object = None):
        self.var = var
        self.next = next


class Pile:

    def __init__(self):
        """<-O<-O<-O"""
        self.head = None

    def empty(self):
        return self.head == None

    def empile(self, element):
        self.head = Cellule(element, self.head)

    def depile(self) -> object:
        if self.empty():
            return None
        x = self.head.var
        self.head = self.head.next
        print(x)
        return x
'''


class UI:

    def __init__(self, autoflush: bool = False):
        self.autoflush = autoflush
        self.end_vprint = True
        self.end_vimage = True
        self.buff_vprint = ""
        self.buff_vimage = list()
        self.buff_vpara = list()
        self.size = gts()

    def update_size(function):

        def vprefct(self, *args, **kwargs):
            self.size = gts()
            #print((args,kwargs))
            function(self, *args, **kwargs)

        return vprefct

    def flush(self, function):
        if function == self.vprint:
            self.vprint('', True)
        elif function == self.vimage:
            lines = []
            for cmi in self.buff_vimage:
                lines.append([])
                for line in cmi:
                    lines[-1].append(line)
                cmi.close()
            self.buff_vimage = list()

            maxlen = max([len(l) for l in lines])
            for obj in lines:
                objlen = len(obj)
                objdiff = maxlen - objlen
                for i in range(objdiff):
                    obj.append("\n")

            for i in range(maxlen):
                for obj in lines:
                    self.vprint(obj[i][:-1], end=False)
                    #print("##################"+self.buff_vprint)
                self.flush(self.vprint)

        elif function == self.vpara:
            lines = []
            for para in self.buff_vpara:
                lines.append([])
                for line in para:
                    lines[-1].append(line)
            self.buff_vpara = list()

            maxlen = max([len(l) for l in lines])
            for obj in lines:
                objlen = len(obj)
                objdiff = maxlen - objlen
                for i in range(objdiff):
                    obj.append("\n")

            for i in range(maxlen):
                for obj in lines:
                    self.vprint(obj[i][:-1], end=False)
                self.flush(self.vprint)

    #@update_size
    def vprint(self, txt, end: bool = None, buff = "    "):
        """Print a TUI line"""
        end = self.autoflush if end == None else end
        self.buff_vprint += buff + txt
        if not end:
            return
        print(self.buff_vprint)
        self.buff_vprint = ""

    def clear(self):
        """Clear the TUI"""
        sys("clear")

    #@update_size
    def vimage(self, fileaspath: str, end: bool = None):
        """Print an Image .cmi (CharMapImage) to the terminal\n
        If end=True, the futur image will be stacked"""
        end = self.autoflush if end == None else end
        self.buff_vimage.append(open(fileaspath, 'r'))
        # Ne print pas si on veut stack
        if not end:
            return

        self.flush(self.vimage)

    def vpara(self, paragraphe: str, end: bool = None):
        end = self.autoflush if end == None else end
        self.buff_vpara.append(
            [line + "\n" for line in paragraphe.split("\n") if line != ['']])
        # Ne print pas si on veut stack
        if not end:
            return

        self.flush(self.vpara)

    def vseparation(self):
        self.vprint("\n",end = True)
        columns,lines = gts()
        del lines
        for i in range(columns):
            self.vprint("#",buff = "")
            self.vprint("#",buff = "")
        self.flush(self.vprint)

    def vinput(self,prompt:str):
        return input(prompt)