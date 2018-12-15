"""
自动加载当前包目录下的子模块
搜索当前包下所有*.py文件。加载模块
"""
__all__=[]
import os
# import pdb
# pdb.set_trace()
#发现自模块
PATH_SEP = os.path.sep
sub_modules = []
current_module_dir = os.getcwd() + PATH_SEP + __name__.replace(".", PATH_SEP)
#print("currentModuleDir:"+current_module_dir)

sub_dirs = os.listdir(current_module_dir)
#print( "sub_dirs length %d" % len(sub_dirs))

for sub_dir in sub_dirs:
    #print(type(sub_dir))
    #print(sub_dir)
    if sub_dir.find(".") == -1:
        continue
    if sub_dir == "__init__.py":
        continue

    full_path = current_module_dir + PATH_SEP + sub_dir
    #print(full_path)
    if not os.path.isfile(full_path):
        continue

    ext_name = sub_dir.split('.')[1]
    if ext_name == 'py':
        modulename = sub_dir.split('.')[0].strip()
        #print(modulename)
        if modulename:
            sub_modules.append(modulename)

#print(len(sub_modules))

#自动加载子模块
for sub_module in sub_modules:
    full_module_name = __name__ + "." + sub_module
    #print(full_module_name)
    __import__(full_module_name)
    #print("import module:"+full_module_name);


