from tree_sitter import Language, Parser
import os
import subprocess
from typing import Optional

# Build the Verilog grammar (you only need to do this once, or when the grammar changes)
# Language.build_library(
#     # Store the library in the `build` directory
#     'build/my-languages.so',
#     # Include one or more languages
#     [
#         './tree-sitter-verilog'
#     ]
# )
#
def build_verilog():
    if os.path.exists("build/verilog.so"):
        return

    # Create build directory if it doesn't exist
    os.makedirs('build', exist_ok=True)

    repo_path = "tree-sitter-verilog"

    if not os.path.exists(repo_path):
        subprocess.run(['git', 'clone', 'https://github.com/tree-sitter/tree-sitter-verilog.git'])

    assert os.path.exists(repo_path + "/src/parser.c")

    # No need to rebuild parser.c
    # build_commands = [
    #     f"cd {repo_path} && npm install",  # Install node dependencies
    #     f"cd {repo_path} && npx tree-sitter generate"  # Generate the parser
    # ]
    #
    # for cmd in build_commands:
    #     try:
    #         subprocess.run(cmd, shell=True, check=True)
    #     except subprocess.CalledProcessError as e:
    #         print(f"Error executing command '{cmd}': {e}")
    #         return None

    Language.build_library(
        'build/verilog.so',
        ['./tree-sitter-verilog']
    )

def parse_verilog_code(code):
    """Parses Verilog code and returns the syntax tree."""
    tree = parser.parse(bytes(code, "utf8"))
    return tree

def traverse_tree(node):
    """Recursively traverses the syntax tree and prints node information."""
    print(f"Node type: {node.type}, Start: {node.start_point}, End: {node.end_point}")
    for child in node.children:
        traverse_tree(child)

if __name__ == "__main__":
    build_verilog()

    VERILOG_LANGUAGE = Language('build/verilog.so', 'verilog')

    parser = Parser()
    parser.set_language(VERILOG_LANGUAGE)

    verilog_code = """
    module my_module (
        input clk,
        input rst,
        output reg [7:0] data
    );

        always @(posedge clk) begin
            if (rst) begin
                data <= 8'b0;
            end else begin
                data <= data + 1;
            end
        end

    endmodule
    """

    tree = parse_verilog_code(verilog_code)
    traverse_tree(tree.root_node)

