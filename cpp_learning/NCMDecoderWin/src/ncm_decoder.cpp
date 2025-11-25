#include "../include/ncm_decoder.h"

#include <fstream>
#include <stdexcept>
#include <vector>
#include <cstring>
#include <filesystem>

#include <openssl/evp.h>
#include <openssl/aes.h>
#include <openssl/bio.h>
#include <openssl/buffer.h>

#include <nlohmann/json.hpp>

using json = nlohmann::json;
namespace fs = std::filesystem;

// CORE_KEY / META_KEY
static const unsigned char CORE_KEY[] =
    {0x68,0x7A,0x48,0x52,0x41,0x6D,0x73,0x6F,0x35,0x6B,0x49,0x6E,0x62,0x61,0x78,0x57};
static const unsigned char META_KEY[] =
    {0x23,0x31,0x34,0x6C,0x6A,0x6B,0x5F,0x21,0x5C,0x5D,0x26,0x30,0x55,0x3C,0x27,0x28};

// PKCS7 去填充
static std::vector<std::uint8_t> Pkcs7Unpad(const std::vector<std::uint8_t>& in)
{
    if (in.empty()) return in;
    auto pad_len = in.back();
    if (pad_len < 1 || pad_len > 16 || pad_len > in.size()) {
        return in; // 容错
    }
    return std::vector<std::uint8_t>(in.begin(), in.end() - pad_len);
}

// AES-ECB 解密
static std::vector<std::uint8_t> AesEcbDecrypt(
    const std::vector<std::uint8_t>& data,
    const unsigned char* key, size_t key_len)
{
    EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();
    if (!ctx) throw std::runtime_error("EVP_CIPHER_CTX_new failed");

    const EVP_CIPHER* cipher = nullptr;
    if (key_len == 16) cipher = EVP_aes_128_ecb();
    else if (key_len == 24) cipher = EVP_aes_192_ecb();
    else if (key_len == 32) cipher = EVP_aes_256_ecb();
    else {
        EVP_CIPHER_CTX_free(ctx);
        throw std::runtime_error("Unsupported AES key length");
    }

    EVP_DecryptInit_ex(ctx, cipher, nullptr, key, nullptr);
    EVP_CIPHER_CTX_set_padding(ctx, 0); // 我们自己做 PKCS7

    std::vector<std::uint8_t> out(data.size() + AES_BLOCK_SIZE);
    int out_len1 = 0;
    int out_len2 = 0;

    if (!EVP_DecryptUpdate(ctx, out.data(), &out_len1, data.data(), (int)data.size())) {
        EVP_CIPHER_CTX_free(ctx);
        throw std::runtime_error("EVP_DecryptUpdate failed");
    }

    if (!EVP_DecryptFinal_ex(ctx, out.data() + out_len1, &out_len2)) {
        EVP_CIPHER_CTX_free(ctx);
        throw std::runtime_error("EVP_DecryptFinal_ex failed");
    }

    EVP_CIPHER_CTX_free(ctx);
    out.resize(out_len1 + out_len2);
    return out;
}

// Base64 解码（用 OpenSSL BIO）
static std::vector<std::uint8_t> Base64Decode(const std::vector<std::uint8_t>& in)
{
    BIO* b64 = BIO_new(BIO_f_base64());
    BIO* bio = BIO_new_mem_buf(in.data(), (int)in.size());
    bio = BIO_push(b64, bio);
    BIO_set_flags(bio, BIO_FLAGS_BASE64_NO_NL);

    std::vector<std::uint8_t> out(in.size());
    int len = BIO_read(bio, out.data(), (int)out.size());
    if (len < 0) {
        BIO_free_all(bio);
        throw std::runtime_error("Base64 decode failed");
    }
    out.resize(len);
    BIO_free_all(bio);
    return out;
}

// 直接抄 Python 结构：ParseNcmFile
NcmDecodeResult ParseNcmFile(const std::string& path)
{
    std::ifstream f(path, std::ios::binary);
    if (!f) {
        throw std::runtime_error("Cannot open file: " + path);
    }

    auto read_bytes = [&](size_t n) {
        std::vector<std::uint8_t> buf(n);
        f.read(reinterpret_cast<char*>(buf.data()), (std::streamsize)n);
        if ((size_t)f.gcount() != n) {
            throw std::runtime_error("Unexpected EOF");
        }
        return buf;
    };

    // 1. header
    auto header = read_bytes(8);
    static const unsigned char MAGIC[] =
        {0x43,0x54,0x45,0x4E,0x46,0x44,0x41,0x4D}; // "CTENFDAM"

    if (!std::equal(header.begin(), header.end(), MAGIC)) {
        throw std::runtime_error("Invalid ncm header");
    }

    // 2. skip 2 bytes
    f.seekg(2, std::ios::cur);

    // 3. key length + key data
    auto key_len_bytes = read_bytes(4);
    uint32_t key_len = *(uint32_t*)key_len_bytes.data(); // 小端
    auto key_data = read_bytes(key_len);
    for (auto& b : key_data) {
        b ^= 0x64;
    }

    auto decrypted_key = AesEcbDecrypt(key_data, CORE_KEY, sizeof(CORE_KEY));
    decrypted_key = Pkcs7Unpad(decrypted_key);

    if (decrypted_key.size() <= 17) {
        throw std::runtime_error("Decrypted key too short");
    }
    std::vector<std::uint8_t> real_key(
        decrypted_key.begin() + 17,
        decrypted_key.end()
    );

    // 4. 构造 key_box
    std::vector<std::uint8_t> key_box(256);
    for (int i = 0; i < 256; ++i) key_box[i] = (std::uint8_t)i;

    int last_byte = 0;
    int key_index = 0;
    int key_len_real = (int)real_key.size();
    if (key_len_real == 0) {
        throw std::runtime_error("real_key length = 0");
    }

    for (int i = 0; i < 256; ++i) {
        int swap = key_box[i];
        last_byte = (swap + last_byte + real_key[key_index]) & 0xFF;
        key_index++;
        if (key_index >= key_len_real) key_index = 0;
        std::swap(key_box[i], key_box[last_byte]);
    }

    // 5. meta length + meta data
    auto meta_len_bytes = read_bytes(4);
    uint32_t meta_len = *(uint32_t*)meta_len_bytes.data();

    NcmMeta meta_out;
    if (meta_len > 0) {
        auto meta_raw = read_bytes(meta_len);
        for (auto& b : meta_raw) {
            b ^= 0x63;
        }
        // 前22字节标识，后面是 base64
        if (meta_raw.size() <= 22) {
            throw std::runtime_error("meta_raw too short");
        }
        std::vector<std::uint8_t> meta_b64_part(
            meta_raw.begin() + 22,
            meta_raw.end()
        );

        auto meta_decoded = Base64Decode(meta_b64_part);
        auto meta_plain = AesEcbDecrypt(meta_decoded, META_KEY, sizeof(META_KEY));
        meta_plain = Pkcs7Unpad(meta_plain);

        std::string text(meta_plain.begin(), meta_plain.end());
        auto colon_pos = text.find(':');
        std::string json_str;
        if (colon_pos != std::string::npos) {
            json_str = text.substr(colon_pos + 1);
        } else {
            json_str = text;
        }

        json meta_obj = json::parse(json_str);

        json real_meta = meta_obj;
        if (meta_obj.contains("mainMusic")) {
            real_meta = meta_obj["mainMusic"];
        }

        meta_out.musicName = real_meta.value("musicName", "");
        meta_out.format    = real_meta.value("format", "mp3");
    }

    // 6. 跳过 crc32 / 5 bytes 保留 / 封面
    auto crc32 = read_bytes(4);
    (void)crc32;
    f.seekg(5, std::ios::cur);

    auto img_size_bytes = read_bytes(4);
    uint32_t img_size = *(uint32_t*)img_size_bytes.data();
    if (img_size > 0) {
        f.seekg(img_size, std::ios::cur);
    }

    // 7. 解音频区
    std::vector<std::uint8_t> audio_data;
    const size_t chunkSize = 0x8000;
    while (true) {
        std::vector<std::uint8_t> chunk(chunkSize);
        f.read(reinterpret_cast<char*>(chunk.data()), (std::streamsize)chunkSize);
        std::streamsize got = f.gcount();
        if (got <= 0) break;
        chunk.resize((size_t)got);

        int chunk_len = (int)chunk.size();
        for (int i = 1; i <= chunk_len; ++i) {
            int j = i & 0xFF;
            int idx = (key_box[j] + key_box[(key_box[j] + j) & 0xFF]) & 0xFF;
            chunk[i - 1] ^= key_box[idx];
        }

        audio_data.insert(audio_data.end(), chunk.begin(), chunk.end());
    }

    NcmDecodeResult result;
    result.meta = meta_out;
    result.audioData = std::move(audio_data);
    return result;
}

// 清理文件名中的非法字符
static std::string CleanFileName(const std::string& name)
{
    std::string s = name;
    const std::string bad = "\\/:*?\"<>|";
    for (char& c : s) {
        if (bad.find(c) != std::string::npos) {
            c = '_';
        }
    }
    if (s.empty()) return "untitled";
    return s;
}

std::string DecryptNcmToFile(const std::string& inPath, const std::string& outDir)
{
    auto res = ParseNcmFile(inPath);

    std::string baseName = res.meta.musicName;
    if (baseName.empty()) {
        baseName = fs::path(inPath).stem().string();
    }
    std::string ext = res.meta.format.empty() ? "mp3" : res.meta.format;

    std::string safe = CleanFileName(baseName);
    std::string outFileName = safe + "." + ext;
    fs::path outPath = fs::path(outDir) / outFileName;

    // 冲突处理
    int counter = 1;
    while (fs::exists(outPath)) {
        outFileName = safe + "_" + std::to_string(counter) + "." + ext;
        outPath = fs::path(outDir) / outFileName;
        ++counter;
    }

    std::ofstream out(outPath, std::ios::binary);
    if (!out) {
        throw std::runtime_error("Cannot open output: " + outPath.string());
    }
    out.write(reinterpret_cast<const char*>(res.audioData.data()),
              (std::streamsize)res.audioData.size());

    return outPath.string();
}
