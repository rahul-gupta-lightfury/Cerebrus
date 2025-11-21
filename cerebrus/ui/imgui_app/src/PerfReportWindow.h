#pragma once

#include "imgui.h"

#include <cstddef>

class PerfReportState
{
public:
    PerfReportState();

    bool HasSubmittedRequest() const;

    char *GetInputPathBuffer();
    char *GetOutputDirectoryBuffer();
    char *GetOutputFileBuffer();
    size_t GetInputPathBufferSize() const;
    size_t GetOutputDirectoryBufferSize() const;
    size_t GetOutputFileBufferSize() const;
    const char *GetStatusText() const;

    void QueueRequest();

private:
    const char *GetValueOrPlaceholder(const char *value) const;

    char m_InputPath[260];
    char m_OutputDirectory[260];
    char m_OutputFile[128];
    bool m_RequestSubmitted;
    char m_StatusText[256];
};

class PerfReportWindow
{
public:
    void Render(const ImGuiIO &io);

private:
    void RenderForm();
    void RenderStatus(const ImGuiIO &io);

    PerfReportState m_State;
};
