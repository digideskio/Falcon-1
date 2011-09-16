import os

DEFAULT_NUM_FLIGHTS = 10

# TODO: use files
all_flights = []

def get_flights(first=DEFAULT_NUM_FLIGHTS, after=None):
    return all_flights[:first] # TODO

def get_flight(n):
    return all_flights[n] # TODO

def add_flight(flight):
    all_flights.append(flight) # TODO: sort?

class Flight:
    def __init__(self, *args, **kwargs):
        arg_names = ('departs', 'dept_time', 'arrives', 'arr_time')
        if len(args) == 1:
            self._init_str(self, args[0])
        elif 'str' in kwargs:
            self._init_str(self, kwargs['str'])
        elif len(args) == 4:
            self._init_arr_dept(self, *args)
        elif reduce(lambda x, y: x and y, 
                    [(name in kwargs) for name in arg_names]):
            self._init_arr_dept(self, **kwargs)
        else:
            raise TypeError('Flight constructor takes either a string or ' +
                            'the arguments (departs, dept_time, arrives, arr_time)')

    def _init_str(self, str):
        self.str = str
        
    def _init_dept_arr(self, departs, dept_time, arrives, arr_time):
        self.str = departs + str(dept_time) + arrives + str(arr_time)
    
    def __str__(self):
        return self.str

def Lookup(Str):
	DictFile = codecs.open('dict.txt', 'r', 'utf-8')
	
	Result = None
	
	Line = DictFile.readline()
	while Line != '':
		if Line[:len(Str) + 1] == Str + ' ':
			Result = Line
			break
		Line = DictFile.readline()
	
	DictFile.close()
	
	return Result

def LookupList(Str):
	Line = Lookup(Str)
	if Line == None:
		return None
	
	# Word
	Result = [Line[:Line.find(' ')]]
	
	# Pronunciation
	Pos = Line.find('/') + 1
	Result.append(Line[Pos:Line.find('/', Pos)])
	
	# Memory tool
	Pos = Line.find('[') + 1
	Result.append(Line[Pos:Line.find(']', Pos)])
	
	# Noun
	Pos = Line.find(']', Pos) + 2
	Result.append(Line[Pos:Line.find(';', Pos)])
	
	# Verb
	Pos = Line.find(';', Pos) + 2
	Result.append(Line[Pos:Line.find(';', Pos)])
	
	# Adjective
	Pos = Line.find(';', Pos) + 2
	Result.append(Line[Pos:-1])
	
	return Result

def AddEntry(Word, Pron, Mem, Noun, Verb, Adj):
	DictFile = codecs.open('dict.txt', 'a', 'utf-8')
	DictFile.write(Word + ' /' + Pron + '/ [' + Mem + '] ' + Noun + '; ' +
			Verb + '; ' + Adj + '\n')
	DictFile.close()
	
	DeclsFile = codecs.open('decls.txt', 'a', 'utf-8')
	Decls = analyze.Analysis(Word).Decl
	DeclsFile.write(Decls[0])
	for Decl in Decls[1:]:
		DeclsFile.write(' ' + Decl)
	DeclsFile.write('\n')
	DeclsFile.close()

def DeleteEntry(Word):
	DictFile = codecs.open('dict.txt', 'r', 'utf-8')
	NewDictFile = codecs.open('dict_new.txt', 'w', 'utf-8')
	
	Line = DictFile.readline()
	while Line != '':
		if Line[:len(Word) + 1] != Word + ' ':
			NewDictFile.write(Line)
		
		Line = DictFile.readline()
	
	DictFile.close()
	NewDictFile.close()
	os.remove('dict.txt')
	os.rename('dict_new.txt', 'dict.txt')
	
	DeclFile = codecs.open('decls.txt', 'r', 'utf-8')
	NewDeclFile = codecs.open('decls_new.txt', 'w', 'utf-8')
	
	Word = analyze.Expand(Word)
	Line = DeclFile.readline()
	while Line != '':
		if Line[:len(Word) + 1] != Word + ' ':
			NewDeclFile.write(Line)
		
		Line = DeclFile.readline()
	
	DeclFile.close()
	NewDeclFile.close()
	os.remove('decls.txt')
	os.rename('decls_new.txt', 'decls.txt')
