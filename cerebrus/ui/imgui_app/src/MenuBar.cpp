#include "MenuBar.h"

#include <cstdio>
#include <sstream>

#include "imgui.h"
#include "JsonUtils.h"

static constexpr int kKeyBindingFieldWidth = 180;

static std::unordered_map<std::string, std::string> GetDefaultKeyBindings()
{
    return {
        {"file.new_window", "Ctrl+Shift+N"},
        {"file.exit", "Alt+F4"},
        {"view.reset_layout", "Ctrl+0"},
        {"profile.new", "Ctrl+N"},
        {"profile.open", "Ctrl+O"},
        {"profile.save", "Ctrl+S"},
        {"profile.edit", "Ctrl+E"},
    };
}

static const std::vector<MenuBar::BindingRow> &GetBindingRowsTemplate()
{
    static std::vector<MenuBar::BindingRow> rows = {
        {"file.new_window", "New Window", {}},
        {"file.exit", "Exit", {}},
        {"view.reset_layout", "Reset Layout", {}},
        {"profile.new", "New Profile", {}},
        {"profile.open", "Open Profile", {}},
        {"profile.save", "Save Profile", {}},
        {"profile.edit", "Edit Profile", {}},
    };
    return rows;
}

MenuBar::MenuBar()
    : m_DefaultBindings(GetDefaultKeyBindings())
{
    m_Bindings = m_DefaultBindings;
    m_StagedBindings = m_Bindings;
    m_BindingRows = GetBindingRowsTemplate();
    SyncBuffersFromBindings();
}

void MenuBar::Render()
{
    if (!ImGui::BeginMainMenuBar())
    {
        return;
    }

    if (ImGui::BeginMenu("File"))
    {
        ImGui::MenuItem("New", GetShortcutForAction("file.new_window"));
        ImGui::MenuItem("Open...", GetShortcutForAction("profile.open"));
        ImGui::MenuItem("Save", GetShortcutForAction("profile.save"));
        ImGui::Separator();
        ImGui::MenuItem("Exit", GetShortcutForAction("file.exit"));
        ImGui::EndMenu();
    }

    if (ImGui::BeginMenu("View"))
    {
        ImGui::MenuItem("Reset Layout", GetShortcutForAction("view.reset_layout"));
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
        ImGui::MenuItem("New", GetShortcutForAction("profile.new"));
        ImGui::MenuItem("Open...", GetShortcutForAction("profile.open"));
        ImGui::MenuItem("Save", GetShortcutForAction("profile.save"));
        ImGui::MenuItem("Edit", GetShortcutForAction("profile.edit"));
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
            if (ImGui::MenuItem("Edit"))
            {
                m_StagedBindings = m_Bindings;
                SyncBuffersFromBindings();
                m_ShowKeyBindingsPopup = true;
            }
            if (ImGui::MenuItem("Import sample"))
            {
                ImportSampleBindings();
            }
            if (ImGui::MenuItem("Export to JSON"))
            {
                m_StagedBindings = m_Bindings;
                SyncBuffersFromBindings();
                ExportBindings();
                m_ShowKeyBindingsPopup = true;
            }
            if (ImGui::MenuItem("Reset To Defaults"))
            {
                ResetBindingsToDefault();
            }
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

    RenderKeyBindingsPopup();
    ImGui::EndMainMenuBar();
}

void MenuBar::RenderKeyBindingsPopup()
{
    if (m_ShowKeyBindingsPopup)
    {
        ImGui::OpenPopup("Key Bindings");
    }

    if (ImGui::BeginPopupModal("Key Bindings", nullptr, ImGuiWindowFlags_AlwaysAutoResize))
    {
        ImGui::TextWrapped("Duplicate bindings are automatically cleared from older actions when you assign a new shortcut.");
        ImGui::Separator();

        if (ImGui::BeginTable("KeyBindingTable", 3, ImGuiTableFlags_SizingStretchSame))
        {
            ImGui::TableSetupColumn("Action", ImGuiTableColumnFlags_WidthFixed, 160.0f);
            ImGui::TableSetupColumn("New Binding", ImGuiTableColumnFlags_WidthStretch);
            ImGui::TableSetupColumn("Active", ImGuiTableColumnFlags_WidthFixed, 180.0f);
            ImGui::TableHeadersRow();

            for (BindingRow &row : m_BindingRows)
            {
                ImGui::TableNextRow();
                ImGui::TableSetColumnIndex(0);
                ImGui::AlignTextToFramePadding();
                ImGui::TextUnformatted(row.label.c_str());

                ImGui::TableSetColumnIndex(1);
                ImGui::SetNextItemWidth(static_cast<float>(kKeyBindingFieldWidth));
                ImGui::InputText(("##" + row.action).c_str(), row.buffer.data(), row.buffer.size());
                ImGui::SameLine();
                if (ImGui::Button(("Assign##" + row.action).c_str()))
                {
                    EnsureLatestWins(row.action, row.buffer.data());
                    SyncBuffersFromBindings();
                }
                ImGui::SameLine();
                if (ImGui::Button(("Clear##" + row.action).c_str()))
                {
                    m_StagedBindings[row.action].clear();
                    SyncBuffersFromBindings();
                }

                ImGui::TableSetColumnIndex(2);
                const auto activeIt = m_StagedBindings.find(row.action);
                const std::string active = (activeIt != m_StagedBindings.end()) ? activeIt->second : std::string();
                ImGui::TextUnformatted(active.empty() ? "<none>" : active.c_str());
            }
            ImGui::EndTable();
        }

        if (ImGui::Button("Restore Defaults"))
        {
            m_StagedBindings = m_DefaultBindings;
            SyncBuffersFromBindings();
        }
        ImGui::SameLine();
        if (ImGui::Button("Import Sample"))
        {
            ImportSampleBindings();
            m_StagedBindings = m_Bindings;
            SyncBuffersFromBindings();
        }
        ImGui::SameLine();
        if (ImGui::Button("Export"))
        {
            ExportBindings();
        }

        if (!m_ExportBuffer.empty())
        {
            ImGui::Separator();
            ImGui::TextDisabled("Export preview:");
            std::string exportPreview = m_ExportBuffer;
            exportPreview.push_back('\0');
            ImGui::InputTextMultiline("##ExportBuffer", exportPreview.data(), exportPreview.size(), ImVec2(480, 120), ImGuiInputTextFlags_ReadOnly);
        }

        ImGui::Separator();
        if (ImGui::Button("OK", ImVec2(120, 0)))
        {
            m_Bindings = m_StagedBindings;
            m_ShowKeyBindingsPopup = false;
            ImGui::CloseCurrentPopup();
        }
        ImGui::SameLine();
        if (ImGui::Button("Cancel", ImVec2(120, 0)))
        {
            m_StagedBindings = m_Bindings;
            SyncBuffersFromBindings();
            m_ShowKeyBindingsPopup = false;
            ImGui::CloseCurrentPopup();
        }

        ImGui::EndPopup();
    }
}

void MenuBar::SyncBuffersFromBindings()
{
    for (BindingRow &row : m_BindingRows)
    {
        const auto it = m_StagedBindings.find(row.action);
        const std::string value = (it != m_StagedBindings.end()) ? it->second : std::string();
        std::snprintf(row.buffer.data(), row.buffer.size(), "%s", value.c_str());
    }
}

void MenuBar::ResetBindingsToDefault()
{
    m_Bindings = m_DefaultBindings;
    m_StagedBindings = m_Bindings;
    SyncBuffersFromBindings();
}

void MenuBar::ImportSampleBindings()
{
    const std::string sampleJson = R"({
  "file.new_window": "Ctrl+Shift+N",
  "file.exit": "Alt+F4",
  "view.reset_layout": "Ctrl+0",
  "profile.new": "Ctrl+N",
  "profile.open": "Ctrl+O",
  "profile.save": "Ctrl+S",
  "profile.edit": "Ctrl+E"
})";
    ImportBindingsFromJson(sampleJson);
}

void MenuBar::ExportBindings()
{
    JsonUtils::StringMap values;
    for (const BindingRow &row : m_BindingRows)
    {
        const auto it = m_StagedBindings.find(row.action);
        values[row.action] = (it != m_StagedBindings.end()) ? it->second : std::string();
    }
    m_ExportBuffer = JsonUtils::WriteFlatObject(values);
}

void MenuBar::ImportBindingsFromJson(const std::string &jsonText)
{
    const JsonUtils::StringMap parsed = JsonUtils::ParseFlatObject(jsonText);
    if (!parsed.empty())
    {
        m_Bindings = parsed;
        m_StagedBindings = m_Bindings;
        SyncBuffersFromBindings();
    }
}

void MenuBar::EnsureLatestWins(const std::string &action, const std::string &binding)
{
    if (binding.empty())
    {
        m_StagedBindings[action].clear();
        return;
    }

    for (auto &entry : m_StagedBindings)
    {
        if (entry.first != action && entry.second == binding)
        {
            entry.second.clear();
        }
    }

    m_StagedBindings[action] = binding;
}

const char *MenuBar::GetShortcutForAction(const std::string &action) const
{
    const auto it = m_Bindings.find(action);
    if (it == m_Bindings.end() || it->second.empty())
    {
        return nullptr;
    }
    return it->second.c_str();
}
