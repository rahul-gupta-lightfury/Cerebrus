#include "PerfReportWindow.h"

#include <algorithm>
#include <chrono>
#include <cfloat>
#include <cstdio>
#include <filesystem>
#include <ctime>
#include <system_error>
#include <iomanip>
#include <sstream>

#include "JsonUtils.h"

namespace
{
    ImVec2 GetBrowseButtonSize()
    {
        const float buttonWidth = 110.0f;
        return ImVec2(buttonWidth, 0.0f);
    }

    std::string GetFilename(const std::filesystem::path &path)
    {
        return path.filename().empty() ? path.string() : path.filename().string();
    }

    std::string MakeTimestamp()
    {
        const auto now = std::chrono::system_clock::now();
        const std::time_t nowTime = std::chrono::system_clock::to_time_t(now);
        std::tm tm{};
#ifdef _WIN32
        localtime_s(&tm, &nowTime);
#else
        localtime_r(&nowTime, &tm);
#endif
        std::ostringstream stream;
        stream << std::put_time(&tm, "%H:%M:%S");
        return stream.str();
    }
}

PerfReportWindow::PerfReportWindow()
{
    m_DeviceRows.push_back({"1 node", "VRC01", "23222333", "London", "Ready"});
    m_DeviceRows.push_back({"DevKit", "XR-12", "44559911", "Lab A", "Available"});
    m_DeviceRows.push_back({"Perf Rig", "P52S", "23222333", "Lab B", "Reserved"});

    m_ScriptNodes.push_back("Input -> Filter nodes");
    m_ScriptNodes.push_back("Calculate nodes per unique filter of node");
    m_ScriptNodes.push_back("Chart: Post Processing node time vs nodes per child of Post Processing node");

    m_FileRoot = std::filesystem::current_path();
    m_SelectedDirectory = m_FileRoot;
    RefreshFileTree();

    m_InputActions = {
        {"generate_report", "Generate report (Ctrl+G)", ImGuiKey_G, true, false, false, [this]() {
             m_State.QueueRequest();
             AppendConsole("Queued perf report via shortcut.");
             BuildScriptPreview();
         }},
        {"save_template", "Save template (Ctrl+S)", ImGuiKey_S, true, false, false, [this]() {
             AppendConsole("Saved template placeholder to disk.");
         }},
        {"load_template", "Load template (Ctrl+O)", ImGuiKey_O, true, false, false, [this]() {
             AppendConsole("Loaded template placeholder from disk.");
         }},
        {"save_script", "Save script (Ctrl+Shift+S)", ImGuiKey_S, true, true, false, [this]() {
             AppendConsole("Saved script preview to file.");
         }},
        {"open_script", "Open script (Ctrl+Shift+O)", ImGuiKey_O, true, true, false, [this]() {
             AppendConsole("Opened script preview from file.");
         }},
        {"refresh_files", "Refresh file view (F5)", ImGuiKey_F5, false, false, false, [this]() {
             RefreshFileTree();
             AppendConsole("Refreshed file system view.");
         }},
    };

    BuildScriptPreview();
}

PerfReportState::PerfReportState()
    : m_InputPath{""},
      m_OutputDirectory{""},
      m_OutputFile{"report"},
      m_RequestSubmitted(false),
      m_StatusText{"Select inputs and generate a report."}
{
}

void PerfReportState::QueueRequest()
{
    m_RequestSubmitted = true;
    std::snprintf(
        m_StatusText,
        IM_ARRAYSIZE(m_StatusText),
        "Queued report for '%s' -> %s/%s",
        GetValueOrPlaceholder(m_InputPath),
        GetValueOrPlaceholder(m_OutputDirectory),
        GetValueOrPlaceholder(m_OutputFile));
}

bool PerfReportState::HasSubmittedRequest() const
{
    return m_RequestSubmitted;
}

char *PerfReportState::GetInputPathBuffer()
{
    return m_InputPath;
}

size_t PerfReportState::GetInputPathBufferSize() const
{
    return IM_ARRAYSIZE(m_InputPath);
}

char *PerfReportState::GetOutputDirectoryBuffer()
{
    return m_OutputDirectory;
}

size_t PerfReportState::GetOutputDirectoryBufferSize() const
{
    return IM_ARRAYSIZE(m_OutputDirectory);
}

char *PerfReportState::GetOutputFileBuffer()
{
    return m_OutputFile;
}

size_t PerfReportState::GetOutputFileBufferSize() const
{
    return IM_ARRAYSIZE(m_OutputFile);
}

const char *PerfReportState::GetStatusText() const
{
    return m_StatusText;
}

const char *PerfReportState::GetValueOrPlaceholder(const char *value) const
{
    static const char *const placeholder = "<unset>";
    return (value == nullptr || value[0] == '\0') ? placeholder : value;
}

void PerfReportWindow::Render(const ImGuiIO &io)
{
    HandleShortcuts(io);

    ImGui::SetNextWindowSize(ImVec2(880, 520), ImGuiCond_FirstUseEver);
    if (!ImGui::Begin("Perf Report"))
    {
        ImGui::End();
        return;
    }

    RenderDeviceAndPackagePanel();
    ImGui::Spacing();
    ImGui::Separator();
    ImGui::Spacing();
    RenderForm();
    RenderDeviceExplorer();
    RenderStatus(io);
    RenderActionsRow();

    ImGui::End();

    RenderInputManager();
    RenderFileTree();
    RenderPrefabs();
    RenderJsonNodeEditor();
    RenderScriptPreview();
    RenderConsole();
}

void PerfReportWindow::HandleShortcuts(const ImGuiIO &io)
{
    for (const InputAction &action : m_InputActions)
    {
        const bool ctrlOk = action.ctrl ? io.KeyCtrl : !io.KeyCtrl;
        const bool shiftOk = action.shift ? io.KeyShift : !io.KeyShift;
        const bool altOk = action.alt ? io.KeyAlt : !io.KeyAlt;
        if (ctrlOk && shiftOk && altOk && ImGui::IsKeyPressed(action.key))
        {
            if (action.callback)
            {
                action.callback();
            }
        }
    }
}

void PerfReportWindow::RenderDeviceAndPackagePanel()
{
    const char *selectedDeviceName = m_DeviceRows.empty() ? "<none>" : m_DeviceRows[m_SelectedDeviceIndex % m_DeviceRows.Size].name;

    ImGui::Text("Selected Device: %s", selectedDeviceName);
    ImGui::SameLine();
    ImGui::Text("Selected Package: %s", m_Profile.packageName[0] == '\0' ? "<unset>" : m_Profile.packageName);
    ImGui::Spacing();

    if (ImGui::BeginTable("DeviceAndPackage", 2, ImGuiTableFlags_Resizable | ImGuiTableFlags_SizingStretchSame | ImGuiTableFlags_BordersInnerV))
    {
        ImGui::TableSetupColumn("Devices", ImGuiTableColumnFlags_WidthStretch, 0.45f);
        ImGui::TableSetupColumn("Package", ImGuiTableColumnFlags_WidthStretch, 0.55f);

        ImGui::TableNextRow();
        ImGui::TableSetColumnIndex(0);
        ImGui::TextUnformatted("Device");
        ImGui::BeginChild("DeviceSelection", ImVec2(0, 200), true);
        if (ImGui::BeginTable("DeviceTable", 3, ImGuiTableFlags_RowBg | ImGuiTableFlags_BordersInnerV))
        {
            ImGui::TableSetupColumn("Name", ImGuiTableColumnFlags_WidthStretch);
            ImGui::TableSetupColumn("Model", ImGuiTableColumnFlags_WidthFixed, 120.0f);
            ImGui::TableSetupColumn("Serial", ImGuiTableColumnFlags_WidthFixed, 140.0f);
            ImGui::TableHeadersRow();

            for (int index = 0; index < m_DeviceRows.Size; ++index)
            {
                const DeviceRow &device = m_DeviceRows[index];
                ImGui::TableNextRow();
                ImGui::TableSetColumnIndex(0);
                const bool selected = (m_SelectedDeviceIndex == index);
                if (ImGui::Selectable(device.name, selected, ImGuiSelectableFlags_SpanAllColumns))
                {
                    m_SelectedDeviceIndex = index;
                    BuildScriptPreview();
                }
                ImGui::TableSetColumnIndex(1);
                ImGui::TextUnformatted(device.model);
                ImGui::TableSetColumnIndex(2);
                ImGui::TextUnformatted(device.serial);
            }
            ImGui::EndTable();
        }
        ImGui::EndChild();

        ImGui::TableSetColumnIndex(1);
        ImGui::TextUnformatted("Package");
        ImGui::PushStyleVar(ImGuiStyleVar_CellPadding, ImVec2(8.0f, 6.0f));
        if (ImGui::BeginTable("PackageForm", 2, ImGuiTableFlags_SizingStretchSame))
        {
            ImGui::TableSetupColumn("Label", ImGuiTableColumnFlags_WidthFixed, 150.0f);
            ImGui::TableSetupColumn("Value", ImGuiTableColumnFlags_WidthStretch);

            ImGui::TableNextRow();
            ImGui::TableSetColumnIndex(0);
            ImGui::AlignTextToFramePadding();
            ImGui::TextUnformatted("Profile Nickname");
            ImGui::TableSetColumnIndex(1);
            ImGui::SetNextItemWidth(-1);
            if (ImGui::InputText("##ProfileNickname", m_Profile.nickname, IM_ARRAYSIZE(m_Profile.nickname)))
            {
                BuildScriptPreview();
            }

            ImGui::TableNextRow();
            ImGui::TableSetColumnIndex(0);
            ImGui::AlignTextToFramePadding();
            ImGui::TextUnformatted("Package Name");
            ImGui::TableSetColumnIndex(1);
            ImGui::SetNextItemWidth(-1);
            if (ImGui::InputText("##PackageName", m_Profile.packageName, IM_ARRAYSIZE(m_Profile.packageName)))
            {
                BuildScriptPreview();
            }

            ImGui::TableNextRow();
            ImGui::TableSetColumnIndex(0);
            ImGui::AlignTextToFramePadding();
            ImGui::TextUnformatted("Security Token (Hex, optional)");
            ImGui::TableSetColumnIndex(1);
            ImGui::SetNextItemWidth(-1);
            if (ImGui::InputText("##SecurityToken", m_Profile.securityToken, IM_ARRAYSIZE(m_Profile.securityToken)))
            {
                BuildScriptPreview();
            }

            ImGui::EndTable();
        }
        ImGui::PopStyleVar();
        ImGui::Spacing();
        ImGui::TextDisabled("Profile JSON example:");
        ImGui::TextWrapped("{\n  \"Profile Nickname\": \"%s\",\n  \"Package Name\": \"%s\",\n  \"Security Token\": \"%s\"\n}",
                           m_Profile.nickname,
                           m_Profile.packageName,
                           m_Profile.securityToken[0] == '\0' ? "<optional>" : m_Profile.securityToken);
        ImGui::EndTable();
    }
}

void PerfReportWindow::RenderForm()
{
    ImGui::TextWrapped(
        "Bootstrap the PerfReportTool flow. Provide an input artifact, where the output should be placed, and the name of the"
        " generated file.");
    ImGui::Spacing();

    ImGui::PushStyleVar(ImGuiStyleVar_CellPadding, ImVec2(8.0f, 6.0f));
    if (ImGui::BeginTable("PerfReportFormTable", 3, ImGuiTableFlags_SizingStretchSame | ImGuiTableFlags_BordersInnerV))
    {
        ImGui::TableSetupColumn("Label", ImGuiTableColumnFlags_WidthFixed, 210.0f);
        ImGui::TableSetupColumn("Input", ImGuiTableColumnFlags_WidthStretch);
        ImGui::TableSetupColumn("Action", ImGuiTableColumnFlags_WidthFixed, 120.0f);

        ImGui::TableNextRow();
        ImGui::TableSetColumnIndex(0);
        ImGui::AlignTextToFramePadding();
        ImGui::TextUnformatted("Input artifact (CSV)");
        ImGui::TableSetColumnIndex(1);
        ImGui::SetNextItemWidth(-1);
        if (ImGui::InputText("##InputArtifact", m_State.GetInputPathBuffer(), m_State.GetInputPathBufferSize()))
        {
            BuildScriptPreview();
        }
        ImGui::TableSetColumnIndex(2);
        ImGui::SetCursorPosY(ImGui::GetCursorPosY() - 2.0f);
        if (ImGui::Button("Browse...", GetBrowseButtonSize()))
        {
            if (!m_SelectedFile.empty())
            {
                ApplySelectedFile();
            }
        }

        ImGui::TableNextRow();
        ImGui::TableSetColumnIndex(0);
        ImGui::AlignTextToFramePadding();
        ImGui::TextUnformatted("Output directory");
        ImGui::TableSetColumnIndex(1);
        ImGui::SetNextItemWidth(-1);
        if (ImGui::InputText("##OutputDirectory", m_State.GetOutputDirectoryBuffer(), m_State.GetOutputDirectoryBufferSize()))
        {
            BuildScriptPreview();
        }
        ImGui::TableSetColumnIndex(2);
        ImGui::SetCursorPosY(ImGui::GetCursorPosY() - 2.0f);
        if (ImGui::Button("Browse...", GetBrowseButtonSize()))
        {
            if (!m_SelectedDirectory.empty())
            {
                std::snprintf(m_State.GetOutputDirectoryBuffer(), m_State.GetOutputDirectoryBufferSize(), "%s", m_SelectedDirectory.string().c_str());
                BuildScriptPreview();
            }
        }

        ImGui::TableNextRow();
        ImGui::TableSetColumnIndex(0);
        ImGui::AlignTextToFramePadding();
        ImGui::TextUnformatted("Output file name (No Extension Needed)");
        ImGui::TableSetColumnIndex(1);
        ImGui::SetNextItemWidth(-1);
        if (ImGui::InputText("##OutputFile", m_State.GetOutputFileBuffer(), m_State.GetOutputFileBufferSize()))
        {
            BuildScriptPreview();
        }
        ImGui::TableSetColumnIndex(2);
        ImGui::Dummy(GetBrowseButtonSize());

        ImGui::EndTable();
    }
    ImGui::PopStyleVar();

    if (ImGui::Button("Generate Perf Report", ImVec2(-1, 0)))
    {
        m_State.QueueRequest();
        AppendConsole("Queued perf report via button click.");
        BuildScriptPreview();
    }
}

void PerfReportWindow::RenderDeviceExplorer()
{
    ImGui::Spacing();
    ImGui::Separator();
    ImGui::Spacing();
    ImGui::TextUnformatted("Device exploration");
    ImGui::Spacing();

    if (ImGui::BeginTable("DeviceExplorer", 2, ImGuiTableFlags_Resizable | ImGuiTableFlags_SizingStretchSame | ImGuiTableFlags_BordersInnerV))
    {
        ImGui::TableSetupColumn("Devices", ImGuiTableColumnFlags_WidthStretch, 0.4f);
        ImGui::TableSetupColumn("Details", ImGuiTableColumnFlags_WidthStretch, 0.6f);

        ImGui::TableNextRow();
        ImGui::TableSetColumnIndex(0);
        if (ImGui::Button("Refresh", ImVec2(-1, 0)))
        {
            AppendConsole("Requested device refresh.");
        }
        if (ImGui::Button("Auto choose best", ImVec2(-1, 0)))
        {
            AppendConsole("Auto-selection placeholder executed.");
        }

        ImGui::BeginChild("DeviceList", ImVec2(0, 160), true);
        for (int index = 0; index < m_DeviceRows.Size; ++index)
        {
            ImGui::PushID(index);
            const bool selected = (m_SelectedDeviceIndex == index);
            if (ImGui::Selectable(m_DeviceRows[index].name, selected))
            {
                m_SelectedDeviceIndex = index;
                BuildScriptPreview();
            }
            ImGui::PopID();
        }
        ImGui::EndChild();

        ImGui::TableSetColumnIndex(1);
        ImGui::BeginChild("DeviceDetails", ImVec2(0, 0), true);
        if (m_DeviceRows.empty())
        {
            ImGui::TextDisabled("No devices found.");
        }
        else
        {
            const DeviceRow &device = m_DeviceRows[m_SelectedDeviceIndex % m_DeviceRows.Size];
            ImGui::Text("Name: %s", device.name);
            ImGui::Text("Model: %s", device.model);
            ImGui::Text("Serial: %s", device.serial);
            ImGui::Text("Location: %s", device.location);
            ImGui::Text("Status: %s", device.status);
            ImGui::Spacing();
            ImGui::TextWrapped("Use the controls on the left to refresh or auto-select the best device. Device pairing and activation "
                               "statuses will surface here once connected to real discovery endpoints.");
        }
        ImGui::EndChild();

        ImGui::EndTable();
    }
}

void PerfReportWindow::RenderStatus(const ImGuiIO &io)
{
    const bool dockingSupported = (io.ConfigFlags & ImGuiConfigFlags_DockingEnable) != 0;

    ImGui::Spacing();
    ImGui::Separator();
    ImGui::Spacing();
    ImGui::TextColored(ImVec4(0.4f, 0.8f, 1.0f, 1.0f), "%s", m_State.GetStatusText());

    if (!m_State.HasSubmittedRequest())
    {
        ImGui::TextDisabled("Hint: connect the button to the PerfReportTool wrapper once available.");
    }
    else
    {
        ImGui::TextDisabled("Request submitted placeholder: integrate command dispatch next.");
    }

    ImGui::Spacing();
    ImGui::Separator();
    ImGui::Spacing();
    ImGui::Text("Docking support: %s", dockingSupported ? "Enabled" : "Unavailable");
    if (dockingSupported)
    {
        ImGui::TextDisabled("Tip: drag this window's tab to dock it in the workspace.");
    }
    else
    {
        ImGui::TextDisabled("Docking is disabled. Ensure Dear ImGui is built with docking branch.");
    }
}

void PerfReportWindow::RenderActionsRow()
{
    ImGui::Spacing();
    ImGui::Separator();
    ImGui::Spacing();
    if (ImGui::Button("Generate Profiling Report"))
    {
        m_State.QueueRequest();
        AppendConsole("Queued profiling report from actions row.");
        BuildScriptPreview();
    }
    ImGui::SameLine();
    if (ImGui::Button("Save template"))
    {
        AppendConsole("Saved template placeholder from actions row.");
    }
    ImGui::SameLine();
    if (ImGui::Button("Load template"))
    {
        AppendConsole("Loaded template placeholder from actions row.");
    }
    ImGui::SameLine();
    if (ImGui::Button("Save Script"))
    {
        AppendConsole("Saved script preview from actions row.");
    }
    ImGui::SameLine();
    if (ImGui::Button("Open Script"))
    {
        AppendConsole("Opened script placeholder from actions row.");
    }
}

void PerfReportWindow::RenderInputManager()
{
    ImGui::SetNextWindowSize(ImVec2(600, 260), ImGuiCond_FirstUseEver);
    if (ImGui::Begin("Perf report input file manager"))
    {
        ImGui::TextUnformatted("Use the file system explorer or load a script file.");
        ImGui::TextUnformatted("Double click a file to copy its location into the Input field above.");
        ImGui::TextUnformatted("Use Script files to add/remove nodes from the active graph.");
        ImGui::Separator();

        const std::filesystem::path directory = m_SelectedDirectory.empty() ? m_FileRoot : m_SelectedDirectory;
        ImGui::Text("Directory: %s", directory.string().c_str());

        std::error_code readError;
        std::vector<std::filesystem::directory_entry> entries;
        for (std::filesystem::directory_iterator it(directory, readError); it != std::filesystem::directory_iterator(); it.increment(readError))
        {
            if (readError)
            {
                break;
            }
            if (it->is_regular_file() || it->is_directory())
            {
                entries.push_back(*it);
            }
        }

        if (readError)
        {
            ImGui::TextColored(ImVec4(1.0f, 0.5f, 0.5f, 1.0f), "Failed to read directory: %s", readError.message().c_str());
        }
        else if (ImGui::BeginTable("InputManagerTable", 3, ImGuiTableFlags_Borders | ImGuiTableFlags_RowBg | ImGuiTableFlags_SizingStretchSame))
        {
            ImGui::TableSetupColumn("Name", ImGuiTableColumnFlags_WidthStretch);
            ImGui::TableSetupColumn("Type", ImGuiTableColumnFlags_WidthFixed, 120.0f);
            ImGui::TableSetupColumn("Action", ImGuiTableColumnFlags_WidthFixed, 120.0f);
            ImGui::TableHeadersRow();

            size_t rowIndex = 0;
            for (const auto &entry : entries)
            {
                const bool isDir = entry.is_directory();
                const std::string filename = GetFilename(entry.path());
                const std::string typeLabel = isDir ? "Folder" : entry.path().extension().string();

                ImGui::TableNextRow();
                ImGui::TableSetColumnIndex(0);
                ImGui::Selectable(filename.c_str(), false);
                if (ImGui::IsItemHovered() && ImGui::IsMouseDoubleClicked(ImGuiMouseButton_Left))
                {
                    m_SelectedFile = entry.path();
                    if (isDir)
                    {
                        m_SelectedDirectory = entry.path();
                    }
                    ApplySelectedFile();
                }

                ImGui::TableSetColumnIndex(1);
                ImGui::TextUnformatted(typeLabel.empty() ? "<unknown>" : typeLabel.c_str());

                ImGui::TableSetColumnIndex(2);
                if (ImGui::Button(("Use##" + std::to_string(rowIndex)).c_str()))
                {
                    m_SelectedFile = entry.path();
                    if (isDir)
                    {
                        m_SelectedDirectory = entry.path();
                    }
                    ApplySelectedFile();
                }
                ++rowIndex;
            }
            ImGui::EndTable();
        }
    }
    ImGui::End();
}

void PerfReportWindow::RenderFileTree()
{
    ImGui::SetNextWindowSize(ImVec2(320, 320), ImGuiCond_FirstUseEver);
    if (ImGui::Begin("File Tree"))
    {
        ImGui::TextUnformatted("Use the tree to select the directory for Perf files to run from.");
        if (ImGui::Button("Refresh"))
        {
            RefreshFileTree();
            AppendConsole("Refreshed file tree.");
        }
        ImGui::Separator();

        std::function<void(const FileNode &)> renderNode = [&](const FileNode &node)
        {
            ImGuiTreeNodeFlags flags = node.isDirectory ? ImGuiTreeNodeFlags_OpenOnArrow : ImGuiTreeNodeFlags_Leaf;
            const bool isSelected = (!node.isDirectory && node.path == m_SelectedFile) || (node.isDirectory && node.path == m_SelectedDirectory);
            if (isSelected)
            {
                flags |= ImGuiTreeNodeFlags_Selected;
            }

            const bool open = ImGui::TreeNodeEx(node.path.string().c_str(), flags, "%s", GetFilename(node.path).c_str());
            if (ImGui::IsItemClicked())
            {
                if (node.isDirectory)
                {
                    m_SelectedDirectory = node.path;
                }
                else
                {
                    m_SelectedFile = node.path;
                    ApplySelectedFile();
                }
            }
            if (open && node.isDirectory)
            {
                for (const FileNode &child : node.children)
                {
                    renderNode(child);
                }
                ImGui::TreePop();
            }
            else if (open)
            {
                ImGui::TreePop();
            }
        };

        for (const FileNode &node : m_FileTree)
        {
            renderNode(node);
        }
    }
    ImGui::End();
}

void PerfReportWindow::RenderPrefabs()
{
    ImGui::SetNextWindowSize(ImVec2(360, 260), ImGuiCond_FirstUseEver);
    if (ImGui::Begin("prefabs"))
    {
        ImGui::TextUnformatted("Presets to initialize the data-set.");
        ImGui::TextUnformatted("Data is normalized and not tied to a specific player or session.");
        ImGui::Spacing();
        ImGui::Separator();
        ImGui::Spacing();

        bool rebuilt = false;
        rebuilt |= ImGui::Checkbox("best render quality", &m_PrefabBestRenderQuality);
        ImGui::SameLine();
        ImGui::TextUnformatted("Set filters for best quality rendering.");
        rebuilt |= ImGui::Checkbox("max throughput", &m_PrefabMaxThroughput);
        ImGui::SameLine();
        ImGui::TextUnformatted("Set filters for maximum throughput.");
        rebuilt |= ImGui::Checkbox("network diagnostics", &m_PrefabNetwork);
        ImGui::SameLine();
        ImGui::TextUnformatted("Network and network+performance with Pcaps.");
        rebuilt |= ImGui::Checkbox("pcaps", &m_PrefabPcaps);
        ImGui::SameLine();
        ImGui::TextUnformatted("Include Pcaps in template and data set.");

        if (rebuilt)
        {
            AppendConsole("Updated prefab toggles.");
            BuildScriptPreview();
        }
    }
    ImGui::End();
}

void PerfReportWindow::RenderJsonNodeEditor()
{
    ImGui::SetNextWindowSize(ImVec2(540, 260), ImGuiCond_FirstUseEver);
    if (ImGui::Begin("Json Node Editor"))
    {
        ImGui::TextUnformatted("Use this to build a Json script with additional steps for Perf reporting");
        ImGui::TextUnformatted("Double click a Json field in the Script Preview window to edit the fields manually.");
        ImGui::Separator();
        ImGui::TextUnformatted("Double click a Json field in the Script Preview window to edit the fields manually.");
        ImGui::TextUnformatted("These nodes can also be edited by script in the editor itself if desired.");
        ImGui::Separator();

        bool updated = false;
        for (size_t index = 0; index < m_ScriptNodes.size(); ++index)
        {
            ImGui::PushID(static_cast<int>(index));
            std::string label = "Json Field " + std::to_string(index + 1);
            char buffer[256] = {};
            std::snprintf(buffer, IM_ARRAYSIZE(buffer), "%s", m_ScriptNodes[index].c_str());
            if (ImGui::InputText(label.c_str(), buffer, IM_ARRAYSIZE(buffer)))
            {
                m_ScriptNodes[index] = buffer;
                updated = true;
            }
            ImGui::PopID();
        }

        if (ImGui::Button("Add Script Node"))
        {
            m_ScriptNodes.emplace_back("New script instruction");
            updated = true;
        }

        if (updated)
        {
            AppendConsole("Updated JSON node editor entries.");
            BuildScriptPreview();
        }
    }
    ImGui::End();
}

void PerfReportWindow::RenderScriptPreview()
{
    ImGui::SetNextWindowSize(ImVec2(500, 300), ImGuiCond_FirstUseEver);
    if (ImGui::Begin("Script Preview"))
    {
        ImGui::Text("File name: %s", m_State.GetOutputFileBuffer());
        ImGui::TextUnformatted("Click a Json field to edit it manually");
        ImGui::Separator();
        std::string previewBuffer = m_ScriptPreview;
        previewBuffer.push_back('\0');
        ImGui::InputTextMultiline("##ScriptPreview", previewBuffer.data(), previewBuffer.size(), ImVec2(-FLT_MIN, -FLT_MIN), ImGuiInputTextFlags_ReadOnly);
    }
    ImGui::End();
}

void PerfReportWindow::RenderConsole()
{
    ImGui::SetNextWindowSize(ImVec2(600, 200), ImGuiCond_FirstUseEver);
    if (ImGui::Begin("Console"))
    {
        ImGui::TextUnformatted("Console");
        ImGui::Separator();
        if (ImGui::BeginChild("ConsoleBuffer", ImVec2(0, 0), true))
        {
            for (const std::string &line : m_ConsoleMessages)
            {
                ImGui::TextUnformatted(line.c_str());
            }
        }
        ImGui::EndChild();
    }
    ImGui::End();
}

void PerfReportWindow::RefreshFileTree()
{
    m_FileTree.clear();
    const int maxDepth = 2;

    std::function<FileNode(const std::filesystem::path &, int)> buildNode = [&](const std::filesystem::path &path, int depth) -> FileNode {
        FileNode node;
        node.path = path;
        node.isDirectory = std::filesystem::is_directory(path);
        if (node.isDirectory && depth < maxDepth)
        {
            std::error_code iterateError;
            for (std::filesystem::directory_iterator it(path, iterateError); it != std::filesystem::directory_iterator(); it.increment(iterateError))
            {
                if (iterateError)
                {
                    break;
                }
                if (it->is_directory() || it->is_regular_file())
                {
                    node.children.push_back(buildNode(it->path(), depth + 1));
                }
            }
            std::sort(node.children.begin(), node.children.end(), [](const FileNode &lhs, const FileNode &rhs) {
                if (lhs.isDirectory == rhs.isDirectory)
                {
                    return lhs.path.filename() < rhs.path.filename();
                }
                return lhs.isDirectory && !rhs.isDirectory;
            });
        }
        return node;
    };

    if (std::filesystem::exists(m_FileRoot))
    {
        m_FileTree.push_back(buildNode(m_FileRoot, 0));
    }
    if (m_SelectedDirectory.empty())
    {
        m_SelectedDirectory = m_FileRoot;
    }
}

void PerfReportWindow::BuildScriptPreview()
{
    JsonUtils::ScriptDocument document;
    document.stringValues["input_artifact"] = m_State.GetInputPathBuffer();
    document.stringValues["output_directory"] = m_State.GetOutputDirectoryBuffer();
    document.stringValues["output_file"] = m_State.GetOutputFileBuffer();
    document.stringValues["package_name"] = m_Profile.packageName;
    document.stringValues["profile_nickname"] = m_Profile.nickname;

    if (!m_DeviceRows.empty())
    {
        const DeviceRow &device = m_DeviceRows[m_SelectedDeviceIndex % m_DeviceRows.Size];
        document.stringValues["device_name"] = device.name;
        document.stringValues["device_location"] = device.location;
    }

    document.boolValues["prefab_best_render_quality"] = m_PrefabBestRenderQuality;
    document.boolValues["prefab_max_throughput"] = m_PrefabMaxThroughput;
    document.boolValues["prefab_network_diagnostics"] = m_PrefabNetwork;
    document.boolValues["prefab_pcaps"] = m_PrefabPcaps;

    int stepIndex = 1;
    document.steps.clear();
    for (const std::string &node : m_ScriptNodes)
    {
        JsonUtils::StringMap step;
        step["step"] = std::to_string(stepIndex++);
        step["description"] = node;
        document.steps.push_back(step);
    }

    m_ScriptPreview = JsonUtils::WriteScriptDocument(document, 2);
}

void PerfReportWindow::AppendConsole(const std::string &line)
{
    std::ostringstream stream;
    stream << "[" << MakeTimestamp() << "] " << line;
    m_ConsoleMessages.push_back(stream.str());
}

void PerfReportWindow::ApplySelectedFile()
{
    if (m_SelectedFile.empty())
    {
        return;
    }

    std::snprintf(m_State.GetInputPathBuffer(), m_State.GetInputPathBufferSize(), "%s", m_SelectedFile.string().c_str());
    if (!m_SelectedFile.parent_path().empty())
    {
        std::snprintf(m_State.GetOutputDirectoryBuffer(), m_State.GetOutputDirectoryBufferSize(), "%s", m_SelectedFile.parent_path().string().c_str());
        m_SelectedDirectory = m_SelectedFile.parent_path();
    }
    AppendConsole("Selected file: " + m_SelectedFile.string());
    BuildScriptPreview();
}

