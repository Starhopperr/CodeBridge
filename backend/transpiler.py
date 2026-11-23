"""
transpiler.py — Robust multi-language code transpiler for CodeBridge.
Translates code cleanly between Python, Java, and C++ (all 6 directions),
ensuring translations include proper entry points (public class Main, int main(), if __name__ == '__main__')
and accurate semantics.
"""
from __future__ import annotations

import ast
import re
from typing import List, Set, Tuple


# ===========================================================================
# 1. Python -> Java Transpiler
# ===========================================================================

class PythonToJavaTranspiler(ast.NodeVisitor):
    def __init__(self):
        self.indent_level = 1
        self.declared_vars: Set[str] = set()
        self.has_math = False
        self.has_arrays = False
        self.functions: List[str] = []

    def indent(self) -> str:
        return "    " * self.indent_level

    def is_main_guard(self, node: ast.AST) -> bool:
        if not isinstance(node, ast.If):
            return False
        if isinstance(node.test, ast.Compare):
            left_str = ast.unparse(node.test.left) if hasattr(ast, "unparse") else ""
            if "__name__" in left_str:
                return True
        return False

    def transpile(self, source_code: str) -> str:
        try:
            tree = ast.parse(source_code)
        except SyntaxError as e:
            return f"// Syntax Error in source Python code at line {e.lineno}:\n// {e.msg}\n// Please correct the syntax."

        func_nodes = []
        top_level_nodes = []
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                func_nodes.append(node)
            elif self.is_main_guard(node):
                top_level_nodes.extend(node.body)
            else:
                top_level_nodes.append(node)

        body_lines: List[str] = []

        # 1. Helper functions & classes
        for node in func_nodes:
            if isinstance(node, ast.FunctionDef):
                self.functions.append(node.name)
                func_code = self.visit_function(node)
                body_lines.append(func_code)
            elif isinstance(node, ast.ClassDef):
                class_code = self.visit_class(node)
                body_lines.append(class_code)

        # 2. Main method (standard Java entry point)
        main_lines = ["    public static void main(String[] args) {"]
        self.indent_level = 2
        self.declared_vars = set()
        if top_level_nodes:
            for node in top_level_nodes:
                line = self.visit_statement(node)
                if line:
                    main_lines.append(self.indent() + line)
        else:
            main_lines.append(self.indent() + "// Entry point")
        self.indent_level = 1
        main_lines.append("    }")

        body_lines.append("\n".join(main_lines))

        imports = ["import java.util.*;"]
        if self.has_math:
            imports.append("import java.lang.Math;")

        out = "\n".join(imports) + "\n\npublic class Main {\n"
        out += "\n\n".join(body_lines)
        out += "\n}\n"
        return out

    def infer_type(self, arg_node: ast.arg, func_body: List[ast.AST]) -> str:
        if arg_node.annotation:
            ann_str = ast.unparse(arg_node.annotation).lower() if hasattr(ast, "unparse") else ""
            if "int" in ann_str and "list" not in ann_str:
                return "int"
            elif "str" in ann_str:
                return "String"
            elif "bool" in ann_str:
                return "boolean"
            elif "float" in ann_str:
                return "double"
            elif "list" in ann_str or "[]" in ann_str:
                return "int[]"

        arg_name = arg_node.arg
        for node in func_body:
            for sub in ast.walk(node):
                if isinstance(sub, ast.Subscript) and isinstance(sub.value, ast.Name) and sub.value.id == arg_name:
                    return "int[]"
                if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name) and sub.func.id == "len":
                    if sub.args and isinstance(sub.args[0], ast.Name) and sub.args[0].id == arg_name:
                        return "int[]"
                if isinstance(sub, ast.For) and isinstance(sub.iter, ast.Name) and sub.iter.id == arg_name:
                    return "int[]"
        return "int"

    def visit_function(self, node: ast.FunctionDef) -> str:
        self.declared_vars = set()
        param_list = []
        for arg in node.args.args:
            t = self.infer_type(arg, node.body)
            param_list.append(f"{t} {arg.arg}")
            self.declared_vars.add(arg.arg)

        args_str = ", ".join(param_list)
        ret_type = "int"

        has_return = False
        for n in ast.walk(node):
            if isinstance(n, ast.Return):
                has_return = True
                if n.value:
                    if isinstance(n.value, ast.Constant):
                        if isinstance(n.value.value, bool):
                            ret_type = "boolean"
                        elif isinstance(n.value.value, str):
                            ret_type = "String"
                        elif isinstance(n.value.value, float):
                            ret_type = "double"
                    elif isinstance(n.value, ast.Compare):
                        ret_type = "boolean"
                    elif isinstance(n.value, ast.List):
                        ret_type = "int[]"

        if not has_return:
            ret_type = "void"

        func_lines = [f"    public static {ret_type} {node.name}({args_str}) {{"]
        self.indent_level = 2
        for stmt in node.body:
            code = self.visit_statement(stmt)
            if code:
                func_lines.append(self.indent() + code)
        self.indent_level = 1
        func_lines.append("    }")
        return "\n".join(func_lines)

    def visit_class(self, node: ast.ClassDef) -> str:
        class_lines = [f"    public static class {node.name} {{"]
        self.indent_level = 2
        for stmt in node.body:
            if isinstance(stmt, ast.FunctionDef):
                class_lines.append(self.visit_function(stmt))
        self.indent_level = 1
        class_lines.append("    }")
        return "\n".join(class_lines)

    def visit_statement(self, node: ast.AST) -> str:
        if isinstance(node, ast.Return):
            if node.value:
                return f"return {self.visit_expr(node.value)};"
            return "return;"
        elif isinstance(node, ast.Assign):
            target = self.visit_expr(node.targets[0])
            val = self.visit_expr(node.value)
            if target in self.declared_vars:
                return f"{target} = {val};"
            else:
                self.declared_vars.add(target)
                var_type = "int"
                if isinstance(node.value, ast.Constant):
                    if isinstance(node.value.value, str):
                        var_type = "String"
                    elif isinstance(node.value.value, bool):
                        var_type = "boolean"
                    elif isinstance(node.value.value, float):
                        var_type = "double"
                elif isinstance(node.value, ast.Compare):
                    var_type = "boolean"
                elif isinstance(node.value, ast.List):
                    var_type = "int[]"
                return f"{var_type} {target} = {val};"
        elif isinstance(node, ast.If):
            test = self.visit_expr(node.test)
            lines = [f"if ({test}) {{"]
            self.indent_level += 1
            for s in node.body:
                lines.append(self.indent() + self.visit_statement(s))
            self.indent_level -= 1
            if node.orelse:
                if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
                    lines.append(self.indent() + "} else " + self.visit_statement(node.orelse[0]))
                else:
                    lines.append(self.indent() + "} else {")
                    self.indent_level += 1
                    for s in node.orelse:
                        lines.append(self.indent() + self.visit_statement(s))
                    self.indent_level -= 1
                    lines.append(self.indent() + "}")
            else:
                lines.append(self.indent() + "}")
            return "\n".join(lines)
        elif isinstance(node, ast.For):
            target = self.visit_expr(node.target)
            self.declared_vars.add(target)
            if isinstance(node.iter, ast.Call) and getattr(node.iter.func, "id", None) == "range":
                r_args = node.iter.args
                if len(r_args) == 1:
                    stop = self.visit_expr(r_args[0])
                    header = f"for (int {target} = 0; {target} < {stop}; {target}++) {{"
                elif len(r_args) == 2:
                    start = self.visit_expr(r_args[0])
                    stop = self.visit_expr(r_args[1])
                    header = f"for (int {target} = {start}; {target} < {stop}; {target}++) {{"
                else:
                    start = self.visit_expr(r_args[0])
                    stop = self.visit_expr(r_args[1])
                    step = self.visit_expr(r_args[2])
                    header = f"for (int {target} = {start}; {target} < {stop}; {target} += {step}) {{"
            else:
                iter_expr = self.visit_expr(node.iter)
                header = f"for (int {target} : {iter_expr}) {{"

            lines = [header]
            self.indent_level += 1
            for s in node.body:
                lines.append(self.indent() + self.visit_statement(s))
            self.indent_level -= 1
            lines.append(self.indent() + "}")
            return "\n".join(lines)
        elif isinstance(node, ast.While):
            test = self.visit_expr(node.test)
            lines = [f"while ({test}) {{"]
            self.indent_level += 1
            for s in node.body:
                lines.append(self.indent() + self.visit_statement(s))
            self.indent_level -= 1
            lines.append(self.indent() + "}")
            return "\n".join(lines)
        elif isinstance(node, ast.Raise):
            if node.exc:
                if isinstance(node.exc, ast.Call):
                    exc_name = self.visit_expr(node.exc.func)
                    arg_str = self.visit_expr(node.exc.args[0]) if node.exc.args else '""'
                    if "ValueError" in exc_name or "TypeError" in exc_name:
                        return f"throw new IllegalArgumentException({arg_str});"
                    elif "ZeroDivisionError" in exc_name:
                        return f"throw new ArithmeticException({arg_str});"
                    return f"throw new RuntimeException({arg_str});"
            return "throw new RuntimeException();"
        elif isinstance(node, ast.Expr):
            return f"{self.visit_expr(node.value)};"
        return f"// Unsupported statement: {type(node).__name__}"

    def visit_expr(self, node: ast.AST) -> str:
        if isinstance(node, ast.Constant):
            if isinstance(node.value, bool):
                return "true" if node.value else "false"
            elif isinstance(node.value, str):
                return f'"{node.value}"'
            elif node.value is None:
                return "null"
            return str(node.value)
        elif isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Subscript):
            val = self.visit_expr(node.value)
            idx = self.visit_expr(node.slice)
            return f"{val}[{idx}]"
        elif isinstance(node, ast.BinOp):
            left = self.visit_expr(node.left)
            right = self.visit_expr(node.right)
            if isinstance(node.op, ast.FloorDiv):
                self.has_math = True
                return f"Math.floorDiv({left}, {right})"
            elif isinstance(node.op, ast.Pow):
                self.has_math = True
                return f"(int)Math.pow({left}, {right})"
            op_map = {
                ast.Add: "+", ast.Sub: "-", ast.Mult: "*",
                ast.Div: "/", ast.Mod: "%"
            }
            op_str = op_map.get(type(node.op), "+")
            return f"({left} {op_str} {right})"
        elif isinstance(node, ast.UnaryOp):
            operand = self.visit_expr(node.operand)
            if isinstance(node.op, ast.Not):
                return f"!({operand})"
            elif isinstance(node.op, ast.USub):
                return f"-{operand}"
            return operand
        elif isinstance(node, ast.Compare):
            left = self.visit_expr(node.left)
            cmp_ops = {
                ast.Eq: "==", ast.NotEq: "!=", ast.Lt: "<",
                ast.LtE: "<=", ast.Gt: ">", ast.GtE: ">="
            }
            right = self.visit_expr(node.comparators[0])
            op_str = cmp_ops.get(type(node.ops[0]), "==")
            return f"({left} {op_str} {right})"
        elif isinstance(node, ast.BoolOp):
            op_str = " && " if isinstance(node.op, ast.And) else " || "
            return f"({op_str.join(self.visit_expr(v) for v in node.values)})"
        elif isinstance(node, ast.Call):
            func = self.visit_expr(node.func)
            args = ", ".join(self.visit_expr(a) for a in node.args)
            if func == "print":
                return f"System.out.println({args})"
            elif func == "len":
                return f"{args}.length"
            elif func == "max":
                self.has_math = True
                return f"Math.max({args})"
            elif func == "min":
                self.has_math = True
                return f"Math.min({args})"
            elif func == "abs":
                self.has_math = True
                return f"Math.abs({args})"
            return f"{func}({args})"
        elif isinstance(node, ast.List):
            self.has_arrays = True
            elements = ", ".join(self.visit_expr(e) for e in node.elts)
            return f"new int[]{{{elements}}}"
        return ""


# ===========================================================================
# 2. Python -> C++ Transpiler
# ===========================================================================

class PythonToCppTranspiler(ast.NodeVisitor):
    def __init__(self):
        self.indent_level = 0
        self.declared_vars: Set[str] = set()
        self.has_cmath = False
        self.has_vector = False
        self.has_iostream = False
        self.has_string = False

    def indent(self) -> str:
        return "    " * self.indent_level

    def is_main_guard(self, node: ast.AST) -> bool:
        if not isinstance(node, ast.If):
            return False
        if isinstance(node.test, ast.Compare):
            left_str = ast.unparse(node.test.left) if hasattr(ast, "unparse") else ""
            if "__name__" in left_str:
                return True
        return False

    def transpile(self, source_code: str) -> str:
        try:
            tree = ast.parse(source_code)
        except SyntaxError as e:
            return f"// Syntax Error in source Python code at line {e.lineno}:\n// {e.msg}\n// Please correct the syntax."

        func_nodes = []
        top_level_nodes = []
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                func_nodes.append(node)
            elif self.is_main_guard(node):
                top_level_nodes.extend(node.body)
            else:
                top_level_nodes.append(node)

        body_lines: List[str] = []
        for node in func_nodes:
            if isinstance(node, ast.FunctionDef):
                func_code = self.visit_function(node)
                body_lines.append(func_code)

        # Standard C++ int main() entry point
        main_lines = ["int main() {"]
        self.indent_level = 1
        self.declared_vars = set()
        if top_level_nodes:
            for node in top_level_nodes:
                line = self.visit_statement(node)
                if line:
                    main_lines.append(self.indent() + line)
        main_lines.append(self.indent() + "return 0;")
        self.indent_level = 0
        main_lines.append("}")

        body_lines.append("\n".join(main_lines))

        includes = []
        # Check if print or top-level output is used
        has_print = any(isinstance(n, ast.Call) and getattr(n.func, "id", "") == "print" for n in ast.walk(tree))
        if self.has_iostream or has_print:
            includes.append("#include <iostream>")
        if self.has_vector:
            includes.append("#include <vector>")
        if self.has_string:
            includes.append("#include <string>")
        if self.has_cmath:
            includes.append("#include <cmath>")
        includes.append("#include <stdexcept>")

        header = "\n".join(includes) + "\n\n" if includes else ""
        return header + "\n\n".join(body_lines) + "\n"

    def infer_type(self, arg_node: ast.arg, func_body: List[ast.AST]) -> str:
        if arg_node.annotation:
            ann_str = ast.unparse(arg_node.annotation).lower() if hasattr(ast, "unparse") else ""
            if "int" in ann_str and "list" not in ann_str:
                return "int"
            elif "str" in ann_str:
                self.has_string = True
                return "const std::string&"
            elif "bool" in ann_str:
                return "bool"
            elif "float" in ann_str:
                return "double"
            elif "list" in ann_str:
                self.has_vector = True
                return "const std::vector<int>&"

        arg_name = arg_node.arg
        for node in func_body:
            for sub in ast.walk(node):
                if isinstance(sub, ast.Subscript) and isinstance(sub.value, ast.Name) and sub.value.id == arg_name:
                    self.has_vector = True
                    return "const std::vector<int>&"
                if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name) and sub.func.id == "len":
                    if sub.args and isinstance(sub.args[0], ast.Name) and sub.args[0].id == arg_name:
                        self.has_vector = True
                        return "const std::vector<int>&"
                if isinstance(sub, ast.For) and isinstance(sub.iter, ast.Name) and sub.iter.id == arg_name:
                    self.has_vector = True
                    return "const std::vector<int>&"
        return "int"

    def visit_function(self, node: ast.FunctionDef) -> str:
        self.declared_vars = set()
        param_list = []
        for arg in node.args.args:
            t = self.infer_type(arg, node.body)
            param_list.append(f"{t} {arg.arg}")
            self.declared_vars.add(arg.arg)

        args_str = ", ".join(param_list)
        ret_type = "int"
        has_return = False
        for n in ast.walk(node):
            if isinstance(n, ast.Return):
                has_return = True
                if n.value:
                    if isinstance(n.value, ast.Constant):
                        if isinstance(n.value.value, bool):
                            ret_type = "bool"
                        elif isinstance(n.value.value, str):
                            self.has_string = True
                            ret_type = "std::string"
                        elif isinstance(n.value.value, float):
                            ret_type = "double"
                    elif isinstance(n.value, ast.Compare):
                        ret_type = "bool"
                    elif isinstance(n.value, ast.List):
                        self.has_vector = True
                        ret_type = "std::vector<int>"

        if not has_return:
            ret_type = "void"

        lines = [f"{ret_type} {node.name}({args_str}) {{"]
        self.indent_level = 1
        for stmt in node.body:
            code = self.visit_statement(stmt)
            if code:
                lines.append(self.indent() + code)
        self.indent_level = 0
        lines.append("}")
        return "\n".join(lines)

    def visit_statement(self, node: ast.AST) -> str:
        if isinstance(node, ast.Return):
            if node.value:
                return f"return {self.visit_expr(node.value)};"
            return "return;"
        elif isinstance(node, ast.Assign):
            target = self.visit_expr(node.targets[0])
            val = self.visit_expr(node.value)
            if target in self.declared_vars:
                return f"{target} = {val};"
            else:
                self.declared_vars.add(target)
                return f"auto {target} = {val};"
        elif isinstance(node, ast.If):
            test = self.visit_expr(node.test)
            lines = [f"if ({test}) {{"]
            self.indent_level += 1
            for s in node.body:
                lines.append(self.indent() + self.visit_statement(s))
            self.indent_level -= 1
            if node.orelse:
                if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
                    lines.append(self.indent() + "} else " + self.visit_statement(node.orelse[0]))
                else:
                    lines.append(self.indent() + "} else {")
                    self.indent_level += 1
                    for s in node.orelse:
                        lines.append(self.indent() + self.visit_statement(s))
                    self.indent_level -= 1
                    lines.append(self.indent() + "}")
            else:
                lines.append(self.indent() + "}")
            return "\n".join(lines)
        elif isinstance(node, ast.For):
            target = self.visit_expr(node.target)
            self.declared_vars.add(target)
            if isinstance(node.iter, ast.Call) and getattr(node.iter.func, "id", None) == "range":
                r_args = node.iter.args
                if len(r_args) == 1:
                    stop = self.visit_expr(r_args[0])
                    header = f"for (int {target} = 0; {target} < {stop}; {target}++) {{"
                elif len(r_args) == 2:
                    start = self.visit_expr(r_args[0])
                    stop = self.visit_expr(r_args[1])
                    header = f"for (int {target} = {start}; {target} < {stop}; {target}++) {{"
                else:
                    start = self.visit_expr(r_args[0])
                    stop = self.visit_expr(r_args[1])
                    step = self.visit_expr(r_args[2])
                    header = f"for (int {target} = {start}; {target} < {stop}; {target} += {step}) {{"
            else:
                iter_expr = self.visit_expr(node.iter)
                header = f"for (const auto& {target} : {iter_expr}) {{"

            lines = [header]
            self.indent_level += 1
            for s in node.body:
                lines.append(self.indent() + self.visit_statement(s))
            self.indent_level -= 1
            lines.append(self.indent() + "}")
            return "\n".join(lines)
        elif isinstance(node, ast.While):
            test = self.visit_expr(node.test)
            lines = [f"while ({test}) {{"]
            self.indent_level += 1
            for s in node.body:
                lines.append(self.indent() + self.visit_statement(s))
            self.indent_level -= 1
            lines.append(self.indent() + "}")
            return "\n".join(lines)
        elif isinstance(node, ast.Raise):
            if node.exc and isinstance(node.exc, ast.Call):
                arg_str = self.visit_expr(node.exc.args[0]) if node.exc.args else '""'
                return f"throw std::invalid_argument({arg_str});"
            return 'throw std::runtime_error("Error");'
        elif isinstance(node, ast.Expr):
            return f"{self.visit_expr(node.value)};"
        return f"// Unsupported: {type(node).__name__}"

    def visit_expr(self, node: ast.AST) -> str:
        if isinstance(node, ast.Constant):
            if isinstance(node.value, bool):
                return "true" if node.value else "false"
            elif isinstance(node.value, str):
                self.has_string = True
                return f'"{node.value}"'
            elif node.value is None:
                return "nullptr"
            return str(node.value)
        elif isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Subscript):
            val = self.visit_expr(node.value)
            idx = self.visit_expr(node.slice)
            return f"{val}[{idx}]"
        elif isinstance(node, ast.BinOp):
            left = self.visit_expr(node.left)
            right = self.visit_expr(node.right)
            if isinstance(node.op, ast.FloorDiv):
                self.has_cmath = True
                return f"static_cast<int>(std::floor(static_cast<double>({left}) / ({right})))"
            elif isinstance(node.op, ast.Pow):
                self.has_cmath = True
                return f"static_cast<int>(std::pow({left}, {right}))"
            op_map = {
                ast.Add: "+", ast.Sub: "-", ast.Mult: "*",
                ast.Div: "/", ast.Mod: "%"
            }
            op_str = op_map.get(type(node.op), "+")
            return f"({left} {op_str} {right})"
        elif isinstance(node, ast.UnaryOp):
            operand = self.visit_expr(node.operand)
            if isinstance(node.op, ast.Not):
                return f"!({operand})"
            elif isinstance(node.op, ast.USub):
                return f"-{operand}"
            return operand
        elif isinstance(node, ast.Compare):
            left = self.visit_expr(node.left)
            cmp_ops = {
                ast.Eq: "==", ast.NotEq: "!=", ast.Lt: "<",
                ast.LtE: "<=", ast.Gt: ">", ast.GtE: ">="
            }
            right = self.visit_expr(node.comparators[0])
            op_str = cmp_ops.get(type(node.ops[0]), "==")
            return f"({left} {op_str} {right})"
        elif isinstance(node, ast.BoolOp):
            op_str = " && " if isinstance(node.op, ast.And) else " || "
            return f"({op_str.join(self.visit_expr(v) for v in node.values)})"
        elif isinstance(node, ast.Call):
            func = self.visit_expr(node.func)
            args = ", ".join(self.visit_expr(a) for a in node.args)
            if func == "print":
                self.has_iostream = True
                return f"std::cout << {args} << std::endl"
            elif func == "len":
                return f"{args}.size()"
            elif func == "max":
                return f"std::max({args})"
            elif func == "min":
                return f"std::min({args})"
            elif func == "abs":
                return f"std::abs({args})"
            return f"{func}({args})"
        elif isinstance(node, ast.List):
            self.has_vector = True
            elements = ", ".join(self.visit_expr(e) for e in node.elts)
            return f"std::vector<int>{{{elements}}}"
        return ""


# ===========================================================================
# 3. Java / C++ -> Python Transpiler
# ===========================================================================

def clean_c_expr(expr: str) -> str:
    expr = re.sub(r"&&", " and ", expr)
    expr = re.sub(r"\|\|", " or ", expr)
    expr = re.sub(r"!([A-Za-z0-9_]+)", r"not \1", expr)
    expr = re.sub(r"\btrue\b", "True", expr)
    expr = re.sub(r"\bfalse\b", "False", expr)
    expr = re.sub(r"\b(?:null|nullptr|NULL)\b", "None", expr)
    expr = re.sub(r"([A-Za-z0-9_]+)\.length\b", r"len(\1)", expr)
    expr = re.sub(r"([A-Za-z0-9_]+)\.size\(\)", r"len(\1)", expr)
    expr = re.sub(r"Math\.max\(([^,]+),\s*([^)]+)\)", r"max(\1, \2)", expr)
    expr = re.sub(r"std::max\(([^,]+),\s*([^)]+)\)", r"max(\1, \2)", expr)
    expr = re.sub(r"Math\.min\(([^,]+),\s*([^)]+)\)", r"min(\1, \2)", expr)
    expr = re.sub(r"std::min\(([^,]+),\s*([^)]+)\)", r"min(\1, \2)", expr)
    expr = re.sub(r"Math\.abs\(([^)]+)\)", r"abs(\1)", expr)
    expr = re.sub(r"std::abs\(([^)]+)\)", r"abs(\1)", expr)
    expr = re.sub(r"Math\.floorDiv\(([^,]+),\s*([^)]+)\)", r"\1 // \2", expr)
    expr = re.sub(r"\s+", " ", expr).strip()
    return expr


def java_or_cpp_to_python(code: str) -> str:
    lines = code.splitlines()
    out_lines: List[str] = []
    main_lines: List[str] = []
    indent_level = 0
    in_main = False
    main_indent = 1

    def indent(lvl=None) -> str:
        cur = indent_level if lvl is None else lvl
        return "    " * cur

    i = 0
    while i < len(lines):
        raw_line = lines[i].strip()
        i += 1

        if not raw_line:
            continue

        if raw_line.startswith(("//", "/*", "*", "import ", "package ", "#include ", "using namespace")):
            continue

        if raw_line == "}":
            if in_main:
                in_main = False
            elif indent_level > 0:
                indent_level -= 1
            continue
        elif raw_line.startswith("}"):
            if in_main:
                in_main = False
            elif indent_level > 0:
                indent_level -= 1
            raw_line = raw_line[1:].strip()

        # Class declaration
        m_class = re.match(r"(?:public\s+|private\s+|protected\s+)?class\s+([A-Za-z0-9_]+)", raw_line)
        if m_class:
            class_name = m_class.group(1)
            if class_name.lower() in ("solution", "main"):
                pass
            else:
                out_lines.append(f"{indent()}class {class_name}:")
                indent_level += 1
            continue

        # Function header
        m_func = re.match(
            r"(?:(?:public|private|protected|static|final|inline|virtual)\s+)*([A-Za-z0-9_<>:&*]+)\s+([A-Za-z0-9_]+)\s*\((.*?)\)\s*\{?",
            raw_line,
        )
        if m_func and not raw_line.startswith(("if", "for", "while", "catch", "switch", "return")):
            func_name = m_func.group(2)
            raw_params = m_func.group(3).strip()

            if func_name == "main":
                in_main = True
                continue

            clean_params = []
            if raw_params:
                for p in raw_params.split(","):
                    p = p.strip()
                    if not p:
                        continue
                    p = re.sub(r"\b(const|final)\b", "", p)
                    p = re.sub(r"[&*]", "", p).strip()
                    tokens = p.split()
                    if tokens:
                        clean_params.append(tokens[-1])

            out_lines.append(f"{indent()}def {func_name}({', '.join(clean_params)}):")
            indent_level += 1
            continue

        target_list = main_lines if in_main else out_lines
        curr_lvl = main_indent if in_main else indent_level

        # Skip return 0; in main
        if in_main and raw_line.startswith("return 0"):
            continue

        # For loop: range
        m_for_range = re.match(
            r"for\s*\(\s*(?:int|size_t|auto)\s+([A-Za-z0-9_]+)\s*=\s*([^;]+);\s*\1\s*(<|<=)\s*([^;]+);\s*(?:\+\+\1|\1\+\+|\1\s*\+=\s*([^;)]+))\s*\)\s*\{?",
            raw_line,
        )
        if m_for_range:
            var_name = m_for_range.group(1)
            start_val = m_for_range.group(2).strip()
            op = m_for_range.group(3).strip()
            stop_val = m_for_range.group(4).strip()
            step = m_for_range.group(5)

            stop_val = re.sub(r"([A-Za-z0-9_]+)\.length\b", r"len(\1)", stop_val)
            stop_val = re.sub(r"([A-Za-z0-9_]+)\.size\(\)", r"len(\1)", stop_val)

            if op == "<=":
                stop_val = f"{stop_val} + 1"

            if start_val == "0" and not step:
                target_list.append(f"{indent(curr_lvl)}for {var_name} in range({stop_val}):")
            elif step:
                target_list.append(f"{indent(curr_lvl)}for {var_name} in range({start_val}, {stop_val}, {step}):")
            else:
                target_list.append(f"{indent(curr_lvl)}for {var_name} in range({start_val}, {stop_val}):")
            if in_main:
                main_indent += 1
            else:
                indent_level += 1
            continue

        # For loop: foreach
        m_for_each = re.match(r"for\s*\(\s*(?:[^:]+)\s+([A-Za-z0-9_]+)\s*:\s*([^)]+)\)\s*\{?", raw_line)
        if m_for_each:
            var_name = m_for_each.group(1)
            iterable = m_for_each.group(2).strip()
            target_list.append(f"{indent(curr_lvl)}for {var_name} in {iterable}:")
            if in_main:
                main_indent += 1
            else:
                indent_level += 1
            continue

        # While loop
        m_while = re.match(r"while\s*\((.*)\)\s*\{?", raw_line)
        if m_while:
            cond = clean_c_expr(m_while.group(1).strip())
            target_list.append(f"{indent(curr_lvl)}while {cond}:")
            if in_main:
                main_indent += 1
            else:
                indent_level += 1
            continue

        # If / Elif / Else
        if raw_line.startswith("else if") or raw_line.startswith("elif"):
            m_elif = re.match(r"(?:else if|elif)\s*\((.*)\)\s*\{?", raw_line)
            if m_elif:
                cond = clean_c_expr(m_elif.group(1).strip())
                target_list.append(f"{indent(curr_lvl)}elif {cond}:")
                continue
        elif raw_line.startswith("if"):
            m_if = re.match(r"if\s*\((.*)\)\s*\{?", raw_line)
            if m_if:
                cond = clean_c_expr(m_if.group(1).strip())
                target_list.append(f"{indent(curr_lvl)}if {cond}:")
                if in_main:
                    main_indent += 1
                else:
                    indent_level += 1
                continue
        elif raw_line.startswith("else"):
            target_list.append(f"{indent(curr_lvl)}else:")
            continue

        # Throw / raise
        m_throw = re.match(r"throw\s+(?:new\s+)?[A-Za-z0-9_:]+\s*\((.*)\);?", raw_line)
        if m_throw:
            msg = m_throw.group(1).strip()
            target_list.append(f"{indent(curr_lvl)}raise ValueError({msg})")
            continue

        # Return
        m_ret = re.match(r"return(?:\s+(.*))?;?", raw_line)
        if m_ret:
            expr = m_ret.group(1)
            if expr:
                expr = clean_c_expr(expr.rstrip(";").strip())
                target_list.append(f"{indent(curr_lvl)}return {expr}")
            else:
                target_list.append(f"{indent(curr_lvl)}return")
            continue

        # Print / println / cout
        m_sysout = re.match(r"System\.out\.println\((.*)\);?", raw_line)
        if m_sysout:
            arg = clean_c_expr(m_sysout.group(1).rstrip(";").strip())
            target_list.append(f"{indent(curr_lvl)}print({arg})")
            continue
        if "cout" in raw_line:
            line_cout = raw_line.replace("std::cout", "").replace("cout", "")
            parts = [
                p.strip()
                for p in line_cout.split("<<")
                if p.strip() and p.strip() not in ("std::endl;", "endl;", ";", "std::endl", "endl")
            ]
            arg = ", ".join(clean_c_expr(p) for p in parts)
            target_list.append(f"{indent(curr_lvl)}print({arg})")
            continue

        # Assignment / expression
        stmt = raw_line.rstrip(";").rstrip("{").strip()
        stmt = re.sub(
            r"^(?:const\s+)?(?:int|long|float|double|boolean|bool|String|std::string|auto|char|size_t|void|vector<[^>]+>|std::vector<[^>]+>|List<[^>]+>|ArrayList<[^>]+>|int\[\]|String\[\])\s+",
            "",
            stmt,
        ).strip()
        stmt = clean_c_expr(stmt)
        if stmt:
            target_list.append(f"{indent(curr_lvl)}{stmt}")

    full_output = []
    if out_lines:
        full_output.append("\n".join(out_lines))
    if main_lines:
        full_output.append('if __name__ == "__main__":\n' + "\n".join(main_lines))

    return "\n\n".join(full_output) if full_output else "# Translated code"


# ===========================================================================
# 4. Java <-> C++ Transpilers
# ===========================================================================

def java_to_cpp(code: str) -> str:
    out = code
    out = re.sub(r"import\s+[^;]+;\s*", "", out)
    out = re.sub(r"package\s+[^;]+;\s*", "", out)

    has_java_main = bool(re.search(r"\bvoid\s+main\s*\(", out))

    # Strip class header and closing brace
    out = re.sub(r"(?:public\s+)?class\s+[A-Za-z0-9_]+\s*\{", "", out)
    lines = out.splitlines()
    clean_lines = []
    found_last_brace = False
    for l in reversed(lines):
        if not found_last_brace and l.strip() == "}":
            found_last_brace = True
            continue
        clean_lines.append(l)
    out = "\n".join(reversed(clean_lines))

    # Convert Java main method to int main()
    out = re.sub(r"\b(?:public\s+)?(?:static\s+)?void\s+main\s*\([^)]*\)\s*\{", "int main() {", out)
    out = re.sub(r"\bpublic\s+static\s+", "", out)
    out = re.sub(r"\bpublic\s+", "", out)
    out = re.sub(r"System\.out\.println\((.*?)\);", r"std::cout << \1 << std::endl;", out)
    out = re.sub(r"System\.out\.print\((.*?)\);", r"std::cout << \1;", out)
    out = re.sub(r"\bString\b", "std::string", out)
    out = re.sub(r"\bboolean\b", "bool", out)
    out = re.sub(r"\bnull\b", "nullptr", out)
    out = re.sub(r"int\[\]\s+([A-Za-z0-9_]+)", r"std::vector<int>& \1", out)
    out = re.sub(r"ArrayList<Integer>", "std::vector<int>", out)
    out = re.sub(r"List<Integer>", "std::vector<int>", out)
    out = re.sub(r"throw\s+new\s+IllegalArgumentException\((.*?)\);", r"throw std::invalid_argument(\1);", out)
    out = re.sub(r"Math\.floorDiv\(([^,]+),\s*([^)]+)\)", r"static_cast<int>(std::floor(static_cast<double>(\1) / (\2)))", out)
    out = re.sub(r"Math\.max\(", "std::max(", out)
    out = re.sub(r"Math\.min\(", "std::min(", out)
    out = re.sub(r"Math\.abs\(", "std::abs(", out)
    out = re.sub(r"([A-Za-z0-9_]+)\.length\b", r"\1.size()", out)

    headers = [
        "#include <iostream>",
        "#include <vector>",
        "#include <string>",
        "#include <cmath>",
        "#include <stdexcept>",
    ]

    if not has_java_main:
        out = out.strip() + "\n\nint main() {\n    return 0;\n}"

    return "\n".join(headers) + "\n\n" + out.strip() + "\n"


def cpp_to_java(code: str) -> str:
    lines = code.splitlines()
    clean_lines = []
    for l in lines:
        if l.strip().startswith(("#include", "using namespace")):
            continue
        clean_lines.append(l)
    out = "\n".join(clean_lines).strip()

    has_cpp_main = bool(re.search(r"\bint\s+main\s*\(", out))

    out = re.sub(r"std::cout\s*<<\s*(.*?)\s*<<\s*std::endl;", r"System.out.println(\1);", out)
    out = re.sub(r"std::string", "String", out)
    out = re.sub(r"\bbool\b", "boolean", out)
    out = re.sub(r"\bnullptr\b", "null", out)
    out = re.sub(r"std::vector<int>&?", "int[]", out)
    out = re.sub(r"throw\s+std::invalid_argument\((.*?)\);", r"throw new IllegalArgumentException(\1);", out)
    out = re.sub(r"std::max\(", "Math.max(", out)
    out = re.sub(r"std::min\(", "Math.min(", out)
    out = re.sub(r"std::abs\(", "Math.abs(", out)
    out = re.sub(r"([A-Za-z0-9_]+)\.size\(\)", r"\1.length", out)

    # Convert int main() to public static void main(String[] args)
    out = re.sub(r"\bint\s+main\s*\([^)]*\)\s*\{", "public static void main(String[] args) {", out)
    out = re.sub(r"return\s+0;\s*", "", out)

    # Polish method headers: remove const and &, add public static
    polished_lines = []
    for l in out.splitlines():
        if re.search(r"\b(int|void|String|boolean|double)\s+[A-Za-z0-9_]+\s*\(", l):
            l = re.sub(r"const\s+", "", l)
            l = re.sub(r"&", "", l)
            if not l.strip().startswith(("public", "private", "protected")):
                l = "    public static " + l.strip()
            else:
                l = "    " + l.strip()
        else:
            if l.strip():
                l = "    " + l.strip()
        polished_lines.append(l)
    out = "\n".join(polished_lines)

    if not has_cpp_main:
        out = out + "\n\n    public static void main(String[] args) {\n        // Entry point\n    }"

    return f"import java.util.*;\n\npublic class Main {{\n{out}\n}}\n"


# ===========================================================================
# Master Translation Dispatcher
# ===========================================================================

def translate_code(source_code: str, source_language: str, target_language: str) -> Tuple[str, List[str], List[str]]:
    """
    Translates code between Python, Java, and C++ (all 6 combinations).
    Guarantees standard execution entry points: public class Main with main(String[] args) in Java,
    int main() in C++, and if __name__ == '__main__': in Python.
    """
    src = source_language.strip().lower()
    tgt = target_language.strip().lower()
    code = source_code.strip()

    if src == tgt:
        return code, ["Source and target languages are identical."], []

    # 1. Python -> Java
    if src == "python" and tgt == "java":
        transpiler = PythonToJavaTranspiler()
        res = transpiler.transpile(code)
        diffs = [
            "Generated standard executable entry point: public class Main with public static void main(String[] args).",
            "Python dynamic typing mapped to static Java types (int, String, boolean, int[]).",
            "Python floor division '//' converted to Math.floorDiv() for negative-safe semantics.",
            "Exceptions mapped from Python ValueError to Java IllegalArgumentException.",
        ]
        return res, diffs, ["Verify boundary integer limits (Java 32-bit vs Python arbitrary precision)."]

    # 2. Python -> C++
    if src == "python" and "c" in tgt:
        transpiler = PythonToCppTranspiler()
        res = transpiler.transpile(code)
        diffs = [
            "Generated standard C++ entry point: int main() { ... return 0; }.",
            "Python dynamic typing converted to static C++ types and std::vector.",
            "Python print() mapped to std::cout << ... << std::endl.",
            "Python floor division '//' converted to std::floor(static_cast<double>(a) / b).",
            "Exceptions mapped to std::invalid_argument.",
        ]
        return res, diffs, ["Verify 32-bit signed overflow conditions."]

    # 3. Java -> Python
    if src == "java" and tgt == "python":
        res = java_or_cpp_to_python(code)
        diffs = [
            "Java public class Main and main(String[] args) converted to Python if __name__ == '__main__': entry point.",
            "Primitive static types (int, boolean, String) converted to dynamic Python typing.",
            "Index loops converted to range(len(arr)).",
            "System.out.println() converted to print().",
        ]
        return res, diffs, ["Python integers have arbitrary precision."]

    # 4. C++ -> Python
    if "c" in src and tgt == "python":
        res = java_or_cpp_to_python(code)
        diffs = [
            "C++ int main() converted to Python if __name__ == '__main__': block.",
            "std::cout replaced with built-in print().",
            "std::vector converted to Python list idioms.",
            "throw std::invalid_argument replaced with raise ValueError().",
        ]
        return res, diffs, ["Zero manual memory allocation in Python."]

    # 5. Java -> C++
    if src == "java" and "c" in tgt:
        res = java_to_cpp(code)
        diffs = [
            "Java main(String[] args) mapped to C++ int main().",
            "Java System.out.println mapped to C++ std::cout.",
            "Java String and ArrayList mapped to std::string and std::vector.",
            "Math.floorDiv mapped to std::floor division.",
        ]
        return res, diffs, ["Verify C++ destructor and vector pass-by-reference semantics."]

    # 6. C++ -> Java
    if "c" in src and tgt == "java":
        res = cpp_to_java(code)
        diffs = [
            "C++ code encapsulated in public class Main with public static void main(String[] args).",
            "std::cout mapped to System.out.println.",
            "std::vector mapped to Java array / collections.",
        ]
        return res, diffs, ["Check for null reference handling in Java."]

    # Fallback default
    return f"// Unsupported language pair: {src} -> {tgt}\n" + code, [], []
