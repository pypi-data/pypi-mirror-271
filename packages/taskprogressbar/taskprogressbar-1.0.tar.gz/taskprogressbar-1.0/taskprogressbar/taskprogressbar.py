import ipywidgets as widgets
from IPython.display import display
import time
import datetime

class TaskProgressBar:
    def __init__(self, task_ids, label="Task Progress", update_interval=0.1, status_order=None):
        self.label = label
        self.update_interval = update_interval
        self.tasks = {task_id: 'pending' for task_id in task_ids}
        self.total_tasks = len(task_ids)
        self.status_counts = {'success': 0, 'pending': self.total_tasks, 'ongoing': 0, 'failed': 0, 'cached': 0}
        self.status_order = status_order or ['cached', 'success', 'ongoing', 'pending', 'failed']
        self.colors = {'success': '#32CD32', 'pending': '#D3D3D3', 'ongoing': '#00BFFF', 'failed': '#FF6347', 'cached': '#FFA500'}
        self.progress_bar = widgets.HTML()
        self.start_time = time.time()
        self.last_update_time = self.start_time
        self.update_all()

    def update_all(self):
        completed_tasks = self.status_counts['success'] + self.status_counts['failed'] + self.status_counts['cached']
        elapsed_time = time.time() - self.start_time
        speed = completed_tasks / elapsed_time if elapsed_time > 0 else 0
        remaining_tasks = self.total_tasks - completed_tasks
        eta = remaining_tasks / speed if speed > 0 and remaining_tasks > 0 else elapsed_time
        eta_str = str(datetime.timedelta(seconds=int(eta))) if remaining_tasks > 0 else str(datetime.timedelta(seconds=int(elapsed_time)))
        
        status_info = "".join([
            f"<span style='color: {self.colors[status]};'>&#9679; {status.capitalize()}: {self.status_counts[status]}</span>"
            for status in self.status_order
        ])

        html = f"""
        <style>
            .info-line {{ display: flex; justify-content: space-between; font-family: Arial, sans-serif; }}
            .progress-bar {{
                width: 100%; background-color: #ddd; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 2px rgba(0,0,0,0.1);
            }}
            .progress-bar div {{ height: 20px; float: left; }}
        </style>
        <div class="info-line">
            <span>{self.label}</span>
            <span>{status_info}</span>
            <span>Speed: {speed:.2f} tasks/sec, ETA: {eta_str}</span>
        </div>
        <div class="progress-bar">
            {"".join([f"<div style='width: {self.status_counts[status] / self.total_tasks * 100}%; background-color: {self.colors[status]};'></div>" for status in self.status_order])}
        </div>
        """
        self.progress_bar.value = html

    def display(self):
        display(self.progress_bar)

    def update_task_status(self, task_id, status):
        current_status = self.tasks[task_id]
        if current_status != status:
            self.tasks[task_id] = status
            self.status_counts[current_status] -= 1
            self.status_counts[status] += 1
            current_time = time.time()
            if current_time - self.last_update_time > self.update_interval:  # Limit updates
                self.update_all()
                self.last_update_time = current_time