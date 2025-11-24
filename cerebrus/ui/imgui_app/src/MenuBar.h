#pragma once

#include <array>
#include <string>
#include <unordered_map>
#include <vector>

class MenuBar
{
public:
    MenuBar();
    void Render();

    struct BindingRow
    {
        std::string action;
        std::string label;
        std::array<char, 32> buffer{};
    };

private:
    void RenderKeyBindingsPopup();
    void SyncBuffersFromBindings();
    void ResetBindingsToDefault();
    void ImportSampleBindings();
    void ExportBindings();
    void EnsureLatestWins(const std::string &action, const std::string &binding);
    const char *GetShortcutForAction(const std::string &action) const;

    bool m_ShowKeyBindingsPopup = false;
    std::unordered_map<std::string, std::string> m_Bindings;
    std::unordered_map<std::string, std::string> m_DefaultBindings;
    std::unordered_map<std::string, std::string> m_StagedBindings;
    std::vector<BindingRow> m_BindingRows;
    std::string m_ExportBuffer;
};
