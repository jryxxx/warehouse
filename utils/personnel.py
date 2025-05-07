# !/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# @Date        : 2025/5/6 19:27
# @Author      : Ruiyang Jia
# @File        : personnel.py
# @Description : 班组与人员调度管理模块

class Worker:
    """
    Worker class representing a worker in the system.
    """

    def __init__(self, worker_id, name, skills):
        self.worker_id = worker_id
        self.name = name
        self.skills = skills
        self.assigned_tasks = []

    def do_one_task(self):
        """
        If one task has been done, remove it.
        :return:
        """
        if self.assigned_tasks:
            task = self.assigned_tasks.pop(0)
            return task
        return None


class WorkGroup:
    """
    WorkGroup class representing a group of workers.
    """

    def __init__(self, group_id, group_name):
        self.group_id = group_id
        self.group_name = group_name
        self.members = []

    def add_member(self, worker):
        """
        Add a worker to the work group.
        :param worker:
        """
        self.members.append(worker)


class Task:
    """
    Task class representing a task in the system.
    """

    def __init__(self, task_id, skill_required, priority=1):
        self.task_id = task_id
        self.skill_required = skill_required
        self.priority = priority
        self.assigned_to = None


class DispatchSystem:
    """
    DispatchSystem class for managing the assignment of tasks to workers.
    """

    def __init__(self):
        self.groups = []
        self.tasks = []
        self.tasks_dict = {}

    def add_group(self, group):
        """
        Add a work group to the dispatch system.
        :param group:
        """
        self.groups.append(group)

    def add_task(self, task):
        """
        Add a task to the dispatch system.
        :param task:
        """
        self.tasks.append(task)

    def assign_tasks(self):
        """
        Assign tasks to workers based on their skills and task priority.
        """
        self.tasks.sort(key=lambda t: -t.priority)
        for task in self.tasks:
            eligible_workers = []
            for group in self.groups:
                for worker in group.members:
                    if task.skill_required in worker.skills:
                        eligible_workers.append(worker)
            if eligible_workers:
                selected = min(eligible_workers, key=lambda w: len(w.assigned_tasks))
                selected.assigned_tasks.append(task)
                task.assigned_to = selected.name

    def show_assignments(self):
        """
        Show the assignments of tasks to workers.
        """
        for group in self.groups:
            print(f"\n Group：{group.group_name}")
            for member in group.members:
                task_list = [t.task_id for t in member.assigned_tasks]
                print(f" {member.name}（skill：{member.skills}）→ task：{task_list}")


if __name__ == "__main__":
    # Example usage
    dispatch_system = DispatchSystem()

    # Create work groups
    group1 = WorkGroup(1, "Group A")
    group2 = WorkGroup(2, "Group B")

    # Create workers
    worker1 = Worker(1, "Alice", ["crane", "transport"])
    worker2 = Worker(2, "Bob", ["crane"])
    worker3 = Worker(3, "Charlie", ["transport"])

    # Add workers to groups
    group1.add_member(worker1)
    group1.add_member(worker2)
    group2.add_member(worker3)

    # Add groups to dispatch system
    dispatch_system.add_group(group1)
    dispatch_system.add_group(group2)

    # Create tasks
    task1 = Task(1, "crane", priority=2)
    task2 = Task(2, "transport")

    # Add tasks to dispatch system
    dispatch_system.add_task(task1)
    dispatch_system.add_task(task2)

    # Assign tasks
    dispatch_system.assign_tasks()

    # Show assignments
    dispatch_system.show_assignments()
