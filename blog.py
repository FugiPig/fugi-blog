#from latex2mathml import convert_tex_to_mml
import markdown
import latex2mathml.converter
with open("template-blog.html","r",encoding="utf-8") as r:
    PAGE_HTML=r.read()
def get_html(filename,blogname):
    mdstr=""
    with open(filename,"r",encoding="utf-8")as r:
        mdstr=r.read()
    #print(markdown.markdown(mdstr))
    #print(mdstr)
    mdstr=PAGE_HTML%(blogname,"%s",markdown.markdown(mdstr))
    #return mdstr
    nmdstr=""
    latstr=""
    flag=False
    for j in range(len(mdstr)):
        i=mdstr[j]
        if i=='$':
            if flag:
                if latstr!=""and (j<len(mdstr)-1 and mdstr[j+1]!='$'):
                    #print(blogname,[latstr],mdstr[-1])
                    nmdstr+=latex2mathml.converter.convert(latstr)
                    latstr=""
                    flag=False
            else:
                flag=True
        elif flag:
            latstr+=i
        else:
            nmdstr+=i
    return nmdstr
if __name__=="__main__":
    with open("try.html","w",encoding="utf-8")as w:
        w.write(get_html(r"D:\Blog\Blog\数学\0011 博弈论简述.md","zs"))