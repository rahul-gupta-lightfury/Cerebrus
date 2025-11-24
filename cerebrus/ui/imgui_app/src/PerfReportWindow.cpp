#include "PerfReportWindow.h"

#include <cstdio>

namespace
{
    ImVec2 GetBrowseButtonSize()
    {
        const float buttonWidth = 110.0f;
        return ImVec2(buttonWidth, 0.0f);
    }
}

PerfReportWindow::PerfReportWindow()
{
    m_DeviceRows.push_back({"1 node", "VRC01", "23222333"});
    m_DeviceRows.push_back({"DevKit", "XR-12", "44559911"});
    m_DeviceRows.push_back({"Perf Rig", "P52S", "23222333"});
    std::snprintf(m_Profile.nickname, IM_ARRAYSIZE(m_Profile.nickname), "%s", "Dev-Mainline");
    std::snprintf(m_Profile.packageName, IM_ARRAYSIZE(m_Profile.packageName), "%s", "com.lightfury.titan");
    std::snprintf(m_Profile.securityToken, IM_ARRAYSIZE(m_Profile.securityToken), "%s", "F33AAEB445176EA93837B69679B3E2C4");
}

PerfReportState::PerfReportState()
    : m_InputPath{""},
      m_OutputDirectory{""},
      m_OutputFile{"report"},
      m_RequestSubmitted(false),
      m_StatusText{"Select inputs and generate a report."}
{
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

const char *PerfReportState::GetValueOrPlaceholder(const char *value) const
{
    static const char *const placeholder = "<unset>";
    return (value == nullptr || value[0] == '\0') ? placeholder : value;
}

void PerfReportWindow::Render(const ImGuiIO &io)
{
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
    RenderStatus(io);

    ImGui::End();
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
            ImGui::InputText("##ProfileNickname", m_Profile.nickname, IM_ARRAYSIZE(m_Profile.nickname));

            ImGui::TableNextRow();
            ImGui::TableSetColumnIndex(0);
            ImGui::AlignTextToFramePadding();
            ImGui::TextUnformatted("Package Name");
            ImGui::TableSetColumnIndex(1);
            ImGui::SetNextItemWidth(-1);
            ImGui::InputText("##PackageName", m_Profile.packageName, IM_ARRAYSIZE(m_Profile.packageName));

            ImGui::TableNextRow();
            ImGui::TableSetColumnIndex(0);
            ImGui::AlignTextToFramePadding();
            ImGui::TextUnformatted("Security Token (Hex, optional)");
            ImGui::TableSetColumnIndex(1);
            ImGui::SetNextItemWidth(-1);
            ImGui::InputText("##SecurityToken", m_Profile.securityToken, IM_ARRAYSIZE(m_Profile.securityToken));

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
        ImGui::InputText("##InputArtifact", m_State.GetInputPathBuffer(), m_State.GetInputPathBufferSize());
        ImGui::TableSetColumnIndex(2);
        ImGui::SetCursorPosY(ImGui::GetCursorPosY() - 2.0f);
        ImGui::Button("Browse...", GetBrowseButtonSize());

        ImGui::TableNextRow();
        ImGui::TableSetColumnIndex(0);
        ImGui::AlignTextToFramePadding();
        ImGui::TextUnformatted("Output directory");
        ImGui::TableSetColumnIndex(1);
        ImGui::SetNextItemWidth(-1);
        ImGui::InputText("##OutputDirectory", m_State.GetOutputDirectoryBuffer(), m_State.GetOutputDirectoryBufferSize());
        ImGui::TableSetColumnIndex(2);
        ImGui::SetCursorPosY(ImGui::GetCursorPosY() - 2.0f);
        ImGui::Button("Browse...", GetBrowseButtonSize());

        ImGui::TableNextRow();
        ImGui::TableSetColumnIndex(0);
        ImGui::AlignTextToFramePadding();
        ImGui::TextUnformatted("Output file name (No Extension Needed)");
        ImGui::TableSetColumnIndex(1);
        ImGui::SetNextItemWidth(-1);
        ImGui::InputText("##OutputFile", m_State.GetOutputFileBuffer(), m_State.GetOutputFileBufferSize());
        ImGui::TableSetColumnIndex(2);
        ImGui::Dummy(GetBrowseButtonSize());

        ImGui::EndTable();
    }
    ImGui::PopStyleVar();
    
    if (ImGui::Button("Generate Perf Report", ImVec2(-1, 0)))
    {
        m_State.QueueRequest();
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
