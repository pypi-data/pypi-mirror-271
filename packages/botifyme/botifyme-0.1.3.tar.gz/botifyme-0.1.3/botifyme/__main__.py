import os
import argparse
import json
from botifyme.runtime import generate_config, load_modules_from_directory
from botifyme.config import get_tool, tool_registry


def execute_tool(tool_name, tool_args, temp_dir=None):
    print("Function name", tool_name)
    print("Args", tool_args, type(tool_args))

    kwargs = json.loads(tool_args) if tool_args else {}

    current_directory = os.getcwd()
    load_modules_from_directory(current_directory)

    print("writing to temp dir", temp_dir)

    for _, tool in tool_registry.items():
        if tool.name == tool_name:
            try:
                output = tool.func(**kwargs)

                print("Output from tool", output)
                print("Output type", type(output))

                # If output is a dictionary or a pydantic model, convert it to a JSON string.
                if isinstance(output, dict) or hasattr(output, "json"):
                    with open(
                        os.path.join(temp_dir, "output.json"), "w", encoding="utf-8"
                    ) as f:
                        json.dump(output, f)

                if isinstance(output, str):
                    with open(
                        os.path.join(temp_dir, "output.txt"), "w", encoding="utf-8"
                    ) as f:
                        f.write(output)

            except Exception as e:
                # with open(
                #     os.path.join(temp_dir, "error.log"), "w", encoding="utf-8"
                # ) as f:
                #     f.write(str(e))

                print(e)
                return e


def list_tools():
    """
    List all the tools that are available in the tool registry.
    """

    current_directory = os.getcwd()
    load_modules_from_directory(current_directory)

    for tool_name in tool_registry.keys():
        print(tool_name)


def main():
    """
    Parse the command line arguments and execute the appropriate command.
    """

    parser = argparse.ArgumentParser(description="Process BotifyMe commands.")
    parser.add_argument_group("commands")
    parser.add_argument(
        "command",
        help="The command to execute. Possible values: generate-config, exec-tool, list-tools.",
    )
    parser.add_argument(
        "--tool-name", type=str, default=None, help="The function to execute."
    )
    parser.add_argument(
        "--tool-args",
        type=str,
        default=None,
        help="The arguments to pass to the function.",
    )

    parser.add_argument(
        "--temp-dir",
        type=str,
        default=None,
        help="The temporary directory to use for the execution.",
    )

    args = parser.parse_args()

    if args.command == "generate-config":
        generate_config()
    elif args.command == "exec-tool":
        execute_tool(args.tool_name, args.tool_args, args.temp_dir)
    elif args.command == "list-tools":
        list_tools()
    else:
        raise ValueError(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
