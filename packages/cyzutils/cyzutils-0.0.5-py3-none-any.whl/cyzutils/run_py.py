'''
使用 cmd 运行 python 代码，只需要提供包含命令行参数的 list，需要对每个参数指定名称

为了兼容更多的情况，本文件不要求执行的 python 文件返回结果
建议在原始文件中打印命令行参数以及文件的运行结果到日志文件中，以便得知运行的情况
'''

import subprocess

def run_py(file_path, **args):
    for key, value in args.items():
        if not isinstance(value, list):
            args[key] = [value]
    
    cmd = ['python', file_path]
    keys = list(args.keys())
    keys.reverse()
    values = [args[key] for key in keys]
    arg_list = nested_loop(**dict(zip(keys, values)))

    print('The following commands will be executed in sequence:')
    for arg in arg_list:
        arg = ' '.join(arg)
        print('python', file_path, arg)
    # if input('Do you want to continue? (y/n)') != 'y':
    #     return

    for arg in arg_list:
        p = subprocess.Popen(cmd + arg)
        p.wait()



def nested_loop(**args):
    if len(args) == 0:
        return [[]]
    key, values = args.popitem()
    res = []
    for value in values:
        for sub_args in nested_loop(**args):
            res.append([f'--{key}', str(value)] + sub_args)
    return res

def main():
    file_path = 'test/test.py'
    test1 = [1, 2]
    test2 = [3, 4]
    test3 = 5
    run_py(file_path, arg1=test1, arg2=test2, arg3=test3)

if __name__ == '__main__':
    main()