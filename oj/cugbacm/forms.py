from django import forms

class UserRegisterForm(forms.Form):
	name = forms.CharField(label = 'name')
	password = forms.CharField(widget = forms.PasswordInput, label = 'password')
	confirmPassword = forms.CharField(widget = forms.PasswordInput, label = 'confirmPassword')
	session = forms.CharField(label = 'session')
	specialty = forms.CharField(label = 'specialty')
	tel = forms.CharField(label = 'tel')
	email = forms.EmailField(label = 'email')
	nickname = forms.CharField(label = 'nickname')

class SubmitForm(forms.Form):
	runID = forms.IntegerField(label = 'runID')
	userName = forms.CharField(label = 'userName')
	problemID = forms.CharField(label = 'problemID')
	status = forms.CharField(label = 'status')
	memory = forms.IntegerField(label = 'memory')
	runTime = forms.IntegerField(label = 'runTime')
	codeLength = forms.IntegerField(label = 'codeLength')
	date = forms.DateField(label = 'date')
	timestamp = forms.TimeField(label = 'timestamp')
	code = forms.CharField(label = 'code', widget=forms.Textarea)

class ProblemForm(forms.Form):
	problemID = forms.IntegerField(label = 'problemID')
	title = forms.CharField(label = 'title')
	timeLimit = forms.IntegerField(label = 'timeLimit')
	memoryLimit = forms.IntegerField(label = 'memoryLimit');
	acceptedSubmission = forms.IntegerField(label = 'acceptedSubmission');
	totalSubmission = forms.IntegerField(label = 'totalSubmission');
	description = forms.CharField(label = 'description', widget = forms.Textarea);
	input = forms.CharField(label = 'input', widget = forms.Textarea);
	output = forms.CharField(label = 'output', widget = forms.Textarea);
	sampleInput = forms.CharField(label = 'sampleInput', widget = forms.Textarea);
	sampleOutput = forms.CharField(label = 'sampleOutput', widget = forms.Textarea);
	author = forms.CharField(label = 'author')
		
