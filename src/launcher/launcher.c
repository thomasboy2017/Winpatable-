#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

int main(int argc, char **argv) {
    // Prepare environment for the Python application
    // Ensure PYTHONPATH includes /app/lib so the bundled modules are found
    setenv("PYTHONPATH", "/app/lib", 1);

    // Ensure PATH contains /app/bin so helpers can be found
    const char *oldpath = getenv("PATH");
    char newpath[4096];
    if (oldpath) {
        snprintf(newpath, sizeof(newpath), "/app/bin:%s", oldpath);
    } else {
        snprintf(newpath, sizeof(newpath), "/app/bin");
    }
    setenv("PATH", newpath, 1);

    // Build argv for exec: python3 /app/lib/winpatable.py <args...>
    int newargc = argc + 2;
    char **newargv = (char**)calloc(newargc + 1, sizeof(char*));
    if (!newargv) {
        fprintf(stderr, "Out of memory\n");
        return 1;
    }

    newargv[0] = "python3";
    newargv[1] = "/app/lib/winpatable.py";
    for (int i = 1; i < argc; ++i) {
        newargv[i+1] = argv[i];
    }
    newargv[newargc] = NULL;

    // Execute Python
    execvp("/usr/bin/python3", newargv);

    // If execvp returns, it's an error
    perror("execvp");
    return 1;
}
