#include "MenuBar.h"

#include "imgui.h"

void MenuBar::Render()
{
    if (!ImGui::BeginMainMenuBar())
    {
        return;
    }

    if (ImGui::BeginMenu("File"))
    {
        ImGui::MenuItem("New", "Ctrl+N");
        ImGui::MenuItem("Open...", "Ctrl+O");
        ImGui::MenuItem("Save", "Ctrl+S");
        ImGui::Separator();
        ImGui::MenuItem("Exit");
        ImGui::EndMenu();
    }

    if (ImGui::BeginMenu("View"))
    {
        ImGui::MenuItem("Reset Layout");
        ImGui::MenuItem("Toggle Grid");
        ImGui::EndMenu();
    }

    if (ImGui::BeginMenu("Tools"))
    {
        ImGui::MenuItem("Echo Test");
        ImGui::EndMenu();
    }

	if (ImGui::BeginMenu("Profile"))
	{
		ImGui::MenuItem("New", "Ctrl+Shift+N");
		ImGui::MenuItem("Open...", "Ctrl+Shift+O");
		ImGui::MenuItem("Save", "Ctrl+Shift+S");
		ImGui::MenuItem("Edit", "Ctrl+E");
		ImGui::EndMenu();
	}

    if (ImGui::BeginMenu("Settings"))
    {
		if (ImGui::BeginMenu("Theme"))
		{
			ImGui::MenuItem("System","");
			ImGui::MenuItem("Light", "");
			ImGui::MenuItem("Dark", "");
			ImGui::MenuItem("Custom", "");
            ImGui::Separator();
            ImGui::MenuItem("Save Custom", "");
            ImGui::MenuItem("Load Custom", "");
            ImGui::Separator();
            // TODO: Load Custom Themes under the THemes subdirectory of the installed location
			ImGui::EndMenu();
		}

		if (ImGui::BeginMenu("Log Colors"))
		{
			ImGui::MenuItem("Edit", "");
			ImGui::MenuItem("Import", "");
			ImGui::MenuItem("Export", "");
			ImGui::MenuItem("Reset To Defaults", "");
			ImGui::EndMenu();
		}

		if (ImGui::BeginMenu("Key Bindings"))
		{
			ImGui::MenuItem("Edit", "");
			ImGui::MenuItem("Import", "");
			ImGui::MenuItem("Export", "");
			ImGui::MenuItem("Reset To Defaults", "");
			ImGui::EndMenu();
		}

        ImGui::EndMenu();
    }

    if (ImGui::BeginMenu("Help"))
    {
        ImGui::MenuItem("Documentation");
        ImGui::MenuItem("About");
        ImGui::EndMenu();
    }

    ImGui::EndMainMenuBar();
}
