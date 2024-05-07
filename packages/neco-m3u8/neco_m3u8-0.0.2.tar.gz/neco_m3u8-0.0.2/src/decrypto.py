from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
from base64 import b64decode
import os


def decrypt_ts_segment(encrypted_ts_data, key: str, iv: str = None):
    def add_16(par):  # 补位到16倍数位
        while len(par) % 16 != 0:
            par += b'\x00'
        return par

    # 确保key和iv是字节串
    key = key.encode('utf-8')
    if isinstance(iv, str):
        iv = add_16(iv.encode('utf-8'))

    # 创建一个cipher对象
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # 解密数据（注意：pycryptodome默认不进行填充，因此我们需要手动处理）
    decrypted_data = cipher.decrypt(encrypted_ts_data)

    # 如果数据是PKCS7填充的，则去除填充
    try:
        unpadded_data = unpad(decrypted_data, AES.block_size)
    except ValueError:
        # 如果解密失败（例如，数据没有正确填充），则返回原始解密数据
        unpadded_data = decrypted_data

    return unpadded_data


if __name__ == '__main__':
    # a = '0x00000000000000000000000000000000'
    # print(int(a))
    a = r'D:\pythoncode\代码\Ne_m3u8\新建文件夹\1\2.ts'
    c = a.replace(os.path.basename(a), f'$${os.path.basename(a)}')
    os.rename(a, c)
    # with open(, 'wb+') as ff:
    #     ff.write(b'11111')
