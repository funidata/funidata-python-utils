import sys


if sys.version_info >= (3, 12):
    from .compat.common_serializers_312 import serialize_as_list  # noqa: F401 ("Unused import")
else:
    from .compat.common_serializers_legacy import serialize_as_list  # noqa: F401 ("Unused import")
