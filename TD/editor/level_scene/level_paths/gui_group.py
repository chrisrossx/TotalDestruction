
from TD.editor.scene import GUIGroup
from TD.paths import path_data

class PanelGUIGroup(GUIGroup):
    
    def get_path_data(self):
        return path_data[self.selected_line_index]

    @property
    def selected_line_index(self):
        return self.parent.selected_line_index

    @property
    def path_edit_mode(self):
        return self.parent.gui_groups["select_mode"].mode

    def on_selected_line_index(self, selected_line_inedx):
        pass

    def clear_mode(self):
        self.parent.gui_groups["select_mode"].clear_mode()
