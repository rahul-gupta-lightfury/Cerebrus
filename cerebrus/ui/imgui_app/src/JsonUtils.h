#pragma once

#include <string>
#include <unordered_map>
#include <vector>

namespace JsonUtils
{
    using StringMap = std::unordered_map<std::string, std::string>;

    struct ScriptDocument
    {
        StringMap stringValues;
        std::unordered_map<std::string, bool> boolValues;
        std::vector<StringMap> steps;
    };

    // Minimal writer and parser helpers for the UI prototypes. This is intentionally
    // lightweight and only supports flat string/bool maps and arrays of objects.
    std::string WriteFlatObject(const StringMap &values, int indentSpaces = 2);
    std::string WriteScriptDocument(const ScriptDocument &document, int indentSpaces = 2);
    StringMap ParseFlatObject(const std::string &jsonText);
}

