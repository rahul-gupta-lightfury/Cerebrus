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

    if (ImGui::BeginMenu("Edit"))
    {
        ImGui::MenuItem("Undo", "Ctrl+Z");
        ImGui::MenuItem("Redo", "Ctrl+Y");
        ImGui::Separator();
        ImGui::MenuItem("Preferences");
        ImGui::EndMenu();
    }

    if (ImGui::BeginMenu("View"))
    {
        ImGui::MenuItem("Reset Layout");
        ImGui::MenuItem("Toggle Grid");
        ImGui::EndMenu();
    }

    if (ImGui::BeginMenu("Repository"))
    {
        ImGui::MenuItem("Clone");
        ImGui::MenuItem("Pull");
        ImGui::MenuItem("Push");
        ImGui::EndMenu();
    }

    if (ImGui::BeginMenu("Actions"))
    {
        ImGui::MenuItem("Build");
        ImGui::MenuItem("Run");
        ImGui::MenuItem("Deploy");
        ImGui::EndMenu();
    }

    if (ImGui::BeginMenu("Tools"))
    {
        ImGui::MenuItem("Profiler");
        ImGui::MenuItem("Metrics");
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
