#pragma once

#include <string>
#include <unordered_map>

// Application-wide constants for the Dear ImGui layer.
inline constexpr int g_KeyBindingFieldWidth = 180;
inline constexpr float g_KeyBindingActionColumnWidth = 160.0f;
inline constexpr float g_KeyBindingActiveColumnWidth = 180.0f;

inline const std::unordered_map<std::string, std::string> g_DefaultKeyBindings = {
    {"file.new_window", "Ctrl+N"},
    {"file.exit", "Alt+F4"},
    {"view.reset_layout", "Ctrl+0"},
    {"profile.new", "Ctrl+Shift+N"},
    {"profile.open", "Ctrl+O"},
    {"profile.save", "Ctrl+S"},
    {"profile.edit", "Ctrl+E"},
};
