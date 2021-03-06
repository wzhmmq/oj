#!/usr/bin/env python
# coding=utf-8

import shlex, subprocess, os, config, logging, shutil, lorun

class UserSubmit(object):
	"""docstring for UserSubmit"""
	solution_id = 0
	problem_id = 0
	language = ""
	user_id = ""
	program = ""
	def __init__(self, solution_id, problem_id, language, user_id, program):
		self.solution_id = solution_id
		self.problem_id = problem_id
		self.language = language
		self.user_id = user_id
		self.program = program

def low_level():
    try:
        os.setuid(int(os.popen("id -u %s" % "nobody").read()))
    except:
        pass

# dangerous code
def check_dangerous_code(solution_id, language):
    if language in ['python2', 'python3']:
        code = file('/work/%s/main.py' % solution_id).readlines()
        support_modules = [
            're',  # 正则表达式
            'sys',  # sys.stdin
            'string',  # 字符串处理
            'scanf',  # 格式化输入
            'math',  # 数学库
            'cmath',  # 复数数学库
            'decimal',  # 数学库，浮点数
            'numbers',  # 抽象基类
            'fractions',  # 有理数
            'random',  # 随机数
            'itertools',  # 迭代函数
            'functools',
            #Higher order functions and operations on callable objects
            'operator',  # 函数操作
            'readline',  # 读文件
            'json',  # 解析json
            'array',  # 数组
            'sets',  # 集合
            'queue',  # 队列
            'types',  # 判断类型
        ]
        for line in code:
            if line.find('import') >= 0:
                words = line.split()
                tag = 0
                for w in words:
                    if w in support_modules:
                        tag = 1
                        break
                if tag == 0:
                    return False
        return True
    if language in ['gcc', 'g++']:
        try:
            code = file('hone/work/%s/main.c' % solution_id).read()
        except:
            code = file('/home/cugbacm/Documents/work_dir/%s/main.cpp' % solution_id).read()
        if code.find('system') >= 0:
            return False
        return True
#  bian yi wen jian
def  compile(solution_id, language):
	low_level()#why?
	'''jiang program bian cheng ke zhi xing wen jian'''
	language = language.lower()
	dir_work = os.path.join(config.work_dir, str(solution_id))
	build_cmd = {
		"gcc":"gcc /home/cugbacm/Documents/core/main.c -o /home/cugbacm/Documents/core/main -Wall -lm -O2 -std=c99 --static -DONLINE_JUDGE",
        "g++": "g++ /home/cugbacm/Documents/work_dir/1/main.cpp -O2 -Wall -lm --static -DONLINE_JUDGE -o /home/cugbacm/Documents/work_dir/1/main",
        "java": "javac Main.java",
        "python2": 'python2 -m py_compile main.py',
        "python3": 'python3 -m py_compile main.py',
	}
	if language not in build_cmd.keys():
		return False
	p = subprocess.Popen(
		build_cmd[language],
        shell=True,
        cwd=dir_work,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
	out, err = p.communicate()# bian yi err xin xi
	err_txt_path = os.path.join(config.work_dir, str(solution_id),'err.txt')
	f = file (err_txt_path, 'w')
	f.write(err)
	f.write(out)
	f.close()
	if p.returncode == 0: #return 0, bian yi cheng gong
		return True
	#dblock.acquire()
	#update_compile_info(solution_id, err + out)
	#dblock.release()
	return False
#pang ti
def  judge(solution_id, problem_id, data_count, time_limit,
		mem_limit, program_info, result_code, language):
	low_level()
	'''ping ce bian yi lei xing yu yan'''
	max_men = 0
	max_time = 0
	if language in ['java', 'python2', 'python3']:
		time_limit = time_limit * 2
		mem_limit = mem_limit * 2
	for i in range(data_count):
		ret = judge_one_mem_time(solution_id,
			problem_id,
			i + 1,
			time_limit + 10,
			mem_limit,
			language
		)
		if ret == False:
			continue
		if ret['result'] == 5:
			program_info['result'] = result_code['Runtime Error']
			return program_info
		elif ret['result'] == 2:
			program_info['result'] = result_code['Time Limit Exceeded']
			program_info['take_time'] = time_limit + 10
			return program_info
		elif ret['result'] == 3:
			program_info['result']  = result_code['Memory Limit Exceeded']
			program_info['take_memory'] = mem_limit
			return program_info
		if max_time < ret['timeused']:
			max_time = ret['timeused']
		if max_men < ret['memoryused']:
			max_men = ret['memoryused']
		result = judge_result(problem_id, solution_id , i + 1)
		if result == False:
			continue
		if result == 'Wrong Answer' or result == 'Output Limit':
			program_info['result'] = result_code[result]
			break
		elif result == 'Presenttation Error':
			program_info['result'] = result_code[result]
		elif result == 'Accepted':
			if program_info['result'] != 'Presenttation Error':
				program_info['result'] = result_code[result]
		#else:#why!!!!!!!!!!!!!!!!
			#logging.error('judge did not get result')
	program_info['take_time'] = max_time
	program_info['take_memory'] = max_men
	return program_info


#one case....one data%s.in
def judge_one_mem_time(solution_id, problem_id, data_count, time_limit, mem_limit, language):
	low_level()
	'''ce yi zu shu zu'''
	input_path = os.path.join(config.data_dir, str(problem_id), 'data%s.in'%data_count)
	try:
		input_data = file(input_path)
	except:
		return False
	out_path = os.path.join(
		config.work_dir, str(solution_id), 'out%s.txt' % data_count)
	temp_out_data = open(out_path, 'w')
	if language == 'java':
		cmd = 'java -cp %s Main' % (os.path.join(config.work_dir, str(solution_id)))
		main_exe = shlex.split(cmd)
	elif language  == 'python2':
		cmd = 'python2 %s' (os.path.join(config.work_dir,str(solution_id), 'main.pyc'))
		main_exe = shlex.split(cmd)
	elif language == 'python3':
		cmd = 'python3 %s' % (os.path.join(config.work_dir, str(solution_id), '__pycache__/main,cpython-33.pyc'))
		main_exe = shlex.split(cmd)
	else:
		main_exe = [os.path.join(config.work_dir,str(solution_id), 'main')]
	runcfg = {
		'args': main_exe,
		'fd_in': input_data.fileno(),
		'fd_out': temp_out_data.fileno(),
		'timelimit': time_limit,#in MS
		'memorylimit': mem_limit,# in KB
	}
	#low_level()
	rst = lorun.run(runcfg)
	input_data.close()
	temp_out_data.close()
	#logging.debug(rst)
	return rst

def judge_result(problem_id, solution_id, data_count):
	low_level()
	'''dui shu chu shu ju jing xing ping ce'''
	#logging.debug('Judging result')
	currect_result = os.path.join(config.data_dir, str(problem_id), 'data%s.out' % data_count)
	user = os.path.join(config.work_dir, str(solution_id), 'out%s.txt' % data_count)
	try:
		curr = file(currect_result).read().replace('\r','')
		user_result = file(user).read().replace('\r','')
	except:
		return False

	if curr == user_result:
		return "Accepted"
	if curr.split() == user_result.split():
		return "Presenttation Error"
	if curr in user_result:
		return "Output Limit"
	return "Wrong Answer"

def run(problem_id, solution_id, language, data_count, user_id):
	low_level()
	''' acquire time and memory'''
	#dblock.acquire()
	#time_limit, mem_limit = get_problem_limit(problem_id)
	#dblock.release()
	time_limit = 10000
	mem_limit = 2175678
	program_info = {


		'solution_id': solution_id,
		'problem_id': problem_id,
		'take_time': 0,
		'take_memory': 0,
		'user_id': user_id,
		'result': 0,
	}
	result_code = {
		'In Queuing': 0,
		'Accepted': 1,
		'Time Limit Exceeded': 2,
		'Memory Limit Exceeded': 3,
		'Wrong Answer': 4,
		'Runtime Error': 5,
		'Output Limit': 6,
		'Compile Error': 7,
		'Presenttation Error': 8,
		'System Error': 11,
		'Judging': 12
	}
	if check_dangerous_code(solution_id, language) == False:
		program_info['result'] = result_code["Runtime Error"]
		return program_info
	compile_result = compile(solution_id, language)
	if compile_result is False:
		program_info['result'] = result_code['Compile Error']
		return program_info
	if data_count == 0:
		program_info['result'] = result_code['System Error'] 
		return program_info
	result = judge(
		solution_id,
		problem_id,
		data_count,
		time_limit,
		mem_limit,
		program_info,
		result_code,
		language
	)
	#logging.debug(result)
	return result

def  clean_work_dir(solution_id):
	dir_name = os.path.join(config.work_dir, str(solution_id))
	shutil.retree(dir_name)

def get_data_count(problem_id):
	full_path = os.path.join(config.data_dir, str(problem_id))
	try:
		files = os.listdir(full_path)
	except OSError as e:
		#logging.error(e)
		return 0
	count = 0
	for item in files:
		if item.endswith('.in') and item.startswith('data'):
			count += 1
	return count

def main(user_submit):

	solution_id = user_submit.solution_id
	problem_id = user_submit.problem_id
	language = user_submit.language
	user_id = user_submit.user_id
	program = user_submit.program
	data_count = get_data_count(user_submit.problem_id)
	print run(problem_id, solution_id, language, data_count, user_id)

if __name__ == '__main__':
	program = "#include<iostream>\n using namespace std; int main(){int  a, b; cin >> a >> b; cout<< a + b<<\" \"<<1111 <<endl; return 0; }"
	open('/home/cugbacm/Documents/work_dir/1/main.cpp','w').write(program)
	user_submit = UserSubmit(1, 1000, 'g++', '1004101117', program)
	main(user_submit)
