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
    m_DeviceRows.push_back({"1 node", "VRC01", "23222333", "London", "Ready"});
    m_DeviceRows.push_back({"DevKit", "XR-12", "44559911", "Lab A", "Available"});
    m_DeviceRows.push_back({"Perf Rig", "P52S", "23222333", "Lab B", "Reserved"});
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
    ImGui::SetNextWindowSize(ImVec2(520, 260), ImGuiCond_FirstUseEver);
    if (!ImGui::Begin("Perf Report"))
    {
        ImGui::End();
        return;
    }

    RenderForm();
    RenderDeviceExplorer();
    RenderStatus(io);

    ImGui::End();
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
            // Placeholder for a refresh action when device discovery is wired up.
        }
        if (ImGui::Button("Auto choose best", ImVec2(-1, 0)))
        {
            // Placeholder for the best-device selection logic.
        }

        ImGui::BeginChild("DeviceList", ImVec2(0, 160), true);
        for (int index = 0; index < m_DeviceRows.Size; ++index)
        {
            ImGui::PushID(index);
            const bool selected = (m_SelectedDeviceIndex == index);
            if (ImGui::Selectable(m_DeviceRows[index].name, selected))
            {
                m_SelectedDeviceIndex = index;
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
