#pragma once

#include "imgui.h"

#include <cstddef>
#include <filesystem>
#include <functional>
#include <string>
#include <vector>

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
    void HandleShortcuts(const ImGuiIO &io);
    void RenderDeviceAndPackagePanel();
    void RenderForm();
    void RenderStatus(const ImGuiIO &io);
    void RenderDeviceExplorer();
    void RenderActionsRow();
    void RenderInputManager();
    void RenderFileTree();
    void RenderPrefabs();
    void RenderJsonNodeEditor();
    void RenderScriptPreview();
    void RenderConsole();
    void RefreshFileTree();
    void BuildScriptPreview();
    void AppendConsole(const std::string &line);
    void ApplySelectedFile();

    struct DeviceRow
    {
        const char *name;
        const char *model;
        const char *serial;
        const char *location;
        const char *status;
    };

    struct PackageProfile
    {
        char nickname[64];
        char packageName[128];
        char securityToken[128];
    };

    struct FileNode
    {
        std::filesystem::path path;
        bool isDirectory = false;
        std::vector<FileNode> children;
    };

    struct InputAction
    {
        std::string name;
        std::string description;
        ImGuiKey key;
        bool ctrl = false;
        bool shift = false;
        bool alt = false;
        std::function<void()> callback;
    };

    PerfReportState m_State;
    PackageProfile m_Profile{};
    int m_SelectedDeviceIndex = 0;
    ImVector<DeviceRow> m_DeviceRows;
    std::vector<FileNode> m_FileTree;
    std::filesystem::path m_FileRoot;
    std::filesystem::path m_SelectedDirectory;
    std::filesystem::path m_SelectedFile;
    bool m_PrefabBestRenderQuality = true;
    bool m_PrefabMaxThroughput = true;
    bool m_PrefabNetwork = false;
    bool m_PrefabPcaps = false;
    std::vector<std::string> m_ScriptNodes;
    std::string m_ScriptPreview;
    std::vector<std::string> m_ConsoleMessages;
    std::vector<InputAction> m_InputActions;
};
