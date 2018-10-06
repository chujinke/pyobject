#   Git

##一、分布式
>Git是分布式版本控制系统。CVS及SVN都是集中式的版本控制系统好处：
>>1、	每个人的电脑上都是一个完整的版本库，不需要联网。
>>2、	某一个人的电脑坏掉了不要紧，随便从其他人那里复制一个就可以了

##二、常用功能及其命令：
>1、	配置名字和Email地址：
>>git config --global user.name "Your Name"
>>git config --global user.email Your Email

>2、把目录变成Git可以管理的仓库：git init
3、	把文件添加到仓库：git add filename
4、	把文件提交到仓库：git commit –m “message”
5、	查看仓库当前的状态：git status
6、	查看具体修改了什么内容：git diff
7、	从最近到最远的提交日志：git log 简约模式加--pretty=oneline参数
8、	返回历史版本：git reset --hard commit_id
9、	查看命令历史：git reflog
10、丢弃工作区的修改：git checkout – filename
11、把暂存区的修改撤销掉：git reset HEAD &lt;file&gt;
12、从版本库中删除该文件：git rm test.txt
13、提交远程仓库：git remote add origin Yourlink
14、推送远程库：git push -u origin master  （master为当前分支）
15、克隆远程库：git clone Yourlink

##三、分支中的功能及其命令：
注：分支如果不推送到远程，对其他人就是不可见的
>1、查看分支：git branch
2、创建分支：git branch &lt;name&gt;
3、切换分支：git checkout &lt;name&gt;
4、创建+切换分支：git checkout -b &lt;name&gt;
5、合并某分支到当前分支：git merge &lt;name&gt;
6、删除分支：git branch -d &lt;name&gt;
7、查看远程库信息：git remote -v
8、推送失败，先用git pull抓取远程的新提交

##四、标签中的功能及其命令
 >1、新建一个标签：git tag &lt;tagname&gt;默认为HEAD，也可以指定一个commit id
2、指定标签信息：git tag -a &lt;tagname&gt; -m " message"
3、查看所有标签：git tag
4、推送一个本地标签:git push origin &lt;tagname&gt;
5、推送全部未推送过的本地标签:git push origin --tags
6、删除一个本地标签：git tag -d &lt;tagname&gt;
7、删除一个远程标签：git push origin :refs/tags/&lt;tagname&gt;








