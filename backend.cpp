#include <fstream>
#include <vector>
#include <windows.h>
#include <cstring>
#define ERR_SUCCESS 0          // 成功
#define ERR_FILE_CREATE 1      // 文件创建失败
#define ERR_FILE_WRITE 2       // 文件写入失败
#define ERR_PATH_GET 3         // 获取DLL路径失败
#define ERR_UNIT_INVALID 4     // 单位不合法
#define ERR_NUM_OVERFLOW 5     // 数值溢出
#define MAX_PATH 260
int write_shuju(const char* path,long long size) {
    const long long buf_size = 1 << 20;
    bool t_n_write = false;
    std::vector<char> buf(buf_size, 0);
    std::ofstream out(path, std::ios::binary|std::ios::trunc);
    if (!out) return ERR_FILE_CREATE;
    long long pos = 0;
    for (; pos + buf_size <= size; pos += buf_size) {      
        out.write(buf.data(), buf_size);
        if (!out) {
            out.close();
			t_n_write = true;
            break;
        }
    }
    if (pos < size && !t_n_write) {
        out.write(buf.data(), size - pos);
        if (!out) {
            out.close();
			t_n_write = true;
        }
    }
    if (t_n_write) {
        DeleteFileA(path);
        return ERR_FILE_WRITE;
    }
    out.close();
    return ERR_SUCCESS;
}
extern "C" __declspec(dllexport)
bool number_size(int side, const char* shuju_type) {
    double num_size = 0.0;
    if (side <= 0) return false;
    if (strcmp(shuju_type, "B") == 0) {
        num_size = side / (1024.0 * 1024.0 * 1024.0);
    }
    else if (strcmp(shuju_type, "KB") == 0) {
        num_size = side / (1024.0 * 1024.0);
    }
    else if (strcmp(shuju_type, "MB") == 0) {
        num_size = side / 1024.0;
    }
	else if (strcmp(shuju_type, "GB") == 0) {
		num_size = side;
	}
    else return false;
	if (num_size > 1024.0) return false;
    else return true;
}
extern "C" __declspec(dllexport)
int number(int side, const char* shuju_type , const char* path) {
    long long int num = 0;
    if (strcmp(shuju_type, "B") == 0) {
        num = side;
    }
    else if (strcmp(shuju_type, "KB") == 0) {
        if (LLONG_MAX / side < 1024LL) return ERR_NUM_OVERFLOW;
        num = 1024LL * side;
    }
    else if (strcmp(shuju_type, "MB") == 0) {
        if (LLONG_MAX / side < 1024LL*1024LL) return ERR_NUM_OVERFLOW;
        num = 1024LL * 1024 * side;
    }
    else if (strcmp(shuju_type, "GB") == 0) {
        if (LLONG_MAX / side < 1024LL*1024LL*1024LL) return ERR_NUM_OVERFLOW;
        num = 1024LL * 1024 * 1024 * side;
    }
    else return ERR_UNIT_INVALID;
    
    char path_get[MAX_PATH] = { 0 };
    strcpy_s(path_get, MAX_PATH, path);
    char* last_backslash = strrchr(path_get, '\\');
    if (last_backslash == nullptr) {
        return ERR_PATH_GET; // 无路径分隔符，非法路径
    }
    size_t path_len = MAX_PATH - (last_backslash - path_get + 1);
    strcpy_s(last_backslash + 1, path_len, "0.bin");
    int yes_no = write_shuju(path_get, num);
    return yes_no;
}