import os
import concurrent.futures

def check_and_fix_off_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    if lines[0].startswith('OFF') and not lines[0].startswith('OFF\n'):
        print(f"修复错误的 OFF 文件: {file_path}")
        fixed_lines = ['OFF\n']
        remaining_content = lines[0][3:].strip()
        fixed_lines.append(remaining_content + '\n')
        fixed_lines.extend(lines[1:])

        with open(file_path, 'w') as file:
            file.writelines(fixed_lines)
    else:
        print(f"文件没有问题: {file_path}")

def check_and_fix_directory(directory, executor):
    for root, dirs, files in os.walk(directory):
        off_files = [os.path.join(root, file) for file in files if file.endswith('.off')]

        # 使用线程池处理每个文件
        futures = [executor.submit(check_and_fix_off_file, file_path) for file_path in off_files]
        concurrent.futures.wait(futures)

if __name__ == '__main__':
    root_directory = './datasets/ModelNet40_200'  # 请修改为你的 OFF 文件所在的目录

    # 设定线程池大小，建议使用与你的 CPU 核心数相同的大小
    num_threads = os.cpu_count()

    # 使用 ThreadPoolExecutor 进行多线程处理
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        check_and_fix_directory(root_directory, executor)
