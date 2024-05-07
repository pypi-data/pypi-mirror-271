import shutil
import subprocess
import os
import random
import glob


def merge_ts_files(input_folder, output_file):
    list_txt_name = f'list{random.randint(1, 999999999999999999999999999)}.txt'
    list_text_path = os.path.join(os.getcwd(), list_txt_name)
    # 使用glob模块获取所有.ts文件
    ts_files = glob.glob(os.path.join(input_folder, '*.ts'))
    ts_files = sorted(ts_files, key=lambda path: int(os.path.splitext(os.path.basename(path))[0]))

    # 使用subprocess调用ffmpeg进行合并
    # 注意：这里我们假设ffmpeg已经被添加到系统的PATH中，或者你需要提供ffmpeg的完整路径
    command = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', list_text_path, '-c', 'copy', output_file]

    # 创建一个名为'list.txt'的文件，其中包含所有要合并的.ts文件的列表
    with open(list_text_path, 'w') as f:
        for ts_file in ts_files:
            f.write("file '{}'\n".format(ts_file))

        # 调用ffmpeg命令
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # 清理创建的'list.txt'文件（可选）
    os.remove(list_txt_name)

    print(f"{output_file}合并完成!")
    del_dir(input_folder, mode=2)


def del_dir(dir_name: str, mode=1):
    """
    :param dir_name: 文件夹名字
    :param mode: 1为删除文件夹里面内容 2为连着文件夹一起删除
    :return:
    """
    if mode == 1:
        for file in os.listdir(dir_name):
            file_path = os.path.join(dir_name, file)
            os.remove(file_path)
    elif mode == 2:
        shutil.rmtree(dir_name)


if __name__ == '__main__':
    save_dir = 'E:/番\精灵宝可梦超世代'
    file_name = '第01集'
    ts_file_dir = os.path.join(save_dir, file_name)
    merge_ts_files(ts_file_dir, os.path.join(save_dir, f'{file_name}.mp4'))
