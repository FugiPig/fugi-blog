import os.path as op
import os
import blog
ERROR_ST=[]
SON_BLOG_HTML="""
<li>
    <div class="blog-button">
        <h3 class="in-button">%d</h2>
        <h2 style="display:inline;">%s</h2>
        <h4 class="in-button"><a href="%s">%s</a></h3>
    </div>
</li>"""
INDEX_HTML='<a style="display: inline;" href="%s">%s</a>'
TOP_HTML='<li class="top-button"><a href="%s">%s</a></li>'
BLOG_CNT=0
with open("template.html","r",encoding="utf-8") as r:
    PAGE_HTML=r.read()
class Blog():
    def __init__(self,filename,fa_dict,first_fa):
        global BLOG_CNT
        if not op.exists(filename):
            ERROR_ST.append("Blog File not Exists:%s"%filename)
            return
        BLOG_CNT+=1
        self.webnum=BLOG_CNT
        self.htmlname="blog-"+str(self.webnum)+".html"
        self.filename=op.basename(filename)
        self.localnum=0
        flag=False
        index=-1
        for i in self.filename:
            if (flag and (i<'0'or i>'9'))or (not flag and i=='-'):
                break
            flag=True
            index+=1
        if(index>-1):
            self.localnum=int(self.filename[:index+1])
        self.blogname=self.filename[index+1:]
        #print(self.filename,index,self.localnum,self.blogname)
        self.html_str=blog.get_html(filename,self.blogname)
        self.falist=[first_fa]
    def write_html(self,path):
        filename=op.join(path,self.htmlname)
        with open(filename,"w",encoding="utf-8")as w:
            print("Writing to:",filename)
            w.write(self.html_str)
    def __lt__(self,blogb):
        return self.localnum>blogb.localnum
    def get_html(self,root_url):
        if root_url[-1]!='/':
            root_url+='/'
        fa_html=""
        for i in self.falist:
            if(fa_html==""):
                fa_html+=i.fa_a
            else:
                fa_html+="("+i.fa_a+")"
            fa_html+="<br>"
        return SON_BLOG_HTML%(self.localnum,fa_html,root_url+self.htmlname,self.blogname)
class Node():
    def __init__(self,path,name,fa_dict,root_url,fa_a):
        self.name=str(name)
        self.path=op.abspath(path)
        self.root_url=root_url
        if self.name in fa_dict:
            ERROR_ST.append("There are same dir name: %s"%self.name)
        fa_dict[self.name]=self
        self.fa_dict=fa_dict
        self.number=len(fa_dict)
        self.htmlname="node-"+str(self.number)+".html"
        self.fa_a=fa_a+INDEX_HTML%(root_url+'/'+self.htmlname,'-'+self.name)
        self.son_node=[]
        self.son_blog=[]
        self.add_son_node()
        self.html_str="<p>ZSBW</p>"
        #print(self.number,self.name,self.path,self.son_node,self.fa_a)
    def add_son_node(self):
        for i in os.listdir(self.path):
            son_path=op.join(self.path,i)
            if op.isfile(son_path):
                continue
            self.son_node.append(Node(son_path,op.basename(son_path),self.fa_dict,self.root_url,self.fa_a))
    def build_html(self,html_path):
        top_index=""
        for i in self.son_node:
            top_index+=TOP_HTML%(self.root_url+'/'+i.htmlname,i.name)
            i.build_html(html_path)
            self.son_blog+=i.son_blog
        if(top_index==""):
            top_index='<h2 class="title-h">No child node.</h2>'
        #print(self.name,top_index)
        for i in os.listdir(self.path):
            son_path=str(op.join(self.path,i))
            if op.isfile(son_path)and son_path.split('.')[-1]=='md':
                self.son_blog.append(Blog(son_path,self.fa_dict,self))
        self.son_blog.sort()
        son_blog=""
        for i in self.son_blog:
            i.write_html(html_path)
            son_blog+=i.get_html(self.root_url)
        if son_blog=="":
            son_blog='<h2 class="title-h">No child blog.</h2>'
        self.html_str=PAGE_HTML%(top_index,self.fa_a,son_blog)
        self.write_html(html_path)
    def write_html(self,path):
        filename=op.join(path,self.htmlname)
        with open(filename,"w",encoding="utf-8")as w:
            print("Writing to:",filename)
            w.write(self.html_str)
class Tree():
    def __init__(self,root_url='',html_path="html",root_path='.'):
        self.root_url=root_url
        self.root_path=op.abspath(root_path)
        self.node_dict={}
        self.root_node=Node(self.root_path,op.basename(self.root_path),self.node_dict,root_url+'/'+html_path,"")
        self.html_path=op.abspath(html_path)
        if not op.exists(self.html_path):
            os.mkdir(self.html_path)
        self.root_node.build_html(self.html_path)
if __name__=="__main__":
    tr=Tree(root_url="/fugi-blog",root_path="Blog")
    if ERROR_ST==[]:
        print("Init sucessfully.")
        #TODO: build html
    else:
        print("Here are the errors:")
        for i in ERROR_ST:
            print(i)