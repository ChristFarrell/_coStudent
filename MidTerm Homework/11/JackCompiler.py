import sys
import re
from pathlib import Path
from typing import List, Tuple, Optional

# -------------------------
# Tokenizer
# -------------------------
TOKEN_SPEC = [
    ('COMMENT', r'//.*|/\*[\s\S]*?\*/'),
    ('STRING',  r'"[^"\n]*"'),
    ('INT',     r'\d+'),
    ('ID',      r'[A-Za-z_][A-Za-z0-9_]*'),
    ('SYMBOL',  r'[{}()\[\].,;+\-*/&|<>=~]'),
    ('WS',      r'[ \t\r\n]+'),
]
TOK_REGEX = '|'.join(f'(?P<{n}>{p})' for n,p in TOKEN_SPEC)
KEYWORDS = {
    'class','constructor','function','method','field','static','var',
    'int','char','boolean','void','true','false','null','this',
    'let','do','if','else','while','return'
}

class Token:
    def __init__(self, kind: str, value: str):
        self.kind = kind
        self.value = value
    def __repr__(self):
        return f"Token({self.kind!r}, {self.value!r})"

class Tokenizer:
    def __init__(self, text: str):
        self.tokens: List[Token] = []
        for m in re.finditer(TOK_REGEX, text):
            kind = m.lastgroup
            val = m.group(0)
            if kind == 'WS' or kind == 'COMMENT':
                continue
            if kind == 'ID' and val in KEYWORDS:
                kind = 'KEYWORD'
            self.tokens.append(Token(kind, val))
        self.pos = 0

    def has_more(self) -> bool:
        return self.pos < len(self.tokens)
    def peek(self) -> Optional[Token]:
        return self.tokens[self.pos] if self.has_more() else None
    def advance(self) -> Optional[Token]:
        t = self.peek()
        if t: self.pos += 1
        return t
    def expect(self, value: Optional[str]=None, kind: Optional[str]=None) -> Token:
        t = self.advance()
        if not t:
            raise SyntaxError(f"Unexpected EOF, expected {value or kind}")
        if kind and t.kind != kind:
            raise SyntaxError(f"Expected kind {kind}, got {t.kind} ('{t.value}')")
        if value and t.value != value:
            raise SyntaxError(f"Expected '{value}', got '{t.value}'")
        return t

# -------------------------
# Symbol Table
# -------------------------
class SymbolTable:
    def __init__(self):
        self.class_scope = {}  # name -> (type, kind, index)
        self.sub_scope = {}
        self.counts = {'static':0,'field':0,'arg':0,'var':0}
    def start_subroutine(self):
        self.sub_scope.clear()
        self.counts['arg'] = 0
        self.counts['var'] = 0
    def define(self, name:str, typ:str, kind:str):
        idx = self.counts[kind]
        self.counts[kind] += 1
        table = self.class_scope if kind in ('static','field') else self.sub_scope
        table[name] = (typ, kind, idx)
    def var_count(self, kind:str) -> int:
        return self.counts[kind]
    def kind_of(self, name:str) -> Optional[str]:
        if name in self.sub_scope: return self.sub_scope[name][1]
        if name in self.class_scope: return self.class_scope[name][1]
        return None
    def type_of(self, name:str) -> Optional[str]:
        if name in self.sub_scope: return self.sub_scope[name][0]
        if name in self.class_scope: return self.class_scope[name][0]
        return None
    def index_of(self, name:str) -> Optional[int]:
        if name in self.sub_scope: return self.sub_scope[name][2]
        if name in self.class_scope: return self.class_scope[name][2]
        return None

# -------------------------
# VM Writer
# -------------------------
class VMWriter:
    def __init__(self, path:Path):
        self.f = open(path, 'w')
    def write(self, line:str):
        self.f.write(line + '\n')
    def write_push(self, segment:str, index:int): self.write(f'push {segment} {index}')
    def write_pop(self, segment:str, index:int):  self.write(f'pop {segment} {index}')
    def write_arithmetic(self, cmd:str): self.write(cmd)
    def write_label(self, label:str): self.write(f'label {label}')
    def write_goto(self, label:str): self.write(f'goto {label}')
    def write_if(self, label:str): self.write(f'if-goto {label}')
    def write_call(self, name:str, n_args:int): self.write(f'call {name} {n_args}')
    def write_function(self, name:str, n_locals:int): self.write(f'function {name} {n_locals}')
    def write_return(self): self.write('return')
    def close(self): self.f.close()

# -------------------------
# Compilation Engine
# -------------------------
class CompilationEngine:
    OP_MAP = {'+':'add','-':'sub','*':'call Math.multiply 2','/':'call Math.divide 2',
              '&':'and','|':'or','<':'lt','>':'gt','=':'eq'}
    UNARY_MAP = {'-':'neg','~':'not'}

    def __init__(self, tokenizer:Tokenizer, writer:VMWriter, sym:SymbolTable, class_name:str):
        self.t = tokenizer
        self.w = writer
        self.sym = sym
        self.class_name = class_name
        self.label_id = 0
    def new_label(self, base='L') -> str:
        self.label_id += 1
        return f"{base}{self.label_id}"
    def kind_to_segment(self, kind:str) -> str:
        return {'static':'static','field':'this','arg':'argument','var':'local'}.get(kind)

    # class -> 'class' className '{' classVarDec* subroutineDec* '}'
    def compile_class(self):
        self.t.expect('class','KEYWORD')
        class_name = self.t.expect(kind='ID').value
        self.class_name = class_name
        self.t.expect('{','SYMBOL')
        while True:
            p = self.t.peek()
            if p and p.kind == 'KEYWORD' and p.value in ('static','field'):
                self.compile_class_var_dec()
            else:
                break
        while True:
            p = self.t.peek()
            if p and p.kind == 'KEYWORD' and p.value in ('constructor','function','method'):
                self.compile_subroutine()
            else:
                break
        self.t.expect('}','SYMBOL')

    def compile_class_var_dec(self):
        kind = self.t.expect(kind='KEYWORD').value  # static|field
        typ_tok = self.t.expect()  # ID or KEYWORD type
        typ = typ_tok.value
        while True:
            name = self.t.expect(kind='ID').value
            self.sym.define(name, typ, 'field' if kind=='field' else 'static')
            if self.t.peek() and self.t.peek().value == ',':
                self.t.advance()
                continue
            break
        self.t.expect(';','SYMBOL')

    def compile_subroutine(self):
        sub_kind = self.t.expect(kind='KEYWORD').value  # constructor|function|method
        # return type
        ret_tok = self.t.expect()
        if ret_tok.kind not in ('KEYWORD','ID'):
            raise SyntaxError('Invalid return type')
        sub_name = self.t.expect(kind='ID').value
        full_name = f"{self.class_name}.{sub_name}"
        self.sym.start_subroutine()
        self.t.expect('(','SYMBOL')
        # if method, first argument is 'this'
        if sub_kind == 'method':
            # register 'this' as arg 0
            self.sym.define('this', self.class_name, 'arg')
        n_params = self.compile_parameter_list()
        self.t.expect(')','SYMBOL')
        self.t.expect('{','SYMBOL')
        # varDec*
        n_locals = 0
        while self.t.peek() and self.t.peek().kind == 'KEYWORD' and self.t.peek().value == 'var':
            self.t.advance()  # consume 'var'
            typ_tok = self.t.expect()  # type
            typ = typ_tok.value
            while True:
                name = self.t.expect(kind='ID').value
                self.sym.define(name, typ, 'var')
                n_locals += 1
                if self.t.peek() and self.t.peek().value == ',':
                    self.t.advance()
                    continue
                break
            self.t.expect(';','SYMBOL')
        # write function header
        self.w.write_function(full_name, n_locals)
        # constructor: allocate fields
        if sub_kind == 'constructor':
            n_fields = self.sym.counts['field']
            self.w.write_push('constant', n_fields)
            self.w.write_call('Memory.alloc', 1)
            self.w.write_pop('pointer', 0)  # this = base
        # method: set pointer 0 to argument 0
        if sub_kind == 'method':
            self.w.write_push('argument', 0)
            self.w.write_pop('pointer', 0)
        # statements
        self.compile_statements()
        self.t.expect('}','SYMBOL')

    def compile_parameter_list(self) -> int:
        count = 0
        # empty parameter list handled by caller (peek for ')')
        while True:
            p = self.t.peek()
            if not p or p.value == ')':
                break
            # type
            typ_tok = self.t.expect()
            if typ_tok.kind not in ('KEYWORD','ID'):
                raise SyntaxError('Expected type in parameter list')
            typ = typ_tok.value
            name = self.t.expect(kind='ID').value
            self.sym.define(name, typ, 'arg')
            count += 1
            if self.t.peek() and self.t.peek().value == ',':
                self.t.advance()
                continue
            break
        return count

    def compile_statements(self):
        while True:
            p = self.t.peek()
            if not p or p.kind != 'KEYWORD': break
            if p.value == 'let': self.compile_let()
            elif p.value == 'if': self.compile_if()
            elif p.value == 'while': self.compile_while()
            elif p.value == 'do': self.compile_do()
            elif p.value == 'return': self.compile_return()
            else: break

    def compile_do(self):
        self.t.expect(value='do', kind='KEYWORD')
        self.compile_subroutine_call()
        # discard return value
        self.w.write_pop('temp', 0)
        self.t.expect(';','SYMBOL')

    def compile_let(self):
        self.t.expect('let','KEYWORD')
        varname = self.t.expect(kind='ID').value
        is_array = False
        if self.t.peek() and self.t.peek().value == '[':
            # array assignment
            self.t.expect('[','SYMBOL')
            self.compile_expression()
            self.t.expect(']','SYMBOL')
            kind = self.sym.kind_of(varname)
            idx = self.sym.index_of(varname)
            seg = self.kind_to_segment(kind)
            if seg is None:
                raise SyntaxError(f"Unknown variable {varname}")
            self.w.write_push(seg, idx)
            self.w.write_arithmetic('add')
            is_array = True
        self.t.expect('=','SYMBOL')
        self.compile_expression()
        self.t.expect(';','SYMBOL')
        if is_array:
            # value, addr on stack -> store
            self.w.write_pop('temp', 0)    # value
            self.w.write_pop('pointer', 1) # that = addr
            self.w.write_push('temp', 0)
            self.w.write_pop('that', 0)
        else:
            kind = self.sym.kind_of(varname)
            idx = self.sym.index_of(varname)
            seg = self.kind_to_segment(kind)
            if seg is None:
                raise SyntaxError(f"Unknown variable {varname}")
            self.w.write_pop(seg, idx)

    def compile_while(self):
        self.t.expect('while','KEYWORD')
        start = self.new_label('WHILE_START')
        end = self.new_label('WHILE_END')
        self.w.write_label(start)
        self.t.expect('(','SYMBOL')
        self.compile_expression()
        self.t.expect(')','SYMBOL')
        # if not expr -> goto end
        self.w.write_arithmetic('not')
        self.w.write_if(end)
        self.t.expect('{','SYMBOL')
        self.compile_statements()
        self.t.expect('}','SYMBOL')
        self.w.write_goto(start)
        self.w.write_label(end)

    def compile_return(self):
        self.t.expect('return','KEYWORD')
        if self.t.peek() and self.t.peek().value != ';':
            self.compile_expression()
        else:
            # push 0 for void returns
            self.w.write_push('constant', 0)
        self.t.expect(';','SYMBOL')
        self.w.write_return()

    def compile_if(self):
        self.t.expect('if','KEYWORD')
        self.t.expect('(','SYMBOL')
        self.compile_expression()
        self.t.expect(')','SYMBOL')
        true_label = self.new_label('IF_TRUE')
        false_label = self.new_label('IF_FALSE')
        end_label = self.new_label('IF_END')
        # if-goto true; goto false; label true; ...
        self.w.write_if(true_label)
        self.w.write_goto(false_label)
        self.w.write_label(true_label)
        self.t.expect('{','SYMBOL')
        self.compile_statements()
        self.t.expect('}','SYMBOL')
        if self.t.peek() and self.t.peek().kind == 'KEYWORD' and self.t.peek().value == 'else':
            self.w.write_goto(end_label)
            self.w.write_label(false_label)
            self.t.expect('else','KEYWORD')
            self.t.expect('{','SYMBOL')
            self.compile_statements()
            self.t.expect('}','SYMBOL')
            self.w.write_label(end_label)
        else:
            self.w.write_label(false_label)

    def compile_expression(self):
        self.compile_term()
        while self.t.peek() and self.t.peek().value in ('+','-','*','/','&','|','<','>','='):
            op = self.t.advance().value
            self.compile_term()
            cmd = self.OP_MAP[op]
            self.w.write_arithmetic(cmd)

    def compile_term(self):
        p = self.t.peek()
        if not p:
            raise SyntaxError('Unexpected EOF in term')
        if p.kind == 'INT':
            val = int(self.t.advance().value)
            self.w.write_push('constant', val)
        elif p.kind == 'STRING':
            s = self.t.advance().value[1:-1]
            self.w.write_push('constant', len(s))
            self.w.write_call('String.new', 1)
            for ch in s:
                self.w.write_push('constant', ord(ch))
                self.w.write_call('String.appendChar', 2)
        elif p.kind == 'KEYWORD' and p.value in ('true','false','null','this'):
            kw = self.t.advance().value
            if kw == 'true':
                self.w.write_push('constant', 0)
                self.w.write_arithmetic('not')
            elif kw in ('false','null'):
                self.w.write_push('constant', 0)
            elif kw == 'this':
                self.w.write_push('pointer', 0)
        elif p.kind == 'SYMBOL' and p.value in ('-','~'):
            op = self.t.advance().value
            self.compile_term()
            self.w.write_arithmetic(self.UNARY_MAP[op])
        elif p.kind == 'ID':
            # could be varName, varName[expr], subroutineCall
            name = self.t.advance().value
            nxt = self.t.peek()
            if nxt and nxt.value == '[':
                # array access
                self.t.expect('[','SYMBOL')
                self.compile_expression()
                self.t.expect(']','SYMBOL')
                kind = self.sym.kind_of(name)
                idx = self.sym.index_of(name)
                seg = self.kind_to_segment(kind)
                self.w.write_push(seg, idx)
                self.w.write_arithmetic('add')
                self.w.write_pop('pointer', 1)
                self.w.write_push('that', 0)
            elif nxt and (nxt.value == '.' or nxt.value == '('):
                # subroutine call; need to handle name already read
                self.compile_subroutine_call(pre_name=name)
            else:
                kind = self.sym.kind_of(name)
                idx = self.sym.index_of(name)
                seg = self.kind_to_segment(kind)
                if seg is None:
                    raise SyntaxError(f"Unknown variable {name}")
                self.w.write_push(seg, idx)
        elif p.kind == 'SYMBOL' and p.value == '(':
            self.t.expect('(','SYMBOL')
            self.compile_expression()
            self.t.expect(')','SYMBOL')
        else:
            raise SyntaxError(f"Unexpected token in term: {p}")

    def compile_expression_list(self) -> int:
        # returns number of expressions parsed
        if self.t.peek() and self.t.peek().value == ')':
            return 0
        n = 0
        while True:
            self.compile_expression()
            n += 1
            if self.t.peek() and self.t.peek().value == ',':
                self.t.advance()
                continue
            break
        return n

    def compile_subroutine_call(self, pre_name:Optional[str]=None):
        # Handles both: subName(exprList)  OR (className|varName).subName(exprList)
        n_args = 0
        if pre_name is None:
            name = self.t.expect(kind='ID').value
        else:
            name = pre_name
        if self.t.peek() and self.t.peek().value == '.':
            self.t.expect('.','SYMBOL')
            subname = self.t.expect(kind='ID').value
            # if name is a variable -> method call on object
            kind = self.sym.kind_of(name)
            if kind:
                seg = self.kind_to_segment(kind)
                idx = self.sym.index_of(name)
                self.w.write_push(seg, idx)
                full_name = f"{self.sym.type_of(name)}.{subname}"
                n_args = 1
            else:
                full_name = f"{name}.{subname}"
            self.t.expect('(','SYMBOL')
            n = self.compile_expression_list()
            n_args += n
            self.t.expect(')','SYMBOL')
            self.w.write_call(full_name, n_args)
        elif self.t.peek() and self.t.peek().value == '(':
            # method in same class -> push pointer 0
            self.t.expect('(','SYMBOL')
            # push this
            self.w.write_push('pointer', 0)
            n_args = 1
            n = self.compile_expression_list()
            n_args += n
            self.t.expect(')','SYMBOL')
            full_name = f"{self.class_name}.{name}"
            self.w.write_call(full_name, n_args)
        else:
            raise SyntaxError('Malformed subroutine call')

# -------------------------
# Driver
# -------------------------
def compile_file(path:Path):
    text = path.read_text()
    tokenizer = Tokenizer(text)
    # find class name
    t2 = Tokenizer(text)
    class_name = None
    while t2.has_more():
        tok = t2.advance()
        if tok.kind == 'KEYWORD' and tok.value == 'class':
            class_name = t2.expect(kind='ID').value
            break
    if not class_name:
        raise SyntaxError('No class declaration found')
    outpath = path.with_suffix('.vm')
    writer = VMWriter(outpath)
    sym = SymbolTable()
    engine = CompilationEngine(tokenizer, writer, sym, class_name)
    engine.compile_class()
    writer.close()
    print(f'Wrote {outpath}')

def main(argv):
    if len(argv) < 2:
        print('Usage: python jack_compiler_full.py <file.jack | directory>')
        return
    p = Path(argv[1])
    if p.is_dir():
        for f in sorted(p.glob('*.jack')):
            compile_file(f)
    elif p.is_file():
        compile_file(p)
    else:
        print('Path not found')

if __name__ == '__main__':
    main(sys.argv)
