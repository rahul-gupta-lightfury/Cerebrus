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
    PerfReportWindow();
    void Render(const ImGuiIO &io);

private:
    void RenderDeviceAndPackagePanel();
    void RenderForm();
    void RenderStatus(const ImGuiIO &io);

    struct DeviceRow
    {
        const char *name;
        const char *model;
        const char *serial;
    };

    struct PackageProfile
    {
        char nickname[64];
        char packageName[128];
        char securityToken[128];
    };

    PerfReportState m_State;
    int m_SelectedDeviceIndex = 0;
    ImVector<DeviceRow> m_DeviceRows;
    PackageProfile m_Profile;
};
