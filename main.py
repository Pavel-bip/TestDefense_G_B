from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import MDList
from kivymd.uix.button import MDRaisedButton, MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty, ListProperty, BooleanProperty, NumericProperty
from kivy.core.window import Window

Window.size = (400, 700)

KV = '''
<PriorityButton@MDFillRoundFlatButton>:
    theme_text_color: "Custom"
    text_color: 1, 1, 1, 1
    size_hint: None, None
    size: "100dp", "40dp"

<TaskItem@MDBoxLayout>:
    orientation: "vertical"
    size_hint_y: None
    height: "80dp"
    padding: "10dp"
    spacing: "5dp"
    md_bg_color: app.theme_cls.bg_normal

    MDBoxLayout:
        orientation: "horizontal"
        size_hint_y: None
        height: "30dp"

        MDLabel:
            id: task_label
            text: ""
            size_hint_x: 0.7
            halign: "left"
            valign: "center"
            font_size: "16sp"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1

        MDRaisedButton:
            id: done_btn
            text: "Выполнено"
            size_hint_x: 0.3
            on_release: root.mark_done()
            md_bg_color: 0.2, 0.6, 0.8, 1
            text_color: 1, 1, 1, 1

    MDLabel:
        id: priority_label
        text: ""
        size_hint_y: None
        height: "20dp"
        font_size: "14sp"
        theme_text_color: "Custom"

<Content>:
    orientation: "vertical"
    padding: "20dp"
    spacing: "15dp"

    MDLabel:
        text: "Планировщик задач"
        halign: "center"
        font_style: "H4"
        size_hint_y: None
        height: self.texture_size[1]
        theme_text_color: "Primary"

    MDBoxLayout:
        orientation: "horizontal"
        size_hint_y: None
        height: "50dp"
        spacing: "10dp"

        MDTextField:
            id: task_input
            hint_text: "Введите задачу"
            mode: "rectangle"
            size_hint_x: 0.7
            on_text_validate: root.add_task()

        MDRaisedButton:
            id: add_button
            text: "Добавить"
            size_hint_x: 0.3
            on_release: root.add_task()
            md_bg_color: 0.2, 0.6, 0.8, 1

    MDLabel:
        text: "Приоритет:"
        size_hint_y: None
        height: self.texture_size[1]
        font_style: "H6"

    MDBoxLayout:
        id: priority_buttons
        orientation: "horizontal"
        spacing: "10dp"
        size_hint_y: None
        height: "50dp"

        PriorityButton:
            id: low_btn
            text: "Низкий"
            md_bg_color: 0.2, 0.7, 0.2, 0.7
            on_release: root.set_priority("low")

        PriorityButton:
            id: medium_btn
            text: "Средний"
            md_bg_color: 1, 0.6, 0, 0.7
            on_release: root.set_priority("medium")

        PriorityButton:
            id: high_btn
            text: "Высокий"
            md_bg_color: 0.9, 0.2, 0.2, 0.7
            on_release: root.set_priority("high")

    MDLabel:
        id: counter_label
        text: "Список задач (0/12):"
        size_hint_y: None
        height: self.texture_size[1]
        font_style: "H6"

    ScrollView:
        MDList:
            id: task_list
            spacing: "10dp"
'''
Builder.load_string(KV)
class TaskItem(MDBoxLayout):
    completed = BooleanProperty(False)

    def __init__(self, text, priority, task_id, callback, **kwargs):
        super().__init__(**kwargs)
        self.task_id = task_id
        self.callback = callback
        self.original_text = text
        self.original_priority = priority
        self.completed = False
        self.ids.task_label.text = text

        priority_text = {
            "high": "Приоритет: Высокий",
            "medium": "Приоритет: Средний",
            "low": "Приоритет: Низкий"
        }[priority]
        self.ids.priority_label.text = priority_text

        self.update_colors()

    def update_colors(self):
        if self.completed:
            self.ids.task_label.text_color = (0.5, 0.5, 0.5, 1)
            self.ids.priority_label.text_color = (0.5, 0.5, 0.5, 1)
            if not self.ids.task_label.text.startswith("✓ "):
                self.ids.task_label.text = "✓ " + self.ids.task_label.text
            if not self.ids.priority_label.text.startswith("✓ "):
                self.ids.priority_label.text = "✓ " + self.ids.priority_label.text
        else:
            if self.original_priority == "high":
                self.ids.task_label.text_color = (1, 0.3, 0.3, 1)
                self.ids.priority_label.text_color = (1, 0.5, 0.5, 1)
            elif self.original_priority == "medium":
                self.ids.task_label.text_color = (1, 0.8, 0.2, 1)
                self.ids.priority_label.text_color = (1, 0.9, 0.5, 1)
            else:
                self.ids.task_label.text_color = (0.3, 0.9, 0.3, 1)
                self.ids.priority_label.text_color = (0.6, 1, 0.6, 1)

    def mark_done(self):
        if not self.completed:
            self.completed = True
            self.ids.done_btn.disabled = True
            self.ids.done_btn.text = "✓ Готово"
            self.ids.done_btn.md_bg_color = (0.3, 0.7, 0.3, 1)

            self.update_colors()
            if self.callback:
                self.callback()


class Content(MDBoxLayout):
    tasks = ListProperty([])
    current_priority = StringProperty("medium")
    task_counter = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_priority("medium")

    def set_priority(self, priority):
        self.current_priority = priority

        self.ids.low_btn.md_bg_color = (0.2, 0.7, 0.2, 0.5)
        self.ids.medium_btn.md_bg_color = (1, 0.6, 0, 0.5)
        self.ids.high_btn.md_bg_color = (0.9, 0.2, 0.2, 0.5)

        if priority == "low":
            self.ids.low_btn.md_bg_color = (0.2, 0.9, 0.2, 1)
        elif priority == "medium":
            self.ids.medium_btn.md_bg_color = (1, 0.8, 0.2, 1)
        elif priority == "high":
            self.ids.high_btn.md_bg_color = (1, 0.3, 0.3, 1)

    def add_task(self):
        task_text = self.ids.task_input.text.strip()

        if len(self.tasks) >= 12:
            return

        if task_text:
            self.task_counter += 1

            task_item = TaskItem(
                text=task_text,
                priority=self.current_priority,
                task_id=self.task_counter,
                callback=self.sort_tasks
            )

            self.ids.task_list.add_widget(task_item)

            self.tasks.append({
                "id": self.task_counter,
                "text": task_text,
                "priority": self.current_priority,
                "widget": task_item,
                "completed": False
            })

            self.sort_tasks()

            self.ids.counter_label.text = f"Список задач ({len(self.tasks)}/12):"
            self.ids.task_input.text = ""

    def sort_tasks(self):
        priority_order = {"high": 0, "medium": 1, "low": 2}

        self.tasks.sort(key=lambda x: (
            0 if not x["widget"].completed else 1,
            priority_order[x["priority"]],
            x["id"]
        ))

        self.ids.task_list.clear_widgets()
        for task in self.tasks:
            self.ids.task_list.add_widget(task["widget"])


class TaskPlannerApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.title = "Тест: Гуров + Бодров"

        return Content()
TaskPlannerApp().run()