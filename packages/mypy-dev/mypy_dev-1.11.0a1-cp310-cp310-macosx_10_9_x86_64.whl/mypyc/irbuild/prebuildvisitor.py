from __future__ import annotations

from mypy.nodes import (
    Block,
    Decorator,
    Expression,
    FuncDef,
    FuncItem,
    Import,
    LambdaExpr,
    MemberExpr,
    MypyFile,
    NameExpr,
    Node,
    SymbolNode,
    Var,
)
from mypy.traverser import ExtendedTraverserVisitor
from mypyc.errors import Errors


class PreBuildVisitor(ExtendedTraverserVisitor):
    """Mypy file AST visitor run before building the IR.

    This collects various things, including:

    * Determine relationships between nested functions and functions that
      contain nested functions
    * Find non-local variables (free variables)
    * Find property setters
    * Find decorators of functions
    * Find module import groups

    The main IR build pass uses this information.
    """

    def __init__(
        self,
        errors: Errors,
        current_file: MypyFile,
        decorators_to_remove: dict[FuncDef, list[int]],
    ) -> None:
        super().__init__()
        # Dict from a function to symbols defined directly in the
        # function that are used as non-local (free) variables within a
        # nested function.
        self.free_variables: dict[FuncItem, set[SymbolNode]] = {}

        # Intermediate data structure used to find the function where
        # a SymbolNode is declared. Initially this may point to a
        # function nested inside the function with the declaration,
        # but we'll eventually update this to refer to the function
        # with the declaration.
        self.symbols_to_funcs: dict[SymbolNode, FuncItem] = {}

        # Stack representing current function nesting.
        self.funcs: list[FuncItem] = []

        # All property setters encountered so far.
        self.prop_setters: set[FuncDef] = set()

        # A map from any function that contains nested functions to
        # a set of all the functions that are nested within it.
        self.encapsulating_funcs: dict[FuncItem, list[FuncItem]] = {}

        # Map nested function to its parent/encapsulating function.
        self.nested_funcs: dict[FuncItem, FuncItem] = {}

        # Map function to its non-special decorators.
        self.funcs_to_decorators: dict[FuncDef, list[Expression]] = {}

        # Map function to indices of decorators to remove
        self.decorators_to_remove: dict[FuncDef, list[int]] = decorators_to_remove

        # A mapping of import groups (a series of Import nodes with
        # nothing inbetween) where each group is keyed by its first
        # import node.
        self.module_import_groups: dict[Import, list[Import]] = {}
        self._current_import_group: Import | None = None

        self.errors: Errors = errors

        self.current_file: MypyFile = current_file

    def visit(self, o: Node) -> bool:
        if not isinstance(o, Import):
            self._current_import_group = None
        return True

    def visit_block(self, block: Block) -> None:
        self._current_import_group = None
        super().visit_block(block)
        self._current_import_group = None

    def visit_decorator(self, dec: Decorator) -> None:
        if dec.decorators:
            # Only add the function being decorated if there exist
            # (ordinary) decorators in the decorator list. Certain
            # decorators (such as @property, @abstractmethod) are
            # special cased and removed from this list by
            # mypy. Functions decorated only by special decorators
            # (and property setters) are not treated as decorated
            # functions by the IR builder.
            if isinstance(dec.decorators[0], MemberExpr) and dec.decorators[0].name == "setter":
                # Property setters are not treated as decorated methods.
                self.prop_setters.add(dec.func)
            else:
                decorators_to_store = dec.decorators.copy()
                if dec.func in self.decorators_to_remove:
                    to_remove = self.decorators_to_remove[dec.func]

                    for i in reversed(to_remove):
                        del decorators_to_store[i]
                    # if all of the decorators are removed, we shouldn't treat this as a decorated
                    # function because there aren't any decorators to apply
                    if not decorators_to_store:
                        return

                self.funcs_to_decorators[dec.func] = decorators_to_store
        super().visit_decorator(dec)

    def visit_func_def(self, fdef: FuncDef) -> None:
        # TODO: What about overloaded functions?
        self.visit_func(fdef)
        self.visit_symbol_node(fdef)

    def visit_lambda_expr(self, expr: LambdaExpr) -> None:
        self.visit_func(expr)

    def visit_func(self, func: FuncItem) -> None:
        # If there were already functions or lambda expressions
        # defined in the function stack, then note the previous
        # FuncItem as containing a nested function and the current
        # FuncItem as being a nested function.
        if self.funcs:
            # Add the new func to the set of nested funcs within the
            # func at top of the func stack.
            self.encapsulating_funcs.setdefault(self.funcs[-1], []).append(func)
            # Add the func at top of the func stack as the parent of
            # new func.
            self.nested_funcs[func] = self.funcs[-1]

        self.funcs.append(func)
        super().visit_func(func)
        self.funcs.pop()

    def visit_import(self, imp: Import) -> None:
        if self._current_import_group is not None:
            self.module_import_groups[self._current_import_group].append(imp)
        else:
            self.module_import_groups[imp] = [imp]
            self._current_import_group = imp
        super().visit_import(imp)

    def visit_name_expr(self, expr: NameExpr) -> None:
        if isinstance(expr.node, (Var, FuncDef)):
            self.visit_symbol_node(expr.node)

    def visit_var(self, var: Var) -> None:
        self.visit_symbol_node(var)

    def visit_symbol_node(self, symbol: SymbolNode) -> None:
        if not self.funcs:
            # We are not inside a function and hence do not need to do
            # anything regarding free variables.
            return

        if symbol in self.symbols_to_funcs:
            orig_func = self.symbols_to_funcs[symbol]
            if self.is_parent(self.funcs[-1], orig_func):
                # The function in which the symbol was previously seen is
                # nested within the function currently being visited. Thus
                # the current function is a better candidate to contain the
                # declaration.
                self.symbols_to_funcs[symbol] = self.funcs[-1]
                # TODO: Remove from the orig_func free_variables set?
                self.free_variables.setdefault(self.funcs[-1], set()).add(symbol)

            elif self.is_parent(orig_func, self.funcs[-1]):
                # The SymbolNode instance has already been visited
                # before in a parent function, thus it's a non-local
                # symbol.
                self.add_free_variable(symbol)

        else:
            # This is the first time the SymbolNode is being
            # visited. We map the SymbolNode to the current FuncDef
            # being visited to note where it was first visited.
            self.symbols_to_funcs[symbol] = self.funcs[-1]

    def is_parent(self, fitem: FuncItem, child: FuncItem) -> bool:
        # Check if child is nested within fdef (possibly indirectly
        # within multiple nested functions).
        if child not in self.nested_funcs:
            return False
        parent = self.nested_funcs[child]
        return parent == fitem or self.is_parent(fitem, parent)

    def add_free_variable(self, symbol: SymbolNode) -> None:
        # Find the function where the symbol was (likely) first declared,
        # and mark is as a non-local symbol within that function.
        func = self.symbols_to_funcs[symbol]
        self.free_variables.setdefault(func, set()).add(symbol)
