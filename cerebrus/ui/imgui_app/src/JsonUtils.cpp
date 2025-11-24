#include "JsonUtils.h"

#include <cctype>
#include <sstream>

static std::string Indent(size_t depth, int indentSpaces)
{
    return std::string(depth * static_cast<size_t>(indentSpaces), ' ');
}

static std::string Escape(const std::string &value)
{
    std::string escaped;
    escaped.reserve(value.size());
    for (const char ch : value)
    {
        switch (ch)
        {
            case '\\':
                escaped += "\\\\";
                break;
            case '"':
                escaped += "\\\"";
                break;
            case '\n':
                escaped += "\\n";
                break;
            case '\r':
                escaped += "\\r";
                break;
            case '\t':
                escaped += "\\t";
                break;
            default:
                escaped.push_back(ch);
                break;
        }
    }
    return escaped;
}

std::string JsonUtils::WriteFlatObject(const StringMap &values, int indentSpaces)
{
    std::ostringstream output;
    output << "{\n";
    size_t index = 0;
    for (const auto &entry : values)
    {
        output << Indent(1, indentSpaces) << "\"" << Escape(entry.first) << "\": \"" << Escape(entry.second) << "\"";
        output << (index + 1 < values.size() ? ",\n" : "\n");
        ++index;
    }
    output << "}";
    return output.str();
}

std::string JsonUtils::WriteScriptDocument(const ScriptDocument &document, int indentSpaces)
{
    std::ostringstream output;
    output << "{\n";

    const auto writeStringField = [&](const std::string &key, const std::string &value, bool hasTrailingComma)
    {
        output << Indent(1, indentSpaces) << "\"" << Escape(key) << "\": \"" << Escape(value) << "\"";
        output << (hasTrailingComma ? ",\n" : "\n");
    };

    const auto writeBoolField = [&](const std::string &key, bool value, bool hasTrailingComma)
    {
        output << Indent(1, indentSpaces) << "\"" << Escape(key) << "\": " << (value ? "true" : "false");
        output << (hasTrailingComma ? ",\n" : "\n");
    };

    size_t stringIndex = 0;
    for (const auto &entry : document.stringValues)
    {
        const bool hasTrailingComma = stringIndex + 1 < document.stringValues.size() || !document.boolValues.empty() || !document.steps.empty();
        writeStringField(entry.first, entry.second, hasTrailingComma);
        ++stringIndex;
    }

    size_t boolIndex = 0;
    for (const auto &entry : document.boolValues)
    {
        const bool hasTrailingComma = boolIndex + 1 < document.boolValues.size() || !document.steps.empty();
        writeBoolField(entry.first, entry.second, hasTrailingComma);
        ++boolIndex;
    }

    output << Indent(1, indentSpaces) << "\"steps\": [";
    if (document.steps.empty())
    {
        output << "]\n";
    }
    else
    {
        output << "\n";
        for (size_t index = 0; index < document.steps.size(); ++index)
        {
            output << Indent(2, indentSpaces) << "{\n";
            const StringMap &step = document.steps[index];
            size_t fieldIndex = 0;
            for (const auto &field : step)
            {
                const bool hasTrailingComma = fieldIndex + 1 < step.size();
                output << Indent(3, indentSpaces) << "\"" << Escape(field.first) << "\": \"" << Escape(field.second) << "\"";
                output << (hasTrailingComma ? ",\n" : "\n");
                ++fieldIndex;
            }
            output << Indent(2, indentSpaces) << "}";
            output << (index + 1 < document.steps.size() ? ",\n" : "\n");
        }
        output << Indent(1, indentSpaces) << "]\n";
    }

    output << "}";
    return output.str();
}

JsonUtils::StringMap JsonUtils::ParseFlatObject(const std::string &jsonText)
{
    StringMap values;
    std::string key;
    std::string value;
    enum class State
    {
        SeekingKey,
        ReadingKey,
        SeekingValue,
        ReadingValue,
    };

    State state = State::SeekingKey;
    for (size_t index = 0; index < jsonText.size(); ++index)
    {
        const char ch = jsonText[index];
        switch (state)
        {
            case State::SeekingKey:
            {
                if (ch == '"')
                {
                    key.clear();
                    state = State::ReadingKey;
                }
                break;
            }
            case State::ReadingKey:
            {
                if (ch == '"')
                {
                    state = State::SeekingValue;
                }
                else
                {
                    key.push_back(ch);
                }
                break;
            }
            case State::SeekingValue:
            {
                if (ch == '"')
                {
                    value.clear();
                    state = State::ReadingValue;
                }
                break;
            }
            case State::ReadingValue:
            {
                if (ch == '"')
                {
                    values[key] = value;
                    state = State::SeekingKey;
                }
                else if (ch == '\\' && index + 1 < jsonText.size())
                {
                    const char next = jsonText[++index];
                    switch (next)
                    {
                        case 'n':
                            value.push_back('\n');
                            break;
                        case 'r':
                            value.push_back('\r');
                            break;
                        case 't':
                            value.push_back('\t');
                            break;
                        case '"':
                            value.push_back('"');
                            break;
                        case '\\':
                            value.push_back('\\');
                            break;
                        default:
                            value.push_back(next);
                            break;
                    }
                }
                else
                {
                    value.push_back(ch);
                }
                break;
            }
        }
    }
    return values;
}

