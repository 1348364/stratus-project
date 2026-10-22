"""Small typed NBT codec for isolated Minecraft test-world data only."""
from dataclasses import dataclass
from io import BytesIO
import gzip,struct

@dataclass
class Tag:
    kind:int
    value:object

def read(data):
    f=BytesIO(data)
    def number(fmt):return struct.unpack('>'+fmt,f.read(struct.calcsize('>'+fmt)))[0]
    def string():return f.read(number('H')).decode('utf-8')
    def payload(k):
        if k in range(1,7):return number({1:'b',2:'h',3:'i',4:'q',5:'f',6:'d'}[k])
        if k==7:return f.read(number('i'))
        if k==8:return string()
        if k==9:
            element=number('B');count=number('i')
            return (element,[Tag(element,payload(element)) for _ in range(count)])
        if k==10:
            out={}
            while True:
                t=number('B')
                if not t:return out
                name=string();out[name]=Tag(t,payload(t))
        if k in (11,12):
            count=number('i');return list(struct.unpack('>'+str(count)+('i' if k==11 else 'q'),f.read(count*(4 if k==11 else 8))))
        raise ValueError(k)
    k=number('B');name=string();return name,Tag(k,payload(k))

def write(name,root):
    f=BytesIO()
    def number(fmt,value):f.write(struct.pack('>'+fmt,value))
    def string(value):
        b=value.encode('utf-8');number('H',len(b));f.write(b)
    def payload(t):
        k,v=t.kind,t.value
        if k in range(1,7):number({1:'b',2:'h',3:'i',4:'q',5:'f',6:'d'}[k],v)
        elif k==7:number('i',len(v));f.write(v)
        elif k==8:string(v)
        elif k==9:
            element,items=v;number('B',element);number('i',len(items))
            for item in items:payload(item)
        elif k==10:
            for name,item in v.items():number('B',item.kind);string(name);payload(item)
            number('B',0)
        elif k in (11,12):
            number('i',len(v));f.write(struct.pack('>'+str(len(v))+('i' if k==11 else 'q'),*v))
        else:raise ValueError(k)
    number('B',root.kind);string(name);payload(root);return f.getvalue()

def load(path):return read(gzip.decompress(path.read_bytes()))
def save(path,name,tag):path.write_bytes(gzip.compress(write(name,tag),mtime=0))
def plain(tag):
    if tag.kind==10:return {k:plain(v) for k,v in tag.value.items()}
    if tag.kind==9:return [plain(v) for v in tag.value[1]]
    return tag.value
