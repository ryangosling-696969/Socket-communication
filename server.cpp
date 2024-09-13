#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <string.h>
#include <iostream>
#include <thread>
#include <sstream>
#include <fstream>
#include <curl/curl.h>

#define PORT 8080

bool login = false;
bool htmlLink = false;
char buffer[1024]={0};
char const *msg = "Enter password1024";
char const *auth = "1024";
char const *option1 = "1. Html";
char const *option2 = "2. Sherlock";

std::size_t callback(
    const char* in,
    std::size_t size,
    std::size_t num,
    std::string* out){
    const std::size_t totalBytes(size * num);
    out->append(in, totalBytes);
    return totalBytes;
}

void downloadPage(std::string url){
    CURL* curl = curl_easy_init();
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    std::string response;
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);
    curl_easy_perform(curl);
    curl_easy_cleanup(curl);
    std::ofstream outFile("downloaded_page.html");
    outFile << response;
    outFile.close();
}

void processRequest(int newSocket){
    send(newSocket, msg, strlen(msg), 0);
    while(1){
        memset(buffer, 0, sizeof(buffer));
        int valread = read(newSocket, buffer, 1024);
        if(valread == 0){
            break;
        }
        if(login || strcmp(buffer, "erebos") == 0){
            login = true;
            send(newSocket, auth, strlen(auth), 0);
            std::this_thread::sleep_for(std::chrono::milliseconds(500));
            send(newSocket, option1, strlen(option1), 0);
            std::this_thread::sleep_for(std::chrono::milliseconds(500));
            send(newSocket, option2, strlen(option2), 0);
        }
        if(strcmp(buffer, "1") == 0 || strcmp(buffer, "sherlock") == 0){
            std::string url = "Enter webpage1024";
            send(newSocket, url.c_str(), url.size(), 0);
            htmlLink=true;
        }
        if(htmlLink){
            std::string page = std::string(buffer);
            downloadPage(page);
            break;
        }
        close(newSocket);
    }
}

int main(int argc, char const *argv[]){
    int server_fd;
    struct sockaddr_in address;

    if((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0){
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    if(bind(server_fd, (struct sockaddr *)&address, sizeof(address))<0){
        perror("bind failed");
        exit(EXIT_FAILURE);
    }
    if(listen(server_fd, 3) < 0){
        perror("listen");
        exit(EXIT_FAILURE);
    }
    int addrlen = sizeof(address);

    while(1){
        printf("\nWaiting for connection\n");
        int newSocket;
        if((newSocket = accept(server_fd, (struct sockaddr *)&address, 
            (socklen_t*)&addrlen))<0){
            perror("accept");
            exit(EXIT_FAILURE);
        }
        printf("Connected by %s:%d\n", inet_ntoa(address.sin_addr), ntohs(address.sin_port));
        std::thread t1(processRequest, newSocket);
        t1.detach();
    }
    close(server_fd);
    return 0;
}