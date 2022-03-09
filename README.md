# I Need Gpu
ING 是一个自动选取GPU并提交任务的脚本
* 自动查询可使用的GPU，每两秒轮询一次
* 根据设置的规则选取GPU，支持模糊匹配，比如指定 a100，就能匹配所有a100，包括40G和80G
* 对满足要求的GPU，选取剩余量最多的GPU，以增大抢到GPU的概率
* 获取到GPU之后，自动修改提交任务的脚本，设置为指定的GPU
* 自动提交任务

# USAGE
1. 在项目目录，新建一个文件 ING.py，把仓库的ING.py复制粘贴进去
2. 根据需求改掉文件的 Needed_GPU 列表，指定满足条件的GPU
运行以下命令，搞定
```
python ING.py your_script_dir
```
![image](https://user-images.githubusercontent.com/101267529/157468650-5c4d0e1c-0bb6-4552-9c7f-8d6f39622a15.png)
