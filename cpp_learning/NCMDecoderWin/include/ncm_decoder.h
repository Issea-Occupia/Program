#pragma once
#include <string>
#include <vector>
#include <cstdint>

// 一个简单的 Meta 信息结构体
struct NcmMeta {
    std::string musicName;
    std::string format;
    // 你可以自己增加 artist / album 等字段
};

struct NcmDecodeResult {
    NcmMeta meta;
    std::vector<std::uint8_t> audioData;
};

// 解析并解密 .ncm 文件，失败抛出 std::runtime_error
NcmDecodeResult ParseNcmFile(const std::string& path);

// 解密并写入输出目录，返回输出路径
std::string DecryptNcmToFile(const std::string& inPath, const std::string& outDir);
