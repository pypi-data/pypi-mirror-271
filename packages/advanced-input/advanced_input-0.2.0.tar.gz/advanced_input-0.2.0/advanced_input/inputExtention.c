#include <stdio.h>

#ifdef LINUX

#include <termios.h>
#include <sys/ioctl.h>
#include <sys/select.h>
#include <unistd.h>

static struct termios oldt, newt;
void stop();
void resume() {
    tcsetattr( STDIN_FILENO, TCSANOW, &newt);
}

int kbhit() {
    resume();
    int bytesWaiting;
    ioctl(STDIN_FILENO, FIONREAD, &bytesWaiting);
    stop();
    return bytesWaiting > 0;
}

int getch() {
    resume();
    int bytesWaiting;
    ioctl(STDIN_FILENO, FIONREAD, &bytesWaiting);
    if (bytesWaiting > 4) {
        bytesWaiting = 4;
    }
    int ch = 0;
    read(STDIN_FILENO, &ch, bytesWaiting);
    stop();
    return ch;
}

#endif

void init() {
    #ifdef LINUX
    tcgetattr( STDIN_FILENO, &oldt);
    newt = oldt;
    newt.c_lflag &= ~(ICANON | ECHO);
    tcsetattr( STDIN_FILENO, TCSANOW, &newt);
    #endif
    fflush(stdin);
    return;
}

int isInputReady() {
    return kbhit();
}

int getCharacter() {
    int ch = getch();
    #ifndef LINUX
    if ((char) ch == '\r') {
        ch = (int) '\n';
    }
    printf("%c", (char) ch);
    #endif
    return ch;
}

void stop() {
    #ifdef LINUX
    tcsetattr( STDIN_FILENO, TCSANOW, &oldt);
    #endif
    return;
}
