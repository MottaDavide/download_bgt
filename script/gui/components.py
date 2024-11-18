import customtkinter
from typing import List

class MyCheckboxFrame(customtkinter.CTkFrame):
    def __init__(self, master, values: List[str], title: str):
        super().__init__(master)
        self.values = values
        self.checkboxes = []

        title_label = customtkinter.CTkLabel(self, text=title, fg_color="#39597B", corner_radius=6)
        title_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

        for i, value in enumerate(self.values):
            checkbox = customtkinter.CTkCheckBox(self, text=value)
            checkbox.grid(row=i + 1, column=0, padx=10, pady=(15, 0), sticky="ew")
            self.checkboxes.append(checkbox)

    def get(self) -> List[str]:
        return [
            checkbox.cget("text") for checkbox in self.checkboxes if checkbox.get() == 1
        ]