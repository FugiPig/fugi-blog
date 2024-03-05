import os.path as op
import os
ERROR_ST=[]
SON_BLOG_HTML="""
<li>
    <div class="blog-button">
        <h2 class="in-button">0000</h2>
        <a class="in-button">图论</a>
        <br>
        <h3 class="in-button">博客目录</h3>
    </div>
</li>"""
with open("template.html","r",encoding="utf-8") as r:
    PAGE_HTML=r.read()
print(PAGE_HTML)
class Blog():
    def __init__(self,path,fa_dict):
        self.number=0
    def __lt__(self,blogb):
        return self.number>blogb.number
    def get_html(self):
        return "ZSWB"
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
        self.fa_a=fa_a+'<a class="in-button" herf="%s">%s</a>'%(self.get_url(),'-'+self.name)
        self.son_node=[]
        self.son_blog=[]
        self.add_son_node()
        self.html_str="<p>ZSBW</p>"
        #print(self.number,self.name,self.path,self.son_node,self.fa_a)
    def get_url(self):
        return self.root_url+'/'+self.htmlname
    def add_son_node(self):
        for i in os.listdir(self.path):
            son_path=op.join(self.path,i)
            if op.isfile(son_path):
                continue
            self.son_node.append(Node(son_path,op.basename(son_path),self.fa_dict,self.root_url,self.fa_a))
    def build_html(self,html_path):
        top_index=""
        for i in self.son_node:
            top_index+='<li class="top-button"><a herf="%s">%s</a></li>'%(i.get_url(),i.name)
            i.build_html(html_path)
            self.son_blog+=i.son_blog
        if(top_index==""):
            top_index='<h2 class="title-h">No child node.</h2>'
        #print(self.name,top_index)
        for i in os.listdir(self.path):
            son_path=str(op.join(self.path,i))
            if op.isfile(son_path)and son_path.split('.')[-1]=='md':
                self.son_blog.append(Blog(son_path,self.fa_dict))
        self.son_blog.sort()
        son_blog=""
        for i in self.son_blog:
            son_blog+=i.get_html()
        if son_blog=="":
            son_blog='<h2 class="title-h">No child blog.</h2>'
        self.html_str=PAGE_HTML%(top_index,son_blog)
        self.write_html(html_path)
    def write_html(self,path):
        filename=op.join(path,self.htmlname)
        with open(filename,"w",encoding="utf-8")as w:
            print("Writing to:",filename)
            w.write(self.html_str)
class Tree():
    def __init__(self,root_url='',root_path='.'):
        self.root_url=root_url
        self.root_path=op.abspath(root_path)
        self.node_dict={}
        self.root_node=Node(self.root_path,op.basename(self.root_path),self.node_dict,root_url,"")
        self.html_path=op.abspath(root_url)
        if not op.exists(self.html_path):
            os.mkdir(self.html_path)
        self.root_node.build_html(self.html_path)
if __name__=="__main__":
    tr=Tree(root_url="html",root_path="Blog")
    if ERROR_ST==[]:
        print("Init sucessfully.")
        #TODO: build html
    else:
        print("Here are the errors:")
        for i in ERROR_ST:
            print(i)