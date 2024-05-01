"""
A shared state for all TypeInfos that holds global cache and dependency information,
and potentially other mutable TypeInfo state. This module contains mutable global state.
"""

from __future__ import annotations

from typing import Dict, Final, Set, Tuple
from typing_extensions import TypeAlias as _TypeAlias

from mypy.nodes import TypeInfo
from mypy.server.trigger import make_trigger
from mypy.types import Instance, Type, TypeVarId, get_proper_type

MAX_NEGATIVE_CACHE_TYPES: Final = 1000
MAX_NEGATIVE_CACHE_ENTRIES: Final = 10000

# Represents that the 'left' instance is a subtype of the 'right' instance
SubtypeRelationship: _TypeAlias = Tuple[Instance, Instance]

# A tuple encoding the specific conditions under which we performed the subtype check.
# (e.g. did we want a proper subtype? A regular subtype while ignoring variance?)
SubtypeKind: _TypeAlias = Tuple[bool, ...]

# A cache that keeps track of whether the given TypeInfo is a part of a particular
# subtype relationship
SubtypeCache: _TypeAlias = Dict[TypeInfo, Dict[SubtypeKind, Set[SubtypeRelationship]]]


class TypeState:
    """This class provides subtype caching to improve performance of subtype checks.
    It also holds protocol fine grained dependencies.

    Note: to avoid leaking global state, 'reset_all_subtype_caches()' should be called
    after a build has finished and after a daemon shutdown. This subtype cache only exists for
    performance reasons, resetting subtype caches for a class has no semantic effect.
    The protocol dependencies however are only stored here, and shouldn't be deleted unless
    not needed any more (e.g. during daemon shutdown).
    """

    # '_subtype_caches' keeps track of (subtype, supertype) pairs where supertypes are
    # instances of the given TypeInfo. The cache also keeps track of whether the check
    # was done in strict optional mode and of the specific *kind* of subtyping relationship,
    # which we represent as an arbitrary hashable tuple.
    # We need the caches, since subtype checks for structural types are very slow.
    _subtype_caches: Final[SubtypeCache]

    # Same as above but for negative subtyping results.
    _negative_subtype_caches: Final[SubtypeCache]

    # This contains protocol dependencies generated after running a full build,
    # or after an update. These dependencies are special because:
    #   * They are a global property of the program; i.e. some dependencies for imported
    #     classes can be generated in the importing modules.
    #   * Because of the above, they are serialized separately, after a full run,
    #     or a full update.
    # `proto_deps` can be None if after deserialization it turns out that they are
    # inconsistent with the other cache files (or an error occurred during deserialization).
    # A blocking error will be generated in this case, since we can't proceed safely.
    # For the description of kinds of protocol dependencies and corresponding examples,
    # see _snapshot_protocol_deps.
    proto_deps: dict[str, set[str]] | None

    # Protocols (full names) a given class attempted to implement.
    # Used to calculate fine grained protocol dependencies and optimize protocol
    # subtype cache invalidation in fine grained mode. For example, if we pass a value
    # of type a.A to a function expecting something compatible with protocol p.P,
    # we'd have 'a.A' -> {'p.P', ...} in the map. This map is flushed after every incremental
    # update.
    _attempted_protocols: Final[dict[str, set[str]]]
    # We also snapshot protocol members of the above protocols. For example, if we pass
    # a value of type a.A to a function expecting something compatible with Iterable, we'd have
    # 'a.A' -> {'__iter__', ...} in the map. This map is also flushed after every incremental
    # update. This map is needed to only generate dependencies like <a.A.__iter__> -> <a.A>
    # instead of a wildcard to avoid unnecessarily invalidating classes.
    _checked_against_members: Final[dict[str, set[str]]]
    # TypeInfos that appeared as a left type (subtype) in a subtype check since latest
    # dependency snapshot update. This is an optimisation for fine grained mode; during a full
    # run we only take a dependency snapshot at the very end, so this set will contain all
    # subtype-checked TypeInfos. After a fine grained update however, we can gather only new
    # dependencies generated from (typically) few TypeInfos that were subtype-checked
    # (i.e. appeared as r.h.s. in an assignment or an argument in a function call in
    # a re-checked target) during the update.
    _rechecked_types: Final[set[TypeInfo]]

    # The two attributes below are assumption stacks for subtyping relationships between
    # recursive type aliases. Normally, one would pass type assumptions as an additional
    # arguments to is_subtype(), but this would mean updating dozens of related functions
    # threading this through all callsites (see also comment for TypeInfo.assuming).
    _assuming: Final[list[tuple[Type, Type]]]
    _assuming_proper: Final[list[tuple[Type, Type]]]
    # Ditto for inference of generic constraints against recursive type aliases.
    inferring: Final[list[tuple[Type, Type]]]
    # Whether to use joins or unions when solving constraints, see checkexpr.py for details.
    infer_unions: bool
    # Whether to use new type inference algorithm that can infer polymorphic types.
    # This is temporary and will be removed soon when new algorithm is more polished.
    infer_polymorphic: bool

    # N.B: We do all of the accesses to these properties through
    # TypeState, instead of making these classmethods and accessing
    # via the cls parameter, since mypyc can optimize accesses to
    # Final attributes of a directly referenced type.

    def __init__(self) -> None:
        self._subtype_caches = {}
        self._negative_subtype_caches = {}
        self.proto_deps = {}
        self._attempted_protocols = {}
        self._checked_against_members = {}
        self._rechecked_types = set()
        self._assuming = []
        self._assuming_proper = []
        self.inferring = []
        self.infer_unions = False
        self.infer_polymorphic = False

    def is_assumed_subtype(self, left: Type, right: Type) -> bool:
        for l, r in reversed(self._assuming):
            if get_proper_type(l) == get_proper_type(left) and get_proper_type(
                r
            ) == get_proper_type(right):
                return True
        return False

    def is_assumed_proper_subtype(self, left: Type, right: Type) -> bool:
        for l, r in reversed(self._assuming_proper):
            if get_proper_type(l) == get_proper_type(left) and get_proper_type(
                r
            ) == get_proper_type(right):
                return True
        return False

    def get_assumptions(self, is_proper: bool) -> list[tuple[Type, Type]]:
        if is_proper:
            return self._assuming_proper
        return self._assuming

    def reset_all_subtype_caches(self) -> None:
        """Completely reset all known subtype caches."""
        self._subtype_caches.clear()
        self._negative_subtype_caches.clear()

    def reset_subtype_caches_for(self, info: TypeInfo) -> None:
        """Reset subtype caches (if any) for a given supertype TypeInfo."""
        if info in self._subtype_caches:
            self._subtype_caches[info].clear()
        if info in self._negative_subtype_caches:
            self._negative_subtype_caches[info].clear()

    def reset_all_subtype_caches_for(self, info: TypeInfo) -> None:
        """Reset subtype caches (if any) for a given supertype TypeInfo and its MRO."""
        for item in info.mro:
            self.reset_subtype_caches_for(item)

    def is_cached_subtype_check(self, kind: SubtypeKind, left: Instance, right: Instance) -> bool:
        if left.last_known_value is not None or right.last_known_value is not None:
            # If there is a literal last known value, give up. There
            # will be an unbounded number of potential types to cache,
            # making caching less effective.
            return False
        info = right.type
        cache = self._subtype_caches.get(info)
        if cache is None:
            return False
        subcache = cache.get(kind)
        if subcache is None:
            return False
        return (left, right) in subcache

    def is_cached_negative_subtype_check(
        self, kind: SubtypeKind, left: Instance, right: Instance
    ) -> bool:
        if left.last_known_value is not None or right.last_known_value is not None:
            # If there is a literal last known value, give up. There
            # will be an unbounded number of potential types to cache,
            # making caching less effective.
            return False
        info = right.type
        cache = self._negative_subtype_caches.get(info)
        if cache is None:
            return False
        subcache = cache.get(kind)
        if subcache is None:
            return False
        return (left, right) in subcache

    def record_subtype_cache_entry(
        self, kind: SubtypeKind, left: Instance, right: Instance
    ) -> None:
        if left.last_known_value is not None or right.last_known_value is not None:
            # These are unlikely to match, due to the large space of
            # possible values.  Avoid uselessly increasing cache sizes.
            return
        cache = self._subtype_caches.setdefault(right.type, {})
        cache.setdefault(kind, set()).add((left, right))

    def record_negative_subtype_cache_entry(
        self, kind: SubtypeKind, left: Instance, right: Instance
    ) -> None:
        if left.last_known_value is not None or right.last_known_value is not None:
            # These are unlikely to match, due to the large space of
            # possible values.  Avoid uselessly increasing cache sizes.
            return
        if len(self._negative_subtype_caches) > MAX_NEGATIVE_CACHE_TYPES:
            self._negative_subtype_caches.clear()
        cache = self._negative_subtype_caches.setdefault(right.type, {})
        subcache = cache.setdefault(kind, set())
        if len(subcache) > MAX_NEGATIVE_CACHE_ENTRIES:
            subcache.clear()
        cache.setdefault(kind, set()).add((left, right))

    def reset_protocol_deps(self) -> None:
        """Reset dependencies after a full run or before a daemon shutdown."""
        self.proto_deps = {}
        self._attempted_protocols.clear()
        self._checked_against_members.clear()
        self._rechecked_types.clear()

    def record_protocol_subtype_check(self, left_type: TypeInfo, right_type: TypeInfo) -> None:
        assert right_type.is_protocol
        self._rechecked_types.add(left_type)
        self._attempted_protocols.setdefault(left_type.fullname, set()).add(right_type.fullname)
        self._checked_against_members.setdefault(left_type.fullname, set()).update(
            right_type.protocol_members
        )

    def _snapshot_protocol_deps(self) -> dict[str, set[str]]:
        """Collect protocol attribute dependencies found so far from registered subtype checks.

        There are three kinds of protocol dependencies. For example, after a subtype check:

            x: Proto = C()

        the following dependencies will be generated:
            1. ..., <SuperProto[wildcard]>, <Proto[wildcard]> -> <Proto>
            2. ..., <B.attr>, <C.attr> -> <C> [for every attr in Proto members]
            3. <C> -> Proto  # this one to invalidate the subtype cache

        The first kind is generated immediately per-module in deps.py (see also an example there
        for motivation why it is needed). While two other kinds are generated here after all
        modules are type checked and we have recorded all the subtype checks. To understand these
        two kinds, consider a simple example:

            class A:
                def __iter__(self) -> Iterator[int]:
                    ...

            it: Iterable[int] = A()

        We add <a.A.__iter__> -> <a.A> to invalidate the assignment (module target in this case),
        whenever the signature of a.A.__iter__ changes. We also add <a.A> -> typing.Iterable,
        to invalidate the subtype caches of the latter. (Note that the same logic applies to
        proper subtype checks, and calculating meets and joins, if this involves calling
        'subtypes.is_protocol_implementation').
        """
        deps: dict[str, set[str]] = {}
        for info in self._rechecked_types:
            for attr in self._checked_against_members[info.fullname]:
                # The need for full MRO here is subtle, during an update, base classes of
                # a concrete class may not be reprocessed, so not all <B.x> -> <C.x> deps
                # are added.
                for base_info in info.mro[:-1]:
                    trigger = make_trigger(f"{base_info.fullname}.{attr}")
                    if "typing" in trigger or "builtins" in trigger:
                        # TODO: avoid everything from typeshed
                        continue
                    deps.setdefault(trigger, set()).add(make_trigger(info.fullname))
            for proto in self._attempted_protocols[info.fullname]:
                trigger = make_trigger(info.fullname)
                if "typing" in trigger or "builtins" in trigger:
                    continue
                # If any class that was checked against a protocol changes,
                # we need to reset the subtype cache for the protocol.
                #
                # Note: strictly speaking, the protocol doesn't need to be
                # re-checked, we only need to reset the cache, and its uses
                # elsewhere are still valid (unless invalidated by other deps).
                deps.setdefault(trigger, set()).add(proto)
        return deps

    def update_protocol_deps(self, second_map: dict[str, set[str]] | None = None) -> None:
        """Update global protocol dependency map.

        We update the global map incrementally, using a snapshot only from recently
        type checked types. If second_map is given, update it as well. This is currently used
        by FineGrainedBuildManager that maintains normal (non-protocol) dependencies.
        """
        assert self.proto_deps is not None, "This should not be called after failed cache load"
        new_deps = self._snapshot_protocol_deps()
        for trigger, targets in new_deps.items():
            self.proto_deps.setdefault(trigger, set()).update(targets)
        if second_map is not None:
            for trigger, targets in new_deps.items():
                second_map.setdefault(trigger, set()).update(targets)
        self._rechecked_types.clear()
        self._attempted_protocols.clear()
        self._checked_against_members.clear()

    def add_all_protocol_deps(self, deps: dict[str, set[str]]) -> None:
        """Add all known protocol dependencies to deps.

        This is used by tests and debug output, and also when collecting
        all collected or loaded dependencies as part of build.
        """
        self.update_protocol_deps()  # just in case
        if self.proto_deps is not None:
            for trigger, targets in self.proto_deps.items():
                deps.setdefault(trigger, set()).update(targets)


type_state: Final = TypeState()


def reset_global_state() -> None:
    """Reset most existing global state.

    Currently most of it is in this module. Few exceptions are strict optional status
    and functools.lru_cache.
    """
    type_state.reset_all_subtype_caches()
    type_state.reset_protocol_deps()
    TypeVarId.next_raw_id = 1
