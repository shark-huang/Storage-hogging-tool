#include <fstream>
#include <vector>
#include <windows.h>
#include<chrono>
#include<cmath>
#define ERR_SUCCESS 0          // 成功
#define ERR_FILE_CREATE 1      // 文件创建失败
#define ERR_FILE_WRITE 2       // 文件写入失败
#define ERR_PATH_GET 3         // 获取DLL路径失败
#define ERR_UNIT_INVALID 4     // 单位不合法
#define ERR_NUM_OVERFLOW 5     // 数值溢出
#define MAX_PATH 260 
struct return_data
{
    int result;
    double speed;
};
struct return_number
{
    bool result;
    long long size;
    char type;
};
void side_1024_num(long long size, const char type, struct return_number* out)
{
    int n = 0;
    char type_choess[4] = {'B', 'K','M', 'G'};
	int len = sizeof(type_choess) / sizeof(type_choess[0]);
    if (size % 1024 == 0) {
        while (size>=1024 && n<4)
        {
	        size /= 1024;
	        n++;
        }
        out->size = size;
        for(int i=0;i<len;i++)
        {
            if(type_choess[i] == type)
            {
                out->type = type_choess[i+n];
                break;
            }
        }
        return;
    }
    else {
        out->size = size;
        out->type = type;
        return;
    }
}
extern "C" __declspec(dllexport)
void number_size(long long side, const char* shuju_type, struct return_number* out_number) {
    double num_size = 0.0;
    if (side <= 0) {
        out_number->result = false;
        return;
    }
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
        num_size = (double)side;
    }
    else {
		out_number->result = false;
        return;
    }
    if (num_size >= 1024.0) {
        out_number->result = false;
        return;
    }
    else {
        side_1024_num(side, *shuju_type, out_number);
        out_number->result = true;
        return;
    }
}
void write_shuju(const char* path, long long size, return_data* out_data) {
    const long long buf_size = 1 << 20;
    bool t_n_write = false;
    std::vector<char> buf(buf_size, 0);
    std::ofstream out(path, std::ios::binary | std::ios::trunc);
    auto time_start = std::chrono::high_resolution_clock::now();
    if (!out) {
        out_data->result = ERR_FILE_CREATE;
        return;
    }
    long long pos = 0;
    for (; pos + buf_size <= size; pos += buf_size) {
        out.write(buf.data(), buf_size);
        if (!out.good()) {
            out.close();
            t_n_write = true;
            break;
        }
    }
    if (pos < size && !t_n_write) {
        out.write(buf.data(), size - pos);
        if (!out.good()) {
            out.close();
            t_n_write = true;
        }
    }
    if (!t_n_write)
    {
        out.flush();
        if (out.is_open())
        {
            out.close();
        }
    }
    auto time_end = std::chrono::high_resolution_clock::now();
    if (t_n_write) {
        out.close();
        DeleteFileA(path);
        out_data->result = ERR_FILE_CREATE;
        return;
    }
    auto cost = std::chrono::duration_cast<std::chrono::duration<double>>(time_end - time_start).count();
    double size_mb = (double)size / 1024.00 / 1024.00;
    double speed_write = size_mb / cost;
    speed_write = round(speed_write * 100.0) / 100.0;
    out_data->result = ERR_SUCCESS;
    out_data->speed = speed_write;
    return;
}
extern "C" __declspec(dllexport)
void number(long long int side, const char* shuju_type, const char* path,struct return_data* out_data) {
    out_data->result = 25;
    out_data->speed = 0;
    long long int num = 0;
    if (strcmp(shuju_type, "B") == 0) {
        num = side;
    }
    else if (strcmp(shuju_type, "KB") == 0) {
        if (LLONG_MAX / side < 1024LL) {
            out_data->result = ERR_NUM_OVERFLOW;
            return;
        }
        num = 1024LL * side;
    }
    else if (strcmp(shuju_type, "MB") == 0) {
        if (LLONG_MAX / side < 1024LL * 1024LL) {
            out_data->result = ERR_NUM_OVERFLOW;
            return;
        }
        num = 1024LL * 1024 * side;
    }
    else if (strcmp(shuju_type, "GB") == 0) {
        if (LLONG_MAX / side < 1024LL * 1024LL * 1024LL) {
            out_data->result = ERR_NUM_OVERFLOW;
            return;
        }
        num = 1024LL * 1024 * 1024 * side;
    }
    else {
        out_data->result = ERR_UNIT_INVALID;
        return;
    }

    char path_get[MAX_PATH] = { 0 };
    strcpy_s(path_get, MAX_PATH, path);
    char* last_backslash = strrchr(path_get, '\\');
    if (last_backslash == nullptr) {
        out_data->result = ERR_PATH_GET;
        return;
    }
    size_t path_len = MAX_PATH - (last_backslash - path_get + 1);
    strcpy_s(last_backslash + 1, path_len, "0.bin");
    write_shuju(path_get, num, out_data);
    return;
}