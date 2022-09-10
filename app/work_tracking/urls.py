from rest_framework.routers import SimpleRouter

from work_tracking import api

router = SimpleRouter()

router.register("job-titles", api.JobTitleViewSet)
router.register("teams", api.TeamViewSet)


urlpatterns = router.urls
