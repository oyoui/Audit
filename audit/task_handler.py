import json
import subprocess
from audit import models
from django.conf import settings
from django.db.transaction import atomic


class Task(object):
    """处理批量任务，包括命令和文件传输"""
    def __init__(self,request):
        self.request = request
        self.errors = []
        self.task_data = None

    def is_valid(self):
        """
        1. 验证命令、主机列表合法
        :return:
        """
        task_data = self.request.POST.get('task_data')
        if task_data:
            self.task_data = json.loads(task_data)
            if self.task_data.get('task_type') == 'cmd':
                if self.task_data.get('cmd') and self.task_data.get('selected_host_ids'):
                    return True
                self.errors.append({'invalid_argument': 'cmd or host_list is empty.'})
            elif self.task_data.get('task_type') == 'file_transfer':
                self.errors.append({'invalid_argument':'cmd or host_list is empty.'})
            else:
                self.errors.append({'invalid_argument':'task_type is invalid.'})
        self.errors.append({'invalid_data':'task_data is not exist '})


    def run(self):
        """start task , and return task id """
        task_func = getattr(self, self.task_data.get('task_type'))
        task_id = task_func()
        return task_id


    def cmd(self):
        """批量任务"""
        #print("run multi task.....")
        task_obj = models.Task.objects.create(
            task_type = 0,
            account = self.request.user.account ,
            content = self.task_data.get('cmd'),
        )
        print("task_obj-------",task_obj)
        tasklog_objs = []
        host_ids = set(self.task_data.get("selected_host_ids"))
        print("host_ids------",host_ids)
        for host_id in host_ids:
            tasklog_objs.append(
                models.TaskLog(task_id=task_obj.id,
                               host_user_bind_id=host_id,
                               status=3
                               )
            )
        a = models.TaskLog.objects.bulk_create(tasklog_objs, 100)
        print("---------aa",a)

        cmd_str = "python3 %s %s" % (settings.MULTI_TASK_SCRIPT, task_obj.id)
        print("cmd_str--------",cmd_str)
        print("task_obj.id----------", task_obj.id)
        multitask_obj = subprocess.Popen(cmd_str,
                                         shell=True,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE)

        return task_obj.id

    def run_cmd(self):
        pass
    def file_transfer(self):
        """批量文件"""
