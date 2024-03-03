#include <iostream>
#include <stdlib.h>
#include <cstdio>
#include <winsock2.h>
#include <cstdlib>
#include<cstring>
#include<string>
#include<unistd.h>
#pragma comment(lib,"ws2_32.lib")//引用库文件
using namespace std;
char headbuf[BUFSIZ];
string source_path="resource";
SOCKET init_socket(const char* ip,unsigned short port)
{
    WSADATA wsaData;
    if(WSAStartup(MAKEWORD(2,2),&wsaData)==WSAEINVAL)
    {
        cout<<"初始化 socket 失败"<<WSAGetLastError()<<endl;
        exit(0);
    }
    SOCKET fd=socket(AF_INET,SOCK_STREAM,IPPROTO_TCP);
    if(fd==INVALID_SOCKET)
    {
        cout<<"socket 无效"<<WSAGetLastError()<<endl;
        return INVALID_SOCKET;
    }
    SOCKADDR_IN addrSrv;
    addrSrv.sin_family=AF_INET;
    addrSrv.sin_port=htons(port);
    addrSrv.sin_addr.S_un.S_addr=inet_addr(ip);
    if(bind(fd,(const struct sockaddr*)&addrSrv,sizeof(addrSrv))==SOCKET_ERROR)
    {
        cout<<"socket 错误"<<WSAGetLastError()<<endl;
        return INVALID_SOCKET;
    }
    listen(fd,5);
    return fd;
}
const char* get_file_type(string filename)
{
    int lastp=-1;
    for(int v1=filename.size()-1;v1>=0;v1--)if(filename[v1]=='.')
    {
        lastp=v1;
        break;
    }
    if(lastp==-1)return "application/octet-stream";
    string suffix=filename.substr(lastp+1,filename.size()-lastp-1);
    if(suffix=="html"||suffix=="css")return ("text/"+suffix).c_str();
    if(suffix=="png"||suffix=="jpg")return ("image/"+(suffix=="jpg"?"jpeg":suffix)).c_str();
    return "application/octet-stream";
}
void send_file(SOCKET fd,string filename)
{
    FILE* fp=fopen(filename.c_str(),"rb");
    if(!fp)
    {
        cout<<"File '"<<filename<<"'open failed."<<endl;
        return;
    }
    fseek(fp,0,SEEK_END);
    int fsize=ftell(fp);
    rewind(fp);
    char buf[BUFSIZ]={0};//send header
    sprintf(buf,"HTTP/1.1 200 OK\r\nDate:2024-3-3\r\nContent-Type:%s\r\n\
Content-Length:%d\r\n\r\n",get_file_type(filename),fsize);
    send(fd,buf,strlen(buf),0);
    while(!feof(fp))
    {
        int len=fread(buf,sizeof(char),BUFSIZ,fp);
        send(fd,buf,len,0);
    }
    fclose(fp);
}
void process_request(SOCKET fd)
{
    recv(fd,headbuf,BUFSIZ,0);
    //process the header
    string mothed,url;
    char *p=headbuf;
    while(*p!=' ')mothed+=*(p++);
    p++;
    while(*p!=' ')url+=*(p++);
    cout<<mothed<<' '<<url<<endl;
    if(mothed=="GET")
    {
        if(url=="/")url="/index.html";
        url=source_path+url;
        if(access(url.c_str(),F_OK))url=source_path+"/index.html";
        send_file(fd,url);
    }
}
void close_socket()
{
    WSACleanup();
}
int main()
{
    SOCKET serfd=init_socket("0.0.0.0",80);
    cout<<"The sever socket:"<<serfd<<endl;
    while(true)
    {
        SOCKET clifd=accept(serfd,NULL,NULL);
        process_request(clifd);
    }
    close_socket();
}