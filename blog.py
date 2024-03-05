#from latex2mathml import convert_tex_to_mml
import markdown
with open("template-blog.html","r",encoding="utf-8") as r:
    PAGE_HTML=r.read()
def get_html(filename,blogname):
    mdstr=""
    with open(filename,"r",encoding="utf-8")as r:
        mdstr=r.read()
    #print(markdown.markdown(mdstr))
    return PAGE_HTML%(blogname,"%s",markdown.markdown(mdstr))
if __name__=="__main__":
    with open("try.html","w",encoding="utf-8")as w:
        w.write(get_html(r"D:\Blog\Blog\数学\0011 博弈论简述.md"))