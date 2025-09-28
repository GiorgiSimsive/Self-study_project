from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"


class IsTeacherOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == "teacher" or request.user.role == "admin")


class ReadOnlyOrTeacherAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and (request.user.role == "teacher" or request.user.role == "admin")


class IsAuthenticatedStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "student"


class IsOwnerOrReadOnly(BasePermission):
    """
    Чтение всем, изменения — только владельцу объекта (или админу).
    Ожидается, что у объекта есть поле .owner (для Course) или .section.course.owner и т.п.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        if not user.is_authenticated:
            return False
        if getattr(user, "role", None) == "admin":
            return True

        owner = None
        if hasattr(obj, "owner"):
            owner = obj.owner
        elif hasattr(obj, "course"):
            owner = obj.course.owner
        elif hasattr(obj, "section"):
            owner = obj.section.course.owner
        elif hasattr(obj, "material"):
            owner = obj.material.section.course.owner
        elif hasattr(obj, "test"):
            owner = obj.test.material.section.course.owner

        return owner == user
