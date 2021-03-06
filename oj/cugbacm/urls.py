from django.conf.urls import patterns, url
from cugbacm import views

urlpatterns = patterns('',
	url(r'^register/$', views.register, name = 'register'),
	url(r'^problem/(?P<problem_id>\d+)/submit$', views.submit, name = 'submit'),
	url(r'^addProblem/$', views.addProblem, name = 'addProblem'),
	url(r'^login/$', views.login, name = 'login'),
	url(r'^problemList/$', views.problemList, name = 'problemList'),
	url(r'^testdata/$', views.testdata, name = 'testdata'),
        url(r'^submitList/$', views.submitList, name = 'submitList'),
	url(r'^userInfo/$', views.userInfo, name = 'userInfo'),
	url(r'^gettest/$', views.gettest, name = 'gettest'),
	url(r'^problem/(?P<problem_id>\d+)$', views.problem, name = 'problem'),
)
