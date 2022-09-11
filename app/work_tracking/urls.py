from rest_framework.routers import SimpleRouter

from work_tracking import api

router = SimpleRouter()

router.register("teams", api.TeamViewSet)
router.register("job-titles", api.JobTitleViewSet)
router.register("employees", api.EmployeeViewSet)
router.register("projects", api.ProjectViewSet)
router.register("tasks", api.TaskViewSet)


urlpatterns = router.urls
