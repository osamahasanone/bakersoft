from rest_framework.routers import SimpleRouter

from work_tracking import api

router = SimpleRouter()

router.register("job-titles", api.JobTitleViewSet)


urlpatterns = router.urls
