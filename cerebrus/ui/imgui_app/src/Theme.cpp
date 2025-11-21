#include "Theme.h"

#include "imgui.h"

void Theme::ApplyDarkGreen()
{
    ImGuiStyle &style = ImGui::GetStyle();
    style.WindowRounding = 4.0f;
    style.FrameRounding = 4.0f;
    style.ScrollbarRounding = 4.0f;
    style.TabRounding = 4.0f;
    style.WindowBorderSize = 1.0f;
    style.FrameBorderSize = 1.0f;

    ImVec4 *colors = style.Colors;
    colors[ImGuiCol_Text] = ImVec4(0.92f, 0.96f, 0.98f, 1.0f);
    colors[ImGuiCol_TextDisabled] = ImVec4(0.55f, 0.60f, 0.64f, 1.0f);
    colors[ImGuiCol_WindowBg] = ImVec4(0.05f, 0.06f, 0.08f, 1.0f);
    colors[ImGuiCol_ChildBg] = ImVec4(0.05f, 0.06f, 0.08f, 1.0f);
    colors[ImGuiCol_PopupBg] = ImVec4(0.07f, 0.08f, 0.12f, 1.0f);
    colors[ImGuiCol_Border] = ImVec4(0.13f, 0.15f, 0.20f, 1.0f);
    colors[ImGuiCol_FrameBg] = ImVec4(0.12f, 0.16f, 0.12f, 1.0f);
    colors[ImGuiCol_FrameBgHovered] = ImVec4(0.20f, 0.35f, 0.22f, 1.0f);
    colors[ImGuiCol_FrameBgActive] = ImVec4(0.28f, 0.50f, 0.30f, 1.0f);
    colors[ImGuiCol_TitleBg] = ImVec4(0.09f, 0.12f, 0.15f, 1.0f);
    colors[ImGuiCol_TitleBgActive] = ImVec4(0.14f, 0.18f, 0.22f, 1.0f);
    colors[ImGuiCol_TitleBgCollapsed] = ImVec4(0.09f, 0.12f, 0.15f, 0.70f);
    colors[ImGuiCol_MenuBarBg] = ImVec4(0.05f, 0.17f, 0.35f, 1.0f);
    colors[ImGuiCol_Header] = ImVec4(0.20f, 0.35f, 0.22f, 1.0f);
    colors[ImGuiCol_HeaderHovered] = ImVec4(0.28f, 0.50f, 0.30f, 1.0f);
    colors[ImGuiCol_HeaderActive] = ImVec4(0.35f, 0.65f, 0.38f, 1.0f);
    colors[ImGuiCol_Button] = ImVec4(0.18f, 0.30f, 0.20f, 1.0f);
    colors[ImGuiCol_ButtonHovered] = ImVec4(0.26f, 0.42f, 0.28f, 1.0f);
    colors[ImGuiCol_ButtonActive] = ImVec4(0.35f, 0.65f, 0.38f, 1.0f);
    colors[ImGuiCol_Tab] = ImVec4(0.14f, 0.18f, 0.22f, 1.0f);
    colors[ImGuiCol_TabHovered] = ImVec4(0.20f, 0.30f, 0.35f, 1.0f);
    colors[ImGuiCol_TabActive] = ImVec4(0.18f, 0.32f, 0.38f, 1.0f);
    colors[ImGuiCol_TabUnfocused] = ImVec4(0.10f, 0.12f, 0.15f, 1.0f);
    colors[ImGuiCol_TabUnfocusedActive] = ImVec4(0.16f, 0.24f, 0.28f, 1.0f);
    colors[ImGuiCol_ScrollbarGrab] = ImVec4(0.18f, 0.30f, 0.20f, 1.0f);
    colors[ImGuiCol_ScrollbarGrabHovered] = ImVec4(0.28f, 0.50f, 0.30f, 1.0f);
    colors[ImGuiCol_ScrollbarGrabActive] = ImVec4(0.35f, 0.65f, 0.38f, 1.0f);
    colors[ImGuiCol_CheckMark] = ImVec4(0.45f, 0.90f, 0.60f, 1.0f);
    colors[ImGuiCol_SliderGrab] = ImVec4(0.28f, 0.50f, 0.30f, 1.0f);
    colors[ImGuiCol_SliderGrabActive] = ImVec4(0.35f, 0.65f, 0.38f, 1.0f);
    colors[ImGuiCol_Separator] = ImVec4(0.10f, 0.13f, 0.16f, 1.0f);
    colors[ImGuiCol_SeparatorHovered] = ImVec4(0.28f, 0.50f, 0.30f, 1.0f);
    colors[ImGuiCol_SeparatorActive] = ImVec4(0.35f, 0.65f, 0.38f, 1.0f);
    colors[ImGuiCol_ResizeGrip] = ImVec4(0.28f, 0.50f, 0.30f, 0.35f);
    colors[ImGuiCol_ResizeGripHovered] = ImVec4(0.35f, 0.65f, 0.38f, 0.78f);
    colors[ImGuiCol_ResizeGripActive] = ImVec4(0.45f, 0.90f, 0.60f, 1.0f);
    colors[ImGuiCol_TableHeaderBg] = ImVec4(0.07f, 0.08f, 0.12f, 1.0f);
    colors[ImGuiCol_TableBorderStrong] = ImVec4(0.10f, 0.13f, 0.16f, 1.0f);
    colors[ImGuiCol_TableBorderLight] = ImVec4(0.06f, 0.08f, 0.11f, 1.0f);
}
