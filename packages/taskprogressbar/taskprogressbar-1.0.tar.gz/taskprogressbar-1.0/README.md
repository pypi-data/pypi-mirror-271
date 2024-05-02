# TaskProgressBar

TaskProgressBar is a Python package designed for visualizing task progress in Jupyter Notebooks. It provides a colorful and intuitive display of multiple task statuses, such as pending, ongoing, success, failed, and cached. The package leverages `ipywidgets` to create dynamic, real-time updating progress bars.

This project is created with the help of GPT-4.

## Features

- **Visual Feedback**: Instant visual feedback on the progress of multiple tasks.
- **Color-Coded**: Tasks are color-coded based on their status for quick assessment.
- **Customizable**: Easy to customize labels, update intervals, and status display order.

## Installation

Install TaskProgressBar by running the following command in your Python environment:

```bash
pip install ipywidgets
pip install taskprogressbar
```

Ensure that you have ipywidgets installed and enabled in your Jupyter environment to use TaskProgressBar.
Usage

Here is a simple example of how to use TaskProgressBar:

```python

from taskprogressbar import TaskProgressbar

# Create a list of task identifiers
task_ids = ['task1', 'task2', 'task3', 'task4']

# Initialize the progress bar with tasks as pending status
progress_bar = TaskProgressbar(task_ids)

# Display the progress bar in a Jupyter Notebook
progress_bar.display()

# Example: Update task statuses
progress_bar.update_task_status('task1', 'ongoing')
progress_bar.update_task_status('task2', 'success')
progress_bar.update_task_status('task3', 'failed')
progress_bar.update_task_status('task4', 'cached')
```

This will display a progress bar in your Jupyter notebook, updating in real-time as tasks change status.
## Contributing

Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.

Please ensure to update tests as appropriate.
## License

Distributed under the MIT License. See LICENSE for more information.