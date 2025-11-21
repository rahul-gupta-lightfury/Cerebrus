#include <d3d11.h>
#include <tchar.h>
#include <windows.h>

#include <cstdio>

#include "imgui.h"
#include "backends/imgui_impl_win32.h"
#include "backends/imgui_impl_dx11.h"

// Dear ImGui Win32 + DirectX11 bootstrap adapted for the Cerebrus perf report prototype.
// The UI renders a single window with inputs for the source artifact, output directory,
// and output file name. A "Generate Perf Report" button simulates kicking off the flow
// while we wire the real tooling.

// Data container for the initial perf-report UI slice.
struct PerfReportState {
    char input_path[260]{""};
    char output_directory[260]{""};
    char output_file[128]{"report.prt"};
    bool request_submitted{false};
    char status_text[256]{"Select inputs and generate a report."};
};

// Forward declarations for Win32/DirectX helpers from the ImGui example.
extern IMGUI_IMPL_API LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);
static LRESULT WINAPI WndProc(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);
static bool CreateDeviceD3D(HWND hWnd);
static void CleanupDeviceD3D();
static void CreateRenderTarget();
static void CleanupRenderTarget();

// DirectX state.
static ID3D11Device* g_pd3dDevice = nullptr;
static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr;
static IDXGISwapChain* g_pSwapChain = nullptr;
static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr;

static bool CreateDeviceD3D(HWND hWnd) {
    DXGI_SWAP_CHAIN_DESC sd = {};
    sd.BufferCount = 2;
    sd.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM;
    sd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;
    sd.OutputWindow = hWnd;
    sd.SampleDesc.Count = 1;
    sd.Windowed = TRUE;
    sd.SwapEffect = DXGI_SWAP_EFFECT_DISCARD;
    sd.Flags = DXGI_SWAP_CHAIN_FLAG_ALLOW_MODE_SWITCH;

    UINT createDeviceFlags = 0;
#ifdef _DEBUG
    createDeviceFlags |= D3D11_CREATE_DEVICE_DEBUG;
#endif

    D3D_FEATURE_LEVEL featureLevel;
    const D3D_FEATURE_LEVEL featureLevelArray[2] = {D3D_FEATURE_LEVEL_11_0, D3D_FEATURE_LEVEL_10_0};
    if (D3D11CreateDeviceAndSwapChain(
            nullptr, D3D_DRIVER_TYPE_HARDWARE, nullptr, createDeviceFlags, featureLevelArray, 2,
            D3D11_SDK_VERSION, &sd, &g_pSwapChain, &g_pd3dDevice, &featureLevel, &g_pd3dDeviceContext) != S_OK) {
        return false;
    }

    CreateRenderTarget();
    return true;
}

static void CleanupDeviceD3D() {
    CleanupRenderTarget();
    if (g_pSwapChain) {
        g_pSwapChain->Release();
        g_pSwapChain = nullptr;
    }
    if (g_pd3dDeviceContext) {
        g_pd3dDeviceContext->Release();
        g_pd3dDeviceContext = nullptr;
    }
    if (g_pd3dDevice) {
        g_pd3dDevice->Release();
        g_pd3dDevice = nullptr;
    }
}

static void CreateRenderTarget() {
    ID3D11Texture2D* pBackBuffer = nullptr;
    g_pSwapChain->GetBuffer(0, IID_PPV_ARGS(&pBackBuffer));
    if (pBackBuffer == nullptr) {
        return;
    }

    g_pd3dDevice->CreateRenderTargetView(pBackBuffer, nullptr, &g_mainRenderTargetView);
    pBackBuffer->Release();
}

static void CleanupRenderTarget() {
    if (g_mainRenderTargetView) {
        g_mainRenderTargetView->Release();
        g_mainRenderTargetView = nullptr;
    }
}

int WINAPI wWinMain(HINSTANCE hInstance, HINSTANCE, PWSTR, int nCmdShow) {
    // Register the Win32 window class.
    WNDCLASSEX wc = {};
    wc.cbSize = sizeof(WNDCLASSEX);
    wc.style = CS_CLASSDC;
    wc.lpfnWndProc = WndProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = _T("CerebrusImGuiWindowClass");
    ::RegisterClassEx(&wc);

    HWND hwnd = ::CreateWindow(wc.lpszClassName, _T("Cerebrus Perf Report Prototype"), WS_OVERLAPPEDWINDOW,
        100, 100, 1280, 720, nullptr, nullptr, wc.hInstance, nullptr);

    if (!CreateDeviceD3D(hwnd)) {
        CleanupDeviceD3D();
        ::UnregisterClass(wc.lpszClassName, wc.hInstance);
        return 1;
    }

    ::ShowWindow(hwnd, nCmdShow);
    ::UpdateWindow(hwnd);

    // Setup Dear ImGui context.
    IMGUI_CHECKVERSION();
    ImGui::CreateContext();
    ImGuiIO& io = ImGui::GetIO();
    io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard;

    ImGui::StyleColorsDark();

    ImGui_ImplWin32_Init(hwnd);
    ImGui_ImplDX11_Init(g_pd3dDevice, g_pd3dDeviceContext);

    PerfReportState state{};

    // Main render loop.
    bool done = false;
    while (!done) {
        MSG msg;
        while (::PeekMessage(&msg, nullptr, 0U, 0U, PM_REMOVE)) {
            if (msg.message == WM_QUIT) {
                done = true;
            }
            ::TranslateMessage(&msg);
            ::DispatchMessage(&msg);
        }
        if (done) {
            break;
        }

        // Start the Dear ImGui frame.
        ImGui_ImplDX11_NewFrame();
        ImGui_ImplWin32_NewFrame();
        ImGui::NewFrame();

        ImGui::SetNextWindowSize(ImVec2(520, 240), ImGuiCond_FirstUseEver);
        if (ImGui::Begin("Perf Report")) {
            ImGui::TextWrapped("Bootstrap the PerfReportTool flow. Provide an input artifact, where the output should be placed, and the name of the generated file.");
            ImGui::Spacing();

            ImGui::InputText("Input artifact (CSV/PRC)", state.input_path, IM_ARRAYSIZE(state.input_path));
            ImGui::InputText("Output directory", state.output_directory, IM_ARRAYSIZE(state.output_directory));
            ImGui::InputText("Output file name", state.output_file, IM_ARRAYSIZE(state.output_file));

            if (ImGui::Button("Generate Perf Report", ImVec2(-1, 0))) {
                state.request_submitted = true;
                std::snprintf(
                    state.status_text,
                    IM_ARRAYSIZE(state.status_text),
                    "Queued report for '%s' -> %s/%s",
                    state.input_path[0] == '\0' ? "<unset>" : state.input_path,
                    state.output_directory[0] == '\0' ? "<unset>" : state.output_directory,
                    state.output_file[0] == '\0' ? "<unset>" : state.output_file);
            }

            ImGui::Spacing();
            ImGui::Separator();
            ImGui::Spacing();
            ImGui::TextColored(ImVec4(0.4f, 0.8f, 1.0f, 1.0f), "%s", state.status_text);

            if (!state.request_submitted) {
                ImGui::TextDisabled("Hint: connect the button to the PerfReportTool wrapper once available.");
            } else {
                ImGui::TextDisabled("Request submitted placeholder: integrate command dispatch next.");
            }
        }
        ImGui::End();

        // Rendering.
        ImGui::Render();
        const float clear_color_with_alpha[4] = {0.08f, 0.09f, 0.12f, 1.0f};
        g_pd3dDeviceContext->OMSetRenderTargets(1, &g_mainRenderTargetView, nullptr);
        g_pd3dDeviceContext->ClearRenderTargetView(g_mainRenderTargetView, clear_color_with_alpha);
        ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());

        g_pSwapChain->Present(1, 0);
    }

    ImGui_ImplDX11_Shutdown();
    ImGui_ImplWin32_Shutdown();
    ImGui::DestroyContext();

    CleanupDeviceD3D();
    ::DestroyWindow(hwnd);
    ::UnregisterClass(wc.lpszClassName, wc.hInstance);

    return 0;
}

LRESULT WINAPI WndProc(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    if (ImGui_ImplWin32_WndProcHandler(hWnd, msg, wParam, lParam)) {
        return true;
    }

    switch (msg) {
        case WM_SIZE:
            if (g_pd3dDevice != nullptr && wParam != SIZE_MINIMIZED) {
                CleanupRenderTarget();
                g_pSwapChain->ResizeBuffers(0, (UINT)LOWORD(lParam), (UINT)HIWORD(lParam), DXGI_FORMAT_UNKNOWN, 0);
                CreateRenderTarget();
            }
            return 0;
        case WM_SYSCOMMAND:
            if ((wParam & 0xfff0) == SC_KEYMENU) { // Disable ALT application menu.
                return 0;
            }
            break;
        case WM_DESTROY:
            ::PostQuitMessage(0);
            return 0;
        default:
            break;
    }
    return ::DefWindowProc(hWnd, msg, wParam, lParam);
}

