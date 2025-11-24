#include "PerfReportWindow.h"

#include <cstdio>

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
    RenderStatus(io);

    ImGui::End();
}

void PerfReportWindow::RenderForm()
{
    ImGui::TextWrapped(
        "Bootstrap the PerfReportTool flow. Provide an input artifact, where the output should be placed, and the name of the"
        " generated file.");
    ImGui::Spacing();

    
    ImGui::TextWrapped("Input artifact (CSV)");
    ImGui::SameLine(0, 20);
    ImGui::InputText("##", m_State.GetInputPathBuffer(), m_State.GetInputPathBufferSize());

    ImGui::TextWrapped("Output directory");
    ImGui::SameLine(0, 20);
    ImGui::InputText("##", m_State.GetOutputDirectoryBuffer(), m_State.GetOutputDirectoryBufferSize());
    
    ImGui::TextWrapped("Output file name (No Extension Needed)");
    ImGui::SameLine(0, 20);
    ImGui::InputText("##", m_State.GetOutputFileBuffer(), m_State.GetOutputFileBufferSize());

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
