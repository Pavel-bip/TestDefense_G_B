from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import MDList, TwoLineListItem
from kivy.properties import StringProperty, ListProperty
from kivy.core.window import Window

Window.size = (400, 600)

KV = '''
<PriorityButton@MDFillRoundFlatButton>:
    theme_text_color: "Custom"
    text_color: 1, 1, 1, 1
    size_hint: None, None
    size: "100dp", "40dp"

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
            md_bg_color: 0.2, 0.7, 0.2, 1 
            on_release: root.set_priority("low")

        PriorityButton:
            id: medium_btn
            text: "Средний"
            md_bg_color: 1, 0.6, 0, 1  
            on_release: root.set_priority("medium")

        PriorityButton:
            id: high_btn
            text: "Высокий"
            md_bg_color: 0.9, 0.2, 0.2, 1  
            on_release: root.set_priority("high")

    MDLabel:
        text: "Список задач:"
        size_hint_y: None
        height: self.texture_size[1]
        font_style: "H6"

    ScrollView:
        MDList:
            id: task_list
            spacing: "10dp"
'''

Builder.load_string(KV)


class Content(MDBoxLayout):
    tasks = ListProperty([])
    current_priority = StringProperty("medium")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_priority("medium")

    def set_priority(self, priority):
        self.current_priority = priority

        self.ids.low_btn.md_bg_color = (0.2, 0.7, 0.2, 0.7)
        self.ids.medium_btn.md_bg_color = (1, 0.6, 0, 0.7)
        self.ids.high_btn.md_bg_color = (0.9, 0.2, 0.2, 0.7)

        if priority == "low":
            self.ids.low_btn.md_bg_color = (0.2, 0.7, 0.2, 1)
        elif priority == "medium":
            self.ids.medium_btn.md_bg_color = (1, 0.6, 0, 1)
        elif priority == "high":
            self.ids.high_btn.md_bg_color = (0.9, 0.2, 0.2, 1)

    def add_task(self):
        task_text = self.ids.task_input.text.strip()

        if task_text:
            item = TwoLineListItem(
                text=task_text,
                secondary_text=f"Приоритет: {self.get_priority_text(self.current_priority)}",
                theme_text_color="Custom" if self.current_priority == "high" else "Primary",
                text_color=(0.9, 0.2, 0.2, 1) if self.current_priority == "high" else (1, 1, 1, 1),
                secondary_theme_text_color="Custom",
                secondary_text_color=(0.2, 0.7, 0.2, 1) if self.current_priority == "low" else
                (1, 0.6, 0, 1) if self.current_priority == "medium" else
                (0.9, 0.2, 0.2, 1)
            )

            self.ids.task_list.add_widget(item)

            self.tasks.append({
                "text": task_text,
                "priority": self.current_priority,
                "widget": item
            })

            self.ids.task_input.text = ""

    def get_priority_text(self, priority):
        return {
            "low": "Низкий",
            "medium": "Средний",
            "high": "Высокий"
        }[priority]
class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.title = "Тест: Гуров + Бодров"
        return Content()
MainApp().run()